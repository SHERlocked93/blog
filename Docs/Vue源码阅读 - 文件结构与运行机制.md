# Vue源码阅读 - 文件结构与运行机制

vue已是目前国内前端web端三分天下之一，同时也作为本人主要技术栈之一，在日常使用中知其然也好奇着所以然，另外最近的社区涌现了一大票vue源码阅读类的文章，在下借这个机会从大家的文章和讨论中汲取了一些营养，同时对一些阅读源码时的想法进行总结，出产一些文章，作为自己思考的输出，本人水平有限，欢迎留言讨论~

目标Vue版本：`2.5.17-beta.0`

vue源码注释：[github.com/SHERlocked9…](https://github.com/SHERlocked93/vue-analysis "https://github.com/SHERlocked93/vue-analysis")

声明：文章中源码的语法都使用 Flow，并且源码根据需要都有删节(为了不被迷糊 @_@)，如果要看完整版的请进入上面的[github地址](https://github.com/SHERlocked93/vue-analysis "https://github.com/SHERlocked93/vue-analysis")，本文是系列文章，文章地址见底部~

感兴趣的同学可以加文末的微信群，一起讨论吧～

## 0. 前备知识

- Flow
- ES6语法
- 常用的设计模式
- 柯里化等函数式编程思想

这里推介几篇前备文章：[JS 静态类型检查工具 Flow](https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E9%9D%99%E6%80%81%E7%B1%BB%E5%9E%8B%E6%A3%80%E6%9F%A5%E5%B7%A5%E5%85%B7%20Flow.md "https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E9%9D%99%E6%80%81%E7%B1%BB%E5%9E%8B%E6%A3%80%E6%9F%A5%E5%B7%A5%E5%85%B7%20Flow.md")，[ECMAScript 6 入门 - 阮一峰](http://es6.ruanyifeng.com/ "http://es6.ruanyifeng.com/")，[JS中的柯里化](https://github.com/SHERlocked93/blog/blob/master/Docs/JavaScript%20%E5%87%BD%E6%95%B0%E5%BC%8F%E7%BC%96%E7%A8%8B%E6%8A%80%E5%B7%A7%20-%20%E6%9F%AF%E9%87%8C%E5%8C%96.md "https://github.com/SHERlocked93/blog/blob/master/Docs/JavaScript%20%E5%87%BD%E6%95%B0%E5%BC%8F%E7%BC%96%E7%A8%8B%E6%8A%80%E5%B7%A7%20-%20%E6%9F%AF%E9%87%8C%E5%8C%96.md")，[JS 观察者模式](https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E8%A7%82%E5%AF%9F%E8%80%85%E6%A8%A1%E5%BC%8F.md "https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E8%A7%82%E5%AF%9F%E8%80%85%E6%A8%A1%E5%BC%8F.md")，[JS 利用高阶函数实现函数缓存(备忘模式)](https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E5%88%A9%E7%94%A8%E9%AB%98%E9%98%B6%E5%87%BD%E6%95%B0%E5%AE%9E%E7%8E%B0%E5%87%BD%E6%95%B0%E7%BC%93%E5%AD%98%28%E5%A4%87%E5%BF%98%E6%A8%A1%E5%BC%8F%29.md "https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E5%88%A9%E7%94%A8%E9%AB%98%E9%98%B6%E5%87%BD%E6%95%B0%E5%AE%9E%E7%8E%B0%E5%87%BD%E6%95%B0%E7%BC%93%E5%AD%98%28%E5%A4%87%E5%BF%98%E6%A8%A1%E5%BC%8F%29.md")

## 1. 文件结构

文件结构在vue的[CONTRIBUTING.md](https://github.com/vuejs/vue/blob/dev/.github/CONTRIBUTING.md "https://github.com/vuejs/vue/blob/dev/.github/CONTRIBUTING.md")中有介绍，这边直接翻译过来：

```bash
├── scripts ------------------------------- 包含与构建相关的脚本和配置文件
│   ├── alias.js -------------------------- 源码中使用到的模块导入别名
│   ├── config.js ------------------------- 项目的构建配置
├── build --------------------------------- 构建相关的文件，一般情况下我们不需要动
├── dist ---------------------------------- 构建后文件的输出目录
├── examples ------------------------------ 存放一些使用Vue开发的应用案例
├── flow ---------------------------------- JS静态类型检查工具 [Flow](https://flowtype.org/) 的类型声明
├── package.json
├── test ---------------------------------- 测试文件
├── src ----------------------------------- 源码目录
│   ├── compiler -------------------------- 编译器代码，用来将 template 编译为 render 函数
│   │   ├── parser ------------------------ 存放将模板字符串转换成元素抽象语法树的代码
│   │   ├── codegen ----------------------- 存放从抽象语法树(AST)生成render函数的代码
│   │   ├── optimizer.js ------------------ 分析静态树，优化vdom渲染
│   ├── core ------------------------------ 存放通用的，平台无关的运行时代码
│   │   ├── observer ---------------------- 响应式实现，包含数据观测的核心代码
│   │   ├── vdom -------------------------- 虚拟DOM的 creation 和 patching 的代码
│   │   ├── instance ---------------------- Vue构造函数与原型相关代码
│   │   ├── global-api -------------------- 给Vue构造函数挂载全局方法(静态方法)或属性的代码
│   │   ├── components -------------------- 包含抽象出来的通用组件，目前只有keep-alive
│   ├── server ---------------------------- 服务端渲染(server-side rendering)的相关代码
│   ├── platforms ------------------------- 不同平台特有的相关代码
│   │   ├── weex -------------------------- weex平台支持
│   │   ├── web --------------------------- web平台支持
│   │   │   ├── entry-runtime.js ---------------- 运行时构建的入口
│   │   │   ├── entry-runtime-with-compiler.js -- 独立构建版本的入口
│   │   │   ├── entry-compiler.js --------------- vue-template-compiler 包的入口文件
│   │   │   ├── entry-server-renderer.js -------- vue-server-renderer 包的入口文件
│   ├── sfc ------------------------------- 包含单文件组件(.vue文件)的解析逻辑，用于vue-template-compiler包
│   ├── shared ---------------------------- 整个代码库通用的代码
```

几个重要的目录：

- **compiler：** 编译，用来将template转化为render函数
- **core：** Vue的核心代码，包括响应式实现、虚拟DOM、Vue实例方法的挂载、全局方法、抽象出来的通用组件等
- **platform：** 不同平台的入口文件，主要是 web 平台和 weex 平台的，不同平台有其特殊的构建过程，当然我们的重点是 web 平台
- **server：** 服务端渲染(SSR)的相关代码，SSR 主要把组件直接渲染为 HTML 并由 Server 端直接提供给 Client 端
- **sfc：** 主要是 .vue 文件解析的逻辑
- **shared：** 一些通用的工具方法，有一些是为了增加代码可读性而设置的

其中在platform下`src/platforms/web/entry-runtime.js`文件作为运行时构建的入口，ESM方式输出 dist/vue.runtime.esm.js，CJS方式输出 dist/vue.runtime.common.js，UMD方式输出 dist/vue.runtime.js，不包含模板 template 到 render 函数的编译器
`src/platforms/web/entry-runtime-with-compiler.js`文件作为运行时构建的入口，ESM方式输出 dist/vue.esm.js，CJS方式输出 dist/vue.common.js，UMD方式输出 dist/vue.js，包含compiler

## 2. 入口文件

任何前端项目都可以从 `package.json` 文件看起，先来看看它的 `script.dev` 就是我们运行 `npm run dev` 的时候它的命令行：

```bash
"scripts": {
    "dev": "rollup -w -c scripts/config.js --environment TARGET:web-full-dev"
}
```

> 这里的 [rollup](http://www.rollupjs.com/ "http://www.rollupjs.com/") 是一个类似于 webpack 的JS模块打包器，事实上 `Vue - v1.0.10` 版本之前用的还是 webpack ，其后改成了 rollup ，如果想知道为什么换成 rollup ，可以看看 [尤雨溪本人的回答](https://www.zhihu.com/question/37861778 "https://www.zhihu.com/question/37861778")，总的来说就是为了打出来的包体积小一点，初始化速度快一点。

可以看到这里 rollup 去运行 `scripts/config.js` 文件，并且给了个参数 `TARGET:web-full-dev`，那来看看 `scripts/config.js` 里面是啥

```js
// scripts/config.js

const builds = {
  'web-full-dev': {
    entry: resolve('web/entry-runtime-with-compiler.js'),  // 入口文件
    dest: resolve('dist/vue.js'),                          // 输出文件
    format: 'umd',                                         // 参看下面的编译方式说明
    env: 'development',                                    // 环境
    alias: { he: './entity-decoder' },                     // 别名
    banner                                        // 每个包前面的注释-版本/作者/日期.etc
  },
}
```

format 编译方式说明：

- **es：** ES Modules，使用ES6的模板语法输出
- **cjs：** CommonJs Module，遵循CommonJs Module规范的文件输出
- **amd：** AMD Module,遵循AMD Module规范的文件输出
- **umd：** 支持外链规范的文件输出，此文件可以直接使用script标签

这里的 `web-full-dev` 就是对应刚刚我们在命令行里传入的命令，那么 rollup 就会按下面的 entry 入口文件开始去打包，还有其他很多命令和其他各种输出方式和格式可以自行查看一下源码。

因此本文主要的关注点在包含 compiler 编译器的 `src/platforms/web/entry-runtime-with-compiler.js` 文件，在生产和开发环境中我们使用 vue-loader 来进行 template 的编译从而不需要带 compiler 的包，但是为了更好的理解原理和流程还是推介从带 compiler 的入口文件看起。

先看看这个文件，这里导入了个 Vue ，看看它从哪来的

```js
// src/platforms/web/entry-runtime-with-compiler.js

import Vue from './runtime/index'
```

继续看

```js
// src/platforms/web/runtime/index.js

import Vue from 'core/index'
```

keep moving

```js
// src/core/index.js

import Vue from './instance/index'
```

keep moving*2

```js
// src/core/instance/index.js

/* 这里就是vue的构造函数了，不用ES6的Class语法是因为mixin模块划分的方便 */
function Vue(options) {
  this._init(options)         // 初始化方法，位于 initMixin 中
}

// 下面的mixin往Vue.prototype上各种挂载
initMixin(Vue)
stateMixin(Vue)
eventsMixin(Vue)
lifecycleMixin(Vue)
renderMixin(Vue)

export default Vue
```

当我们 `new Vue( )` 的时候，实际上调用的就是这个构造函数，可以从这里开始看了。

## 3. 运行机制

这里我用xmind粗略的画了一张运行机制图，基本上后面的分析都在这张图上面的某些部分了

本文 Vue 实例都是用 `vm` 来表示

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/36a919176cdfc68ab1c0fe4e347e14ecd52e861a3506344f506e7b44283c903b.webp)

上面这个图可以分为多个部分细加阅读，具体的实现我们在后面的文章中详细讨论，这里先贴一部分源码尝尝鲜

### 3.1 初始化 _init( )

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/12e46bff16d3cd0d4d0b31d5d3741ee1ba8316a61ba6a642676e9fed69517893.webp)

当我们在 main.js 里 `new Vue( )` 后，Vue 会调用构造函数的 `_init( )` 方法，这个方法是位于 core/instance/index.js 的 `initMixin( )` 方法中定义的

```js
// src/core/instance/index.js

/* 这里就是Vue的构造函数 */
function Vue(options) {
  this._init(options)              // 初始化方法，位于 initMixin 中
}

// 下面的mixin往Vue.prototype上各种挂载，这是在加载的时候已经挂载好的
initMixin(Vue)                     // 给Vue.prototype添加：_init函数,...
stateMixin(Vue)                    // 给Vue.prototype添加：$data属性, $props属性, $set函数, $delete函数, $watch函数,...
eventsMixin(Vue)                   // 给Vue.prototype添加：$on函数, $once函数, $off函数, $emit函数, $watch方法,...
lifecycleMixin(Vue)                // 给Vue.prototype添加: _update方法, $forceUpdate函数, $destroy函数,...
renderMixin(Vue)                   // 给Vue.prototype添加: $nextTick函数, _render函数,...

export default Vue
```

我们可以看看 `init( )` 这个方法到底进行了哪些初始化：

```js
// src/core/instance/index.js

Vue.prototype._init = function(options?: Object) {
  const vm: Component = this

  initLifecycle(vm)                     // 初始化生命周期 src/core/instance/lifecycle.js
  initEvents(vm)                        // 初始化事件 src/core/instance/events.js
  initRender(vm)                        // 初始化render src/core/instance/render.js
  callHook(vm, 'beforeCreate')          // 调用beforeCreate钩子
  initInjections(vm)                    // 初始化注入值 before data/props src/core/instance/inject.js
  initState(vm)                         // 挂载 data/props/methods/watcher/computed
  initProvide(vm)                       // 初始化Provide after data/props
  callHook(vm, 'created')               // 调用created钩子

  if (vm.$options.el) {                    // $options可以认为是我们传给 `new Vue(options)` 的options
    vm.$mount(vm.$options.el)              // $mount方法
  }
}
```

这里 `_init()` 方法中会对当前 `vm` 实例进行一系列初始化设置，比较重要的是初始化 State 的方法 `initState(vm)` 的时候进行 `data/props` 的响应式化，这就是传说中的通过 `Object.defineProperty()` 方法对需要响应式化的对象设置 `getter/setter`，以此为基础进行依赖搜集(Dependency Collection)，达到数据变化驱动视图变化的目的。

最后检测 `vm.$options` 上面有没有 `el` 属性，如果有的话使用 `vm.$mount` 方法挂载 `vm`，形成数据层和视图层的联系。这也是如果没有提供 `el` 选项就需要自己手动 `vm.$mount('#app')` 的原因。

我们看到 `created` 钩子是在挂载 `$mount` 之前调用的，所以我们在 `created` 钩子触发之前是无法操作 DOM 的，这是因为还没有渲染到 DOM 上。

### 3.2 挂载 $mount( )

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/5953d66c89760b46b14d9704f772963878788c8b8ad71d2f37354a9a23fac0c8.webp)

挂载方法 `vm.$mount( )` 在多个地方有定义，是根据不同打包方式和平台有关的，`src/platform/web/entry-runtime-with-compiler.js`、`src/platform/web/runtime/index.js`、`src/platform/weex/runtime/index.js`，我们的关注点在第一个文件，但在 `entry-runtime-with-compiler.js` 文件中会首先把 `runtime/index.js` 中的 `$mount` 方法保存下来，并在最后用 call 运行：

```js
// src/platform/web/entry-runtime-with-compiler.js

const mount = Vue.prototype.$mount    // 把原来的$mount保存下来，位于 src/platform/web/runtime/index.js
Vue.prototype.$mount = function(
  el?: string | Element,    // 挂载的元素
  hydrating?: boolean       // 服务端渲染相关参数
): Component {
  el = el && query(el)

  const options = this.$options
  if (!options.render) {                // 如果没有定义render方法
    let template = options.template

    // 把获取到的template通过编译的手段转化为render函数
    if (template) {
      const { render, staticRenderFns } = compileToFunctions(template, {...}, this)
      options.render = render
    }
  }
  return mount.call(this, el, hydrating)      // 执行原来的$mount
}
```

在 Vue 2.0 版本中，所有 Vue 的组件的渲染最终都需要 render 方法，无论我们是用单文件 .vue 方式开发组件，还是写了 el 或者 template 属性，最终都会转换成 render 方法。这里的 `compileToFunctions` 就是把 template 编译为 render 的方法，后面会介绍。

```js
// src/platform/weex/runtime/index.js

Vue.prototype.$mount = function (
  el?: string | Element,    // 挂载的元素
  hydrating?: boolean       // 服务端渲染相关参数
): Component {
  el = el && inBrowser ? query(el) : undefined        // query就是document.querySelector方法
  return mountComponent(this, el, hydrating)          // 位于core/instance/lifecycle.js
}
```

这里的 `el` 一开始如果不是DOM元素的话会被 query 方法换成DOM元素再被传给 `mountComponent` 方法，我们继续看 `mountComponent` 的定义：

```js
// src/core/instance/lifecycle.js

export function mountComponent (
  vm: Component,
  el: ?Element,
  hydrating?: boolean
): Component {
  vm.$el = el
  if (!vm.$options.render) {
    vm.$options.render = createEmptyVNode
  }
  callHook(vm, 'beforeMount')            // 调用beforeMount钩子

  // 渲染watcher，当数据更改，updateComponent作为Watcher对象的getter函数，用来依赖收集，并渲染视图
  let updateComponent
  updateComponent = () => {
    vm._update(vm._render(), hydrating)
  }

  // 渲染watcher, Watcher 在这里起到两个作用，一个是初始化的时候会执行回调函数
  // ，另一个是当 vm 实例中的监测的数据发生变化的时候执行回调函数
  new Watcher(vm, updateComponent, noop, {
    before () {
      if (vm._isMounted) {
        callHook(vm, 'beforeUpdate')            // 调用beforeUpdate钩子
      }
    }
  }, true /* isRenderWatcher */)

  // 这里注意 vm.$vnode 表示 Vue 实例的父虚拟 Node，所以它为 Null 则表示当前是根 Vue 的实例
  if (vm.$vnode == null) {
    vm._isMounted = true               // 表示这个实例已经挂载
    callHook(vm, 'mounted')            // 调用mounted钩子
  }
  return vm
}
```

在 `mountComponent` 方法里实例化了一个渲染 `Watcher`，并且传入了一个 `updateComponent` ，这个方法：`() => { vm._update(vm._render(), hydrating) }` 首先使用 `_render` 方法生成 `VNode`，再调用 `_update` 方法更新DOM。可以看看视图更新部分的介绍

这里调用了几个钩子，他们的时机可以关注一下。

### 3.3 编译 compile( )

如果在需要转换 render 的场景下，比如我们写的 template ，将会被 compiler 转换为 render 函数，这其中会有几个步骤组成：

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/c5bb408e11d76e02c60ebe78269bdd70bb2d7f25d7a5b1b0ca4b82961b26ab4e.webp)

入口位于刚刚 src/platform/web/entry-runtime-with-compiler.js 的 `compileToFunctions` 方法：

```js
// src/platforms/web/compiler/index.js

const { compile, compileToFunctions } = createCompiler(baseOptions)
export { compile, compileToFunctions }
```

继续看这里的 `createCompiler` 方法：

```js
// src/compiler/index.js

export const createCompiler = createCompilerCreator(function baseCompile (
  template: string,
  options: CompilerOptions
): CompiledResult {
  const ast = parse(template.trim(), options)
  if (options.optimize !== false) {
    optimize(ast, options)
  }
  const code = generate(ast, options)
  return {
    ast,
    render: code.render,
    staticRenderFns: code.staticRenderFns
  }
})
```

这里可以看到有三个重要的过程 `parse`、`optimize`、`generate`，之后生成了 render 方法代码。

- `parse`：会用正则等方式解析 template 模板中的指令、class、style等数据，形成抽象语法树 AST
- `optimize`：优化AST，生成模板AST树，检测不需要进行DOM改变的静态子树，减少 patch 的压力
- `generate`：把 AST 生成 render 方法的代码

### 3.4 响应式化 observe( )

Vue作为一个MVVM框架，我们知道它的 Model 层和 View 层之间的桥梁 ViewModel 是做到数据驱动的关键，Vue的响应式是通过 [Object.defineProperty](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty") 来实现，给被响应式化的对象设置 `getter/setter` ，当 render 函数被渲染的时候会触发读取响应式化对象的 `getter` 进行**依赖收集**，而在修改响应式化对象的时候会触发设置 `setter`，`setter` 方法会 `notify` 它之前收集到的每一个 `watcher` 来告诉他们自己的值更新了，从而触发 `watcher` 的 `update` 去 `patch` 更新视图。

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/2762e9b6d7eb704fac1995b355d8102bbe18f988ea5a175cdd2a846a201088d9.webp)

响应式化的入口位于 src/core/instance/init.js 的 `initState` 中：

```js
// src/core/instance/state.js

export function initState(vm: Component) {
  vm._watchers = []
  const opts = vm.$options
  if (opts.props) initProps(vm, opts.props)
  if (opts.methods) initMethods(vm, opts.methods)
  if (opts.data) {
    initData(vm)
  } else {
    observe(vm._data = {}, true /* asRootData */)
  }
  if (opts.computed) initComputed(vm, opts.computed)
  if (opts.watch && opts.watch !== nativeWatch) {
    initWatch(vm, opts.watch)
  }
}
```

它非常规律的定义了几个方法来初始化 `props`、`methods`、`data`、`computed`、`wathcer`，这里只看 `initData` 方法，来窥一豹

```js
// src/core/instance/state.js

function initData(vm: Component) {
  let data = vm.$options.data
  data = vm._data = typeof data === 'function'
                    ? getData(data, vm)
                    : data || {}

  observe(data, true /* asRootData */) // 给data做响应式处理
}
```

首先判断了下 data 是不是函数，是则取返回值不是则取自身，之后有一个 `observe` 方法对 `data` 进行处理，看看这个方法

```js
// src/core/observer/index.js

export function observe (value: any, asRootData: ?boolean): Observer | void {
  let ob: Observer | void
  ob = new Observer(value)
  return ob
}
```

这个方法主要用 `data` 去实例化一个 Observer 对象实例，Observer 是一个 Class，Observer 的构造函数使用 `defineReactive` 方法给对象的键响应式化，它给对象的属性递归添加 `getter/setter`，用于依赖收集和 notify 更新，这个方法大概是这样的

```js
// src/core/observer/index.js

function defineReactive (obj, key, val) {
    Object.defineProperty(obj, key, {
        enumerable: true,
        configurable: true,
        get: function reactiveGetter () {
            /* 进行依赖收集 */
            return val;
        },
        set: function reactiveSetter (newVal) {
            if (newVal === val) return;
            notify();                // 触发更新
        }
    });
}
```

### 3.5 视图更新 patch( )

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/b0a4cfbb17057a43597311200195f4991a0c407aa19aa554c5215dc1471f6119.webp)

