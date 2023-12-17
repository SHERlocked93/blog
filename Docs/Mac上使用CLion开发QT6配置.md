# Mac 上使用 CLion开发 QT6 配置

[TOC]

QtCreator 的开发体验自然是不如 CLion 的，刚好最近有开发 QT6 的需求，要在 CLion 中开发 QT 需要做一些配置，这里记录一下，看起来简单，其实也有一些坑，留作后询，且不定期更新。

## 1. 安装 QT6

在线安装地址在官网地址 ： https://download.qt.io/official_releases/online_installers/

也可以选择[清华大学源](https://mirrors.tuna.tsinghua.edu.cn/qt/official_releases/online_installers/)

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20231209163002697-20231209-zZc3Qs.png)

对应自己的系统选择版本就可以，开始需要登录 QT 账户，这需要在 QT 的[官网](https://www.qt.io/)注册账号，登录之后就一直下一步安装了。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20231209165358046-20231209-CWYbos.png)

选择组件的时候选上感兴趣的组件，下面是我的选择，这次没安装上也没关系，后面安装结束之后还可以使用 Qt Maintenance Tool 增删和更新组件。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20231209165845360-20231209-IwshZo.png)

主要是 QtCreator 和 QT 库，安装完就可以配置 CLion 了。

## 2. 配置工具

### 2.1 配置工具链

首先在 CLion 配置的 `构建、执行、部署 -> 工具链` 中增加一个工具链，我这里命名为 QT，路径选择你刚刚安装路径下面的 Qt Creator.app 应用，下面的 CMake 和调试器什么的可以带出来。

![image-20231209170019327](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20231209170019327-20231209-EbfjZQ.png)

### 2.2 配置 CMake

QT6 及之后全面使用 CMake 而不是 QMake 来管理项目，这是好事，毕竟现在 CMake 使用的越来越广泛，已经是事实意义上的标准工具链了。

下面做一下 CMake 的配置，这样 CLion 在打开 QT 的应用的时候，CMake 才能找到 QT 的库文件，代码才能高亮。在 `构建、执行、部署 -> CMake` 中增加一个配置，我这里把默认的 Debug 配置复制了一个，如下

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20231209170446464-20231209-rK7aYD.png)

### 2.3 配置 QtDesigner

如果希望像 QtCreator 那样对 UI 文件修改，需要配置一下外部工具 QtDesigner，如下

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20231209170802900-20231209-hqbF0O.png)

这里注意了，首先程序路径要选到安装的 QtCreator 内部 Designer 的 exec 可执行文件。

另外，实参 `$FileName$` 必不可少，否则我们在 UI 文件上右键只能打开 Designer 而无法打开当前文件。

### 2.4 配置 UIC

为什么要配置 UIC 呢，因为如果文件中希望索引到 UI 文件的控件，需要 `#include "./ui_mainwindow.h"` 这样引入一个由 UI 生成的头文件，由于 `.ui` 文件是 XML 文件，这个头文件是需要 UIC 这个工具生成的，如下

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20231209172000172-20231209-IFodbR.png)

这个实参就是 UIC 要生成的文件名，比如在 `mainwindow.ui` 上右键使用 UIC，那么生成的就是 `-o` 命令后面这个文件名模板，也就是 `ui_mainwindow.h`

如果你修改了 UI 之后，发现在源文件中还是找不到这个控件，那么就需要在 `.ui` 文件上右键执行一下这个 UIC 工具。

![image-20231209172510342](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20231209172510342-20231209-wAidG5.png)

QtCreator 同理，有时候 QtCreator 抽风，修改了 UI 文件之后还是找不到这个控件，就得去生成文件夹下把 `ui_xxx.h` 删掉，然后重新构建一下就行了。

注意，如果 CMake 下配置了 `set(CMAKE_AUTOUIC ON)` 那么在运行项目的时候，CMake 会自动将 UI 文件转化为 `ui_xxx.h` 放在生成目录下。

