# CPP 从 0 到 1 完成一个支持 future/promise 的 Windows 异步串口通信库

由于我在工作环境中不断由于需要为了不同硬件设备写新的串口通信库，所以我写了一个集成了 `future/promise` 的异步串口通信库，并且已经用在了每天有数十万人使用的生产环境设备上，下面分享一下如何从零开始构建一个集成 C++11 的 `future/promise` 机制的实用的异步串口通信库。

## 1. 异步串口通信库的设计思路

设计思路：

1. 首先创建一个串口通信工具库，支持同步方式的串口消息收发；
2. 然后我们创建一个生产者消费者队列，需要请求数据的时候往这个队列里存 `promise` 并立即给使用者返回一个 `future`，串口库获得回复或者超时的时候给这个 `promise` 回复信息，这样使用者就可以通过 `future` 获得返回的结果；
3. 生产者消费者队列需要满足：
   1. 在生产消息的时候通过条件变量通知消费者线程取队列中的消息来消费，这个消息在成功取到结果或超时的时候出队；
   2. 如果生产消息时在队列满则进行等待；
4. 在使用者实例化这个串口通信库的时候，将串口解析协议（`ValidateFrame` 一个解析函数，返回 int 表示解析到的针头地址）传入，以可以适配不同硬件设备的不同串口通信协议；

用户的使用流程：

1. 用户发起异步请求，立即获得 `future` 对象；
2. 其请求被封装成任务并投递到队列中；
3. 之后消费者线程从队列中取出任务并执行串口通信；
4. 通信完成或超时后，通过 `promise` 设置结果；
5. 用户通过 `future` 获取最终结果；

## 2. Windows 串口通信 API 封装

底层串口通信基于 Windows 提供的原生 API 实现，主要包括：

- `CreateFile`：打开串口设备；
- `SetCommState`：配置串口参数（波特率、数据位等）；
- `WriteFile`：发送数据到串口；
- `ReadFile`：从串口读取数据；
- `PurgeComm`：清空串口缓冲区；

为了适配不同硬件设备的通信协议，库提供了可插拔的协议解析接口 `ValidateFrame`，在消费消息的时候不断检索缓冲区，在超时之前缓冲区中是否有满足用户需要的报文体，如果有就成功返回，否则继续检索。

```cpp
// 用户自定义的协议解析函数
// 返回值：0-继续等待，-1-无效帧，>0-有效帧长度
using ValidFrameCallback = std::function<int(const unsigned char *, int)>;
```