当使用 `defineReactive` 方法将对象响应式化后，当 render 函数被渲染的时候，会读取响应化对象的 `getter` 从而触发 `getter` 进行 `watcher` 依赖的收集，而在修改响应化对象的值的时候，会触发 `setter` 通知 `notify` 之前收集的依赖，通知自己已被修改，请按需重新渲染视图。被通知的 `watcher` 调用 `update` 方法去更新视图，位于上面介绍过的传递给 `new Watcher( )` 的 `updateComponent` 方法中，这个方法会调用 `update` 方法去 `patch` 更新视图。

```js
// src/core/instance/lifecycle.js

let updateComponent
updateComponent = () => {
  vm._update(vm._render(), hydrating)
}

// 渲染watcher, Watcher 在这里起到两个作用，一个是初始化的时候会执行回调函数
// ，另一个是当 vm 实例中的监测的数据发生变化的时候执行回调函数
new Watcher(vm, updateComponent, noop, {...}, true /* isRenderWatcher */)
```

这个 `_render` 方法生成虚拟 Node， `_update` 方法中的会将新的 VNode 与旧的 VNode 一起传入 `patch`

```js
// src/core/instance/lifecycle.js

Vue.prototype._update = function(vnode: VNode, hydrating?: boolean) { // 调用此方法去更新视图
  const vm: Component = this
  const prevVnode = vm._vnode
  vm._vnode = vnode

  if (!prevVnode) {
    // 初始化
    vm.$el = vm.__patch__(vm.$el, vnode, hydrating, false /* removeOnly */)
  } else {
    //更新
    vm.$el = vm.__patch__(prevVnode, vnode)
  }
}
```

