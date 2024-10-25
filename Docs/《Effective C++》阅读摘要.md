#  《Effective C++》阅读摘要

[TOC]



声明 `declaration` 告诉编译器某个东西的名称和类型。

- 函数的声明称为签名 `signature`，也就是参数和返回类型。

定义 `definition` 提供编译器一些声明所遗漏的细节。

- 对对象，定义是编译器为此对象拨发内存的地点。
- 对函数或函数模板，定义提供了代码本体。
- 对类或模版类，定义列出它的成员。

初始化 `initialization`，是给予对象初值的过程。

- 对用户自定义的对象，初始化由构造函数完成。
- 声明为 `explicit` 的构造函数用来禁止非预期的隐式类型转换。
- 值传递的函数传参意味着会调用拷贝构造函数。

## 一、 让自己习惯 C++

### 1. 视 C++ 为一个语言联邦

现在的 C++ 可以视为 4 个次语言的集合：

1. **C 语言**，包括代码块 block、语句 statements、预处理器 preprocessor、内置数据类型 build-in data type、指针 pointer 等。
2. **OO 风格 C++**，包括类 class、构造函数 constructor、析构函数 destructor、封装 encapsulation、继承 inheritance、多态 polymorphism、虚函数 virtual、纯虚函数 pure virtual 等。
3. **Template C++**，范型编程 generic programming。
4. **STL**，是个特殊的 template 库，包含容器 container、迭代器 iterator、算法 algorithm、函数对象 function object等。

对于不同的 C++ 次语言，最佳实践会发生变化。例如对于内置数据类型而言，值传递往往比引用传递高效；而对于 OO 风格 C++，由于用户自定义构造与析构函数的存在，传递 const 引用类型往往更高效。

### 2. 尽量使用 const、enum、inline 代替 #define

或许应该说「用编译器替换预处理器」比较好，某种意义上说，预处理器不应被视为语言的一部分。

比如 #define 了一个宏变量后，这个变量对编译器来说是不可见的，因为编译器开始处理源码前就已经被预处理器移走了，所以宏变量并不会进入记号表内。

对于浮点常量，使用 const 声明会比使用 #define 使用更少的目标码(object code)，因为目标码中会出现多份浮点数。

`#define` 宏变量并不重视作用域，一旦定义了宏变量，它会在以后的所有编译过程中有效，除非在某处被 #undef。

`#define` 在预处理器宏替换的时候引入奇怪的问题。

对于形似函数的宏，最好使用 inline 函数替换，或使用 inline 模版函数。

### 3. 尽可能使用 `const`

声明为 `const` 可以帮助编译器侦测出错误用法。

对于类中的 `const` 成员函数，如果某些成员变量一定要被改变的话，可以声明为 mutable。

### 4. 确定对象被使用前已被初始化

如使用 C++ 的 C 次语言部分，且初始化可能增加运行期成本，那么不保证进行初始化，非 C 次语言部分会相反。比如使用数组 array 时就不保证其内容被初始化，而使用向量 vector 的时候就会保证内容被初始化。

比如对于内置数据类型 int，作为全局变量和静态变量会被初始化为 0，而作为函数的局部变量就不会被隐式初始化。这是因为全局变量和静态变量存放在程序的数据段，而局部变量存放在栈上。程序启动时，操作系统会数据段变量分配存储空间，并按照语言规范进行默认初始化（如果没有用户提供的初始化）。而局部变量的生命周期仅在其所在的函数或代码块中。当函数或代码块执行完毕，这些局部变量就会被销毁。为提高效率，编译器通常不会对栈上的局部变量进行初始化，除非程序员明确要求。如果尝试访问未初始化的局部变量，会得到一个不确定的值，这通常会导致程序出错。

所以最佳实践是，**在使用对象前始终进行初始化**。

对于内置类型以外的类型，初始化是构造函数的责任。对于类成员的初始化：

```cpp
// 构造函数初始化
class B {
public:
    explicit B(const int num, const std::string& name) {
        m_num = num;
        m_name = name;   // 赋值而非初始化
    }
    int m_num;
    std::string m_name;
};

// 成员初始化列表
class B {
public:
    explicit B(const int num, const std::string& name)
        : m_name(name), m_num(num) {} // 初始化
    int m_num;
    std::string m_name;
};
```

对于构造函数初始化方式，非内置类型（如这里的 `std::string`）成员变量的初始化发生在类对象构造过程时，此时会调用这些类型的默认初始化函数初始化这些成员变量（这里的 `m_name` 会用 `string` 的默认构造函数），然后才进入自定义的构造函数。所以对于非内置类型成员变量，自定义构造函数中的 = 是赋值。对于内置类型（如 `int`、`double`等）如这里的 `m_num`，进入构造函数前它们的初始值是未定义的。

对于成员初始化列表方式，内置类型和非内置类型的成员变量都是在构造函数执行时被初始化，所以**成员初始化列表方式的效率较高**。