完整实现涉及较多细节，具体可以到[ Github 仓库](https://github.com/SHERlocked93/cpp_easy_serial)里查阅代码。

## 3. 生产者/消费者消息队列实现

首先，创建一个生产者消费者的有界消息队列 `BoundedQueue` 用来管理待处理消息，这个队列是一个模板类，传入的模板 `MSG_BASE` 是消息体，如果消息被成功返回，使用者可以从这个消息体中获取返回的消息码和报文体，队列在实例化的时候需这个队列的容量，内部则通过条件变量来协调消费线程对消息的消费：

```c++
template <typename MSG_BASE>
class BoundedQueue {
 public:
  explicit BoundedQueue(size_t capacity) : capacity_(capacity) {}

  bool push(std::unique_ptr<MSG_BASE> message) {
    std::unique_lock lock(mutex_);
    not_full_.wait(lock, [this]() { return queue_.size() < capacity_; });

    queue_.push(std::move(message));
    lock.unlock();
    not_empty_.notify_one(); // 通知消费者有新消息
    return true;
  }

  std::unique_ptr<MSG_BASE> pop() {
    std::unique_lock lock(mutex_);
    not_empty_.wait(lock, [this]() { return !queue_.empty(); });

    auto message = std::move(queue_.front());
    queue_.pop();
    lock.unlock();
    not_full_.notify_one();
    return message;
  }

  bool empty() const {
    std::lock_guard lock(mutex_);
    return queue_.empty();
  }

  size_t size() const {
    std::lock_guard lock(mutex_);
    return queue_.size();
  }

 private:
  const size_t capacity_;
  std::queue<std::unique_ptr<MSG_BASE>> queue_;
  mutable std::mutex mutex_;

  std::condition_variable not_empty_;
  std::condition_variable not_full_;
};
```

注意对队列的操作需要加锁，以保证线程安全。

## 3. 消费者管理类和消息相关类设计

消费者管理类并持有之前的生产者消费者队列实例，做的事比较简单，就是负责创建和管理消费线程，消费线程会不断从队列中取消息出来消费：

```c++
template <typename MSG_BASE>
class ConsumerManager {
 public:
  ConsumerManager(BoundedQueue<MSG_BASE>& queue, size_t thread_count = 1)
      : queue_(queue), running_(true) {
    for (size_t i = 0; i < thread_count; ++i) {
      threads_.emplace_back(&ConsumerManager::worker, this);
    }
  }

  ~ConsumerManager() { stop(); }

  void stop() {
    running_ = false;
    for (auto& thread : threads_) {
      if (thread.joinable()) {
        thread.join();
      }
    }
  }

 private:
  void worker() const {
    while (running_) {
      if (const auto taskItem = queue_.pop()) {
        taskItem->execute();
      }
    }
  }

  BoundedQueue<MSG_BASE>& queue_;
  std::atomic<bool> running_;
  std::vector<std::thread> threads_;
};
```


消息相关的模板类 `Message` 作为通信的消息容器，继承自 `MessageBase`，通过模板支持多种返回类型，并提供 `execute` 方法作为消费线程的入口，使用者可以传递一个返回值类型给 `Message` 类，消费者管理类会在消费消息之后通过 `Message` 传递返回值给使用者：

```c++
template <typename T>
struct is_future : std::false_type {};

template <typename T>
struct is_future<std::future<T>> : std::true_type {};

template <typename T>
inline constexpr bool is_future_v = is_future<T>::value;

class MessageBase {
 public:
  virtual ~MessageBase() = default;
  virtual std::unique_ptr<void> execute() = 0;

  template <typename RetType>
  std::future<RetType> getFuture() {
    promise_ = std::make_shared<std::promise<std::unique_ptr<void>>>();
    return std::async(std::launch::deferred, [promise = promise_]() -> RetType {
      auto result = promise->get_future().get();
      if constexpr (is_future_v<RetType>) {
        auto* future_ptr = static_cast<RetType*>(result.get());
        return std::move(*future_ptr);
      } else {
        return *static_cast<RetType*>(result.get());
      }
    });
  }

 protected:
  std::shared_ptr<std::promise<std::unique_ptr<void>>> promise_;
};

template <typename RetType>
class Message : public MessageBase {
 public:
  using ExecutorType = std::function<RetType()>;

  explicit Message(ExecutorType executor) : executor_(std::move(executor)) {}

  std::unique_ptr<void> execute() override {
    auto result = executor_();
    return std::make_unique<RetType>(std::move(result));
  }

 private:
  ExecutorType executor_;
};
```

## 5. 完整使用示例

```c++
#include <iostream>
#include <random>
#include <thread>
#include <chrono>

// 生成测试数据
std::vector<unsigned char> generateRandomData() {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 0xFF);

    return {0xAA, static_cast<unsigned char>(dis(gen)),
            static_cast<unsigned char>(dis(gen)),
            static_cast<unsigned char>(dis(gen)), 0xBB};
}

// 示例协议解析函数
// 协议格式：0xAA [数据] 0xBB
int validateFrame(const unsigned char* buffer, int length) {
    if (length < 4) return 0;  // 数据不足，继续等待

    if (buffer[0] == 0xAA) {
        // 查找结束标志
        for (int i = 3; i < length; i++) {
            if (buffer[i] == 0xBB) {
                return i + 1;  // 返回完整帧长度
            }
        }
    }

    return -1;  // 无效帧
}

// 串口任务封装类
class SerialTask {
public:
    explicit SerialTask(std::shared_ptr<SerialComm> serial) : serial_(serial) {}

    std::future<SerialRet> sendAsync(const std::vector<unsigned char>& data,
                                   int timeout = 10000) const {
        std::cout << "发送数据: " << bytes2hexStr(data) << std::endl;
        return serial_->SendCommandAsync(data, validateFrame, timeout);
    }

private:
    std::shared_ptr<SerialComm> serial_;
};

int main() {
    // 初始化串口通信
    auto serial = std::make_shared<SerialComm>();
    constexpr int comPort = 1;
    constexpr int baudRate = 115200;

    if (int res = serial->OpenCom(comPort, baudRate); res != 0) {
        std::cout << "打开串口失败，错误代码: " << res << std::endl;
        return 1;
    }
    std::cout << "串口打开成功!" << std::endl;

    // 创建消息队列和消费者管理器
    BoundedQueue<Message<SerialRet>> queue(10);
    ConsumerManager consumer(queue);

    // 创建串口任务封装器
    SerialTask serialTask(serial);

    // 主循环：处理用户输入
    std::string line;
    std::cout << "请按回车发送随机数据，输入 'quit' 退出..." << std::endl;
    
    while (std::getline(std::cin, line)) {
        if (line == "quit") break;

        // 创建异步任务
        auto task = std::make_unique<Message<SerialRet>>([&serialTask]() -> SerialRet {
            auto fut = serialTask.sendAsync(generateRandomData());
            auto [ret, response] = fut.get();
            
            if (ret > 0) {
                std::cout << "任务完成，收到响应: " << bytes2hexStr(response) << std::endl;
            } else {
                std::cout << "任务失败，错误代码: " << ret << std::endl;
            }
            
            return std::make_tuple(ret, response);
        });

        // 投递到队列
        queue.push(std::move(task));

        // 短暂等待以观察结果
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    // 清理资源
    consumer.stop();
    serial->CloseCom();
    std::cout << "程序退出" << std::endl;

    return 0;
}
```

## 6. 总结

代码已开源，项目地址：https://github.com/SHERlocked93/cpp_easy_serial

这个库已在生产环境中验证，支持高并发场景下的稳定运行。如果你在项目中需要进行串口通信，不妨试试这个库，也可以在这个基础上进行修改迭代，欢迎给提 pr 提 issue 一起讨论啊！

---

网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出，如果本文帮助到了你，别忘了点赞支持一下，你的点赞是我更新的最大动力！~

PS：本文同步更新于在下的博客 [Github - SHERlocked93/blog](https://link.juejin.cn?target=https%3A%2F%2Fgithub.com%2FSHERlocked93%2Fblog) 系列文章中，欢迎大家关注我的公众号 `CPP下午茶`，直接搜索即可添加，持续为大家推送 CPP 以及 CPP 周边相关优质技术文，共同进步，一起加油~

另外可以加入「前端下午茶交流qun」，vx 搜索  `sherlocked_93` 加我，备注 **1**，我拉你～

