# 好用不卡，这些插件和配置让你的 Webstorm 更牛逼！

[TOC]

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/asher-zhang-8JJ_sPcUaNA-unsplash-20220222-hSfDmf-20220222-0BcO9y.jpg)

作为前端开发者，最趁手的搬砖工具无外乎 Webstorm 和 VSCode，Webstorm 像苹果系统，闭源、收费、官方有良好而强大的开发能力、智能索引和补全功能无出其右者，VSCode 就像安卓，开源、持续迭代更新、社区充满活力。

Webstorm 的 2021.3 版更新后，以往卡顿的情况缓解了很多，就算重新安装 node_modules 也不会像以前一样卡死半天，因为卡顿退坑 Webstorm 的小伙伴可以回来看看 😂

在下使用 Webstorm 较多，总结了一些不错的插件和实用 Tips，希望能帮到你~

本文是 [<那些好用的工具>](https://github.com/SHERlocked93/blog?tab=readme-ov-file#%E9%82%A3%E4%BA%9B%E5%A5%BD%E7%94%A8%E7%9A%84%E5%B7%A5%E5%85%B7) 系列文章之一：

1. [打造舒适搬砖环境，这些是我最想推介的桌面好物](https://juejin.im/post/5ee9fca5f265da02d3377e38)
2. [推介几款 windows 下非常好用的工具](https://juejin.im/post/5c2eca54f265da61171cdc48)
3. [干货满满！推介几款 Mac 下非常好用的软件（第一弹）](https://juejin.im/post/5de664e5f265da33b82bcfce)
4. [干货满满！推介几款 Mac 下非常好用的软件（第二弹）](https://juejin.im/post/5e037fe2518825123f0c70cb)
5. [干货满满！推介几款 Mac 下非常好用的软件（第三弹）](https://juejin.cn/post/6903689654797598728)
6. [干货满满！推介几款 Mac 下非常好用的软件（第四弹）](https://juejin.cn/post/7315304715809390592)
7. [好用不卡，这些插件和配置让你的 Webstorm 更牛逼！](https://juejin.cn/post/7067703148734840869)

另外，我弄了个 [Github 仓库](https://github.com/SHERlocked93/awesome-tools)记录这些好用的软件，包含 Mac/Win/IDE/浏览器 里好用的应用和插件，将经常会更新，也可以给我提 issue，人生苦短，如果你不知道使用什么样的软件，不妨试试我推荐的这些软件，可称为 SHERlocked93 严选。

## 1. 插件推介

以下推介的插件都可以在 Webstorm 官方插件市场下载，直接搜索插件名安装即可。

有一些感觉并没有解决痛点的插件比如打字特效 activate-power-mode、彩虹括号 Rainbow Brackets、彩虹进度条 Dmitry Batkovich 就没有推介了。

还有一些第三方智能代码补全的插件比如 Codota、Kite、Tabnine，我觉得 Webstorm 自带的机器学习智能补全就挺好用了，用第三方插件有时候代码补全速度有点慢，要额外占用内存，有时候还会跟自带的补全冲突或者重复。可能是我机器配置不够高，感兴趣可以安装了试试看。

### Chinese Language Pack / 中文语言包

早期没有官方中文语言包，还要靠 Github 上有个长期没有更新的翻译插件，好在 2021 年官方推出了中文语言包，弥补了在下弱鸡的英语能力（六级 436 飘过），不是说原英文的界面不能用，只是觉得英文的有些设置不能做到一目了然，要找半天。

有的大佬可能觉得英文的用着挺好，用习惯了也一样，看你个人需要了~

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/1-20220222-hPqvyx.png)

### AceJump：光标快速定位

可以将插入光标快速导航到编辑器中可见的任何位置，有了 AceJump 脱离鼠标全键盘开发不在话下，还有个很好的地方在于即使编辑器窗口拆分了，也可以在不同的窗口之间导航，快捷键 `control/ctrl + ;`

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/acejump-20220222-T8WDVp.gif)

### GitToolBox：Git功能扩展

很多 Git 的功能增强，比如自动 fetch 代码，状态栏中显示当前 Git 分支的未提交和落后提交数显示，过时分支清理，commit 窗口支持 emoji 表情，Inline Blame 可以看到每行代码是谁提交的、什么时候提交的、以及 commit 信息等等，如果你经常用 Git，这个插件必装了。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220222103014541-20220222-J8W3dB.png)

### HighlightBracketPair：高亮括号

有些大佬会推介彩虹括号插件 Rainbow Brackets，我也下载过，但括号多了之后花花绿绿的看着也一样分不清。

后来发现 HighlightBracketPair 插件，这个插件会在当前括号上高亮之外，还会在左侧代码行数那显示括号范围，比彩虹括号插件更加直观而且不容易看花眼。

![HighlightBracketPair](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/HighlightBracketPair-20220221-40P3m0.gif)

### Key Promoter X / Presentation Assistant：快捷键显示

很多大佬的博客推介 Key Promoter X，可以在你点某个功能的时候提示你这个功能的快捷键，多用一用就可以脱离鼠标，使用快捷键触发这些功能。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/screenshot_17105-20220222-7nX67c.png)

还有一个很棒的插件叫 Presentation Assistant，支持功能的汉化显示，而且还可以将 Mac 和 Win 环境的快捷键都展示出来。

![Presentation Assistant](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220221201746283-20220221-o5wzWE.png)

### One Dark Theme / Material Theme UI Lite：好看的免费主题

原来有个很好用的插件 Material Theme UI，但后来收费了，不过没关系，还有一些免费的主题也很好用，比如 [Material Theme UI Lite](https://plugins.jetbrains.com/plugin/12124-material-theme-ui-lite)、[Coderpillr Theme](https://plugins.jetbrains.com/plugin/12878-coderpillr-theme)、[One Dark theme](https://plugins.jetbrains.com/plugin/11938-one-dark-theme) 等等，都挺好看的，自己挑个喜欢的主题吧~ 

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/screenshot_19346-20220221-pFhsCJ.png)

### Atom Material Icons：好看的图标

以前有个编辑器叫 Atom，现在用的人不多了，它最大的贡献就是主题和图标设计的非常好看，这个插件就是将 Atom 的图标引入到 Webstorm 的文件夹、文件上，让编译器看起来更美观。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/screenshot_21309-20220221-lKxfBm.png)

### IntelliVue：Vue功能增强

Webstorm 上对 Vue 支持很棒的插件，现在已经支持 Vue3 的一些语法，可以快速创建 Vue2 的 data、methods 等，或者 Vue3 的 setup method 等，帮你少些一些模板代码。

安装后菜单栏会多一个 Vue 的选项，下拉框里有一些操作功能，对 Vue2 项目比较好用。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220222111016455-20220222-2uumrQ.png)

### Translation：最佳翻译插件

可以便捷地在 Webstorm 中进行翻译，省去了打开翻译软件的操作，支持右键方式选中翻译，也可以打开独立窗口进行整段的翻译。

个人感觉最方便的功能就是翻译并替换功能，Mac 上快捷键 `command + control + O`，Win 上为 `ctrl + shift + X`，在写业务代码的时候会自动翻译汉字的业务词条自动翻译，字符串可以选择大驼峰或小驼峰什么的。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/traslation-20220222-vipcrf.gif)

### String Manipulation / CamelCase：字符串处理

这两个插件都是处理字符串的，可以将英文字符串在 kebab-case、SNAKE_CASE、PascalCase、camelCase、snake_case、space case 形态间切换。

第一个 String Manipulation 插件比较大，推荐经常处理字符串的小伙伴用，第二个 CamelCase 插件比较轻量，日常使用完全足够，使用也很简单，快捷键 `option/alt +shift + U` 就可以进行切换了。Webstorm 自带切换大小写的快捷键是 `command/ctrl + shift + U`，这两个差不多的快捷键也很好记。

![CamelCase](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/CamelCase-20220221-iVWqzi.gif)

### .ignore：版本管理工具的忽略文件插件

`.ignore` 插件支持创建多种 `.ignore` 文件比如 `.gitignore`、`.eslintignore`、`.dockerignore` 等等，我们最常用的基本都支持，新建的时候支持选择不同类型的框架或库常用的忽略配置，如 `node_modules`、`dist`、`.cache` 等。

![在项目文件夹上右键、新建、.ignore File](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220222100315230-20220222-E5p7NF.png)

在文件上右键也可以快速添加到忽略文件中，是使用 Git 必装的小插件。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220222094324570-20220222-QRwR8M.png)

也支持将文件旋选中右键快速添加到 `.gitignore` 文件中。

### Import Cost：显示引入的包体积大小

VSCode 上也有这个插件，会在你引入的库后面告诉你这个库的体积大小，和 gzip 后的包体积。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220222112257231-20220222-DIIViV.png)