注意，无论成员初始化列表中的顺序书写如何，类成员变量的初始化方式始终以其声明的顺序初始化。也就是说对于上面代码例子的写法，即使初始化列表中 `m_name` 写在前，实际上也是 `m_num` 先被初始化。

## 二、构造、析构、赋值运算

### 5. 了解 C++ 默默编写并调用哪些函数

编译器会隐式为类创建默认构造函数、拷贝构造函数、拷贝赋值操作符和析构函数。

默认创建的拷贝赋值运算符和拷贝构造函数行为基本一致，但某些情况下，编译器会拒绝给类创建拷贝赋值运算符：

1. 类具有引用类型成员变量，引用类型不允许指向不同对象。
2. 类具有 `const` 成员变量，更改 `const` 类型的成员是非法的。
3. 基类将拷贝赋值运算符声明为私有，派生类无法调用基类中私有方法。

### 6. 若不想使用编译器自动生成的函数，就该明确拒绝

如果不希望编译器自动生成某函数，可以将对应的函数声明为 private 并且不予实现，使用类似于下面这样的 Uncopyable 的类也可：

```cpp
class Uncopyable {
protected:
    Uncopyable() = default;
    ~Uncopyable() = default;

private:
    Uncopyable(const Uncopyable&);
    Uncopyable& operator=(const Uncopyable&);
};

class B : Uncopyable {}
```

或者在 C++11 后直接使用 `= delete` 声明即可。

### 7. 为多态基类声明 virtual 析构函数

当派生类对象经由一个基类指针被删除，而该基类带着一个非 virtual 的析构函数，其结果未定义——实际执行时通常发生的事对象的派生部分未被销毁。 

解决这个问题的方法很简单，给基类一个 virtual 的析构函数。

### 8. 别让异常逃离析构函数

析构函数不要抛出异常，如果一个被析构函数调用的函数可能抛出异常，析构函数应捕捉任何异常并吞下（catch）或者直接结束程序。

如果需要对某个操作函数运行期间抛出的异常作出反应，类应该提供一个普通函数（而非在析构函数中）执行该操作，如下：

```cpp
class DBConn {
  public:
  	void close() {   
      db.close();
      closed = true;
    }
  	~DBConn() {
      if (!closed) {  // 如果用户未关闭
        try { db.close(); }
        catch(...) {
          // 吞下异常，记录close调用失败日志
        }
      }
    }
  private:
  	DBConnection db;
  	bool closed;
}
```

### 9. 绝不在构造和析构过程中调用 virtual 函数 

不应该在构造函数和析构函数中调用 virtual 函数。

```cpp
struct TransBase {
  TransBase() { logTrans(); }
  virtual void logTrans() { cout << "TransBase" << endl; }
};

struct TransA : TransBase {
  TransA() { logTrans(); }
  virtual void logTrans() { std::cout << "TransA" << std::endl; }
};

int main() {
  TransA a;
}
// 打印：TransBase
//      TransA
```

派生类对象构造函数内，会先执行基类构造函数，再执行派生类构造函数。在派生类构造函数运行期间的基类构造过程中，基类的 virtual 函数并不会下降到派生类阶层：在基类构造期间，virtual 函数不是 virtual 函数。

由于基类构造函数的执行早于派生类构造函数，当基类构造函数执行时，派生类的成员变量并未初始化。如果此时调用的 virtual 函数下降到派生类阶层，要知道派生类函数必然使用其成员变量，而这些成员变量并未初始化，这是一种不安全行为。

如果在基类中使用运行期类型信息（runtime type information, ex: dynamic_cast, typeid）此时的对象也被视为基类类型。

根本的说，在派生类对象的基类构造期间，对象的类型是基类类型，而不是派生类类型。同样的道理也适用于析构函数。一个解决办法是将基类的 virtual 函数设为非 virtual，然后在派生类构造时传递相关参数给基类对应函数。

### 10. 令 operator= 返回一个 *this 的引用

关于赋值和+=操作符重载可以写成如下形式：

```cpp
class A {
 public:
  A(int val_) : val(val_) {}
  int getVal() const { return val; }

  A& operator=(const A& rhs) {
    val = rhs.getVal();
    return *this;
  }

  A& operator+=(A& rhs) {
    val += rhs.getVal();
    return *this;
  }

 private:
  int val;
};

int main() {
  A a(2), b(3), c(4);
  b += a += c;  // b: 9, a: 6, c: 4
  b = a = c;    // a: 4, c: 4, b: 4
}
```

为了实现连续操作，重载的赋值运算符需返回一个指向操作符左侧实参的引用。

### 11. 在 operator= 中处理自我赋值

自我赋值经常发生在对象赋值给自己时。

```cpp
class B {};
class A {
  B* pb;

 public:
  A() = default;

  // ❌ 一个不安全的operator=实现
  A& operator=(const A& rhs) {
    delete pb;
    pb = new B(*rhs.pb);
    return *this;
  }
};

int main() {
  A a;
  a = a;
}
```

