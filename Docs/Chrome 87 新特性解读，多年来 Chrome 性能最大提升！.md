# Chrome 87 新特性解读，多年来 Chrome 性能最大提升！

今天 Chrome 更新了 87 最新版，这是今年最后一次 Chrome 更新了，这个版本是多年来 Chrome 性能获得最大提升的一次，开发者工具也进行了大幅度更新。

有用户认为，原本 Chrome 的性能问题诟病已久，然而在新 Edge 出来了以后，性能突然就提升了，这显然是谷歌方面受到了 Edge 市场份额暴增带来的压力。

另外，在 Mac 上的 Chrome 还更新了图标，这应该是为了适配 Big Sur 专门进行的设计。

原文： [developers.google.com/web/updates…](https://developers.google.com/web/updates/2020/10/devtools "https://developers.google.com/web/updates/2020/10/devtools")

> PS： 最新的 Chrome 更新视频是一个日裔女的解说，这英语口语真是醉了...

## 1. 新的 CSS Grid 调试工具

现在 DevTools 对 CSS 的 Grid 有了更好的支持。

![CSS grid debugging](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/6a968cebe7e2126a2c4e27bf8357814434588a5fd0a04f712b49ca78c0e09e52.webp)

当页面上的 HTML 元素具有 `display: grid` 或 `display: inline-grid` 时，可以在 Elements 面板中看到它旁边的一个 Grid 标记。单击标记可以切换页面上 Grid 覆盖的高亮显示。

新的 Layout 子面板有一个 Grid 标签，提供了查看 Grid 的一些选项。

查看[文档](https://developers.google.com/web/tools/chrome-devtools/css/grid "https://developers.google.com/web/tools/chrome-devtools/css/grid")以了解更多信息。

对应 Chromium issue: [1047356](https://crbug.com/1047356 "https://crbug.com/1047356")

## 2. 新的 WebAuthn 面板

现在，可以模拟身份验证器并使用新的 [WebAuthn 选项卡](https://developers.google.com/web/tools/chrome-devtools/webauthn "https://developers.google.com/web/tools/chrome-devtools/webauthn")调试 [Web 身份验证 API](https://w3c.github.io/webauthn/ "https://w3c.github.io/webauthn/")。

![WebAuthn](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/064a6aa9b3fd009435b9f7f42dcb6c62fb44187aa2b312fab61498ebbd3c2e3d.webp)

如图选择 More options > More tools > WebAuthn 可以打开 WebAuthn 面板。

![WebAuthn tab](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/50375e0ba03a582ba07330650ffddef8534f1ec0872733bdb3aaf71d1c72a80d.webp)

在 WebAuthn 标签出现之前，Chrome 上不支持原生的 WebAuthn 调试。开发人员需要物理身份验证器来测试他们的 Web 应用程序。

有了新的 WebAuthn 标签，Web 开发人员现在可以模拟认证器，定制它们的功能，并检查它们的状态，而不需要任何物理认证器。这使得调试体验更加容易。

查看我们的[文档](https://developers.google.com/web/tools/chrome-devtools/webauthn "https://developers.google.com/web/tools/chrome-devtools/webauthn")了解更多关于 WebAuthn 特性的信息。

对应 Chromium issue: [1034663](https://crbug.com/1034663 "https://crbug.com/1034663")

## 3. 开发者工具的面板现在支持垂直分屏

DevTools 现在支持将 DevTools 工具面板移动到顶部和底部，通过这种方式，可以同时分屏查看任意两个工具面板。

例如，如果想同时查看 Elements 和 Sources 面板，可以右键单击 Sources 面板，并选择移动到底部。

![Move to bottom](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/21fe9f275b23ec3899b86c8e694272854132a48f7538b82139ab95c5640f3a02.webp)

类似地，可以将任何底部选项卡移动到顶部，方法是右键单击选项卡并选择 Move to top。

![Move to top](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/2d4595a14bd3c8738e9c46d0654e137e539c48866f92f78c935b0470f1e45180.webp)

## 4. Elements 面板功能更新

### 4.1 在 Styles 子面板中查看 Computed 侧边栏

现在可以切换 Styles 面板中的 Computed 侧边栏。

默认情况下，Styles 面板中的 Computed 侧边栏是折叠的，单击按钮可以切换展开状态。

![Computed sidebar pane](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/4db624a8c475bd833b64b96dfc4753626800988ab857e3269ac26d98c7b90374.webp)

对应 Chromium issue: [1073899](https://crbug.com/1073899 "https://crbug.com/1073899")

### 4.2 在 Computed 面板中对 CSS 属性进行分组

现在可以在 Computed 侧边栏中按类别对 CSS 属性进行分组。

有了这个新的分组特性，在 Computed 中查找和选择性地关注一组相关 CSS 属性变得更加容易。

在 Elements 面板上，选择一个元素，单击 Group 复选框，可以对 CSS 属性进行分组/取消分组。

![Grouping CSS properties](https://raw.githubusercontent.com/SHERlocked93/pic/master/uPic/06-grouping-css-prop.png)

对应 Chromium issues: [1096230](https://crbug.com/1096230 "https://crbug.com/1096230"), [1084673](https://crbug.com/1084673 "https://crbug.com/1084673"), [1106251](https://crbug.com/1106251 "https://crbug.com/1106251")

## 5. Lighthouse 更新 Lighthouse 6.4

Lighthouse 面板现在更新到了 Lighthouse 6.4，查看 [release notes](https://github.com/GoogleChrome/lighthouse/releases "https://github.com/GoogleChrome/lighthouse/releases") 可以看到完整的新特性清单。

![Lighthouse](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/85493371ef4a0392481a62b1075409dba0ecef245b68a29528c61d76423fde56.webp)

Lighthouse 6.4 中的新特性：

1. Preload fonts：报告是否所有使用了 font-display: optional 的字体文件是否都有预加载成
2. Valid sourcemaps：报告页面上非第三方 JS 的 sourcemap 文件是否正确
3. Large JavaScript library（实验性特性）：报告页面上的大型 JS 库（比如：moment.js)

对应 Chromium issue: [772558](https://crbug.com/772558 "https://crbug.com/772558")

## 6. 在 Performance 面板中的事件线（Timings）上将标记出 performance.mark() 事件

Performance 面板记录的 Timing 部分现在会标记 `Performance.mark()` 事件。

![Performance.mark events](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/1543c07aa0d9f212ed1eb7c4aded66c4bb30a8eae4f2c23e26e37a281eef8d45.webp)

## 7. Network 面板新增 resource-type、url 筛选条件

现在可以使用 Network 面板中的 `resource-type` 和 `url` 关键字筛选网络请求。

例如，使用 `resource-type: image` 可以筛选出请求图像的网络请求。

![resource-type filter](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/bec7eba50365b391f789079b201dd0358cf72e020553b22539d542c5c1d0e5dc.webp)

点击[更多的筛选条件](https://developers.google.com/web/tools/chrome-devtools/network/reference#filter-by-property "https://developers.google.com/web/tools/chrome-devtools/network/reference#filter-by-property")，可以查看到更多类似于 `resource-type` 和 `url` 的筛选用法。

对应 Chromium issues: [1121141](https://crbug.com/1121141 "https://crbug.com/1121141"), [1104188](https://crbug.com/1104188 "https://crbug.com/1104188")

## 8. Application 面板中 Frames 子面板相关的更新

### 8.1 支持展示 `COEP` 和 `COOP` 的向谁报告字段

现在可以在 Application 面板的 Frames 子面板的 Security & Isolation 部分查看向终端报告的 `COEP` （Cross-Origin Embedder Policy）和 `COOP`（Cross-Origin Opener Policy）。

[Reporting Api](https://developers.google.com/web/updates/2018/09/reportingapi "https://developers.google.com/web/updates/2018/09/reportingapi") 定义了一个叫做 Report-To 的新的 HTTP Header，当网站中出现违背 `COEP` （Cross-Origin Embedder Policy）和 `COOP`（Cross-Origin Opener Policy）的情况时，浏览器会向这个头部指定的地址发送报告。

![reporting to endpoint](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/0b929d6378fe044f2b6ebaea092a8ea8021dd295216d13f9a25677849f1f43e2.webp)

关于如何开启 `COEP` 和 `COOP` 来使你的网站实现跨源隔离（cross-origin isolated）可以查看[这篇文章](https://web.dev/coop-coep/ "https://web.dev/coop-coep/")

对应 Chromium issue: [1051466](https://crbug.com/1051466 "https://crbug.com/1051466")

### 8.2 展示 COEP 和 COOP 的 report-only 模式

Devtools 对于 COEP、COOP 为 report-only 的情况，新增了标记展示

![report-only label](https://raw.githubusercontent.com/SHERlocked93/pic/master/uPic/11-report-only.png)

观看[这个视频](https://youtu.be/XLNJYhjA-0c "https://youtu.be/XLNJYhjA-0c")，学习如何防止信息泄漏，以及如何开启 COOP 和 COEP。

对应 Chromium issue: [1051466](https://crbug.com/1051466 "https://crbug.com/1051466")

## 9. 移除 More tools 菜单中的 Setting 按钮

More tools 菜单中的 Setting 已不推荐使用，请从主面板打开 Setting。

![Settings in the main panel](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/b33404ba9d1b597d34fbde1583db52e03cc6a037921cab45a88aa2789cf292ad.webp)

对应 Chromium issue: [1121312](https://crbug.com/1121312 "https://crbug.com/1121312")

## 10. 实验特性

以下特性均需要开启 Settings > Experiments 下的相关选项

### 10.1 CSS Overview 面板中支持查看、修复色彩对比度问题

CSS Overview 面板展示了你的页面中低色彩对比文本的色彩列表。

这个 [Demo 页面](https://jec.fyi/demo/accessible-color-multi "https://jec.fyi/demo/accessible-color-multi")展示了一个低色彩对比度的反面案例，打开这个 CSS Overview 面板可以查看到所有有问题的元素列表。

![Low color contrast issues](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/a5bc297a9999fbed1ea08a1594da60e2a0cac15ee932c98f3ca656f0fe1d33c7.webp)

单击列表中的某个元素可以打开 Elements 面板中的元素，DevTools 将提供自动颜色建议，帮助修复文本的低色彩对比度问题。

对应 Chromium issue: [1120316](https://crbug.com/1120316 "https://crbug.com/1120316")

## 10.2 DevTools 支持自定义键盘快捷键了

现在可以在 DevTools 中自定义键盘快捷键。

进入 Settings > Shortcuts，将鼠标悬停在一个命令上，点击编辑按钮来自定义快捷键。

![Customize keyboard shortcuts](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/6bdb4a64d6dab2081afd1523560282dece895f033b4177189a7490437b88418d.webp)

要重置所有快捷方式，请单击 Restore default shortcuts 还原默认快捷键。

对应 Chromium issue: [174309](https://crbug.com/174309 "https://crbug.com/174309")

---
