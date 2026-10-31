# Vue源码阅读 - 依赖收集原理

vue已是目前国内前端web端三分天下之一，同时也作为本人主要技术栈之一，在日常使用中知其然也好奇着所以然，另外最近的社区涌现了一大票vue源码阅读类的文章，在下借这个机会从大家的文章和讨论中汲取了一些营养，同时对一些阅读源码时的想法进行总结，出产一些文章，作为自己思考的输出，本人水平有限，欢迎留言讨论~

目标Vue版本：`2.5.17-beta.0`

vue源码注释：[github.com/SHERlocked9…](https://github.com/SHERlocked93/vue-analysis "https://github.com/SHERlocked93/vue-analysis")

声明：文章中源码的语法都使用 Flow，并且源码根据需要都有删节(为了不被迷糊 @_@)，如果要看完整版的请进入上面的[github地址](https://github.com/SHERlocked93/vue-analysis "https://github.com/SHERlocked93/vue-analysis")，本文是系列文章，文章地址见底部~

感兴趣的同学可以加文末的微信群，一起讨论吧～

## 1. 响应式系统

通过官网的介绍我们知道 Vue.js 是一个MVVM框架，它并不关心视图变化，而通过数据驱动视图更新，这让我们的状态管理非常简单，而这是怎么实现的呢。盗用官网一张图

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/b970721efe20cc875fcc3fe96575a5cb55156730749e235859908cfcb552290c.webp)

每个组件实例都有相应的 `Watcher` 实例对象，它会在组件渲染的过程中把属性记录为依赖，之后当依赖项的 `setter` 被调用时，会通知 `watcher` 重新计算，从而致使它关联的组件得以更新。

这里有三个重要的概念 `Observe`、`Dep`、`Watcher`，分别位于`src/core/observer/index.js`、`src/core/observer/dep.js`、`src/core/observer/watcher.js`

- `Observe` 类主要给响应式对象的属性添加 `getter/setter` 用于依赖收集与派发更新
- `Dep` 类用于收集当前响应式对象的依赖关系
- `Watcher` 类是观察者，实例分为渲染 watcher、计算属性 watcher、侦听器 watcher三种

## 2. 代码实现

### 2.1 initState

响应式化的入口位于 src/core/instance/init.js 的 `initState` 中：

```js
// src/core/instance/state.js

export function initState(vm: Component) {
  const opts = vm.$options
  if (opts.props) initProps(vm, opts.props)              // 初始化props
  if (opts.methods) initMethods(vm, opts.methods)        // 初始化methods
  if (opts.data) initData(vm)                            // 初始化data
  if (opts.computed) initComputed(vm, opts.computed)     // 初始化computed
  if (opts.watch) initWatch(vm, opts.watch)              // 初始化watch
  }
}
```

它非常规律的定义了几个方法来初始化 `props`、`methods`、`data`、`computed`、`wathcer`，这里看一下 `initData` 方法，来窥一豹

```js
// src/core/instance/state.js

function initData(vm: Component) {
  let data = vm.$options.data
  data = vm._data = typeof data === 'function'
                    ? getData(data, vm)
                    : data || {}
  observe(data, true /* asRootData */)             // 给data做响应式处理
}
```

首先判断了下 data 是不是函数，是则取返回值不是则取自身，之后有一个 `observe` 方法对 `data` 进行处理，这个方法尝试给创建一个Observer实例 `__ob__`，如果成功创建则返回新的Observer实例，如果已有Observer实例则返回现有的Observer实例

### 2.2 Observer/defineReactive

```js
// src/core/observer/index.js

export function observe (value: any, asRootData: ?boolean): Observer | void {
  let ob: Observer | void
  ob = new Observer(value)
  return ob
}
```

这个方法主要用 `data` 作为参数去实例化一个 Observer 对象实例，Observer 是一个 Class，用于依赖收集和 `notify` 更新，Observer 的构造函数使用 `defineReactive` 方法给对象的键响应式化，给对象的属性递归添加 `getter/setter` ，当data被取值的时候触发 `getter` 并搜集依赖，当被修改值的时候先触发 `getter` 再触发 `setter` 并派发更新

```js
// src/core/observer/index.js

export class Observer {
  value: any;
  dep: Dep;

  constructor (value: any) {
    value: any;
    this.dep = new Dep()
    def(value, '__ob__', this)    // def方法保证不可枚举
    this.walk(value)
  }

  // 遍历对象的每一个属性并将它们转换为getter/setter
  walk (obj: Object) {
    const keys = Object.keys(obj)
    for (let i = 0; i < keys.length; i++) { // 把所有可遍历的对象响应式化
      defineReactive(obj, keys[i])
    }
  }
}

export function defineReactive ( obj: Object, key: string, val: any, customSetter?: ?Function, shallow?: boolean) {
  const dep = new Dep()         // 在每个响应式键值的闭包中定义一个dep对象

  // 如果之前该对象已经预设了getter/setter则将其缓存，新定义的getter/setter中会将其执行
  const getter = property && property.get
  const setter = property && property.set

  let childOb = !shallow && observe(val)
  Object.defineProperty(obj, key, {
    enumerable: true,
    configurable: true,
    get: function reactiveGetter () {
      const value = getter ? getter.call(obj) : val         // 如果原本对象拥有getter方法则执行
      if (Dep.target) {                    // 如果当前有watcher在读取当前值
        dep.depend()                       // 那么进行依赖收集，dep.addSub
      }
      return value
    },
    set: function reactiveSetter (newVal) {
      const value = getter ? getter.call(obj) : val    // 先getter
      if (newVal === value || (newVal !== newVal && value !== value)) {   // 如果跟原来值一样则不管
        return
      }
      if (setter) { setter.call(obj, newVal) }         // 如果原本对象拥有setter方法则执行
      else { val = newVal }
      dep.notify()                                     // 如果发生变更，则通知更新，调用watcher.update()
    }
  })
}
```

`getter` 的时候进行依赖的收集，注意这里，只有在 `Dep.target` 中有值的时候才会进行依赖收集，这个 `Dep.target` 是在Watcher实例的 `get` 方法调用的时候 `pushTarget` 会把当前取值的watcher推入 `Dep.target`，原先的watcher压栈到 `targetStack` 栈中，当前取值的watcher取值结束后出栈并把原先的watcher值赋给 `Dep.target`，`cleanupDeps` 最后把新的 `newDeps` 里已经没有的watcher清空，以防止视图上已经不需要的无用watcher触发

`setter` 的时候首先 `getter`，并且比对旧值没有变化则return，如果发生变更，则dep通知所有subs中存放的依赖本数据的Watcher实例 `update` 进行更新，这里 `update` 中会 `queueWatcher( )` 异步推送到调度者观察者队列 `queue` 中，在nextTick时 `flushSchedulerQueue( )` 把队列中的watcher取出来执行 `watcher.run` 且执行相关钩子函数

### 2.3 Dep

上面多次提到了一个关键词 `Dep`，他是依赖收集的容器，或者称为**依赖搜集器**，他记录了哪些Watcher依赖自己的变化，或者说，哪些Watcher订阅了自己的变化；这里引用一个网友的发言：

> @liuhongyi0101 ：简单点说就是引用计数 ，谁借了我的钱，我就把那个人记下来，以后我的钱少了 我就通知他们说我没钱了

而把借钱的人记下来的小本本就是这里 `Dep` 实例里的subs

```js
// src/core/observer/dep.js

let uid = 0            // Dep实例的id，为了方便去重

export default class Dep {
  static target: ?Watcher           // 当前是谁在进行依赖的收集
  id: number
  subs: Array<Watcher>              // 观察者集合

  constructor() {
    this.id = uid++                             // Dep实例的id，为了方便去重
    this.subs = []                              // 存储收集器中需要通知的Watcher
  }

  addSub(sub: Watcher) { ... }  /* 添加一个观察者对象 */
  removeSub(sub: Watcher) { ... }  /* 移除一个观察者对象 */
  depend() { ... }  /* 依赖收集，当存在Dep.target的时候把自己添加观察者的依赖中 */
  notify() { ... }  /* 通知所有订阅者 */
}

const targetStack = []           // watcher栈

export function pushTarget(_target: ?Watcher) { ... }  /* 将watcher观察者实例设置给Dep.target，用以依赖收集。同时将该实例存入target栈中 */
export function popTarget() { ... }  /* 将观察者实例从target栈中取出并设置给Dep.target */
```

这里 `Dep` 的实例中的 `subs` 搜集的依赖就是 watcher 了，它是 `Watcher` 的实例，将来用来通知更新

### 2.4 Watcher

```js
// src/core/observer/watcher.js

/* 一个解析表达式，进行依赖收集的观察者，同时在表达式数据变更时触发回调函数。它被用于$watch api以及指令 */
export default class Watcher {
  constructor(
    vm: Component,
    expOrFn: string | Function,
    cb: Function,
    options?: ?Object,
    isRenderWatcher?: boolean      // 是否是渲染watcher的标志位
  ) {
    this.getter = expOrFn                // 在get方法中执行
    if (this.computed) {                   // 是否是 计算属性
      this.value = undefined
      this.dep = new Dep()                 // 计算属性创建过程中并未求值
    } else {                               // 不是计算属性会立刻求值
      this.value = this.get()
    }
  }

  /* 获得getter的值并且重新进行依赖收集 */
  get() {
    pushTarget(this)                // 设置Dep.target = this
    let value
    value = this.getter.call(vm, vm)
    popTarget()                      // 将观察者实例从target栈中取出并设置给Dep.target
    this.cleanupDeps()
    return value
  }

  addDep(dep: Dep) { ... }  /* 添加一个依赖关系到Deps集合中 */
  cleanupDeps() { ... }  /* 清理newDeps里没有的无用watcher依赖 */
  update() { ... }  /* 调度者接口，当依赖发生改变的时候进行回调 */
  run() { ... }  /* 调度者工作接口，将被调度者回调 */
  getAndInvoke(cb: Function) { ... }
  evaluate() { ... }  /* 收集该watcher的所有deps依赖 */
  depend() { ... }  /* 收集该watcher的所有deps依赖，只有计算属性使用 */
  teardown() { ... }  /* 将自身从所有依赖收集订阅列表删除 */
}
```

`get` 方法中执行的 `getter` 就是在一开始new渲染watcher时传入的 `updateComponent = () => { vm._update(vm._render(), hydrating) }`，这个方法首先 `vm._render()` 生成渲染VNode树，在这个过程中完成对当前Vue实例 `vm` 上的数据访问，触发相应一众响应式对象的 `getter`，然后 `vm._update()` 去 `patch`

注意这里的 `get` 方法最后执行了 `getAndInvoke`，这个方法首先遍历watcher中存的 `deps`，移除 `newDep` 中已经没有的订阅，然后 `depIds = newDepIds; deps = newDeps` ，把 `newDepIds` 和 `newDeps` 清空。每次添加完新的订阅后移除旧的已经不需要的订阅，这样在某些情况，比如 `v-if` 已不需要的模板依赖的数据发生变化时就不会通知watcher去 `update` 了

### 2.5 小结

整个收集的流程大约是这样的，可以对照着上面的流程看一下

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/720df875a7bce00815f3c1db8d852445bfbfe0bec79cc97ac9fe52023463f1da.webp)

watcher 有下面几种使用场景：

- `render watcher` 渲染 watcher，渲染视图用的 watcher
- `computed watcher` 计算属性 watcher，因为计算属性即依赖别人也被人依赖，因此也会持有一个 `Dep` 实例
- `watch watcher` 侦听器 watcher

只要会被别的观察者 (`watchers`) 依赖，比如data、data的属性、计算属性、props，就会在闭包里生成一个 Dep 的实例 `dep` 并在被调用 `getter` 的时候 `dep.depend` 收集它被谁依赖了，并把被依赖的watcher存放到自己的subs中 `this.subs.push(sub)`，以便在自身改变的时候通知 `notify` 存放在 `dep.subs` 数组中依赖自己的 `watchers` 自己改变了，请及时 `update` ~

只要依赖别的响应式化对象的对象，都会生成一个观察者 `watcher` ，用来统计这个 `watcher` 依赖了哪些响应式对象，在这个 `watcher` 求值前把当前 `watcher` 设置到全局 `Dep.target`，并在自己依赖的响应式对象发生改变的时候及时 `update`

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
> 7. [Vue.js源码学习一 —— 数据选项 State 学习](https://segmentfault.com/a/1190000013579636 "https://segmentfault.com/a/1190000013579636")
