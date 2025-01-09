# C++ 为什么需要 extern "C"

[toc]

在 C++ 调用 C 语言编译器编译的库时，是不是经常遇到下面这个报错：

```bash
error LNK2019: 无法解析的外部符号 "int __cdecl add(int,int)" (?add@@YAHHH@Z)，函数 main 中引用了该符号
```

正如 [《Effective C++》](https://juejin.cn/post/7429677850514784308) 开篇所说， C++ 是一个 C 语言、OO 风格、模板、STL 风格组成的语言联邦，C++ 是可以直接引入 C 语言代码编译的库的，而 C 语言和 C++ 由于链接器符号设计的差异，引发了一些问题，下面一起讨论一下。

## 1. C++ 与 C 的符号差异

与 C++ 不同，C 语言是不支持命名空间、类和函数重载的，因此它的符号名称简单直接，只需函数名即可标识。而对于 C++，为了唯一标识共享了相同名称的函数或方法，C++ 链接器在为函数入口点建立符号时，会使用**名称修饰**（Name Mangling）来包含函数的输入参数的信息。

名称修饰会将函数名、函数的从属信息、函数的参数列表进行组合，最后生成可以保证唯一性的符号名称，比如上述报错信息中的 `?add@@YAHHH@Z` 就是 C++ 链接器为签名为 `int add(int,int)` 的函数生成的修饰名称。

注意，由于名称修饰没有统一的标准，不同编译器有自己的生成规则，不同编译器为同一个源文件中的同一个符号生成的修饰名称很可能是不一样的。

## 2. C++ 中编译动态库

比如，下面有一个 `mylib` 的头和源文件，代码如下：

```cpp
// mylib.h
namespace hello {
 int add(int a, int b);
 double add(double a, double b);
}

// mylib.cpp
#include "mylib.h"
int hello::add(int a, int b) { return a + b; }
double hello::add(double a, double b) { return a + b; }
```

在 Linux 环境下，使用 `g++` 执行编译，设置导出动态库为 `libmylib.so`，然后查看导出的动态库中的符号：

```bash
# linux 下编译为 libmylibc.so
g++ -shared -fPIC -o libmylib.so mylib.cpp

# 查看导出的动态符号
objdump -T libmylib.so

# win下编译生成动态库，同时生成导入库
# cl /LD /MD mylib.cpp /link /OUT:mylib.dll /IMPLIB:mylib.lib
# win下查看动态符号
# dumpbin /EXPORTS mylib.dll
```

结果如下：

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/202501081908503.png)

动态库导出的符号中有两个函数，分别是 `hello::add(int, int)` 和 `hello::add(double, double)`，其符号名称被编译器修饰为了 `_ZN5hello3addEii` 和 `_ZN5hello3addEdd`，符号名中包含了命名空间、函数名及参数类型等信息，其符号类型为 DF 也就是函数符号 Function Symbol。

最前面一列的一长串 8 个字节的 `0000000000001115` 为这个符号在动态库中的地址偏移量，在动态链接过程中，动态链接器会根据名称修饰后的符号名称（如 `_ZN5hello3addEii`）找到动态库中对应的符号地址，加上动态库在内存中的基地址，计算出符号在进程地址空间中的绝对地址，可执行文件就可以拿到函数具体的地址了。

后面的 `g` 表示全局符号 Global Symbol 意为这个符号是对外可见的，`.text` 表示符号所在的节 Section 为代码段，之后的 8 个字节为代码段长度。

## 3. 使用 `extern "C"` 避免名称修饰

当我们在 C++ 中调用 C 语言库时，为了解决符号差异问题，可以使用 `extern "C"`  指示编译器按照 C 语言的方式生成符号，避免名称修饰。

修改 `mylib.h`  如下：

```cpp
// mylib.h
#ifdef __cplusplus
extern "C" {
#endif

int add(int a, int b);

#ifdef __cplusplus
}
#endif

// mylib.cpp
#include "mylib.h"
int add(int a, int b) { return a + b; }
```

然后执行编译，对于 `extern "C"` 的我们导出为 `libmylibc.so`

```bash
# 编译为 libmylibc.so
g++ -shared -fPIC -o libmylibc.so mylib.cpp

# 查看导出的动态符号
objdump -T libmylibc.so
```

结果如下：

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/202501090837733.png)

可以看到这个符号就叫 `add`，没有经过名称修饰，也就是说如果声明了 `extern "C"` ，确实影响了链接器生成符号时的名称修饰行为。

## 4. 为什么调用 C 标准库函数时不需要 `extern "C"`

在 C++ 编译器中，即便 C 风格的函数不需要名称修饰，链接器默认也会为其创建带修饰的名称。如果希望避免名称修饰，需要使用 `extern "C"` 关键字来告知链接器不要修饰符号名称，那么链接器会创建不带修饰的符号名称。

在编写 C++ 代码时，我们经常调用 C 语言标准库中的函数，如 `strcpy`、`memcpy` 和 `printf`。为什么这些函数不需要显式地使用 `extern "C"` 呢？实际上，这些 C 标准库的头文件（如 `stdio.h` 和 `string.h` 可以点进去看看）在 C++ 环境中已经被包裹在 `extern "C"` 中。因此，C++ 编译器会自动处理这些符号，避免名称修饰。

---

网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出，如果本文帮助到了你，别忘了点赞支持一下，你的点赞是我更新的最大动力！~

> 参考文档：
>
> 1. [高级C/C++编译技术](https://book.douban.com/subject/26414485/)

PS：本文同步更新于在下的博客 [Github - SHERlocked93/blog](https://github.com/SHERlocked93/blog) 系列文章中，欢迎大家关注我的公众号 `CPP下午茶`，直接搜索即可添加，持续为大家推送 CPP 以及 CPP 周边相关优质技术文，共同进步，一起加油~

另外可以加入「前端下午茶交流qun」，vx 搜索  `sherlocked_93` 加我，备注 **1**，我拉你～