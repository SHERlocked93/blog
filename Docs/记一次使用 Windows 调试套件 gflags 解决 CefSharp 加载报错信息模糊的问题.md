# 记一次使用 Windows 调试套件 gflags 解决 CefSharp 加载报错信息模糊的问题

[TOC]

最近写 CPP 项目遇到了一个问题，用了几个工具来解决，这里记录一下，和大家一起讨论。

## 1. 起因

我的一个 CPP 项目的 UI 框架使用的是 CefSharp，UI 层是 C#，而一些模块代码使用的是 CPP，运行报错如下

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20240228183846499-20240228-2cl0NF.png)

报错信息是

> System.IO.FileLoadException:"未能加由"CefSharp.Core.Runtime.dl"导入的过程

第一感觉是进程加载某个配置文件或 dll 未成功，或者动态库版本问题，但错报不出来，而且 VS 的 Debugger 无法显示更多内容，用 Dependencies 看进程，dll 都是找到了的，那会是什么原因呢？

## 2. 分析

经过同事的提示，使用微软提供的 Windows Debugging Tools 调试套件 `gflags.exe` 工具，让进程加载过程中的日志能在 VS 的<输出>报出来，配置如下。在 `Image File` 中输入完整进程名，然后选中 Show loader snaps 显示加载器快照，然后重启进程。

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/2024022819385.png)

然后重新运行，在 VS 的输出中就可以看到进程加载过程中的日志，如下。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20240228184403251-20240228-9qJIkR.png)

在输出中搜 ERROR，可以看到加载哪些 dll 失败、警告等信息，有一些不重要，继续找发现加载的一个 dbghelp.dll 文件后，使用它的一个函数 `SymGetSearchPathW` 未找到失败，到库目录发现这个文件的时间比较老了，这个方法需要在 6.3 以上版本的 dbghelp.dll 文件才提供。

可以使用 dumpbin 命令的 `dumpbin dbghelp.dll /EXPORTS` 命令看到这个 dll 里并没有这个`SymGetSearchPathW` 方法，如下

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20240228184430505-20240228-gozZMY.png)

也可以使用 [Dependencies](https://github.com/lucasg/Dependencies) 这个工具来看 dll 中的入口函数，如下

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/1.png)

## 3. 解决

将项目的库目录里老版本 dbghelp.dll 删掉，让进程去系统的库目录里找较新的 dll，然后运行成功。

## 4. 复盘

对于进程（也就是 Image File），`gflags.exe` 的 Show loader snaps 选项开启之后会允许捕获加载和卸载 dll 的信息，并在调试器控制台中显示这些信息，如果过程中有报错信息也可以一并展示，所以可以用来查找类似于加载卸载动态库报错的问题。这个工具还可以做很多事情，监控内存分配、检查内存泄露等等，非常实用，后面再找个时间学习一下。

Windows 上的 `dumpbin` 命令和 linux 下的 `ldd` 命令，是用来查看动态库信息的，包括可执行文件和动态链接库文件的依赖项。`dumpbin` 命令可以用来看动态库导出了哪些函数 `dumpbin /EXPORTS a.dll` ，exe 加载了哪些动态库 `dumpbin /IMPORTS a.exe`，查看静态链接库中包含哪些函数 `dumpbin /ALL /RAWDATA:none a.lib`。另外，这个命令默认是不在 cmd 里，安装了 VS 的话需要在 VS 的开发者命令提示 Developer Command Prompt 里运行才能找到这个命令。

