# C++ 并发编程实战

[TOC]



## 第 1 章 你好， C++并发世界

多进程并发
1. 将一个应用软件拆分成多个独立进程同时运行，都只含单一线程；
2. 缺点1：或设置复杂，或速度慢，甚至二者兼有，因为操作系统往往要在进程之间提供大量防护措施，以免某进程意外改动另一个进程的数据；
3. 缺点2：是运行多个进程的固定开销大，进程的启动花费时间，操作系统必须调配内部资源来管控进程，等等。
4. 优点1：操作系统在进程间提供额外保护和高级通信机制，相比于线程，多进程并发更安全。运用独立的进程实现并发；
5. 优点2：通过网络连接，独立的进程能够在不同的计算机上运行。这样做虽然增加了通信开销，可是只要系统设计精良，此法足以低廉而有效地增强并发力度，改进性能。

多线程并发

1. 在单一进程内运行多线程。
2. 线程非常像轻量级进程：每个线程都独立运行，并能各自执行不同的指令序列；
3. 同一进程内的所有线程都共用相同的地址空间，且所有线程都能直接访问大部分数据。全局变量依然全局可见，指向对象或数据的指针和引用能在线程间传递。

什么时候避免并发：

1. 编写多线程代码需要额外的开发时间和相关维护成本；
2. 性能增幅可能不如预期，线程启动本身需要开销，由于系统须妥善分配相关的内核资源和栈空间，然后才可以往调度器添加新线程，这些都会耗费时间；
3. 若一次运行太多线程，便会消耗操作系统资源，可能令系统整体变慢；运行的线程越多，操作系统所做的上下文切换就越频繁，每一次切换都会减少本该用于实质工作的时间；
4. 每个线程都需要独立的栈空间，如果线程太多，就可能耗尽所属进程的可用内存或地址空间。在采用扁平模式内存架构的 32 位进程中，可用的地址空间是4GB：假定每个线程栈的大小都是1MB（这个大小常见于许多系统，Windows 默认线程堆栈大小 1MB，Linux 为 8MB，可以用 ulimit -s 查看和修改默认线程堆栈大小），那么 32 位系统上 4096 个线程即会耗尽地址空间；

简单的 HelloWorld：

```c++
#include <iostream>
#include <thread>

int main() {
    std::thread t([](){ std::cout<<"Hello Concurrent World\n"; });  
    t.join();
}
```

`std::thread` 新线程启动后立刻开始执行，主线程继续执行。如果主线程不等待新线程结束，很可能直接终止整个程序的时候，新线程还没有机会启动，这是要调用 `join()` 的原因。

如果线程对象不 `join()` 或 `detach()`，程序会在 `std::thread` 对象析构时崩溃（析构时调用 `std::terminate`）。

- C++ 标准（C++11 及以上）设计 `std::thread` 时，要求线程的生命周期管理必须显式由程序员控制。
- 不调用 `join()` 或 `detach()` 意味着线程的状态未明确定义：
  - `join()` 表示主线程等待子线程完成，资源由系统同步回收。
  - `detach()` 表示子线程独立运行，资源由系统管理，系统自动回收资源。
- 如果两者都不调用，`std::thread` 无法安全销毁底层线程句柄，可能会导致资源泄漏或未定义行为。

## 第 2 章 线程管控

### 生存期问题

如果程序不等待线程结束，那么在线程运行结束前，需保证它所访问的外部数据始终正确、有效。这种**生存期问题**在多线程场景下比较常见。

比如对于分离 `detach` 的线程，访问已销毁的资源：

```c++
struct func {
    int& i;
    func(int& i_):i(i_){}
    void operator()(){
        for(unsigned j=0;j<1000000;++j) {
            do_something(i);   // ①隐患：可能访问悬空引用
        }
    }
};
void oops() {
    int some_local_state=0;
    func my_func(some_local_state);
    std::thread my_thread(my_func);
    my_thread.detach();   // ②不等待新线程结束
}    // ③新线程可能仍在运行，而线程所在的作用域却已释放
```

新线程上的函数持有指针或引用，指向父作用域中局部变量，但父作用域退出后，新线程却还没结束，此时就会访问已销毁的局部变量。

这种生存期问题通常处理办法：令线程函数完全自含（self-contained），将数据复制到新线程内部，而不是共享数据。

#### join 的时机

如果打算等待线程结束，调用 `join()` 时需要注意，如果线程启动以后有异常抛出，而 `join()` 尚未执行，则该 `join()` 调用会被略过。

