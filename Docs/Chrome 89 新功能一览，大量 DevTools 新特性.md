# Chrome 89 新功能一览，性能提升明显，大量 DevTools 新特性

[TOC]

今天 Chrome 更新了最新版本 Chrome89，新版本在启动、响应速度上更快，同时 CPU 占用率大幅下降。

比如，提供前进后退缓存（20%的页面可瞬时进退）等特性，号称启动速度快了 25%、载入页面速度快了 7%、CPU 占用减少了 5 倍、可增加额外 1.25 小时续航，内存占用量也优化了。

> 原文：https://developers.google.com/web/updates/2021/01/devtools

下面来具体看看更新了哪些内容。

## 1. Elements 面板相关更新

### 支持选择 CSS 的 `:target` 伪类

现在可以使用 DevTools 选中和检查 `:target` 状态。

在 Elements 面板中，选择一个元素，可以在右侧切换 `:target`。

当 URL 中的 hash 和 DOM 元素的 id 相同时，将触发该元素的 `:target` 伪类。可以点击这个 [Demo](https://jec.fyi/demo/css-target#section-2) 看看效果，这个新的 DevTools 特性可以让你测试这些样式，而不必一直手动更改 URL。

![forcing the CSS `:target` state](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/force-target-20210303-qXklNj.png)

对应 Chromium issue: [1156628](https://crbug.com/1156628)

### 复制 DOM 元素的新选项

右键单击元素面板中的一个元素，选择 Duplicate element，将在其下面快速创建一个新元素。

或者，你可以使用键盘快捷键复制元素：

- Mac: `Shift` + `Option` + `⬇️`
- Window/ Linux: `Shift` + `Alt` + `⬇️`

![Duplicate element](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/duplicate-element-20210303-577kMn.png)

对应 Chromium issue: [1150797](https://crbug.com/1150797), [1150797](https://crbug.com/1150797)

### 自定义 CSS 属性的颜色选择器

在 Elements 面板的 Styles 窗格现在可以显示自定义 CSS 属性的颜色选择器。

此外，按住 Shift 键并单击颜色选择器，可以切换颜色值的 RGBA、 HSLA 和 Hex 表示。

![Color pickers for custom CSS properties](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/color-picker-20210303-ofah7M.png)

对应 Chromium issue: [1147016](https://crbug.com/1147016)

### 复制 CSS 属性的新选项

你现在可以用新的快捷方式更快地复制 CSS 属性。

在 Elements 面板中，选择一个元素。然后，在 Styles 窗格中右键单击 CSS 类或 CSS 属性以复制该值。

![New shortcuts to copy CSS properties](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/copy-css-20210303-apDVKT.png)


类的复制选项:

- Copy selector：复制当前选择器名称；
- Copy rule：复制当前选择器的规则；
- Copy all declarations：复制当前规则下的所有声明，包括无效属性和带前缀的属性。

属性的复制选项:

- Copy declaration：复制当前行的声明；
- Copy property：复制当前行的属性；
- Copy value：复制当前行的值。

对应 Chromium issue: [1152391](https://crbug.com/1152391)

## 2. Network 面板相关升级

### 保持记录网络日志

DevTools 现在始终保持记录网络日志（Record network log）设置。以前，每当页面重新加载时，DevTools 都会重置用户的选择。

![Record network log](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/network-log-20210303-QVgAa7.png)

对应 Chromium issue: [1122580](https://crbug.com/1122580)

### 在 Network 面板中查看 WebTransport 连接

网络面板现在显示 WebTransport 连接。

![WebTransport connections](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/webtransport-20210303-kO5FmW.png)

[WebTransport](https://web.dev/webtransport/) 是一个新的 API，可以提供低延迟的客户端与服务端的双向消息传递。

对应 Chromium issue: [1152290](https://crbug.com/1152290)

### “Online” 改为 “No throttling”

网络模拟选项 Online 现在被重命名为 No Throttling。

![Record network log](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/no-throttling-20210303-3kAO5A.png)

对应 Chromium issue: [1028078](https://crbug.com/1028078)

## 3. Console、Sources、Styles 面板中新的复制选项

### Console、Sources 面板中复制对象的新选项

现在可以使用 Console 和 Sources 面板中的新选项来快捷复制对象值。这非常方便，尤其是当需要复制一个比较大的对象（例如一个长数组）时。

![Copy object in the Console](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/copy-object-console-20210303-KSIfqt.png)

![Copy object in the Sources panel](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/copy-object-sources-20210303-YEMD55.png)

对应 Chromium issues: [1149859](https://crbug.com/1149859), [1148353](https://crbug.com/1148353)

### Sources、Styles 面板中复制文件名的新选项

你现在可以通过右键点击复制文件名：

1. 在 Sources 面板的文件名
2. 在 Elements 面板中的 Styles 标签的文件名

从上下文菜单中选择 Copy file name 以复制文件名。

![Copy file name in the Sources panel](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/copy-file-name-20210303-l77jUx.png)

![Copy file name in the Styles pane](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/copy-file-name-2-20210303-S0hZ2n.png)

对应 Chromium issue: [1155120](https://crbug.com/1155120)

## 4. 对可信类型（Trusted Types）的调试支持

### 可信类型断点

现在可以在 Source 面板中设置断点和捕获可信类型违规的异常。

[可信类型（Trusted Types）](https://github.com/w3c/webappsec-trusted-types) API 有助于防止基于 DOM 的跨站脚本攻击（XSS）。点击[这里](https://web.dev/trusted-types/)了解如何使用可信类型来避免 XSS 攻击。

你可以自己试试这个[演示页面](https://tt-enforced.glitch.me/)中尝试一下，在 Sources 面板中，打开右侧调试器。展开 CSP Violation Breakpoints 部分，并启用 Trusted Type violations 复选框来在异常发生时暂停 script 运行。

![Breakpoint on Trusted Type violations](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/trusted-type-violations-20210303-OXOoWd.png)

对应 Chromium issue: [1142804](https://crbug.com/1142804)

### 在 Issues 选项卡中链接 Sources 面板中的提示框

现在，Sources 面板在违反 Trusted Type 的代码行旁边显示了一个警告图标，将鼠标悬停在这个图标上时可以预览异常。单击它展开 Issues 选项卡，选项卡提供了关于异常的更多细节，以及如何修复异常的提示。

![Link issue in the Sources panel to the Issues tab](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/trusted-type-link-20210303-VrsFhd.png)

对应 Chromium issue: [1150883](https://crbug.com/1150883)

## 5. 支持超出视口的元素截图

现在可以捕获一个包括视口外的内容完整的节点屏幕截图。在此之前，屏幕截图因为无法截取视口外的内容而得不到完整的截图。

整个浏览器页面的截图现在也可以得到同样的完整截图。

在 Element 面板中，右键单击一个 DOM 元素并选择 Capture node screenshot 可以使用元素截图功能。

![Capture node screenshot beyond viewport](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/node-screenshot-20210303-Cm5AFt.png)

对应 Chromium issue: [1003629](https://crbug.com/1003629)

## 6. Network 面板中新增的 Trust Tokens 选项卡

使用新的 Trust Tokens 选项卡检查网络请求的可信类型。

[Trust Token](https://web.dev/trust-tokens/) 是一个新的 API，可以在不需要被动跟踪帮助打击网络诈骗、区分机器人和真人。

进一步的调试支持将在 Chrome 下一个版本中提供。

![New Trust Token tab for network requests](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/trust-token-20210303-6lC9qG.png)

对应 Chromium issue: [1126824](https://crbug.com/1126824)

## 7. Lighthouse 面板升级到 Lighthouse7

Lighthouse 现在升级到了 Lighthouse7，点击[这里](https://github.com/GoogleChrome/lighthouse/releases/tag/v7.0.0)了解具体变更明细。

![Lighthouse 7 in the Lighthouse panel](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/lighthouse-20210303-nQtPGK.png)

对应 Chromium issue: [772558](https://crbug.com/772558)



## 8. Cookies 相关更新

### 显示 url 解码后的 cookie 的新选项

现在，可以在 Cookies 窗格中查看 url 解码后的 cookie 值。

转到 Application 面板并选择左侧的 Cookies 选项。选择列表中的任何 cookie。启用新的 Show URL decoded 复选框可以查看解码后的 cookie。

![Option to show URL-decoded cookies](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/cookies-decoded-20210303-F1NpzU.png)

对应 Chromium issue: [997625](https://crbug.com/997625)

### 只清除过滤后的 cookie

Cookies 选项窗格中的 Clear all cookies 按钮现在被 Clear filtered cookies 按钮取代。

在 Application > Cookies 窗格中，在文本框中输入文本以过滤 cookie。下图我们使用 PREF 过滤列表。单击 Clear filtered cookies 按钮删除可见的 cookie。清除过滤文本后，你将看到其他 cookie 仍然保留在列表中。以前，你只能选择清除所有 cookie。

![Clear only visible cookies](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/clear-cookies-20210303-9YE1z2.png)

对应 Chromium issue: [978059](https://crbug.com/978059)

### 清除 Storage 窗格中第三方 cookies 的新选项

当清除 Storage 窗格中的站点数据时，DevTools 现在默认情况下只清除本站 cookie。选中 including third-party cookies 复选框后，浏览器也会清除第三方 cookies。

![Option to clear third-party cookies](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/third-party-cookies-20210303-a97vAR.png)

对应 Chromium issue: [1012337](https://crbug.com/1012337)

## 9. 为自定义设备编辑 User-Agent Client Hints

现在可以编辑自定义设备的 User-Agent Client Hints。

进入 Settings > Devices，然后点击 Add custom device。展开 User agent client hints 部分来编辑客户端提示。

![Edit User-Agent Client Hints](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/ua-ch-20210303-Mqr6YI.png)

[User-Agent Client Hints](https://web.dev/user-agent-client-hints/) 是字符串形式 User-Agent 的替代，它使得开发人员可以以更符合人体工程学的方式访问 User-Agent 的信息，并且有利于保护用户隐私。

对应 Chromium issue: [1073909](https://crbug.com/1073909)



## 10. Frames 面板更新

### 在 Frames 面板中的 Service Workers 信息

DevTools 现在独立显示 Service Workers 信息。

在 Application 面板中，在 Service Workers 选项中选择一个 Service Worker 以查看详细信息。

![Service Workers information in the Frame details view](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/sw-20210303-K5COKR.png)

对应 Chromium issue: [1122507](https://crbug.com/1122507)

### Frames 面板中显示内存统计信息

新的 `performance.measureMemory()` API 可用状态现在显示在 API availability 选项下。

`performance.measureMemory()` API 可以统计当前整个网页的内存使用量，可以在[这篇文章](https://web.dev/monitor-total-page-memory-usage)中学习使用这个 API 的使用。

![Measure Memory](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/measure-memory-20210303-QfQBqa.png)

对应 Chromium issue: [1139899](https://crbug.com/1139899)

## 11. 在 Issues 标签中提供反馈

如果你想改善一个问题的消息，转到 Console > Issues 标签，或者 More Settings > More tools > Issues 来打开 Issues 标签。展开一个 Issues 消息，并单击 Is the issue message helpful to you? ，然后你可以在弹出窗口中提供反馈。

![Issue feedback link](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/issues-feedback-20210303-8qAHYu.png)

## 12. Performance 面板的掉帧提示

在 [Performance 面板中分析加载性能](https://developers.google.com/chrome-devtools/evaluate-performance/reference#record-load)时，Frames 现在将掉帧部分标记为红色。将鼠标悬停在上面，可以看到帧速率。

![Dropped frames](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/dropped-frames-20210303-Wabh7a.png)

对应 Chromium issue: [1075865](https://crbug.com/1075865)

## 13. 在设备模式下模拟双屏和可折叠屏幕

现在可以在 DevTools 中模拟双屏幕和可折叠设备。

在[启用设备模式](https://developers.google.com/web/tools/chrome-devtools/device-mode#viewport)后，选择 Surface Duo 或三星 Galaxy Fold 其中一个设备。

单击新的 span 图标可以在单屏幕或折叠屏幕与双屏幕或折叠式体式之间切换。

启用 Web Platform 实验特性后，可以使用 CSS 的 `screen-spanning` 特性和 JavaScript 的 `getWindowSegments` API。右边的实验小图标显示了 Experimental Web Platform features 开关状态，如果图标高亮则表示开关已被打开。在浏览器中访问 `chrome://flags` 可以切换这个开关。

![Emulate dual-screen](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/dual-screen-20210303-X37FKZ.png)

对应 Chromium issue: [1054281](https://crbug.com/1054281)

## 14. 实验性新特性

### 使用 Puppeteer Recorder 自动化浏览器测试

> 要启用该实验性新特性，请选中 Settings > Experiments 下的 Recorder 复选框

现在，DevTools 可以基于你与浏览器的交互来生成 [Puppeteer](https://pptr.dev/) 脚本，便于你进行自动化浏览器测试。Puppeteer 是一个 Node.js 库，它提供了一个高级 API 来通过 [DevTools 协议](https://chromedevtools.github.io/devtools-protocol/)控制 Chrome 或 Chromium。

进入这个[演示页面](https://jec.fyi/demo/recorder)，在 DevTools 中打开 Sources 面板，选择左上的 Recording 选项卡，添加一个新的记录并命名（例如 test01.js）。

点击底部的 Record 按钮开始记录交互，试着填写屏幕上的表格。可以看到 Puppeteer 命令被相应地附加到文件中。再次点击 Record 按钮停止录制。

要运行该脚本，请遵循 Puppeteer 官网的[指南](https://pptr.dev/)。

请注意，这是一个早期阶段的实验特性，以后这个功能可能会有所变更。

![Puppeteer Recorder](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/recorder-20210303-hN6iNP.png)

对应 Chromium issue: [1144127](https://crbug.com/1144127)

### Styles 面板中的字体编辑器

> 要启用该实验性新特性，请选中 Settings > Experiments 下的 Enable new Font Editor tools within Styles pane 复选框

Styles 面板中新的字体编辑器是一个字体相关的属性编辑功能，以帮助开发者为网页找到更合适的排版。

弹出窗口提供了一个简洁的用户界面，可以使用一系列直观的输入动态地操作字体。

![Font editor in the Styles pane](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/font-20210303-YnzCk7.png)

对应 Chromium issue: [1093229](https://crbug.com/1093229)

### CSS flexbox 调试工具

> 要启用该实验性新特性，请选中 Settings > Experiments 下的 Enable CSS Flexbox debugging features 复选框

[从上次发布以来](https://developers.google.com/web/updates/2020/11/devtools#flexbox)，DevTools 增加了对 flexbox 调试的支持。

DevTools 现在绘制了一条指导线，更好地可视化 `align-items` 属性。同时也更好的支持了 `gap` 属性。在这里的例子中，设置了 `gap: 12px; `,注意下图缝隙的阴影图案。

![flexbox](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/flexbox-20210303-RqXWZA.png)

对应 Chromium issue: [1139949](https://crbug.com/1139949)

### 新的 CSP Violations 标签 

> 要启用该实验性新特性，请选中 Settings > Experiments 下的 Show CSP Violations view 复选框

在新的 CSP Violations 标签中查看所有内容安全策略（CSP）违规。这个新标签是一个实验性特性，用来方便的处理存在大量 CSP 与可信类型报错的页面。

![CSP Violations tab](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/csp-20210303-2ZWsHK.png)

对应 Chromium issue: [1137837](https://crbug.com/1137837)

### 新的颜色对比度算法-先进感知对比度算法(APCA)

> 要启用该实验性新特性，请选中 Settings > Experiments 下的 Enable new Advanced Perceptual Contrast Algorithm (APCA) replacing previous contrast ratio and AA/AAA guidelines 复选框

[先进感知对比度算法（APCA）](https://w3c.github.io/silver/guidelines/methods/Method-font-characteristic-contrast.html)正在取代[颜色选择器](https://developers.google.com/web/tools/chrome-devtools/accessibility/reference#contrast)中的 [AA/AAA](https://www.w3.org/WAI/WCAG21/quickref/#contrast-enhanced) 对比度提示。

APCA 是在现代色觉研究的基础上发展起来的一种新的计算对比度的方法。与 AA/AAA 相比，APCA 更依赖于上下文。对比度是根据文本的空间属性（字体重量和大小）、颜色（文本和背景之间可感知的明度差）和上下文（环境光线、环境、文本的预期目的）来计算的。

![APCA in Color Picker](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/apca-20210303-1m01Sk.png)

对应 Chromium issue: [1121900](https://crbug.com/1121900)

---
网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出，如果本文帮助到了你，别忘了点赞支持一下哦，你的点赞是我更新的最大动力！（收藏不点赞，都是耍流氓 🤣）~


> 参考文档：
>
> 1. [What's New In DevTools (Chrome 89)  |  Web  |  Google Developers](https://developers.google.com/web/updates/2021/01/devtools?utm_source=devtools#trusted-types)

PS：本文收录在在下的博客 [Github - SHERlocked93/blog](https://github.com/SHERlocked93/blog) 系列文章中，欢迎大家关注我的公众号 `前端下午茶`，直接搜索即可添加或者点[这里](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/TJt4p2-19-56-21.jpg)添加，持续为大家推送前端以及前端周边相关优质技术文，共同进步，一起加油~

另外可以加入「前端下午茶交流群」微信群，微信搜索  `qianyu443033099` 加我好友，备注**加群**，我拉你入群～