### CodeGlance：右侧代码小地图

在代码面板的右侧显示一个代码缩略图，像 VSCode 里那样。我看有人在用这个插件，但在下不怎么用，在编辑器里使用分屏的时候觉得有些碍事，长文件中用着还行，看你个人喜好了。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220221220721364-20220221-K5yQRg.png)

### .env files support：配置文件支持

可以给 `.env` 环境配置文件增加语法高亮，给配置文件中定义的变量增加智能索引。另外在使用 Webpack 进行打包的时候，我们会有一些环境变，安装该插件后，就会提示环境变量文件中所拥有的环境变量。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220222140541915-20220222-Kkzoms.png)

### JetBrains Toolbox：全家桶管理软件

用来集中管理 Webstorm、IntelliJ、GoLand 等 JetBrains 全家桶软件，管理常用设置、项目导航，以及自动更新、插件更新、回滚和降级软件版本等功能，如果你 JetBrains 系列软件安装了不止一款，那十分推介安装。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220221195056031-20220221-HQ2cJd.png)

## 2. 实用设置 Tips

### 2.1 关闭不需要的插件

Webstorm 安装后自带了很多内置插件，有些不需要的或不常用可以将其关闭，项目开启速度可以进一步增加。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220222141327512-20220222-6yHqGP.png)