对于自我赋值的场景，`operator=` 中的 `delete` 会销毁 `rhs` 也就是自己的 `pb`。

下面有两个实现可以实现自我赋值安全：

```cpp
// 自我赋值安全，不具备异常安全
A& operator=(const A& rhs) {
  if (this == &rhs) return *this; // 增加认同测试
  delete pb;
  pb = new B(*rhs.pb);  // 如果new抛出异常，此时pb已释放
  return *this;
}

// 自我赋值安全，异常安全
A& operator=(const A& rhs) {
  auto* old_p = pb;
  pb = new B(*rhs.pb);  // 即使new抛出异常，pb还保持原状，并未销毁
  delete old_p;
  return *this;
}
```

另一个常见且不错的解决办法是利用值传递会创建副本原理的 copy and swap 复制并交换技巧：

```cpp
void swap(A& rhs);  // 交换*this与rhs数据，见第29条
A& operator=(const A& rhs) {
  A a_(*rhs.pb);   // 用rhs制作一个副本
  swap(a_);        // 交换
  return *this;
}

// 或直接利用传参时的值传递
A& operator=(A rhs) {
  swap(rhs);
  return *this;
}
```

### 12. 复制对象时别忘其每个成分

如果你声明了自定义拷贝函数（自定义拷贝构造函数或拷贝赋值 `operator=` 运算符重载实现），那么如果你每为类增加一个成员变量，需同时修改对应的自定义拷贝函数。

1. 当你不使用默认拷贝构造函数，应确保复制对象内所有成员变量，以及基类部分。
2. 当你不使用默认 `operator=` 函数，而使用自定义 `operator=` 函数时，注意复制派生类所有成员变量，且调用所有基类的适当 `operator=` 函数。

对于一个基类 Base，其有自定义拷贝构造函数，以及自定义拷贝赋值运算符：

```cpp
class Base {   // 基类
  std::string name_ = "-";

 public:
  Base() = default;
  // 自定义拷贝构造
  Base(const Base &rhs) : name_(rhs.getName()) {}
  // 自定义拷贝赋值
  Base &operator=(const Base &rhs) {
    name_ = rhs.getName();
    return *this;
  }
  std::string getName() const { return name_; }
  void setName(const std::string &name) { name_ = name; }
};
```

观察以下派生类代码：

```cpp
class A : public Base {  // 派生类
  int member_id_;

 public:
  A() = default;
  // 派生类自定义拷贝构造
  A(const A &rhs) : member_id_(rhs.getMemberId()) {}   // ❌ 错误用法
  // 派生类自定义拷贝赋值
  A &operator=(const A &rhs) {   // ❌ 错误用法
    member_id_ = rhs.getMemberId();
    return *this;
  }
  int getMemberId() const { return member_id_; }
  void setMemberId(int member_id) { member_id_ = member_id; }
};

int main() {
  A a;
  a.setName("SHERlocked93");
  a.setMemberId(2);  // a "SHERlocked93" 2

  A b(a);   // b "-" 2 使用自定义拷贝构造
  A c = a;  // c "-" 2 使用自定义拷贝赋值
}
```

为什么拷贝构造函数并未正确拷贝待拷贝对象的基类部分呢，因为派生类的自定义拷贝构造函数并没有指定实参给基类构造函数，也就是 A 派生类构造函数的成员初始化列表中没有调用 Base 的自定义构造函数，所以实际上在执行 `b` 的拷贝构造过程中使用的是 `Base` 基类的 `default` 默认构造函数，因此 `b` 实例的 `name_` 是默认值。对于自定义拷贝赋值是类似的情况。

正确的方式如下：

```cpp
class A : public Base {  // 派生类
  int member_id_;

 public:
  A() = default;
  // 派生类自定义拷贝构造
  A(const A &rhs) : Base(rhs), member_id_(rhs.getMemberId()) {}  // 调用基类拷贝赋值构造函数
  // 派生类自定义拷贝赋值
  A &operator=(const A &rhs) {
    Base::operator=(rhs);           // 调用基类operator=
    member_id_ = rhs.getMemberId();
    return *this;
  }
  int getMemberId() const { return member_id_; }
  void setMemberId(int member_id) { member_id_ = member_id; }
};

int main() {
  A a;
  a.setName("SHERlocked93");
  a.setMemberId(2);  // a "SHERlocked93" 2

  A b(a);   // b "SHERlocked93" 2
  A c = a;  // c "SHERlocked93" 2
}
```

另外注意，即使拷贝赋值运算符重载实现和拷贝构造函数的实现中有相近代码，也不要相互调用，因为语义上没有意义，通常消除重复代码的方式是新建一个类似于 `init` 的成员函数给他们调用。

## 三、资源管理

对于 C++ 中的资源，一旦用了它，当你不再使用时，必须将其还给系统，如动态分配内存 heap、文件描述符 file descriptors、互斥锁 mutex locks、数据库连接 database connection、网络 sockets 等。

