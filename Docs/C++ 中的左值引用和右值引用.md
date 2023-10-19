# C++ 中左值引用和右值引用

[TOC]



最近看拷贝复制部分内容的时候看到移动构造函数和移动赋值运算符的声明中有个 `&&` 符号，另外在看多线程的时候也看到了这个符号，所以把这个右值引用集中学习了一下，同时做了一些输出，希望也可以帮助到大家。

C 语言中的左/右值和 C++ 中的左/右值是不一样的，C 语言中的左值可以位于赋值语句的左侧，右值不能，比较直观，但 C++ 中的左值和右值里面的内容就比较多一些。

## 1. 左值和右值

在 C++ 中，**左值**（Lvalue）是可以被赋值的表达式，通常具有内存地址，可以被引用和修改。例如，变量、数组元素和对象成员等都是左值。

**右值**（Rvalue）则是临时的、无法被赋值的表达式，通常是计算结果或临时对象。右值不能被引用或修改，因为它们没有明确的内存地址。例如，常量、字面量和临时对象都是右值。

左值和右值的主要区别在于内存持久性，左值有持久的状态，比如变量，而右值要么是字面常量，要么是在表达式求值过程中创建的临时对象。

《C++ Primer》 中对左值和右值有个形象的描述：当一个对象被用作右值的时候，用的是对象的值（内容）；当对象被用作左值的时候，用的是对象的身份（在内存中的位置）。

所以当一个左值被当成右值使用时，实际使用的是它的内容（值）。在需要右值的地方可以用左值来代替，但是不能把右值当成左值（也就是位置）使用。比如取地址符 `&`，就是对一个左值取地址，取出来的地址是个右值，因为右值只有内容，在内存中没有位置。而对一个地址解引用 `*p`，或者对一个数组取下标 `arr[0]`，就获得了左值。有时候左值不一定可以放在表达式左边，因为有些左值不能被赋值，比如数组名和常量。

## 2. 左值引用和右值引用

C++11 引入了右值引用 `&&` 的概念，允许将右值绑定到一个引用上，并且可以修改其内容，这提供了更多的灵活性和效率。

右值引用指向将要被销毁的对象，比如一个表达式。

```cpp
int i = 10;
int& j = i;           // 正确：左值引用
int& k = i * 1;       // 错误：左值引用不能绑定右值
int&& m = i * 1;      // 正确：右值引用
int&& n = i;          // 错误：右值引用不能绑定左值
const int& p = i * 1; // 正确：const左值引用可以绑定右值
```

如果说变量是左值，那么问题来了，右值引用的变量也是变量，这个变量是左值么，比如这里的 `m`。

答案为左值，所以下面这个表达式是错误的：

```cpp
int&& q = m;          // 错误：右值引用不能绑定左值，即使这个左值是右值引用类型的变量
```

虽然直接把右值引用类型的变量绑定到变量上，但可以使用 `move` 来获取绑定到左值上的右值引用。

```cpp
int&& q = std::move(m);    // 正确：std::move可以将左值转换为右值
```

## 3. 使用场景

### 3.1 移动构造函数和移动赋值运算符

看《C++ Primer》这本书到的拷贝控制这一章的时候，就会经常碰到右值引用符号 `&&` ，它 常常用在移动构造函数和移动赋值运算符上。

![CPP拷贝控制](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/%E6%8B%B7%E8%B4%9D%E6%8E%A7%E5%88%B6-20231016-GFSbVF.png)

移动构造函数和移动赋值运算符要求传入右值，这时需要使用 `std::move` 获取右值。

```cpp
#include <iomanip>
#include <iostream>
#include <string>
#include <utility>

using namespace std;

class MyClass {
public:
    std::string data;

    explicit MyClass(std::string _data = "")
        : data(std::move(_data)){};

    MyClass(MyClass&& other) noexcept
    {
        cout << "移动构造函数  " ;
        data = std::move(other.data);
    }

    MyClass& operator=(MyClass&& other) noexcept
    {
        cout << "移动赋值运算符  " ;
        if (this != &other) {
            data = std::move(other.data);
        }
        return *this;
    }
};

int main()
{
    MyClass A("SHERlocked93");

    MyClass D = std::move(A); // 移动构造
    cout << D.data << endl;

		//    MyClass E(std::move(D)); // 移动构造
		//    cout << E.data << endl;

    MyClass G;
    G = std::move(D); // 移动赋值
    cout << G.data << endl;
}

// 打印：
// 移动构造函数  SHERlocked93
// 移动赋值运算符  SHERlocked93
```

