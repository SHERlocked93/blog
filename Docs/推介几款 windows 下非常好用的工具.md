

# 推介几款 windows 下非常好用的工具

[TOC]

![](https://i.loli.net/2019/12/25/tk54zCWj1oFiPTu.jpg)

在下工具控一枚，平时会留意收集各种各样给我们生活生产带来便捷的工具，毕竟人生苦短；下面主要介绍一些我在 Windows 系统上发现的一些好用的工具，并且会一笔带过主要优点特点，具体详细用法可以搜一下，相关帖子挺多的，每个都详细介绍的话篇章那就太长啦。

本文是 [<那些好用的工具>](https://github.com/SHERlocked93/blog?tab=readme-ov-file#%E9%82%A3%E4%BA%9B%E5%A5%BD%E7%94%A8%E7%9A%84%E5%B7%A5%E5%85%B7) 系列文章之一：

1. [打造舒适搬砖环境，这些是我最想推介的桌面好物](https://juejin.im/post/5ee9fca5f265da02d3377e38)
2. [推介几款 windows 下非常好用的工具](https://juejin.im/post/5c2eca54f265da61171cdc48)
3. [干货满满！推介几款 Mac 下非常好用的软件（第一弹）](https://juejin.im/post/5de664e5f265da33b82bcfce)
4. [干货满满！推介几款 Mac 下非常好用的软件（第二弹）](https://juejin.im/post/5e037fe2518825123f0c70cb)
5. [干货满满！推介几款 Mac 下非常好用的软件（第三弹）](https://juejin.cn/post/6903689654797598728)
6. [干货满满！推介几款 Mac 下非常好用的软件（第四弹）](https://juejin.cn/post/7315304715809390592)
7. [好用不卡，这些插件和配置让你的 Webstorm 更牛逼！](https://juejin.cn/post/7067703148734840869)

另外，我弄了个 [Github 仓库](https://github.com/SHERlocked93/awesome-tools)记录这些好用的软件，包含 Mac/Win/IDE/浏览器 里好用的应用和插件，将经常会更新，也可以给我提 issue，人生苦短，如果你不知道使用什么样的软件，不妨试试我推荐的这些软件，可称为 SHERlocked93 严选。

## 1. Listary

啥都憋说了，[Listary](https://www.listary.com/) 必须排在第一个，用过 Everything，觉得还是 Listary 更胜一筹；它不仅可以在本地非常快速的搜索，还可以打开网站、在搜索引擎中搜索、随时随地打开快捷菜单、文件快速定位、快速打开cmd窗口等等优秀的功能；

比如输入`cmd`打开cmd窗口，输入`cmda`使用管理员权限打开cmd窗口，输入`wyyyy`打开网易云音乐，找到某个文件的时候`Enter`直接打开，`Ctrl + Enter` 是打开文件所在文件夹；

值得一提的是搜索关键词功能，让我们可以非常便捷的打开相应网站或在对应网站搜索，比如输入`gg 我的存款呢？`就可以直接使用默认浏览器在谷歌搜索中搜索了，我们还可以自定义输入其他关键字，只需把搜索链接中的关键字换成`{query}` ~

![](https://i.loli.net/2019/01/03/5c2e27585eb71.png)

## 2. Ditto

[Ditto](https://ditto-cp.sourceforge.io/) 是一款免费开源的windows剪切板管理工具，作为`Ctrl C V`工程师，复制粘贴少不了，更厉害的是，可以用它来批量的复制，`Ctrl+C`一堆别人的代码，一次性全粘上，岂不美哉；

使用快捷键打开剪切板历史，然后`Ctrl / Shift`来选择你希望粘贴的内容，`Enter`即可选择性的粘贴多行内容；另外剪切板历史还可以搜索，快速找到复制内容；

只需设置寥寥几个快捷键，就可以很方便的操作剪切板，带来极大幸福~

![](https://i.loli.net/2019/01/03/5c2e140547472.png)

## 3. Winsnap

看到上面的截图没，旁边都有很骚包的阴影，怎么做到的？不需要各种高大上的图片处理软件，只需 [Winsnap](https://www.ntwind.com/) ，它可以在截图的时候自动帮你加上背景阴影，然后帮你自动复制到剪切板；

它可以使用全屏、应用程序、窗口、对象等捕捉模式，更牛的是它还可以在截图的时候同时选择和捕捉多个对象，按住`Ctrl`或`Shift`选择多个窗口或对象...这个就比较厉害了，不信你试试？

![](https://i.loli.net/2019/01/03/5c2e1bff50446.png)

## 4. Cmder

[Cmder](http://cmder.net/) 是一个美观又实用的命令行工具，它支持大部分Linux命令，支持ssh连Linux，还可以在它的窗口中新建cmd和powershell，更多玩法等你来战~

比较方便的是在安装目录下 `\config\user-aliases.cmd `设置 alias 别名，比如参见的 Git 操作：

```bash
ga=git add $*
gb=git branch $*
gc=git commit $*
gch=git checkout $*
gd=git diff $*
gl=git log $*
gs=git status $*
```

还可以将cmder配置到右键菜单，快捷在当前目录打开cmder，方法是先把这个地址加到系统的path环境变量里面，比如我的是`D:cmder`，然后右键`Cmder.exe`属性-兼容性-以管理员身份运行此程序，再重新打开`Cmder.exe`输入`Cmder.exe /REGISTER ALL`就行了~

记得安装完在配置`Setting-Startup-Environment`里面加上`set LANG=zh_CN.UTF8`，否则输出的一些中文会乱码；

![](https://i.loli.net/2019/01/03/5c2e1cee1ba1d.png)

## 5. Typora

使用过很多 Markdown 编辑器，最后选择了 [Typora](https://www.typora.io/)，与主流编辑器一边编辑一边预览的形式，Typora 是将编辑和预览合并到一起，简洁大方，目光也不需要在复杂的编辑区和预览区中来回切换了，只有当焦点移入的时候才显示 Markdown 语法；

另外 Typora 还支持 Latex、`[TOC]`动态目录、拖拽图片自动生成本地预览链接、自定义主题等方便的功能；

![](https://i.loli.net/2019/01/03/5c2e27367a215.png)

## 6. Quick Look

[QuickLook](https://www.microsoft.com/zh-cn/p/quicklook/9nv4bs3l1h4s) 是在 Microsoft Store 里面下载的一个速览工具，有时候打开一个PDF、TXT、图片之类的需要等关联程序启动半天，有了它之后只要选中目标文件，按空格，就可以快速预览了，速度非常快，支持图片、视频、音频、压缩包、PDF、文本文件、Markdown、HTML等格式；

用它来看一些代码什么的，甚至不需要 Sublime\VSCode 启动就可以直接看了，如果只是速览一下的话是非常适合的了。

![](https://i.loli.net/2019/01/04/5c2eb5f3a8429.png)

## 7. Myper Splash

[Myper Splash](https://www.microsoft.com/zh-cn/p/myersplash-wallpaper/9nblggh4vcsn) 也是可以在 Microsoft Store 里面下载的一款高质量壁纸库，所有壁纸来源 Unsplash 网站，均无版权可以免费使用，再加上简洁美观的UI/UX设计，让你体验一见钟情的感觉。

另外 MyperSplash 可以设置自动每天自动更换壁纸或锁屏，每天早晨来到办公室点亮屏幕就可以看到 Awesome 的锁屏或壁纸，让你带着好心情开启一天的工作。

![](https://i.loli.net/2019/01/04/5c2eb8b503cea.png)

## 8. GifCam / ScreenToGif

相信大家都有过需要截一个 Gif 的时候，这里有两个免费 Gif 屏幕录制工具都很不错，小而美的 [GifCam](https://gifcam.en.softonic.com/) 和开源强大的 [ScreenToGif](https://github.com/NickeManarin/ScreenToGif) ；

GifCam 小巧便捷，如果希望快速录屏分享，那么它是不二选择，可以选择录屏帧率，录制的过程可以调整窗口大小和位置，也可以暂停和继续，足以满足大部分的使用场景；

![](https://i.loli.net/2019/01/04/5c2ebe13b641f.gif)

SceenToGif 的编辑功能更为强大，可以单独操作录制的帧，删除或者加快或者修改，试试看吧~

![](https://i.loli.net/2019/01/04/5c2ebe43f24a7.gif)

## 9. Free Download Manage

[Free Download Manage](https://www.freedownloadmanager.org/) (FDM) 是一款免费的下载工具，如果你已经受够了国内一些软件的广告和限速，那么 FDM 是一个不错的选择，另外多线程、断点续传、计划任务等功能让 FDM 值得推介。

![](https://i.loli.net/2019/01/04/5c2ebf112069d.png)

## 10. Sourcetree

[Sourcetree](https://www.sourcetreeapp.com/) 是跨平台免费的 Git 客户端管理工具，如果受够了手打各种 Git 操作命令，那么 Sourcetree 是一个不错的选择；

Sourcetree 可以大大简化你的代码操作，特别是对于一些不甚熟悉 Git 命令的人来说灰常实用；一些对 Git 操作比较熟练的用户也可以用它来提升效率，减少出错。

![](https://i.loli.net/2019/01/04/5c2ec0ec203f1.png)