此时我们可以使用一个 RAII （Resource Acquisition Is Initialization） 的管理类：

```c++
class thread_guard {
    std::thread& t;
public:
    explicit thread_guard(std::thread& t_): t(t_) {}
    ~thread_guard() {
        if(t.joinable()) {   //  ①
            t.join();    //  ②
        }
    }
    thread_guard(thread_guard const&)=delete;    // ③
    thread_guard& operator=(thread_guard const&)=delete;
};

void f() {
    int some_local_state=0;
    func my_func(some_local_state);
    std::thread t(my_func);
    thread_guard g(t);
    do_something_in_current_thread();
}
```

这样在 `thread_guard` 析构的时候，会去检查线程对象是否有 `join()`，从而避免 `std::terminate`

### 给线程函数传参

`std::thread` 具有内部存储空间，参数按照**值传递**方式先复制到该处，这些副本被当成临时变量，以**右值形式**传给新线程上的函数或可调用对象。即便函数的相关参数按设想应该是引用，上述过程依然会发生。

比如：

```c++
class A {};
void test1(A& data_) {}  // 注意入参
int main() {
  A data{};
  std::thread t(test1, data);  // 注意传参
  t.join();
  return 0;
}

// 编译报错：static assertion failed: std::thread arguments must be invocable after conversion to rvalues
```

对于这样的函数 `test1`，入参为非 const 左值引用，看上去没问题，但其实 `std::thread` 构造函数并不知道 `test1` 要求参数是引用，它内部会这样处理：

将 `data` 复制一份，打包到内部的线程存储区域，然后在新线程里用这些副本（右值）来调用 `test1`，所以调用过程等效于`std::thread t(test1, std::move(data))`，而 C++ 禁止将右值直接绑定到非 const 左值引用，所以编译失败了。

为了解决这个问题，可以：

1. 方法1：用 `std::ref` 方式传递参数，明确告诉 `std::thread` 不要值复制 `data`，传递左值引用；
2. 方法2：修改线程函数签名为 const 左值引用，const 左值引用可以绑定右值；
3. 方法3：修改线程函数签名为值传递；

另外对于 `std::unque_ptr`，由于其不能被复制，所以传递给 `std::thread` 的时候，需要明确使用 `std::move` 来进行所有权转移：

```c++
void test1(std::unique_ptr<int> data) {}
void main() {
  std::unique_ptr<int> data{};
  // std::thread t(test1, data);   // 编译报错
  std::thread t(test1, std::move(data));
}
```

### 移交线程归属权

在 `std::thread` 对象析构前，必须明确这个线程是 `join` 还是 `detach`。不然，便会导致关联的线程终结。赋值操作也有类似的原则：只要 `std::thread` 对象正管控着一个线程，就不能简单地向它赋新值，否则该线程会因此被遗弃并 `terminate`。

`std::thread` 支持移动操作，可以通过函数函数传出线程对象来转移线程归属权，也可以用右值作为参数传递（也只能是右值，因为线程不可复制）给函数。

### 在运行时选择线程数量

`std::thread::hardware_concurrency()` 可以获取程序在运行中可以真正并发的线程数，多核系统中，返回值可能是CPU核芯的数量。

### 识别线程

使用 `std::this_thread::get_id()` 可以获取线程 ID，在一些场景中，可以采用线程 ID 作为键值的关联容器，利用这种容器存储信息以便在线程间互相传递。

## 第 3 章 在线程间共享数据

### 用互斥保护数据

通过构造 `std::mutex` 的实例来创建互斥，调用成员函数 lock() 对其加锁，调用 `unlock()` 解锁；

`std::lock_guard<T>`，在构造时给互斥加锁，在析构时解锁，从而保证互斥总被正确解锁。

`std::scoped_lock` 可以同时锁多个互斥量，从而避免多个互斥量循环等待导致死锁的情况；

### 死锁

避免死锁的建议：始终按相同顺序对两个互斥加锁；

即使没有牵涉锁，也会发生死锁现象。假定有两个线程，各自关联了 `std::thread` 实例，若它们同时在对方的 `std::thread` 实例上调用 `join()`，就能制造出死锁现象却不涉及锁操作。为了防范这个情况，需要注意，只要另一线程有可能正在等待当前线程，那么当前线程千万不能反过来等待它。

避免死锁的建议：