顺便说一下，如果一个类有拷贝构造函数而没有移动构造函数，那么原来使用移动构造函数的场景就使用比如 `MyClass B(move(A))` 就会调用拷贝构造函数。拷贝赋值运算符和移动赋值运算符的情况也类似。

### 3.2 移动语义

上面移动构造函数和移动赋值运算符这个例子中，其实是右值引用在移动语义的一个使用场景，目的是减少不必要的拷贝操作，减少资源的不必要复制、销毁的性能开销，提高性能。使用移动语义提高性能的做法非常普遍，做实际项目的时候会经常用到。

常见的用法比如向一个数组中增加一个元素：

```cpp
vec.push_back(std::move(obj));   // 减少obj对象的复制，或者直接用emplace_back
vec.emplace_back(obj);
```

或者来个具体的，比如合并两个数组，如果希望使用移动语义减少拷贝操作，可以使用移动迭代器  `std::make_move_iterator` 实现：

```cpp
#include <iostream>
#include <string>
#include <utility>
#include <vector>

using namespace std;

class MyClass {
public:
    std::string data;

    explicit MyClass(std::string _data = "")
        : data(std::move(_data)){};

    MyClass(const MyClass& other)
    {
        cout << "拷贝构造函数  ";
        data = other.data;
    }

    MyClass(MyClass&& other) noexcept
    {
        cout << "移动构造函数  ";
        data = std::move(other.data);
    }

    MyClass& operator=(MyClass&& other) noexcept
    {
        cout << "移动赋值运算符  ";
        if (this != &other) {
            data = std::move(other.data);
        }
        return *this;
    }

    MyClass& operator=(const MyClass& other)
    {
        cout << "拷贝赋值运算符  ";
        if (this != &other) {
            data = other.data;
        }
        return *this;
    }
};

template <typename T>
std::vector<T> concat(std::vector<T>& vec1,
                      std::vector<T>& vec2)
{
    std::vector<T> res;
    res.reserve(vec1.size() + vec2.size());

    res.insert(res.end(), std::make_move_iterator(vec1.begin()), std::make_move_iterator(vec1.end()));
    res.insert(res.end(), std::make_move_iterator(vec2.begin()), std::make_move_iterator(vec2.end()));

    return res;
}

int main()
{
    vector<MyClass> a;
    vector<MyClass> b;
    a.emplace_back(MyClass("SHERlocked93"));
    b.emplace_back(MyClass("hello wrold!"));

    cout << endl;
    auto r = concat(a, b);

    cout << endl;
    cout << r[0].data << "-" << r[1].data << endl;
}

// 打印：
// 移动构造函数  移动构造函数  移动构造函数  移动构造函数  
// SHERlocked93-hello wrold!
```

可以看到只调用了移动构造函数，而没有使用拷贝构造函数，如果将移动迭代器改为普通迭代器，就会使用拷贝构造函数了。

除了移动语义外，右值引用还被用在完美转发上，另外比如在函数返回一个大对象时，可以返回一个临时对象的右值引用，而不是进行拷贝操作，除此之外还有其他一些应用场景，以后遇到了再探讨一下。

---

网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出，如果本文帮助到了你，别忘了点赞支持一下哦，你的点赞是我更新的最大动力！ 🤣~


> 参考文档：
>
> 1. [MDN - 引用声明符：`&&`](https://learn.microsoft.com/zh-cn/cpp/cpp/rvalue-reference-declarator-amp-amp?view=msvc-170)

PS：本文收录在在下的博客 [Github - SHERlocked93/blog](https://github.com/SHERlocked93/blog) 系列文章中，欢迎大家关注我的公众号 `前端下午茶`，直接搜索即可添加或者点[这里](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/TJt4p2-19-56-21.jpg)添加，持续为大家推送前端以及前端周边相关优质技术文，共同进步，一起加油~

另外可以加入「前端下午茶交流群」微信群，微信搜索  `sherlocked_93` 加我好友，备注**加群**，我拉你入群～