`_update` 调用 `__patch__` 方法，它主要是对新老 VNode 进行比较 `patchVnode`，经过 diff 算法得出它们的差异直接，最后这些差异的对应 DOM 进行更新。

到这里基本上一个主要的流程就介绍完了，我们大概了解了一个 Vue 从一个构造函数的实例化开始是如何运转的，后面会展开来讨论一下各个部分的内容，在下才疏学浅，未免纰漏，欢迎大家讨论~

---

**本文是系列文章，随后会更新后面的部分，共同进步~**

> 1. [Vue源码阅读 - 文件结构与运行机制](https://github.com/SHERlocked93/blog/blob/master/Docs/Vue%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%20-%20%E6%96%87%E4%BB%B6%E7%BB%93%E6%9E%84%E4%B8%8E%E8%BF%90%E8%A1%8C%E6%9C%BA%E5%88%B6.md "https://github.com/SHERlocked93/blog/blob/master/Docs/Vue%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%20-%20%E6%96%87%E4%BB%B6%E7%BB%93%E6%9E%84%E4%B8%8E%E8%BF%90%E8%A1%8C%E6%9C%BA%E5%88%B6.md")
> 2. [Vue源码阅读 - 依赖收集原理](https://github.com/SHERlocked93/blog/blob/master/Docs/Vue%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%20-%20%E4%BE%9D%E8%B5%96%E6%94%B6%E9%9B%86%E5%8E%9F%E7%90%86.md "https://github.com/SHERlocked93/blog/blob/master/Docs/Vue%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%20-%20%E4%BE%9D%E8%B5%96%E6%94%B6%E9%9B%86%E5%8E%9F%E7%90%86.md")
> 3. [Vue源码阅读 - 批量异步更新与nextTick原理](https://github.com/SHERlocked93/blog/blob/master/Docs/Vue%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%20-%20%E6%89%B9%E9%87%8F%E5%BC%82%E6%AD%A5%E6%9B%B4%E6%96%B0%E4%B8%8EnextTick.md "https://github.com/SHERlocked93/blog/blob/master/Docs/Vue%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%20-%20%E6%89%B9%E9%87%8F%E5%BC%82%E6%AD%A5%E6%9B%B4%E6%96%B0%E4%B8%8EnextTick.md")

> 参考：
>
> 1. [Vue2.1.7源码学习](http://hcysun.me/2017/03/03/Vue%E6%BA%90%E7%A0%81%E5%AD%A6%E4%B9%A0/ "http://hcysun.me/2017/03/03/Vue%E6%BA%90%E7%A0%81%E5%AD%A6%E4%B9%A0/")
> 2. [Vue.js 技术揭秘](https://ustbhuangyi.github.io/vue-analysis "https://ustbhuangyi.github.io/vue-analysis")
> 3. [剖析 Vue.js 内部运行机制](https://juejin.im/book/6844733705089449991/ "https://juejin.im/book/6844733705089449991/")
> 4. [Vue.js 文档](https://cn.vuejs.org/ "https://cn.vuejs.org/")
> 5. [【大型干货】手拉手带你过一遍vue部分源码](https://juejin.im/post/6844903598258651144 "https://juejin.im/post/6844903598258651144")
> 6. [MDN - Object.defineProperty()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty")
