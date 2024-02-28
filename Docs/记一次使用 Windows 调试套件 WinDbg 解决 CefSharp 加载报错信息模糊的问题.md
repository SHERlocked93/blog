# 记一次使用 Windows 调试套件 WinDbg 解决 CefSharp 加载报错信息模糊的问题

[TOC]



## 1. 起因

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20240228183846499-20240228-2cl0NF.png)

CPP 项目使用 cef 框架的报错

> System.IO.FileLoadException:"未能加由"CefSharp.Core.Runtime.dl"导入的过程

明显是进程加载某个配置文件或 dll 未成功，但错报不出来，VS 的 Debugger 无法显示更多内容



## 2. 分析

经过同事的提示使用微软提供的 Windows Debugging Tools 调试套件 gflags.exe 工具，让进程加载过程中的日志能在 VS 的<输出>报出来，配置如下。在 `Image File` 中输入完整进程名，然后选中 Show loader snaps



然后重新运行，在 VS 的输出中就可以看到进程加载过程中的日志，如下。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20240228184403251-20240228-9qJIkR.png)

在输出中搜 ERROR，可以看到加载哪些 dll 失败、警告等信息，有一些不重要，继续找发现加载的一个 dbghelp.dll 文件后，使用它的一个函数 SymGetSearchPathW 未找到失败，到库目录发现这个文件的时间比较老了，这个方法需要在 6.3 以上版本的 dbghelp.dll 文件才提供。

可以使用 `dumpbin dbghelp.dll /EXPORTS` 命令看到这个 dll 里并没有这个`SymGetSearchPathW` 方法，（也可以使用 Dependencies 看），如下

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20240228184430505-20240228-gozZMY.png)

## 3. 解决

将 Debug 目录的老版本 dbghelp.dll 删掉，让进程去系统目录里找这个 dll，后运行成功