本章主要讨论如何合理管理资源。

### 13. 以对象管理资源

以对象管理资源的观念通常被称为资源获取即初始化(Resource Acquisition Is Initialization, RAII)，通过 RAII 可以将资源的生命周期与某个对象的生命周期绑定在一起，当对象被析构时，也会释放对应资源，从而达到防止资源泄漏的目的。

对于一个创建某资源管理类实例并返回一个指针的方法 `A* createManager()`， 使用者有责任释放这个指针，但实际情况控制流经常无法触及 `delete` 语句。此时可以使用 `auto_ptr` 或 `share_ptr` 来在管理资源对象析构时自动释放该指针：

```cpp
{
  std::share_ptr<A> pAptr(createManager());
  // 出作用域后自动释放pAptr指向的资源
}
```

### 14. 在资源管理类中小心 copying 行为

并不是所有的资源都是在堆上管理的（heap-based），这时候智能指针就不适用，需要自己实现一个资源管理类 RAII。处理一个 RAII 对象的复制行为通常有下面几种方式：

1. **禁止复制**：参考**条款06**，许多时候允许 RAII 对象被复制并不合理。
2. **共享底层资源的所有权**：成员用`shared_ptr`管理，并自定义`deleter`（析构时`unlock`而不是释放`Mutex`对象）。
3. **深度复制底层资源**：自定义拷贝构造函数和拷贝赋值操作符，拷贝 RAII 对象时，连带其所管理的资源（不仅是指针，还有指针所指的内容）一并做一份深拷贝。
4. **转移底层资源的所有权**：当希望资源只有一份时，将底层资源用独占所有权的 `unique_ptr` 进行管理，自定义拷贝构造函数和拷贝赋值操作符以完成**所有权转移**（`std::move`）的动作。

### 15. 在资源管理类中提供对原始资源的访问

很多时候，APIs直接指涉资源管理类中的原始资源（raw resources），这就需要资源管理类要提供访问原始资源的方法。

对智能指针而言，提供了`get`方法来获取其中的裸指针；此外，智能指针还重载了`operator->`和`operator*`操作符，使其能够隐式地转换成裸指针，从而能像裸指针一样去访问类的成员函数。

对于自定义的资源管理类，同样也有**显式**和**隐式**两种方式转换成原始资源。一般来讲，显示转换更安全，隐式转换更方便。

```cpp
FontHandle getFont();							// C API 获取字体资源
void releaseFont(FontHandle fh);				// C API 释放字体资源
void changeFontSize(FontHandle f, int newSize);	// C API 直接指涉原始资源

// 自定义资源管理类
class Font {
public:
    explicit Font(FontHandle fh) : f(fh){}
	  ~Font() { releaseFont(f); }
    
    // 显示转换函数
    FontHandle get() const { return f; }
    // 隐式转换函数
    operator FontHandle() const { return f; }
private:
	FontHandle f;    
};

// 用法
Font f(getFont());
int newFontSize = 10;
...
// 显示转换
changeFontSize(f.get(), newFontSize);
// 隐式转换
changeFontSize(f, newFontSize);

// 一种隐式转换的可能的误用
Font f1(getFont());
FontHandle f2 = f1;  // 本意是复制一个Font对象，却复制了一个原始资源
```

### 16. 成对使用new和delete时要采取相同形式

一句话总结：`new` 与 `delete` 搭配使用，`new[]` 与 `delete[]` 搭配使用。因为数组所用的内存通常还包括数组大小的记录，以便 `delete` 知道需要调用多少次析构函数，单一对象则没有。如果这两个方式错配，则会造成错误析构。

尽量不要对数组形式使用`typedef`，容易造成`new`和`delete`的错配。

如果可以，直接使用 `vector`、`list` 等 C++ 标准库里的模版，不要使用数组。

### 17. 以独立语句将 new 出来的对象置入智能指针

考虑下面的代码：

```cpp
// 不推介的方式
processWidget(std::shared_ptr<Widget>(new Widget), getPriority());

// 推荐的方式
std::shared_ptr<Widget> pw(new Widget);		// 在独立语句中将 newed 对象置入智能指针
processWidget(pw, getPriority());			
```

上一种方式代码总共做了3件事：

1. 调用`getPriority`;
1. 执行`new Widget()`;
1. 调用`std::shared_ptr`的构造函数；

C++ 编译器总能保证先步骤2后步骤3的执行次序（因为2是3的入参），但却无法保证步骤1的执行次序不在2和3之间（可能出于优化性能的考虑）。若在这种情况下，步骤1的执行过程中抛出异常，步骤2返回的指针将会被遗弃，无法置入智能指针中，从而导致了资源泄漏。

**以独立语句将 newed 对象置入智能指针** （下面的用法）可以规避该风险，因为编译器对于跨越语句的各项操作，没有重新排列的自由。

