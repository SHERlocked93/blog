# Vue项目预渲染机制引入实践
[TOC]

周末想顺便把已经做好静态页面的webApp项目做一下SEO优化，由于不想写蹩脚的[SSR](https://ssr.vuejs.org/zh/)代码，所以准备采用预渲染，本来想着网上有这么多[预渲染](https://ssr.vuejs.org/zh/#%E6%9C%8D%E5%8A%A1%E5%99%A8%E7%AB%AF%E6%B8%B2%E6%9F%93-vs-%E9%A2%84%E6%B8%B2%E6%9F%93-ssr-vs-prerendering)的文章，随便找个来跟着做不就完了嘛，结果年轻的我付出了整个周末..... 这篇文章就记录一下最后是怎么配置的 T.T

声明：

1. 以下配置只保留有必要的
2. 生成目录这里使用`base`代替，请自行修改
3. vue-cli模板使用`webpack`，其他模板类推
4. [webApp - 在线预览](http://www.sherlocked93.club/imanuf_portal_mobile/)

## 1. 简介与使用场景

我们知道SPA有很多优点，不过一个缺点就是对(不是Google的)愚蠢的搜索引擎的SEO不友好，为了照顾这些引擎，目前主要有两个方案：**服务端渲染**(Server Side Rendering)、**预渲染**(Prerending)。

如果你只需要改善少数页面（例如 `/`, `/about`, `/contact` 等）的 `SEO`，那么你可能需要预渲染。无需使用 web 服务器实时动态编译 HTML (服务端渲染, SSR)，而是使用预渲染方式，在构建时(build time)简单地生成针对特定路由的静态 HTML 文件。它主要使用 [prerender-spa-plugin](https://github.com/chrisvfritz/prerender-spa-plugin) 插件，其与SSR一样都可以加快页面的加载速度，并且侵入性更小，在已上线的项目稍加改动也可以轻松引入预渲染机制，而SSR方案则需要将整个项目结构推翻；

访问预渲染出来的页面在访问时与`SSR`一样快，并且它将服务端编译HTML的时机提前到了构建时，因此也降低了服务端的压力，如果你的服务器跟我的一样买的 **1M1G1核** 的小水管服务器 ( 穷 )，那么预渲染可能更适合你。不过SSR和预渲染的使用场景还是有较明显的区别的。预渲染的使用场景更多是简单的静态页面。服务端渲染适用于复杂、较大型、与服务端交互频繁的功能型网站，比如电商网站。

## 2. 安装配置

首先来看看相关技术栈：vue^2.5.2、vue-router^3.0.1、vue-cli^2.9.6、webpack^3.6.0、prerender-spa-plugin^3.3.0

### 2.1 安装

安装跟其他库一样

```bash
# Yarn
$ yarn add prerender-spa-plugin -D
# or NPM
$ npm install prerender-spa-plugin --save-dev
```

### 2.2 前端配置

首先看看文件结构，用的是vue-cli2的webpack模板生成的文件结构

```bash
│ .babelrc
│ index.html
│ package.json
│ README.md
├─build
│ build.js
│ check-versions.js
│ utils.js
│ vue-loader.conf.js
│ webpack.base.conf.js
│ webpack.dev.conf.js
│ webpack.prod.conf.js
├─config
│ dev.env.js
│ index.js
│ prod.env.js
├─src
│ │ App.vue
│ │ main.js
│ │
│ ├─assets
│ ├─components
│ ├─router
│ │ index.js
│ ├─styles
│ ├─utils
│ └─views
│ BigData.vue
│ CompanyHonor.vue
```



然后是router/index.js的配置，预渲染要求是histroy模式，有的文章说不需要history模式，这是错的，否则生成的页面都是同一个html。另外注意加上`base`否则如果你希望跳转到二级页面的`localhost/base/home`时候，在页面中点击`<router-link to="/home">home</router-link>`的时候会跳转`localhost/home`

// src/router/index.js

```js
import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: '/base/',
  routes: [...]
})

```

然后是config，这里注意`assetsPublicPath`不是`./`,

// config/index.js

```js
const path = require("path")

module.exports = {
  build: {
    index: path.resolve(__dirname, "../base/index.html"),
    assetsRoot: path.resolve(__dirname, ".."),
    assetsSubDirectory: "base/static",
    assetsPublicPath: "/",
  }
}
```

然后是插件的配置，是放在`prod`中的，因为只有build的时候会用

// build/webpack.prod.conf.js

```js
const path = require('path')
const config = require('../config')
const PrerenderSPAPlugin = require('prerender-spa-plugin')
const Renderer = PrerenderSPAPlugin.PuppeteerRenderer

const webpackConfig = merge(baseWebpackConfig, {
  new PrerenderSPAPlugin({
   staticDir: config.build.assetsRoot,
   outputDir: path.join(config.build.assetsRoot, 'base'),
   indexPath: config.build.index,

   // 对应路由文件的path
   routes: [
     '/',
     '/BigData',
     '/CompanyHonor'
   ],

   renderer: new Renderer({
     headless: false,
     renderAfterDocumentEvent: 'render-event'
   })
  })
})
```

注意上面一个`renderAfterDocumentEvent: 'render-event'`了么，这个意思是在`render-event`事件触发之后执行prerender，这个事件我们在main.js中mounted钩子触发

// src/main.js

```js
import Vue from 'vue'
import App from './App'

new Vue({
  el: '#app',
  render: h => h(App),
  mounted() {
    document.dispatchEvent(new Event('render-event'))
  }
})
```

还有个配置要注意下在 build/utils.js 中的 `ExtractTextPlugin.extract` 的 `publicPath` ，否则一些vue中引用的资源会找不到

// build/utils.js

```js
ExtractTextPlugin.extract({
  use: loaders,
  fallback: 'vue-style-loader',
  // publicPath: '../../'
})
```

这时候执行`npm run build`就可以生成刚刚配置在`PrerenderSPAPlugin`插件中routes中的页面html了，这过程中会一闪而过的短暂打开chromium浏览器，不用管。

最后生成的目录树：

```bash
│ index.html
├─BigData
│ index.html
├─CompanyHonor
│ index.html
└─static
    ├─css
    ├─fonts
    ├─img
    └─js
```

最后如果希望进一步优化生成出来页面的SEO，可以配合 [vue-meta-info](https://github.com/muwoo/vue-meta-info) 这个网上有很多文章，就不赘述了

### 2.3 nginx配置

顺便贴一下nginx配置

```nginx
location ~ ^/base/ {
  try_files $uri $uri/ /base/index.html =404;
}
```





---



网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出~



> 参考：
>
> 1. [Vue.js 服务器端渲染指南](https://ssr.vuejs.org/zh/)
> 2. [Vue 服务端渲染 & 预渲染](https://blog.csdn.net/csdn_yudong/article/details/80769424)
> 3. [vue-cli v3, can't get it to work.. issue #215](https://github.com/chrisvfritz/prerender-spa-plugin/issues/215#)
> 4. [When assetsPublicPath is set, the... issue #176](https://github.com/chrisvfritz/prerender-spa-plugin/issues/176)
> 5. [vue.js vue-router history模式路由，域名二级目录子目录nginx配置](https://segmentfault.com/a/1190000015753352?utm_source=tag-newest)
