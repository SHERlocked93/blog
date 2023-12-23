# 干货满满！推介几款 Mac 下非常好用的软件（第三弹）

[TOC]

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/JsjXnWlh8-g-20-07-37.jpg)

经常在分享某些我用的桌面好物后，有群友找来要链接，看来大家还是对这方面比较感兴趣，所以在下把我个人推介的桌面清单整理一下，应该会帮到一些朋友。

如果本文确实帮助到了你，那么别忘了点赞 👍，你的点赞是我继续写作的动力呀 🤪～

本文是 [<那些好用的工具>](https://github.com/SHERlocked93/blog?tab=readme-ov-file#%E9%82%A3%E4%BA%9B%E5%A5%BD%E7%94%A8%E7%9A%84%E5%B7%A5%E5%85%B7) 系列文章之一：

1. [打造舒适搬砖环境，这些是我最想推介的桌面好物](https://juejin.im/post/5ee9fca5f265da02d3377e38)
2. [推介几款 windows 下非常好用的工具](https://juejin.im/post/5c2eca54f265da61171cdc48)
3. [干货满满！推介几款 Mac 下非常好用的软件（第一弹）](https://juejin.im/post/5de664e5f265da33b82bcfce)
4. [干货满满！推介几款 Mac 下非常好用的软件（第二弹）](https://juejin.im/post/5e037fe2518825123f0c70cb)
5. [干货满满！推介几款 Mac 下非常好用的软件（第三弹）](https://juejin.cn/post/6903689654797598728)
6. [干货满满！推介几款 Mac 下非常好用的软件（第四弹）](https://juejin.cn/post/7315304715809390592)
7. [好用不卡，这些插件和配置让你的 Webstorm 更牛逼！](https://juejin.cn/post/7067703148734840869)

另外，我弄了个 [Github 仓库](https://github.com/SHERlocked93/awesome-tools)记录这些好用的软件，包含 Mac/Win/IDE/浏览器 里好用的应用和插件，将经常会更新，也可以给我提 issue，人生苦短，如果你不知道使用什么样的软件，不妨试试我推荐的这些软件，可称为 SHERlocked93 严选。
## 1. uPic

由于原来的图床软件 PicGo 经常在上传时报错，因此我这边卸载了 PicGo，转向更好用的（个人感觉）开源图床软件 [uPic](https://github.com/gee1k/uPic)，同时 [Typora](https://juejin.im/post/6844904012920127495#heading-10) 经过多次更新之后，已经支持在把图片复制到页面后自动通过 uPic 上传，并把图片连接替换到页面中，可谓非常便捷，如果你经常进行文字记录工作，不要错过这个工具组合。

支持拖拽上传、快捷键上传、本地文件右键直接上传、多图同时上传、截图上传、剪切板上传（结合快捷键爽飞！）等功能，可以配置大多数常用图床，上传图片完成后 自动把上传后的连接复制到剪切板，可以选择输出格式为 URL 或者 Markdown 格式，这一套下来完全解决了我的痛点，也覆盖了大多数人的大多数使用场景，好顶赞！

一般我的使用流程是，先用 [Xnip](https://juejin.im/post/6844904012920127495#heading-5) 截一个带阴影效果的图，这个图片会被 Xnip 复制到剪切板 📋，再使用在 uPic 中设置的快捷键 `ctrl + shift + command + u` 将截图上传，图片上传到图床后 uPic 会有个桌面通知和音效来提醒你，图片链接已经被复制到你的剪切板中，之后就可以随意使用了～

![uPic拖拽上传图片](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/68747470733a2f2f63646e2e6a7364656c6976722e6e65742f67682f676565316b2f6f7373406d61737465722f73637265656e73686f742f755069632d656e2f6472616746696c652e676966.gif)

在下使用的是 GitHub 图床（至少不会像某些免费图床一样突然暴毙 😂），Github 图床的配置可以参考[这个配置教程](https://blog.svend.cc/upic/tutorials/github/)。另一个免费图床我使用的 SM.MS 图床，不过这个图床有时候也会连接不上，当 Github 由于某些原因上不去，就改用这个图床，结合起来使用基本满足在下的图床需求。

![Github图床配置](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/image-20201011161728653.png)

> PS： 少数派专门有[篇文章](https://sspai.com/post/55933)介绍 uPic 的，可以看一下，介绍的更详细。

uPic 是免费的，可以在 Github [Release](https://github.com/gee1k/uPic/releases) 上下载最新的软件包，或者也可以在 [app store](https://apps.apple.com/cn/app/upic%E4%BC%98%E5%9B%BE-%E5%9B%BE%E7%89%87%E5%8E%8B%E7%BC%A9-%E6%97%A0%E6%8D%9F%E7%98%A6%E8%BA%AB-%E6%A0%BC%E5%BC%8F%E8%BD%AC%E6%8D%A2/id1341586328?mt=12) 里下载，或者 Homebrew 下载 `brew cask install upic`。

## 2. Tooth Fairy

虽然 AirPods 和 Beats X 等耳机都内置了 W1 芯片，可以在多个苹果设备之间无缝切换，但需要在 Mac 上连接耳机时，你需要先点击菜单栏中的蓝牙图标，再去选择相应的耳机作为输出。在连接上无线耳机之后，从菜单栏也不能直观看到你连接的设备。

Tooth Fairly 它可以记住你的所有蓝牙设备，然后通过设置好的快捷键**一键切换连接或断开**的状态，不用在蓝牙菜单里面找了，真正做到了多设备无缝切换（但也相应占用宝贵的菜单栏位置，不过可以用第二篇文章的 [Dozer](https://juejin.im/post/6844904031685443592#heading-7) 来做隐藏），还可以给蓝牙设备的切换设置快捷键，很炫酷了。

![image-20201011155153762](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/gr74LqNeyWzE5CH.png)

现在桌面日趋无线化，围绕电脑常常有多个蓝牙设备，尤其适合蓝牙耳机、蓝牙键盘、蓝牙触摸板等设备，这个软件你迟早用得上 😂。

Tooth Fairly 可以在 [app store](https://apps.apple.com/cn/app/toothfairy/id1191449274?mt=12) 中下载，也可以自己找资源。

## 3. Itsycal

**免费开源**的轻量状态栏日历软件，同时可以联动 Google Account、iCloud Account 系统日历的内容，每次你需要查看的时候只需要点击一下菜单栏上的按钮即可查看到所有的信息，很直观，也很美观。

📆 特别是有时候设置任务时间、排计划的场景的时候，当月日历有个明显的轮廓，十分友好。

整个软件就 2MB，很轻量了，对硬盘只有 256GB 的在下来说，还蛮贴心的 😂。 虽然体积小，但事件提醒、自定义时间展示、键盘快捷键、暗黑模式都一应俱全。

![Itsycal](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/image-20201011155741925.png)

可以在[官网](https://www.mowglii.com/itsycal/)免费下载，也可以在 [Github](https://github.com/sfsam/Itsycal) 下载任意版本的 release 版。

## 4. AltTab

如果你是从 Windows 系统转到 MacOS 的（一般都是吧 😂），那 Win 系统上的 `Alt + Tab` 跟 `Win + Tab` 快捷键切换应用十分熟悉了，Mac 上的任务切换就做的没 Win 上好，AltTab 这个软件可以带你找到 Win 上熟悉的窗口切换感觉，而且更进一步 ，可以设置切换的应用范围，是在所有桌面还是当前桌面上的应用，隐藏、最小化的应用是否可以切换到等等，更个性化。

还可以调整缩略图的大小等等，还能直接在缩略图中关闭、最小化、全屏等等操作，帮助更好更便捷的进行窗口操作。

![AltTab](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/windows-theme-20-53-57.jpg)

良心的是，AltTab 还支持中文 👍，而且是免费，在[这里](https://github.com/lwouis/alt-tab-macos/releases/download/v6.7.3/AltTab-6.7.3.zip)下载应用，也可以 HomeBrew 下载 `brew cask install alt-tab` ，但注意 HomeBrew 下载的并不是最新版本的，所以推介使用前面的链接下载。

## 5. FinalShell

打开后朴素的界面告诉你，这是国内个人开发者开发（或许是钢铁直男？），但功能很全也很实用。

支持多标签、批量管理服务器，登录 SSH 远程并记住配置下次双击直接连 SSH，支持设置自定义快捷命令，自动压缩解压，一大堆皮肤可以自由选择，快捷键可以自定义，sftp 与终端同屏显示，还可以直接拖拽本地的文件夹到 sftp 的文件夹自动传到服务器。

![Finalshell](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/image-20201203201321707-20-13-23.png)

FinalShell 的免费版已经够用了，在[这里](http://www.hostbuf.com/c/131.html)下载，有 Mac 版也有 Win 版。Mac 上可以命令行一键安装：

```bash
curl -L -o finalshell_install.sh www.hostbuf.com/downloads/finalshell_install.sh;chmod +x finalshell_install.sh;sudo ./finalshell_install.sh
```

除此之外还用过挺多 Shell 工具，颜值比较高的有一款 [Termius](https://apps.apple.com/cn/app/termius-ssh-client/id1176074088?mt=12) 也挺不错，但是收费，另外老牌的 XShell 也很推介。

## 6. Keka / The Unarchiver

正如 Windows 上装机必备之一就是解压工具，Mac 上自带的解压缩工具虽然挺好用，但支持的格式不多需要别的软件来补充，这里推介两个很不错的软件，一个主动一个被动，两款都支持中文。

Keka 是主动型的软件，可以压缩也可以解压，压缩支持设置解压密码、分卷压缩、选择压缩格式，支捷键生成压缩包，使用也很方便，在解压的时候直接拖拽到 Dock 的 Keka 图标上，或者使用快捷键，或者使用右键菜单栏里选择 `服务->使用 Keka 压缩`。

![keka](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/image-20201207184146970-18-41-47-19-04-03.png)

Keka 在 [App Store](https://apps.apple.com/cn/app/keka/id470158793?mt=12) 上现在 18 块，可以等活动的时候看看，或者你不 care 直接入手，如果你是经常使用压缩解压的工作者，这个工具推介了。另外，在[官网](https://www.keka.io/en/)下载使用是免费的（那为啥在 App Store 里面收费 😅）。

The Unarchiver 是被动型的解压缩软件（只能解压不能压缩），安装之后就不用管了，就像 Mac 上默认的应用一样，使用方式也是直接双击，速度很快。可以解压许多不同类型的存档文件，支持 Zip、RAR、7-zip、Tar、Gzip 和 Bzip2 等常见格式，和一些旧格式。也能打开其他各种文件，例如 ISO 和 BIN 磁盘镜像、windows.exe 安装程序。可以正确处理其打开存档的文件名编码，在编码不一样的地方（比如国外）解压文件，也不会出现杂乱的文件名。

![The Unarchiver](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/image-20201207181329840-20-02-10.png)

总之 The Unarchiver 简单易用、功能全面、免费实用，绿色无广告，宛如系统内置应用，在 [App Store](https://apps.apple.com/cn/app/the-unarchiver/id425424353?mt=12) 中即可下载，如果你是跟我一样基本上只是日常使用，压缩只会用到 Mac 系统覆盖的 `.zip`，解压缩也只会在网上下载到的常见格式，那么只安装这个就够了。

## 7. Multitouch

Multitouch 可以将自定义的动作绑定到触控板或鼠标手势。网上推介的人挺多，比较适合经常使用触控板的人，下面是我的设置，仅供参考。

![image-20200723141007287](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@env/uPic/2020-07-23-image-20200723141007287.png)

我设置了重按触控板左上角（触控板的按下分两个阶段，第二阶段是重按）将应用设置为当前桌面的左边 2/3，类似于 [Magnet](https://juejin.cn/post/6844904012920127495#heading-3) 的左 2/3 功能，同样右上角重按设置为右 2/3，这两个是我最常用的功能。左上角轻按设置为左 1/2，右上角轻按设置为右 1/2。

在浏览器里一个手指不动另一个手指上滑是选择左边的标签页，另一个手指下滑选择右边的标签页，这个功能我也经常使用。可以设置的功能还挺多，自己探索探索，也可以设置使用快捷键，喜欢折腾的可以一个个功能试一试。

App Store 里面没得下，只能在[官网](https://multitouch.app/)下载，挺骚气的，不过挺贵（100 块），不过也可以自己想想办法，网上到处都是 😂。

## 8. Glance

Mac 的空格键文件预览功能 QuickLook 相信是很多刚从 Win 换到 Mac 的人最惊艳的功能，但支持的格式并不是很多。Glance 是开源免费的 Mac 应用（但是 Github 上的仓库现在是 Archived 状态，可能是作者想拿去变现？），可用于预览多种原来 QuickLook 不被支持的文件格式，特别是 Markdown 和代码文件的临时预览，是我最常用的功能，比较骚的是还能预览未解压缩的压缩包里的内容。

除了整合在 QuickLook 里之外，还被整合在了 Finder、Spotlight 可以在这些场景预览文件，和上面介绍的 The Unarchiver 一样属于增强 Mac 系统的被动型技能。

![Glance](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/image-20201207192414874-20-03-59.png)

支持的文件格式很多 `.cpp`，`.js`，`.json`，`.py` 等代码文件（码农不要错过），还有 Markdown、压缩包、Jupyter Notebook 等多种不同文件格式。

![Glance preview](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/spZM4OPUEfrqQVR-20-03-02.jpg)

![Glance preview2](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/5zwjIr9vFLPYuHn-20-03-08.jpg)

可以在 Github 的 [Releases](https://github.com/samuelmeuli/glance/releases) 里下载最新的安装包，好东西。

## 9. TeamViewer

Mac 上最好用的远程控制软件，只需在两台设备上同时运行 TeamViewer ，将 TeamViewer 软件界面出现的 ID 和密码告诉对方即可实现远程控制，TeamViewer 还支持无人值守、文件传输、会议、视频、演示，和多平台之间的远程控制（Mac、Windows、Linux、iOS、Android、Windows Phone），可以说是打工人必备。

![TeamViewer](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/image-20201207193809670-19-38-10.png)

因为控制电脑比较敏感，所以第一次在新设备上登录的时候需要验证邮箱。每次电脑重启后 TeamViewer 都会重新分配一个 ID 和密码，那如果是给客户远程服务，客户又不在电脑面前岂不是麻烦？TeamViewer 可以设置菜单栏的 `连接->设置无人值守` 后 ID 和密码就不再改变了，可以给办公室的电脑设置一个，这样在家也可以改 Bug 了，岂不是很方便！ 😅

可以在[官网](https://www.teamviewer.cn/cn/download/mac-os/)免费下载，免费的个人版就已经足够日常使用了。

## 10. Yoink

你是不是有时候有这种需求，你需要将一个文件拖拽到某个地方，但这个文件在桌面上，而你的屏幕又比较小，比如在一个 13 寸的 Mac 上像下面这个动图一样把一个文件拖拽到一个工具中，这种拖动对你来说不方便一步到位。Yoink 就是提供一个中转站，你可以把文件先拖到 Yoink 的侧边栏中，然后在你想拖动这个文件夹的地方再从侧边栏的中转站拖出来。

![Yoink示例](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@env/uPic/Yoink示例.gif)

或者你也可以把 Yoink 当成文件、图片、音视频等物料的临时存放处，将你的注意力集中在内容的收集和整理，从而提升效率。现在 Yoink 支持 iCloud 同步了，可以在 iPhone、iPad、Mac 上进行同步，还支持剪贴板、Share Sheet、iCloud Drive 和相册导入。

Yoink 支持和 Alfred Action 联动，当你在 Alfred 选中一个文件后，使用你设置的 Actions 触发快捷键，可以快捷的把一个文件发送到 Yoink 中，爽到！只要在 Yoink 偏好设置的扩展里面就可以安装这个 Alfred File Action 扩展。

![Alfred with Yoink](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/image-20201203213016313-21-30-16.png)

[Yoink](https://apps.apple.com/cn/app/yoink-%E6%8B%96%E6%94%BE%E4%B9%9F%E5%8F%AF%E4%BB%A5%E8%BD%BB%E6%9D%BE%E8%87%AA%E5%A6%82/id457622435?mt=12) 是收费应用，平时 50 块，可以考虑在做活动的时候买，或者你有钱可以支持一下，总之是个好工具，如果你屏幕比较小又经常遇到拖拽文件的场景，可以考虑入一个。

## 11. 微云同步助手

一开始我希望找一个类似于 iCloud 那样可以自动同步某个指定文件夹的，而且可以在 Win/Mac 多系统都可以同步。经过一番寻找，找到一个很好用的微云同步助手，可以把我 PC 上某个文件夹和云盘里的文件夹保持同步，在多端也可以顺利工作，我经常用来当 U 盘用，或者保存一些配置文件什么的。

微云同步助手本身是轻量级的，体积很小，免费用户容量 10G，基本可以满足在下的使用需求，收费用户可以到达 6TB 的空间，看你需要了。

![微云同步助手](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/image-20201011161119017.png)

直接在[腾讯微云官网](https://www.weiyun.com/download.html)就可以下载，免费版的已经很香了，同步完之后也可以在微云云盘里面访问到你同步的文件，可能由于送的空间不那么大，所以名声不太大，知道的人不多，但企鹅家的产品你懂的，基本没有客服和反馈渠道。

听人说坚果云也挺好使的，改天体验一下看看，或者有深度使用的小伙伴来说一下好不好使 😂。

---
网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出，如果本文帮助到了你，别忘了点赞支持一下哦，你的点赞是我更新的最大动力！（收藏不点赞，都是耍流氓 🤣）~

PS：本文收录在在下的[博客](https://github.com/SHERlocked93/blog)的 <那些好用的工具> 系列文章中，欢迎大家关注我的公众号 `前端下午茶`，直接搜索即可添加或者点[这里](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/TJt4p2-19-56-21.jpg)添加，持续为大家推送前端以及前端周边相关优质技术文，共同进步，一起加油~

另外可以加入「前端下午茶交流群」微信群，微信搜索  `qianyu443033099` 加我好友，备注**加群**，我拉你入群～