### 2.2 连体字

现在不少字体都可以设置连体字，比如 `Fira Code` 或者 2021 年 JetBrains 增加的专用于编程的 `JetBrains Mono` 字体。强烈推介后者，2021 及以后版本内置于 Webstorm，是最新发布专用于编程的字体，清晰、易读、辨识度高。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/jetbrains_mono_typeface-20220221-vvWaTO.gif)

设置使用 `JetBrains Mono` 字体后，可以达到下面这样的效果：

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220221181024804-20220221-DFetno.png)

如果你喜欢这种风格，在设置的 `编辑器->配色方案->配色方案字体` 中修改。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220221180527712-20220221-Tyoaqr.png)

### 2.3 设置默认内存

相信很多人装上 Webstorm 第一件事就是改默认内存，可以在 `.vmoptions` 设置文件里手动改，也可以在 `帮助->更改内存设置` 中更改，建议设置为 4096 或者更高一点。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220221212554345-20220221-wGRiG6.png)

当前的占用内存在软件界面右下角可以看到，如果感觉内存设置的不够，可以再改大点。

### 2.4 设置配置同步

可以在 `文件 -> 管理IDE设置 -> IDE设置同步` 中设置配置同步，Webstorm 会将你的配置与你的账户绑定，这样你家里的电脑就可以和公司的电脑使用相同的配置和快捷键。

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220221215234904-20220221-2wZ1Dv.png)


## 3. Tips
### 3.1 强悍的后缀补全功能

经常听到别人说代码自动补全，但我很少听人说过 Webstorm 的后缀补全，但特别实用，对于有些已经脱离或者希望脱离鼠标的高手来说，后缀补全可以让你少按很多次 `←` 键。

下面是 `.const` 补全的例子：

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/%E5%90%8E%E7%BC%80%E8%A1%A5%E5%85%A81-20220221-dWkxgS.gif)

还有补全表达式的括号 `.par` 和 return 语句的 `.return` 方式：

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/%E5%90%8E%E7%BC%80%E8%A1%A5%E5%85%A82-20220221-Gj4ogQ.gif)

全部的后缀补全可以在 `编辑器->常规->后缀补全` 中看到，也可以自定义喜欢的补全方式。