## 3. 进入开发

### 3.1 生成项目

至此我们就可以进入开发了，在新建项目的时候注意选择一下 CMake 前缀路径

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20231209173936095-20231209-Iy11yT.png)

新建的时候没选也没关系，新建完在 `CMakeLists.txt` 文件中加一句 `set(CMAKE_PREFIX_PATH "...")` 再重新加载 CMake 项目就可以了。

CMake 文件如下：

```cmake
cmake_minimum_required(VERSION 3.27) # cmake版本
project(helloworldqt)   # 项目名

set(CMAKE_CXX_STANDARD 20) # 使用的CPP标准
set(CMAKE_AUTOMOC ON)   
set(CMAKE_AUTORCC ON)   
set(CMAKE_AUTOUIC ON)   

# 前缀配置，cmake 将在这个路径下查找包和库，注意需要放在 find_package 前
set(CMAKE_PREFIX_PATH "/Users/sherlocked93/Qt/6.6.1/macos/lib/cmake")

find_package(Qt6 COMPONENTS Core Gui Widgets REQUIRED)  # 需求组件 

add_executable(helloworldqt main.cpp)     # 可执行文件目标
target_link_libraries(helloworldqt Qt::Core Qt::Gui Qt::Widgets)  # 链接
```

解释一下用于配置 CMake 和 Qt 的自动化集成工具的几个选项：

1. `CMAKE_AUTOMOC`：如项目中使用了QObject 宏、信号槽机制，CMake 会自动调用 moc 工具来生成对应的 MOC 文件和相应 cpp 代码。
2. `CMAKE_AUTORCC`：让 CMake 自动处理 `.qrc` 资源文件，CMake会自动检测项目中的资源文件，并生成对应代码，使得项目在运行时访问这些资源。
3. `CMAKE_AUTOUIC`：让 CMake 自动处理 `.ui` 文件，转化为对应 `ui_xxx.h` 放在生成目录的 autogen 文件夹下。

### 3.2 增加 UI 文件

然后新建一个 Qt UI 类

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20231209175246582-20231209-oXj1P1.png)

创建一个 UI 文件，在其上右键打开 QtDesigner 控件，增加一个按钮控件

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20231209175541681-20231209-tQL0c5.png)

在 `.ui` 文件上右键，使用 UIC 生成 `ui_xxx.h` 头文件。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20231209175850475-20231209-MXTINn.png)

此时我们修改一下 `main.cpp` 将刚刚生成的窗口引入：

```cpp
#include <QApplication>

#include "mainwindow.h"

int main(int argc, char *argv[]) {
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    return QApplication::exec();
}
```

然后增加一个按钮，给按钮配个事件

```cpp
// mainwindow.h 增加槽
public slots:
    void on_pushButton_clicked();

// mainwindow.cpp  增加信号
void MainWindow::on_pushButton_clicked() {
    QMessageBox::warning(nullptr, "你好", "Hello World!");
}
```

然后点运行（Shift + F10），效果如下

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/2023-12-09%2018-10-05.2023-12-09%2018_11_30-20231209-m18EPm.gif)



***

网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出，如果本文帮助到了你，别忘了点赞支持一下哦，你的点赞是我更新的最大动力！\~

> 参考文档：
>
> 1. [使用 clion 开发 QT - 知乎](https://zhuanlan.zhihu.com/p/461896034)
> 2. [使用Clion开发Qt | 范子琦的博客](https://www.robotsfan.com/posts/113f8d22.html)
> 3. [使用Clion进行Qt项目开发_clion qt](https://blog.csdn.net/qq_43715171/article/details/123719588)

PS：本文收录在在下的博客 [Github - SHERlocked93/blog](https://github.com/SHERlocked93/blog) 系列文章中，欢迎大家关注我的公众号 `CPP下午茶`，直接搜索即可添加，持续为大家推送 CPP 以及 CPP 周边相关优质技术文，共同进步，一起加油\~