1. **避免嵌套锁**，假如已经持有锁，就不要试图获取第二个锁；万一确实需要多个锁，应该使用 `std::lock` 或 `std::scoped_lock` 对多个互斥量同时加锁；
2. 持锁时避免调用由用户提供的程序接口；
3. **固定顺序获取锁**，如果需要多个锁是必要的，却无法 `std::lock()` 同时加锁，只能退而求其次，在每个线程内部都依从固定顺序获取这些锁；
4. **按层级加锁**，按特定方式规定加锁次序；

### 初始化过程中保护共享数据

`std::once_flag` 和 `std::call_once` 提供了一种线程安全的方式，确保某段初始化代码只执行一次，哪怕有多个线程并发访问，非常适用于**单例模式**或者**懒加载初始化**场景。

```c++
#include <iostream>
#include <mutex>
#include <thread>

class Singleton {
  static Singleton* instance;
  static std::once_flag initFlag;
  Singleton() { std::cout << "Singleton constructor\n"; }

 public:
  static Singleton& getInstance() {
    std::call_once(initFlag, []() {  // 只会初始化一次
      instance = new Singleton();
    });
    return *instance;
  }

  void sayHello() { std::cout << "Hello from Singleton!\n"; }
};

Singleton* Singleton::instance = nullptr;
std::once_flag Singleton::initFlag;

int main() {
  auto task = []() {
    Singleton::getInstance().sayHello();
  };

  std::thread t1(task), t2(task), t3(task);

  t1.join();
  t2.join();
  t3.join();
}
```

或者可以直接用静态声明，C11 规定静态数据的初始化只会在某一线程上单独发生，且不会在初始化完成前越过静态数据的声明继续运行，所以下面的方式可以替代 `std::call_once`

```c++
class my_class;
Singleton& getInstance()   // 线程安全的初始化，C++11标准保证其正确性
{
    static Singleton instance;  
    return instance;
}
```

### 读写锁分离

读写互斥：允许单独一个写线程进行完全排他的访问，也允许多个读线程共享数据或并发访问。

```c++
class SharedData {
 public:
  void write(int val) {
    std::unique_lock<std::shared_mutex> lock(mutex_);
    std::cout << "Writing " << val << " by " << std::this_thread::get_id() << "\n";
    data_ = val;
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
  }

  void read() {
    std::shared_lock<std::shared_mutex> lock(mutex_);
    std::cout << "Reading " << data_ << " by " << std::this_thread::get_id() << "\n";
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
  }

 private:
  int data_ = 0;
  std::shared_mutex mutex_;
};

int main() {
  SharedData shared;
  std::vector<std::thread> threads;
  // 启动多个读线程
  for (int i = 0; i < 5; ++i) threads.emplace_back([&] { shared.read(); });

  // 启动一个写线程
  threads.emplace_back([&] { shared.write(42); });

  // 启动多个读线程
  for (int i = 0; i < 5; ++i) threads.emplace_back([&] { shared.read(); });

  for (auto& t : threads) t.join();
}
```

这里多个线程可以同时读操作，但写操作是独占的，需要其他读线程释放锁才会执行，在写线程执行时，其他读线程会被阻塞。

标准库中的 `std::shared_mutex` 一般实现是写优先，防止写线程被饿死。

不要在持有共享锁的同时尝试获取独占锁，容易死锁。

### 递归加锁

`std::recursive_mutex` 让线程在同一互斥量上多次重复加锁，而无须解锁，其工作方式与 `std::mutex` 相似，不同之处是，其允许同一线程对某互斥的同一实例多次加锁。必须先释放全部的锁，才可以让另一个线程锁住该互斥。如对它调用了 3 次 `lock()` ，就必须调用 3 次 `unlock()`。

使用递归锁需要谨慎，可能你并不需要递归锁。

## 第 4 章 并发操作的同步

### 条件变量

条件变量是与互斥相关联的一种用于多线程之间关于共享数据状态改变的通信机制，当一个线程的行为依赖于另外一个线程对共享数据状态的改变时，这时候就可以使用条件变量。本质上是忙等待（busy-wait）的一种优化，即设置一个线程不断轮训的方式；。

条件变量将**解锁与挂起封装成原子操作**：等待一个条件变量时，会**解开**与该条件变量相关的锁，条件满足时该互斥量会被自动加锁，所以，在完成操作之后需要解锁。

下面是一个典型的条件变量使用场景：

