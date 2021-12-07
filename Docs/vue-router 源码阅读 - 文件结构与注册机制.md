# vue-router 源码阅读 - 文件结构与注册机制
[TOC]



![](https://i.loli.net/2019/02/23/5c71619fc2cf0.jpg)

前端路由是我们前端开发日常开发中经常碰到的概念，在下在日常使用中知其然也好奇着所以然，因此对 vue-router 的源码进行了一些阅读，也汲取了社区的一些文章优秀的思想，于本文记录总结作为自己思考的输出，本人水平有限，欢迎留言讨论~
目标 vue-rouer 版本：`3.0.2`
vue-router源码注释：[vue\-router\-analysis](https://github.com/SHERlocked93/vue-router-analysis)
声明：文章中源码的语法都使用 Flow，并且源码根据需要都有删节(为了不被迷糊 @_@)，如果要看完整版的请进入上面的 [github地址](https://github.com/SHERlocked93/vue-router-analysis) ~ 
本文是系列文章，链接见底部 ~

## 0. 前备知识
- Flow
- ES6语法
- 设计模式 - 外观模式
- HTML5 History Api
如果你对这些还没有了解的话，可以看一下本文末尾的推介阅读。
## 1. 文件结构
首先我们来看看文件结构：
```bash
.
├── build                    // 打包相关配置
├── scripts                    // 构建相关
├── dist                    // 构建后文件目录
├── docs                    // 项目文档
├── docs-gitbook            // gitbook配置
├── examples                // 示例代码，调试的时候使用
├── flow                    // Flow 声明
├── src                        // 源码目录
│   ├── components             // 公共组件
│   ├── history                // 路由类实现
│   ├── util                // 相关工具库
│   ├── create-matcher.js    // 根据传入的配置对象创建路由映射表
│   ├── create-route-map.js    // 根据routes配置对象创建路由映射表 
│   ├── index.js            // 主入口
│   └── install.js            // VueRouter装载入口
├── test                    // 测试文件
└── types                    // TypeScript 声明
```
我们主要关注的就是 `src` 中的内容。

## 2. 入口文件
### 2.1 rollup 出口与入口
按照惯例，首先从 `package.json` 看起，这里有两个命令值得注意一下：
```json
{
    "scripts": {
        "dev:dist": "rollup -wm -c build/rollup.dev.config.js",
        "build": "node build/build.js"
  }
}
```
`dev:dist` 用配置文件 `rollup.dev.config.js` 生成 `dist` 目录下方便开发调试相关生成文件，对应于下面的配置环境 `development`；
`build` 是用 `node` 运行 `build/build.js` 生成正式的文件，包括 `es6`、`commonjs`、`IIFE` 方式的导出文件和压缩之后的导出文件；
这两种方式都是使用 `build/configs.js` 这个配置文件来生成的，其中有一段语义化比较不错的代码挺有意思，跟 Vue 的配置生成文件比较类似：
```javascript
// vue-router/build/configs.js
module.exports = [{                     // 打包出口
    file: resolve('dist/vue-router.js'),
    format: 'umd',
    env: 'development'
  },{
    file: resolve('dist/vue-router.min.js'),
    format: 'umd',
    env: 'production'
  },{
    file: resolve('dist/vue-router.common.js'),
    format: 'cjs'
  },{
    file: resolve('dist/vue-router.esm.js'),
    format: 'es'
  }
].map(genConfig)
function genConfig (opts) {
  const config = {
    input: {
      input: resolve('src/index.js'),     // 打包入口
      plugins: [...]
    },
    output: {
      file: opts.file,
      format: opts.format,
      banner,
      name: 'VueRouter'
    }
  }
  return config
}
```
可以清晰的看到 `rollup` 打包的出口和入口，入口是 `src/index.js` 文件，而出口就是上面那部分的配置，`env` 是开发/生产环境标记，`format` 为编译输出的方式：
- **es：** ES Modules，使用ES6的模板语法输出
- **cjs：** CommonJs Module，遵循CommonJs Module规范的文件输出
- **umd：** 支持外链规范的文件输出，此文件可以直接使用script标签，其实也就是 IIFE 的方式
那么正式输出是使用 `build` 方式，我们可以从 `src/index.js` 看起
```javascript
// src/index.js
import { install } from './install'
export default class VueRouter { ... }
VueRouter.install = install
```
首先这个文件导出了一个类 `VueRouter`，这个就是我们在 Vue 项目中引入 vue-router 的时候 `Vue.use(VueRouter)` 所用到的，而 `Vue.use` 的主要作用就是找注册插件上的 `install` 方法并执行，往下看最后一行，从一个 `install.js` 文件中导出的 install 被赋给了 `VueRouter.install`，这就是 `Vue.use` 中执行所用到的 `install` 方法。
### 2.2 Vue.use
可以简单看一下 Vue 中 `Vue.use` 这个方法是如何实现的：
```javascript
// vue/src/core/global-api/use.js
export function initUse (Vue: GlobalAPI) {
  Vue.use = function (plugin: Function | Object) {
    // ... 省略一些判重操作
    const args = toArray(arguments, 1)
    args.unshift(this)            // 注意这个this，是vue对象
    if (typeof plugin.install === 'function') {
      plugin.install.apply(plugin, args)
    }
    return this
  }
}
```
上面可以看到 `Vue.use` 这个方法就是执行待注册插件上的 `install` 方法，并将这个插件实例保存起来。值得注意的是 `install` 方法执行时的第一个参数是通过 `unshift` 推入的 `this`，因此 `install` 执行时可以拿到 Vue 对象。
对应上一小节，这里的 `plugin.install` 就是 `VueRouter.install`。
## 3. 路由注册
### 3.1 install
接之前，看一下 `install.js` 里面是如何进行路由插件的注册：
```javascript
// vue-router/src/install.js
/* vue-router 的注册过程 Vue.use(VueRouter) */
export function install(Vue) {
  _Vue = Vue    // 这样拿到 Vue 不会因为 import 带来的打包体积增加

  const isDef = v => v !== undefined

  const registerInstance = (vm, callVal) => {
    let i = vm.$options._parentVnode // 至少存在一个 VueComponent 时, _parentVnode 属性才存在
    // registerRouteInstance 在 src/components/view.js
    if (isDef(i) && isDef(i = i.data) && isDef(i = i.registerRouteInstance)) {
      i(vm, callVal)
    }
  }

  // new Vue 时或者创建新组件时，在 beforeCreate 钩子中调用
  Vue.mixin({
    beforeCreate() {
      if (isDef(this.$options.router)) { // 组件是否存在$options.router，该对象只在根组件上有
        this._routerRoot = this // 这里的this是根vue实例
        this._router = this.$options.router    // VueRouter实例
        this._router.init(this)
        Vue.util.defineReactive(this, '_route', this._router.history.current)
      } else { // 组件实例才会进入，通过$parent一级级获取_routerRoot
        this._routerRoot = (this.$parent && this.$parent._routerRoot) || this
      }
      registerInstance(this, this)
    },
    destroyed() {
      registerInstance(this)
    }
  })

  // 所有实例中 this.$router 等同于访问 this._routerRoot._router
  Object.defineProperty(Vue.prototype, '$router', {
    get() { return this._routerRoot._router }
  })

  // 所有实例中 this.$route 等同于访问 this._routerRoot._route
  Object.defineProperty(Vue.prototype, '$route', {
    get() { return this._routerRoot._route }
  })

  Vue.component('RouterView', View) // 注册公共组件 router-view
  Vue.component('RouterLink', Link) // 注册公共组件 router-link

  const strats = Vue.config.optionMergeStrategies
  strats.beforeRouteEnter = strats.beforeRouteLeave = strats.beforeRouteUpdate = strats.created
}
```
`install` 方法主要分为几个部分：
1. 通过 `Vue.mixin` 在 `beforeCreate`、 `destroyed` 的时候将一些路由方法挂载到每个 vue 实例中
2. 给每个 vue 实例中挂载路由对象以保证在 `methods` 等地方可以通过 `this.$router`、`this.$route` 访问到相关信息
3. 注册公共组件 `router-view`、`router-link`
4. 注册路由的生命周期函数

`Vue.mixin` 将定义的两个钩子在组件 `extend` 的时候合并到该组件的 `options` 中，从而注册到每个组件实例。看看 `beforeCreate`，一开始访问了一个 `this.$options.router` 这个是 Vue 项目里面 `app.js` 中的 `new Vue({ router })` 这里传入的这个 router，当然也只有在 `new Vue` 这时才会传入 router，也就是说 `this.$options.router` 只有根实例上才有。这个传入 router 到底是什么呢，我们看看它的使用方式就知道了：
```javascript
const router = new VueRouter({
  mode: 'hash',
  routes: [{ path: '/', component: Home },
        { path: '/foo', component: Foo },
        { path: '/bar', component: Bar }]
})
new Vue({
  router,
  template: `<div id="app"></div>`
}).$mount('#app')
```
可以看到这个 `this.$options.router` 也就是 Vue 实例中的 `this._route` 其实就是 VueRouter 的实例。
剩下的一顿眼花缭乱的操作，是为了在每个 Vue 组件实例中都可以通过 `_routerRoot` 访问根 Vue 实例，其上的 `_route`、`_router` 被赋到 Vue 的原型上，这样每个 Vue 的实例中都可以通过 `this.$route`、`this.$router` 访问到挂载在根实例 `_routerRoot` 上的 `_route`、`_router`，后面用 Vue 上的响应式化方法 `defineReactive` 来将 `_route` 响应式化，另外在根组件上用 `this._router.init()` 进行了初始化操作。
随便找个 Vue 组件，打印一下其上的 `_routerRoot`：
![](https://i.loli.net/2019/02/21/5c6e1f71ccb33.png)
可以看到这是 Vue 的根组件。
### 3.2 VueRouter
在之前我们已经看过 `src/index.js` 了，这里来详细看一下 VueRouter 这个类
```javascript
// vue-router/src/index.js
export default class VueRouter {  
  constructor(options: RouterOptions = {}) { }

  /* install 方法会调用 init 来初始化 */
  init(app: any /* Vue组件实例 */) { }

  /* createMatcher 方法返回的 match 方法 */
  match(raw: RawLocation, current?: Route, redirectedFrom?: Location) { }

  /* 当前路由对象 */
  get currentRoute() { }

  /* 注册 beforeHooks 事件 */
  beforeEach(fn: Function): Function { }

  /* 注册 resolveHooks 事件 */
  beforeResolve(fn: Function): Function { }

  /* 注册 afterHooks 事件 */
  afterEach(fn: Function): Function { }

  /* onReady 事件 */
  onReady(cb: Function, errorCb?: Function) { }

  /* onError 事件 */
  onError(errorCb: Function) { }

  /* 调用 transitionTo 跳转路由 */
  push(location: RawLocation, onComplete?: Function, onAbort?: Function) { }

  /* 调用 transitionTo 跳转路由 */
  replace(location: RawLocation, onComplete?: Function, onAbort?: Function) { }

  /* 跳转到指定历史记录 */
  go(n: number) { }

  /* 后退 */
  back() { }

  /* 前进 */
  forward() { }

  /* 获取路由匹配的组件 */
  getMatchedComponents(to?: RawLocation | Route) { }

  /* 根据路由对象返回浏览器路径等信息 */
  resolve(to: RawLocation, current?: Route, append?: boolean) { }

  /* 动态添加路由 */
  addRoutes(routes: Array<RouteConfig>) { }
}
```
VueRouter 类中除了一坨实例方法之外，主要关注的是它的构造函数和初始化方法 `init`。
首先看看构造函数，其中的 `mode` 代表路由创建的模式，由用户配置与应用场景决定，主要有三种 History、Hash、Abstract，前两种我们已经很熟悉了，Abstract 代表非浏览器环境，比如 Node、weex 等；`this.history` 主要是路由的具体实例。实现如下：
```javascript
// vue-router/src/index.js
export default class VueRouter {  
  constructor(options: RouterOptions = {}) {
    this.matcher = createMatcher(options.routes || [], this) // 添加路由匹配器
    let mode = options.mode || 'hash' // 路由匹配方式，默认为hash
    this.fallback = mode === 'history' && !supportsPushState && options.fallback !== false
    if (this.fallback) { mode = 'hash' } // 如果不支持history则退化为hash
    if (!inBrowser) { mode = 'abstract' } // 非浏览器环境强制abstract，比如node中
    this.mode = mode

    switch (mode) { // 外观模式
      case 'history': // history 方式
        this.history = new HTML5History(this, options.base)
        break
      case 'hash': // hash 方式
        this.history = new HashHistory(this, options.base, this.fallback)
        break
      case 'abstract': // abstract 方式
        this.history = new AbstractHistory(this, options.base)
        break
      default: ...
    }
  }
}
```
`init` 初始化方法是在 install 时的 `Vue.mixin` 所注册的 `beforeCreate` 钩子中调用的，可以翻上去看看，调用方式是 `this._router.init(this)`。另外初始化方法需要负责从任一个路径跳转到项目中时的路由初始化，以 Hash 模式为例，此时还没有对相关事件进行绑定，因此在第一次执行的时候就要进行事件绑定与 `popstate`、`hashchange` 事件触发，然后手动触发一次路由跳转。实现如下：
```javascript
// vue-router/src/index.js
export default class VueRouter {  
  /* install 方法会调用 init 来初始化 */
  init(app: any /* Vue组件实例 */) {
    const history = this.history

    if (history instanceof HTML5History) {
      // 调用 history 实例的 transitionTo 方法
      history.transitionTo(history.getCurrentLocation())
    } else if (history instanceof HashHistory) { 
      const setupHashListener = () => {
          history.setupListeners() // 设置 popstate/hashchange 事件监听
      }
      history.transitionTo(             // 调用 history 实例的 transitionTo 方法
          history.getCurrentLocation(), // 浏览器 window 地址的 hash 值
          setupHashListener,         // 成功回调
          setupHashListener        // 失败回调
      )
    }
  }
}
```

除此之外，VueRouter 还有很多实例方法，用来实现各种功能的，剩下的将在系列文章分享 ~

---
本文是**系列文章**，随后会更新后面的部分，共同进步~
> 1. [vue-router 源码阅读 - 文件结构与注册机制](https://segmentfault.com/a/1190000018262346)

网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出~

> 推介阅读：
>
>1. [H5 History Api - MDN](https://developer.mozilla.org/zh-CN/docs/Mozilla/Add-ons/WebExtensions/API/history)
>2. [ECMAScript 6 入门 \- 阮一峰](http://es6.ruanyifeng.com/)
>3. [JS 静态类型检查工具 Flow \- SegmentFault 思否](https://segmentfault.com/a/1190000014367450)
>4. [JS 外观模式 \- SegmentFault 思否](https://segmentfault.com/a/1190000012431621)
>5. [前端路由跳转基本原理 \- 掘金](https://juejin.im/post/5c52da9ee51d45221f242804)
>
>参考：
>
>1. [Vue\.js 技术揭秘](https://ustbhuangyi.github.io/vue-analysis/vue-router/router.html)

PS：欢迎大家关注我的公众号【前端下午茶】，一起加油吧~
![](https://i.loli.net/2019/03/26/5c99d1685fff9.png)
