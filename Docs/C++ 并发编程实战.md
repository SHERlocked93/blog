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





🍓另外，如果线程对象不 `join()` 或 `detach()`，程序会在 `std::thread` 对象析构时崩溃（析构时调用 `std::terminate`）。

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



## 第 3 章 在线程间共享数据
## 第 4 章 并发操作的同步
## 第 5 章 C++内存模型和原子操作
## 第 6 章 设计基于锁的井发数据结构
## 第 7 章 设计无锁数据结构
## 第 8 章 设计共发代码
## 第 9 章 高级线程管理
## 第 10 章 并行算法函数
## 第 11 章 多线程应用的测试和除错