### 3.2 正则表达式快捷验证

在正则表达式上按 `option/alt + enter` 可以就地快捷验证正则表达式，这是一个快速功能，在做表单验证的一些正则表达式的时候非常实用

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/%E6%AD%A3%E5%88%99%E5%BF%AB%E9%80%9F%E6%A0%A1%E9%AA%8C-20220221-lXv3F7.gif)

## 4. 实用快捷键

### 4.1 全局搜索

双击 `shift` 可以打开随处搜索功能，这里可以搜索设置、代码、文件名、文件夹名、改变主题等等，是 Webstorm 上最强功能之一，相当于 VSC 的 `command/ctrl + shift + P`

![search everywhere](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/search-20220222-ZMiEEQ.gif)

### 4.2 打开最近的文件

`command/ctrl + E` 可以打开最近的文件，在这些文件中间跳转，文件列表中也包括已关闭的文件。比如你刚刚关闭了一个文件，再想把这个文件打开，就可以使用这个快捷键，相当于浏览器的 `command + shift + T`

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220221181606903-20220221-BVsVqs.png)

### 4.3 在项目视图中打开文件

在项目视图中打开文件是一个很方便的功能，就是项目文件目录面板上面两个同心圆一样的图标，可以在文件目录中快速打开当前并定位到当前文件：

![在项目视图中打开文件](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/%E5%9C%A8%E9%A1%B9%E7%9B%AE%E8%A7%86%E5%9B%BE%E4%B8%AD%E6%89%93%E5%BC%80%E6%96%87%E4%BB%B6-20220221-mrQj4Y.gif)

默认设置里并没有给这个功能增加快捷键，建议在 `键盘映射->其他->在项目视图中选择文件` 中添加自己的快捷键，我设置的是 `option/alt + 1` ，仅供参考：

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220221194518771-20220221-mlX3DA.png)

### 4.4 查看用途

使用 `option/alt + F7` 可以查看当前变量、函数、类的使用、读取、导入的地方，在阅读别人的代码理清逻辑关系的时候非常好用，有了这个功能阅读源码终于不用 `command/ctrl + shift + F` 一个个找变量了。

![查看用途](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220221201913141-20220221-xAtbFa.png)

快速显示用法的快捷键是 `command/ctrl + option/alt + F7` 

### 4.5 其他超级快捷键

1. `command/ctrl + option/alt + O`：import 优化，移除没用到的 import
2. `command/ctrl + option/alt + L`：重新格式化代码
3. `command/ctrl + option/alt + Z`：Git 回滚当前区域的代码
4. `command/ctrl + J`：查看预定义代码模板
5. `command/ctrl + shift + up/down`：智能移动代码块，如果移动函数，可以将这个函数整体移动到上一个函数上
5. `control/ctrl + shift + J`：合并两行
6. `command/ctrl + G`：选择下一个相同匹配项
7. `command/ctrl + D`：复制当前行
8. `F2`：导航到编辑器报错或者报警告的地方

查看官方的所有快捷键可以点击 `帮助->键盘快捷键 PDF`，或者双击 `shift` 输入「键盘快捷键」就可以看到官方快捷键参考 PDF，内容非常全，多看看经常可以发现惊喜。

![快捷键PDF](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/image-20220221205302589-20220221-sozX2P.png)



---
网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出，如果本文帮助到了你，别忘了点赞支持一下哦，你的点赞是我更新的最大动力~


> 参考文档：
>
> 1. [都 2021 了你居然还在用 WebStorm ？](https://juejin.cn/post/6963835326821302303)
> 1. [Tips - WebStorm Guide](https://www.jetbrains.com/webstorm/guide/tips/)

PS：本文收录在在下的博客 [Github - SHERlocked93/blog](https://github.com/SHERlocked93/blog) 系列文章中，欢迎大家关注我的公众号 `前端下午茶`，直接搜索即可添加或者点[这里](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/TJt4p2-19-56-21.jpg)添加，持续为大家推送前端以及前端周边相关优质技术文，共同进步，一起加油~

另外可以加入「前端下午茶交流群」微信群，微信搜索  `sherlocked_93` 加我好友，备注**加群**，我拉你入群～