```c++
std::mutex mut;
std::queue<int> data_queue;  // ⇽---  ①
std::condition_variable data_cond;

void data_preparation_thread() {  // 生产线程乙
  while (more_data_to_prepare()) {
    int const data = prepare_data();
    {
      std::lock_guard<std::mutex> lk(mut);
      data_queue.push(data);  // ⇽---  ②
    }
    data_cond.notify_one();  // ⇽---  ③
  }
}
void data_processing_thread() { // 消费线程甲
  while (true) {
    std::unique_lock<std::mutex> lk(mut, std::defer_lock);  // ⇽---  ④
    data_cond.wait(lk, [] { return !data_queue.empty(); });
    int data = data_queue.front();
    data_queue.pop();
    lk.unlock();  // ⇽---  ⑥

    process(data);
    if (is_last_chunk(data)) break;
  }
}
```

这里使用一个互斥锁来保护数据队列 1，2 处在互斥锁的保护下操作数据队列，3 处由于操作了数据队列，所以通知一个正在等待的线程以处理数据，4 处声明了一个 `std::unique_lock`，然后注意了，下面使用了一个条件变量来检查是否满足 lambda 表达式中的条件，如果：

1. 不满足则会**释放** `mut` 然后阻塞线程继续等待被 `std::condition_variable` 来 `notify`，此时线程会让出 CPU，不消耗资源；
2. 满足则会**锁住** `mut` 并且往下执行，所以在不需要互斥锁的时候，需要**解锁**操作；

`wait()` 期间，条件变量可以多次查验给定的条件，次数不受限制；在查验时，互斥总会被锁住；另外，当且仅当传入的判定函数返回 true 时，`wait()` 才会立即返回。如果线程甲重新获得互斥，并且查验条件，而这一行为却不是直接响应线程乙的通知 `notify`，则称之为虚假唤醒（spurious wake）。

由上面的代码示例，我们将条件变量、锁、队列等封装成一个线程安全的队列容器：

```c++
template <typename T>
class threadsafe_queue {
  mutable std::mutex mtx_;  // ①互斥必须用mutable修饰（针对const对象，准许其数据成员发生变动）
  std::queue<T> data_queue;
  std::condition_variable cv_;

 public:
  threadsafe_queue() {}
  threadsafe_queue(threadsafe_queue const& other) {
    std::lock_guard<std::mutex> lk(other.mtx_);
    data_queue = other.data_queue;
  }
  void push(T new_value) {
    std::lock_guard<std::mutex> lk(mtx_);
    data_queue.push(new_value);
    cv_.notify_one();
  }
  void wait_and_pop(T& value) {
    std::unique_lock<std::mutex> lk(mtx_);
    cv_.wait(lk, [this] { return !data_queue.empty(); });
    value = data_queue.front();
    data_queue.pop();
  }
  std::shared_ptr<T> wait_and_pop() {
    std::unique_lock<std::mutex> lk(mtx_);
    cv_.wait(lk, [this] { return !data_queue.empty(); });
    std::shared_ptr<T> res(std::make_shared<T>(data_queue.front()));
    data_queue.pop();
    return res;
  }
  bool try_pop(T& value) {
    std::lock_guard<std::mutex> lk(mtx_);
    if (data_queue.empty()) return false;
    value = data_queue.front();
    data_queue.pop();
    return true;
  }
  std::shared_ptr<T> try_pop() {
    std::lock_guard<std::mutex> lk(mtx_);
    if (data_queue.empty()) return std::shared_ptr<T>();
    std::shared_ptr<T> res(std::make_shared<T>(data_queue.front()));
    data_queue.pop();
    return res;
  }
  bool empty() const {
    std::lock_guard<std::mutex> lk(mtx_);
    return data_queue.empty();
  }
};

// 下面是使用示例
threadsafe_queue<data_chunk> data_queue;  // ⇽---  ①
void data_preparation_thread() {
  while (more_data_to_prepare()) {
    data_chunk const data = prepare_data();
    data_queue.push(data);  // ⇽---  ②
  }
}
void data_processing_thread() {
  while (true) {
    data_chunk data;
    data_queue.wait_and_pop(data);  // ⇽---  ③
    process(data);
    if (is_last_chunk(data)) break;
  }
}
```

### 使用 future 等待一次性事件



## 第 5 章 C++内存模型和原子操作
## 第 6 章 设计基于锁的并发数据结构
## 第 7 章 设计无锁数据结构
## 第 8 章 设计共发代码
## 第 9 章 高级线程管理
## 第 10 章 并行算法函数
## 第 11 章 多线程应用的测试和除错