## 四、设计与声明

### 18. 让接口容易被正确使用，不易被误用

想要开发一个容易被正确使用，不易被误用的接口，首先要考虑使用者会犯什么错误，并设法阻止。

限制类型内什么事情可做，什么事情不可做，比如不能修改的变量设置 `const`。

尽量让你的自定义类型的行为与内置类型一致，比如容器类变量增加一个 `.size` 方法。

不要寄希望于使用者为你的接口“擦屁股”，比如不要让你的方法返回一个指向堆的指针并指望使用者会销毁其中申请的内存。

### 19. 设计类犹如设计type

1. 新 type 的对象应当如何被创建和销毁？决定构造函数和析构函数的实现。
2. 对象的初始化和对象的赋值该有什么样的差别？决定构造函数和赋值操作符的实现。
3. 新 type 的对象如果被 passed by value（传值），意味着什么？决定拷贝构造函数的实现。
4. 什么是新 type 的“合法值”？决定class必须维护的约束条件（invariants）,必须进行的错误检查工作，异常抛出，非法值拦截，返回错误码等。
5. 新 type 需要配合某个继承图谱（inheritance graph）吗？如果继承自某个基类，则受限于基类virtual和non-virtual函数的设计；若允许其他类继承你的类，则要考虑你所声明的函数，特别是析构函数（条款07），是否应当为virtual。
6. 你的新 type 需要什么样的类型转换？若希望T1类型可以隐式的转换为T2类型，要么在 class T1 内实现一个类型转换函数operator T2()，要么在 class T2中实现一个non-explicit-one-argument构造函数。若你不希望隐式转换存在，则得专门实现负责执行转换操作的函数。关于隐式转换和显示转换的讨论还可见条款15。
7. 什么样的操作符和函数对此新 type 而言是合理的？决定class将要声明哪些函数，函数是成员函数还是非成员函数，参见条款23，24，26。
8. 什么样的标准函数应当被驳回？参见条款06，不希望被拷贝的类应当将copy构造函数和copy赋值操作符声明为private，或使用C++新特性 `=delete`。
9. 谁该取用新type的成员？决定成员该为 `private/protected/public`，以及决定哪一个外部类或函数能成为 `friend`。
10. 什么是新 type 的“未声明清楚的接口”（undeclared interface）？参见条款29。
11. 新 type 有多么一般化？对于一般化的问题处理，考虑定义一个新的 class template 而不是一个新的class。
12. 你真的需要一个新 type 吗？如果只是定义一个派生类为既有的类添加新的功能，说不定单纯定义一个或多个非成员函数或者模板更合适。

### 20. const 引用传递优于按值传递

以值传递参数时，函数形参是实参的一个副本（确保函数不会修改实参），这意味着要执行拷贝构造函数，然后在函数退出时，函数形参生命周期结束，会再执行析构函数。这些可能是不小的开销，尤其是当类存在成员对象或者继承关系时，成员对象和基类的构造和析构也在这个过程中。

以 `const` 引用传递参数时，没有任何新对象被创建，因此不涉及构造和析构操作。其中 const 是关键，其同样可以保证函数不会修改实参。

不只是函数参数，返回值也遵循同样的规则。但请注意，不要返回局部变量的引用，因为局部变量会在函数退出时到达生命周期的终点，返回局部变量的引用只会得到一个悬空的变量。

以引用方式传递参数可以避免对象切割问题（slicing problem）。所谓对象切割，指的是当一个派生类对象以值方式传递给一个基类参数时，基类的拷贝构造函数会被调用，从而导致该对象作为派生类的特性被切割掉，退化成一个基类对象。而以 by reference-to-const 的方式传递参数则可以避免对象切割问题。

从 C++ 编译器的底层实现来看，引用往往以指针形式来实现，因此传递引用通常意味着真正传递的是指针。所以对于内置数据类型（如 int），直接传值反而效率更高。

### 21. 必须返回对象时，别妄想返回其引用

通常情况下，不要返回如下几种对象的引用（指针同理）：

1. 不要返回局部栈对象（局部变量）的引用。局部变量会在函数退出时到达生命周期的终点，返回局部变量的引用只会得到一个悬空的变量。
2. 不要返回局部堆对象（函数中 `new` 的对象）的引用。将销毁对象的责任推到了函数之外，甚至有时候连销毁的机会都没有。
3. 不要返回局部 `static` 对象（静态局部变量）的引用。和所有静态对象一样，首先能够想到的就是多线程安全性。除此之外，静态局部变量只有一份，只初始化一次，不同函数更新的是同一份变量。

### 22. 将成员变量声明为私有

成员变量应该是 `private`，如果它们不是，就会有无限量的函数可以访问它们，它们也就毫无封装性，一旦将一个成员变量公开且被广泛使用，后面再想对它做修改就异常艰难。

