# 记一次使用 Windows 调试套件 WinDbg 解决 CefSharp 加载报错信息模糊的问题

[TOC]



## 1. 起因

我的一个 CPP 项目的 UI 框架使用的是 CefSharp，一些模块代码是 CPP，昨天

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20240228183846499-20240228-2cl0NF.png)

CPP 项目使用 cef 框架的报错

> System.IO.FileLoadException:"未能加由"CefSharp.Core.Runtime.dl"导入的过程

明显是进程加载某个配置文件或 dll 未成功，但错报不出来，VS 的 Debugger 无法显示更多内容



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

将项目生成目录的老版本 dbghelp.dll 删掉，让进程去系统的库目录里找较新的 dll，运行成功。

## 4. 分析

`gflags.exe` 的 Show loader snaps 选项是允许捕获有关加载和卸载可执行映像及其支持库模块的详细信息，并在调试器控制台中显示这些信息。

Windows 上的 dumpbin 命令和 linux 下的 ldd 命令，是用来查看动态库信息的，包括可执行文件和动态链接库文件的依赖项。