1. 访问对象成员变量的唯一方法就是通过 `get` 成员函数。
2. 根据是否有 `get/set` 成员函数来精确控制成员的读写权限。
3. 将成员变量隐藏在函数接口的背后，可以为所有可能的实现提供弹性。如可以使得成员变量被读或被写时轻松通知其它对象、验证类的约束条件以及函数的前提与事后状态、可以在多线程环境中执行同步控制等等。

### 23. 非成员非友元函数替换成员函数

`namespace` 可以跨越多个源码文件，而 `class` 不能，因此可以将不同功能的非成员函数放在不同的 `.h` 头文件的同一 `namespace` 下，这样可以让模块划分更清晰，还可以降低不必要的编译依赖关系。这也是 C++ 标准程序库的组织方式，使用者只需要包含自己需要使用的模块的头文件（如 `#include <vector>` ）。

### 24. 当所有参数都需要进行类型转换时，将函数定义为非成员函数

如果你需要为某个函数的所有参数（包括被 `this` 指针所指的那个隐喻参数）进行类型转换，那么这个函数必须是非成员函数。

考虑下面这个例子：

```cpp
// 有理数类
class Rational {
public:
    Rational(int numerator = 0, int denominator = 1)
        : numerator_(numerator), denominator_(denominator) {}
    // 有理数相乘，分子x分子，分母x分母
    const Rational operator* (const Rational & rhs) const {
        return Rational(numerator_ * rhs.numerator_(),	
                        denominator_ * rhs.denominator());
    }
    
    int numerator() const { return numerator_; }     // 分子
    int denominator() const { return denominator_; } // 分母
    
private:
    int numerator_ = 0;
  
    int denominator_ = 1;
};
```

对于这个有理数类：

1. 构造函数是非 `explicit` 的，是为了支持整数到有理数的隐式转换；
2. 乘法运算符 `operator*` 被重载成了一个成员函数；

有下面的运算结果：

```cpp
Rational oneEighth(1, 8);   // 有理数 1/8
Rational oneHalf(1, 2);     // 有理数 1/2

Rational result = oneHalf * oneEighth;	// 正确
result = result * oneEighth;  // 正确
result = oneHalf * 2;					// 正确
result = 2 * oneHalf;					// 错误，无法通过编译
```

为什么有上面的结果呢，对于 `oneHalf * 2`，由于 `oneHalf` 是 `Rational` 类的实例，且非 `explicit` 的 `operator*` 运算符可以将 `int` 类型的变量隐式转换为 `Rational` 类实例，所以这个表达式等价于 `oneHalf.operator*(2)`。

但是对于 `2 * oneHalf`，整数 2 并没有对应的类成员函数 `operator*`，编译器会尝试在作用域中寻找可以这样调用的非成员函数 `operator*(2, oneHalf)`，但并没有找到。

对于本例，比较好的办法是移除类 `Rational` 类中的 `operator*` 方法，然后增加一个非成员函数 non-member 函数：

```cpp
const Rational operator*(const Rational& lhs, const Rational& rhs) {
  return Rational(lhs.numerator() * rhs.numerator(), lhs.denominator() * rhs.denominator());
}
```

## 五、实现

### 26. 尽可能延后变量定义式的出现时间

可以避免不必要的构造和析构成本：比如在使用某对象前，因某些原因函数返回或抛出异常，若已定义了该对象，便仍需要承担构造和析构成本，即便你并未真正的使用它。

```cpp
std::string a;
if (...) throw logic_error("some err");  // 如果这里抛错，则上面的变量的构造与析构成本是不必要的
```

延后变量定义式的真正意义并不只是延后变量定义式的位置，甚至**应当延后定义直到能为其提供初值实参为止**。这样可以避免无意义的构造成本，而且用具有明显意义的初值来初始化变量，还可以附带说明变量的目的。

对于循环，考虑下面两种写法的成本：

```cpp
// 定义于循环外 成本：1次构造 + 1次析构 + n次赋值
Widget w;
for(int i = 0 ; i< n; ++i){
    w = 取决于 i 的某个值;
    // ...
}

// 定于于循环内 成本：n次构造 + n次析构
for(int i = 0 ; i< n; ++i){
    Widget w(取决于 i 的某个值);
    // ...
}
```

### 27. 尽量少做转型

转型（casts）会破坏C++的类型系统（type system）。

```cpp
(T)expression   // C风格的转型动作（旧式转型）
T(expression)   // 函数风格的转型（旧式转型）

// C++风格的转型动作（新式转型）
const_cast<T> (expression)     // 移除 const
dynamic_cast<T> (expression)   // 安全向下转型
reinterpret_cast<T> (expression)  // 处理无关类型之间的低级转型
static_cast<T> (expression)    // 强制隐式转换
    
// C++11 推出针对智能指针的转型
const_pointer_cast<T> (expression)
dynamic_pointer_cast<T> (expression)
reinterpret_pointer_cast<T> (expression)
static_pointer_cast<T> (expression)
```

考虑下面的实现：

```cpp
class Window {
public:
    virtual void onResize() { ... }
};

class SpecialWindow : public Window {
public:
    virtual void onResize() {
        static_cast<Window>(*this).onResize();  // 错误调用基类方法方式
        // Window::onResize();    正确调用基类方法方式
    }
};
```

此处可能原意是希望派生类中的虚函数先调用基类的虚函数实现，然后再执行一些派生类专属的操作。但是转型动作构建了一个 `*this` 对象的基类类型副本，并由这个副本调用 `onResize` 函数，那么通用操作所修改的属性是这个副本的，而不是 `*this` 对象的。

尽量避免使用转型，尤其是在注重效率的代码中避免使用`dynamic_cast`。

### 28. 避免返回 handles 指向对象内部成分

所谓的句柄 `handles` 包括指针、引用和迭代器。

如果你在某个类内部传出 `handler`，那么就可能出现外部的 `handler` 比其所指对象更长寿的情况。而且用户也可以通过返回的 `handler` 间接的更改实例对象的内部数据。

### 29. 异常安全的函数

当异常被抛出时，异常安全的函数会不泄漏任何资源，不允许数据被破坏。

异常安全函数提供以下三个保证之一：

1. 基本承诺：如果异常被抛出，程序内的任何事物仍然保持在有效状态下。没有对象或数据结构会因此而被破坏；
2. 强烈保证：如果异常被抛出，程序状态不改变。即保持原子性，要么函数成功，要么函数失败；
3. 不抛异常保证：承诺绝不抛出异常，因为它们总能完成它们原先承诺的功能。

### 30. 了解 `inline`

`inline` 一般来说可以令程序运行速度变快，但也不是绝对的。它会使程序体积增大，如果过度热衷 inlining 导致程序体积太大，那么会导致程序出现换页 `paging` 行为，降低指令高速缓存装置的命中率 instruction cache hit rate，这样反而会降低运行效率。

`inline` 只是对编译器的一个申请，不是强制命令。它一般定义在头文件内，在编译过程中会将一个函数调用替换为被调用函数的本体。

`inline` 函数和 `template` 函数通常都被定义于头文件中（这是因为 `inline` 的函数体替换操作和 `template` 的具现化操作通常都是在编译期执行的），而且不少简短的 `template` 函数都是带有 `inline` 关键字，但两者并无必然的因果关系。

### 31. 将文件间的编译依存关系降到最低

C++ 并没有把将接口从实现中分离这件事做的很好。即头文件中类定义不仅可以包含声明，而且可以有实现。

考虑下面的实现：

```cpp
#include <string>
#include "date.h"		  // 其中定义 Date 类
#include "address.h"	// 其中定义 Address 类

class Person {
public:
    // 接口
    Person(const std::string& name, const Date& birthday, const Address& addr);
    std::string name() const;
    ...
private:
    // 实现
    std::string theName;
    Date theBirthDate;
    Address theAddress;
};
```

在上例中，`Person` 类头文件通过 `#include` 与 `date.h` 和 `address.h` 形成了**编译依存关系**（compilation dependency），如果这些头文件中有任何变化，或者这些头文件所依赖的其他头文件有任何变化，则任何使用了 `Person` 类的文件都得重新编译。

推荐的做法是前置声明和实现类指针 pimpl （pointer to implementation）方式可以实现接口和实现的分离：

```cpp
// person.h
#include <string>
#include <memory>

// 用前置声明替代 #include
class PersonImpl;	// Person实现类的前置声明
class Date;
class Address;

class Person {
public:
    // 接口 只声明，实现部分放到cpp中
    Person(const std::string& name, const Date& birthday, const Address& addr);
    std::string name() const;
    std::string birthDate() const;
    std::string address() const;
    ...
private:
    std::shared_ptr<PersonImpl> pImpl;	// 指针指向Person实现类
};

// person.cpp
#include "person.h"
#include "person_impl.h"
#include "date.h"
#include "address.h"

Person::Person(const std::string& name, const Date& birthday, const Address& addr)
    : pImpl(new PersonImpl(name, birthday, addr)) {}

std::string Person::name() const {
    return pImpl->name();
}
```

分离的关键点在于用**声明的依存性**替代**定义的依存性**。这正是编译依存性最小化的本质：让头文件尽可能自我满足，如果做不到，则也要依赖于其他文件的声明式而非定义式。

## 六、继承与面向对象设计

### 32. 公有继承是 is-a 关系

以 C++ 进行面向对象编程时，最重要的一条规则是：public inheritance（公有继承）意味着 is-a 的关系。也就是说，每一个公有继承的派生类对象同时也是一个基类对象，反之不成立，基类是更一般化的概念，派生类是更特殊化的概念。即里氏替换原则（Liskov Substitution Principle）：任何基类可以出现的地方，子类一定可以出现。

### 33. 避免遮掩继承而来的名称

所谓遮掩，是指对名称（变量名或函数名）的覆盖。最常见的就是，内层作用域的名称会遮掩外层作用域的名称。

在继承体系中，派生类作用域的名称会遮掩基类作用域的**名称**，与名称的类型无关。

```cpp
class Base {
   public:
    virtual void mf1() = 0;   // 纯虚函数
    virtual void mf1(int) {}  // 重载
};
class Derived : public Base {
   public:
    virtual void mf1() {}  // 纯虚函数重写
};

Derived d;
int x;
d.mf1();   // 没问题，调用Derived::mf1
d.mf1(x);  // 编译错误 error: 'x' was not declared in this scope
           // Base::mf1被Derived::mf1遮掩，即使只是名称一样，签名不一样
```

这个例子中，`mf1` 遮掩了基类中的所有同名函数，导致基类的重载不可用。

可以使用 `using` 方式解决：

```cpp
class Derived: public Base {
    using Base::mf1;     // 使用using声明式可以让Derived忽略名称遮掩，看到Base作用域内的函数（并且 public）
    virtual void mf1();			// 纯虚函数重写
};

Derived d;
int x;
d.mf1();		// 没问题，调用Derived::mf1
d.mf1(x);		// 现在没问题，调用Base::mf1
```

`using` 声明会令继承而来的某给定名称的所有同名函数都在派生类中可见。

如果派生类以私有方式继承基类，则使用转发函数 forward function：

```cpp
class Derived: private Base {	// 注意是private继承
    virtual void mf1() {		// 转发函数
        Base::mf1();			  // 调用基类的实现
    }
};

Derived d;
int x;
d.mf1();		// 没问题，调用Derived::mf1
d.mf1(x);		// 编译错误，Base::mf1被Derived::mf1遮掩
```

### 34. 区分接口继承和实现继承

公有继承下，成员函数继承由两部分组成：函数接口继承和函数实现继承。设计类时，一定要清楚我们希望的，到底是继承接口还是继承实现，还是两个都要。

1. 对于公有继承，成员函数（无论是非虚函数、虚函数还是纯虚函数）的接口总是会被继承；
2. 声明纯虚函数的目的是为了让派生类只继承函数的接口；
3. 声明虚函数的目的是让派生类继承该函数的接口和缺省实现。如果派生类没有实现该函数，则默认使用父类的函数实现；
4. 声明非虚函数的目的是为了令派生类继承函数的接口及一份强制性实现。由于非虚函数代表的意义是不变性（invariant）凌驾特异性（specialization），所以它绝不该在派生类中被重新定义。

### 36.  绝不重新定义继承而来的非虚函数

虚函数是动态绑定，而非虚函数是静态绑定。

```c++
class Base {
public:
    void mf();
}; 
```

如果这时候有个 D 代码继承 B，并在 D 里面也实现了 mf 方法：

```c++
class Derived: public Base {
public:
    void mf();
};

Derived x;
Base* pb = &x;
Derived* pd = &x;

pb->mf(); //调用 B::mf
pd->mf(); //调用 D::mf
```

那么由于 `mf` 是非虚的，所以都是静态绑定，实际上就会很诧异的各自调用到各自的方法中。所以千万不要新定义继承而来的非虚函数。

### 37. 绝不重新定义继承而来的缺省参数值

虚函数是动态绑定的，而缺省参数值是静态绑定的。

```cpp
enum class ShapeColor 
{ 
    Red = 0,
 	  Green,
 	  Blue
};

class Shape {
public:
    virtual void draw(ShapeColor color = ShapeColor::Red) const = 0;
};

class Rectangle: public Shape {
public:
    // 派生类重新定义了缺省参数值
    virtual void draw(ShapeColor color = ShapeColor::Green) const override;
};

class Circle: public Shape {  // 与Rectangle继承同一个纯虚基类
public:
    // 派生类移除了缺省参数值
    virtual void draw(ShapeColor color) const override;
};

// 用户代码
Shape* ps;					// 静态类型为Shape*，无动态类型
Shape* pc = new Circle;		// 静态类型为Shape*，动态类型为Circle*
Shape* pr = new Rectangle;	// 静态类型为Shape*，动态类型为Rectangle*
```

静态类型是指声明的类型，动态类型的意思是目前所指对象的类型，会随着赋值动作而变化。

由于虚函数是动态绑定的，即究竟调用虚函数的哪一种实现，取决于调用对象的动态类型。所以：

```cpp
pc->draw(ShapeColor::Red);// 调用Circle::draw(ShapeColor::Red)
pr->draw();		            // 调用Rectangle::draw(ShapeColor::Red)
```

## 七、模板与泛型编程

### 41. 了解隐式接口和编译期多态

类和模板都支持接口（interfaces）和多态（polymorphism）。

对于类而言，接口是显式的，多态是通过虚函数实现的**运行期**多态。

对于模板而言，接口是隐式的，多态则是通过模板具现化和函数重载解析（function overloading resolution）实现的**编译期**多态。

