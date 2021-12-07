# Vue源码阅读 - 批量异步更新与nextTick原理

[TOC]

 

vue已是目前国内前端web端三分天下之一，同时也作为本人主要技术栈之一，在日常使用中知其然也好奇着所以然，另外最近的社区涌现了一大票vue源码阅读类的文章，在下借这个机会从大家的文章和讨论中汲取了一些营养，同时对一些阅读源码时的想法进行总结，出产一些文章，作为自己思考的总结，本人水平有限，欢迎留言讨论~

目标Vue版本：`2.5.17-beta.0`

vue源码注释：[https://github.com/SHERlocked93/vue-analysis](https://github.com/SHERlocked93/vue-analysis)

声明：文章中源码的语法都使用 Flow，并且源码根据需要都有删节(为了不被迷糊 @_@)，如果要看完整版的请进入上面的[github地址](https://github.com/SHERlocked93/vue-analysis)，本文是系列文章，文章地址见底部~



## 1. 异步更新 

[上一篇文章](https://juejin.im/post/5b38830de51d455888216675)我们在依赖收集原理的响应式化方法 `defineReactive` 中的 `setter` 访问器中有派发更新 `dep.notify()` 方法，这个方法会挨个通知在 `dep` 的 `subs` 中收集的订阅自己变动的watchers执行update。一起来看看 `update` 方法的实现：

```js
// src/core/observer/watcher.js

/* Subscriber接口，当依赖发生改变的时候进行回调 */
update() {
  if (this.computed) {
    // 一个computed watcher有两种模式：activated lazy(默认)
    // 只有当它被至少一个订阅者依赖时才置activated，这通常是另一个计算属性或组件的render function
    if (this.dep.subs.length === 0) {       // 如果没人订阅这个计算属性的变化
      // lazy时，我们希望它只在必要时执行计算，所以我们只是简单地将观察者标记为dirty
      // 当计算属性被访问时，实际的计算在this.evaluate()中执行
      this.dirty = true
    } else {
      // activated模式下，我们希望主动执行计算，但只有当值确实发生变化时才通知我们的订阅者
      this.getAndInvoke(() => {
        this.dep.notify()     // 通知渲染watcher重新渲染，通知依赖自己的所有watcher执行update
      })
    }
  } else if (this.sync) {	  // 同步
    this.run()
  } else {
    queueWatcher(this)        // 异步推送到调度者观察者队列中，下一个tick时调用
  }
}
```

如果不是 `computed watcher` 也非 `sync` 会把调用update的当前watcher推送到调度者队列中，下一个tick时调用，看看 `queueWatcher` ：

```js
// src/core/observer/scheduler.js

/* 将一个观察者对象push进观察者队列，在队列中已经存在相同的id则
 * 该watcher将被跳过，除非它是在队列正被flush时推送
 */
export function queueWatcher (watcher: Watcher) {
  const id = watcher.id
  if (has[id] == null) {     // 检验id是否存在，已经存在则直接跳过，不存在则标记哈希表has，用于下次检验
    has[id] = true
    queue.push(watcher)      // 如果没有正在flush，直接push到队列中
    if (!waiting) {          // 标记是否已传给nextTick
      waiting = true
      nextTick(flushSchedulerQueue)
    }
  }
}

/* 重置调度者状态 */
function resetSchedulerState () {
  queue.length = 0
  has = {}
  waiting = false
}
```

这里使用了一个 `has` 的哈希map用来检查是否当前watcher的id是否存在，若已存在则跳过，不存在则就push到 `queue` 队列中并标记哈希表has，用于下次检验，防止重复添加。这就是一个去重的过程，比每次查重都要去queue中找要文明，在渲染的时候就不会重复 `patch` 相同watcher的变化，这样就算同步修改了一百次视图中用到的data，异步 `patch` 的时候也只会更新最后一次修改。

这里的 `waiting` 方法是用来标记 `flushSchedulerQueue` 是否已经传递给 `nextTick` 的标记位，如果已经传递则只push到队列中不传递 `flushSchedulerQueue` 给 `nextTick`，等到 `resetSchedulerState` 重置调度者状态的时候 `waiting` 会被置回 `false` 允许 `flushSchedulerQueue` 被传递给下一个tick的回调，总之保证了 `flushSchedulerQueue` 回调在一个tick内只允许被传入一次。来看看被传递给 `nextTick` 的回调 `flushSchedulerQueue` 做了什么：

```js
// src/core/observer/scheduler.js

/* nextTick的回调函数，在下一个tick时flush掉两个队列同时运行watchers */
function flushSchedulerQueue () {
  flushing = true
  let watcher, id

  queue.sort((a, b) => a.id - b.id)					// 排序

  for (index = 0; index < queue.length; index++) {	 // 不要将length进行缓存
    watcher = queue[index]
    if (watcher.before) {         // 如果watcher有before则执行
      watcher.before()
    }
    id = watcher.id
    has[id] = null                // 将has的标记删除
    watcher.run()                 // 执行watcher
    if (process.env.NODE_ENV !== 'production' && has[id] != null) {  // 在dev环境下检查是否进入死循环
      circular[id] = (circular[id] || 0) + 1     // 比如user watcher订阅自己的情况
      if (circular[id] > MAX_UPDATE_COUNT) {     // 持续执行了一百次watch代表可能存在死循环
        warn()								  // 进入死循环的警告
        break
      }
    }
  }
  resetSchedulerState()           // 重置调度者状态
  callActivatedHooks()            // 使子组件状态都置成active同时调用activated钩子
  callUpdatedHooks()              // 调用updated钩子
}
```

在 `nextTick` 方法中执行 `flushSchedulerQueue` 方法，这个方法挨个执行 `queue` 中的watcher的 `run` 方法。我们看到在首先有个 `queue.sort()` 方法把队列中的watcher按id从小到大排了个序，这样做可以保证：

1. 组件更新的顺序是从父组件到子组件的顺序，因为父组件总是比子组件先创建。
2. 一个组件的user watchers(侦听器watcher)比render watcher先运行，因为user watchers往往比render watcher更早创建
3. 如果一个组件在父组件watcher运行期间被销毁，它的watcher执行将被跳过

在挨个执行队列中的for循环中，`index < queue.length` 这里没有将length进行缓存，因为在执行处理现有watcher对象期间，更多的watcher对象可能会被push进queue。

那么数据的修改从model层反映到view的过程：`数据更改 -> setter -> Dep -> Watcher -> nextTick -> patch -> 更新视图`

## 2. nextTick原理

### 2.1 宏任务/微任务

这里就来看看包含着每个watcher执行的方法被作为回调传入 `nextTick` 之后，`nextTick` 对这个方法做了什么。不过首先要了解一下浏览器中的 `EventLoop`、`macro task`、`micro task`几个概念，不了解可以参考一下 [JS与Node.js中的事件循环](https://segmentfault.com/a/1190000012362096#articleHeader6) 这篇文章，这里就用一张图来表明一下后两者在主线程中的执行关系：

![clipboard.png](https://segmentfault.com/img/bV3EIf?w=547&h=261) 

解释一下，当主线程执行完同步任务后：

1. 引擎首先从macrotask queue中取出第一个任务，执行完毕后，将microtask queue中的所有任务取出，按顺序全部执行；
2. 然后再从macrotask queue中取下一个，执行完毕后，再次将microtask queue中的全部取出；
3. 循环往复，直到两个queue中的任务都取完。

浏览器环境中常见的异步任务种类，按照优先级：

- `macro task` ：同步代码、`setImmediate`、`MessageChannel`、`setTimeout/setInterval`
- `micro task`：`Promise.then`、`MutationObserver`

有的文章把 `micro task` 叫微任务，`macro task` 叫宏任务，因为这两个单词拼写太像了 -。- ，所以后面的注释多用中文表示~

先来看看源码中对 `micro task ` 与 `macro task` 的实现： `macroTimerFunc`、`microTimerFunc`

```js
// src/core/util/next-tick.js

const callbacks = []     // 存放异步执行的回调
let pending = false      // 一个标记位，如果已经有timerFunc被推送到任务队列中去则不需要重复推送

/* 挨个同步执行callbacks中回调 */
function flushCallbacks() {
  pending = false
  const copies = callbacks.slice(0)
  callbacks.length = 0
  for (let i = 0; i < copies.length; i++) {
    copies[i]()
  }
}

let microTimerFunc        // 微任务执行方法
let macroTimerFunc        // 宏任务执行方法
let useMacroTask = false  // 是否强制为宏任务，默认使用微任务

// 宏任务
if (typeof setImmediate !== 'undefined' && isNative(setImmediate)) {
  macroTimerFunc = () => {
    setImmediate(flushCallbacks)
  }
} else if (typeof MessageChannel !== 'undefined' && (
  isNative(MessageChannel) ||
  MessageChannel.toString() === '[object MessageChannelConstructor]'  // PhantomJS
)) {
  const channel = new MessageChannel()
  const port = channel.port2
  channel.port1.onmessage = flushCallbacks
  macroTimerFunc = () => {
    port.postMessage(1)
  }
} else {
  macroTimerFunc = () => {
    setTimeout(flushCallbacks, 0)
  }
}

// 微任务
if (typeof Promise !== 'undefined' && isNative(Promise)) {
  const p = Promise.resolve()
  microTimerFunc = () => {
    p.then(flushCallbacks)
  }
} else {
  microTimerFunc = macroTimerFunc      // fallback to macro
}
```

`flushCallbacks` 这个方法就是挨个同步的去执行callbacks中的回调函数们，callbacks中的回调函数是在调用 `nextTick` 的时候添加进去的；那么怎么去使用 `micro task` 与 `macro task` 去执行 `flushCallbacks` 呢，这里他们的实现 `macroTimerFunc`、`microTimerFunc` 使用浏览器中宏任务/微任务的API对`flushCallbacks` 方法进行了一层包装。比如宏任务方法 `macroTimerFunc=()=>{ setImmediate(flushCallbacks) }`，这样在触发宏任务执行的时候 `macroTimerFunc()` 就可以在浏览器中的下一个宏任务loop的时候消费这些保存在callbacks数组中的回调了，微任务同理。同时也可以看出传给 `nextTick` 的异步回调函数是被压成了一个同步任务在一个tick执行完的，而不是开启多个异步任务。

注意这里有个比较难理解的地方，第一次调用 `nextTick` 的时候 `pending` 为false，此时已经push到浏览器event loop中一个宏任务或微任务的task，如果在没有flush掉的情况下继续往callbacks里面添加，那么在执行这个占位queue的时候会执行之后添加的回调，所以 `macroTimerFunc`、`microTimerFunc` 相当于task queue的占位，以后 `pending` 为true则继续往占位queue里面添加，event loop轮到这个task queue的时候将一并执行。执行 `flushCallbacks` 时 `pending` 置false，允许下一轮执行 `nextTick` 时往event loop占位。

可以看到上面 `macroTimerFunc` 与 `microTimerFunc` 进行了在不同浏览器兼容性下的平稳退化，或者说**降级策略**：

1. `macroTimerFunc` ：`setImmediate -> MessageChannel -> setTimeout `。首先检测是否原生支持 `setImmediate `，这个方法只在 IE、Edge 浏览器中原生实现，然后检测是否支持 [MessageChannel](https://developer.mozilla.org/zh-CN/docs/Web/API/MessageChannel)，如果对 `MessageChannel` 不了解可以参考一下[这篇文章](https://zhuanlan.zhihu.com/p/37589777)，还不支持的话最后使用 `setTimeout `；
   为什么优先使用 `setImmediate ` 与 `MessageChannel` 而不直接使用 `setTimeout ` 呢，是因为HTML5规定[setTimeout执行的最小延时为4ms](https://developer.mozilla.org/zh-CN/docs/Web/API/Window/setTimeout)，而嵌套的timeout表现为10ms，为了尽可能快的让回调执行，没有最小延时限制的前两者显然要优于 `setTimeout`。
2. `microTimerFunc`：`Promise.then -> macroTimerFunc` 。首先检查是否支持 `Promise`，如果支持的话通过 `Promise.then` 来调用 `flushCallbacks` 方法，否则退化为 `macroTimerFunc` ；
   vue2.5之后 `nextTick` 中因为兼容性原因删除了微任务平稳退化的 `MutationObserver` 的方式。

### 2.2 nextTick实现

最后来看看我们平常用到的 `nextTick` 方法到底是如何实现的：

```js
// src/core/util/next-tick.js

export function nextTick(cb?: Function, ctx?: Object) {
  let _resolve
  callbacks.push(() => {
    if (cb) {
      try {
        cb.call(ctx)
      } catch (e) {
        handleError(e, ctx, 'nextTick')
      }
    } else if (_resolve) {
      _resolve(ctx)
    }
  })
  if (!pending) {
    pending = true
    if (useMacroTask) {
      macroTimerFunc()
    } else {
      microTimerFunc()
    }
  }
  if (!cb && typeof Promise !== 'undefined') {
    return new Promise(resolve => {
      _resolve = resolve
    })
  }
}

/* 强制使用macrotask的方法 */
export function withMacroTask(fn: Function): Function {
  return fn._withTask || (fn._withTask = function() {
    useMacroTask = true
    const res = fn.apply(null, arguments)
    useMacroTask = false
    return res
  })
}
```

 `nextTick` 在这里分为三个部分，我们一起来看一下；

1. 首先 `nextTick` 把传入的 `cb` 回调函数用 `try-catch` 包裹后放在一个匿名函数中推入callbacks数组中，这么做是因为防止单个 `cb` 如果执行错误不至于让整个JS线程挂掉，每个 `cb` 都包裹是防止这些回调函数如果执行错误不会相互影响，比如前一个抛错了后一个仍然可以执行。
2. 然后检查 `pending` 状态，这个跟之前介绍的 `queueWatcher` 中的 `waiting` 是一个意思，它是一个标记位，一开始是 `false` 在进入 `macroTimerFunc`、`microTimerFunc` 方法前被置为 `true`，因此下次调用 `nextTick` 就不会进入 `macroTimerFunc`、`microTimerFunc` 方法，这两个方法中会在下一个 `macro/micro tick` 时候 `flushCallbacks` 异步的去执行callbacks队列中收集的任务，而 `flushCallbacks` 方法在执行一开始会把 `pending` 置 `false`，因此下一次调用 `nextTick` 时候又能开启新一轮的 `macroTimerFunc`、`microTimerFunc`，这样就形成了vue中的 `event loop`。
3. 最后检查是否传入了 `cb`，因为 `nextTick` 还支持Promise化的调用：`nextTick().then(() => {})`，所以如果没有传入 `cb` 就直接return了一个Promise实例，并且把resolve传递给_resolve，这样后者执行的时候就跳到我们调用的时候传递进 `then` 的方法中。

Vue源码中 `next-tick.js` 文件还有一段重要的[注释](https://github.com/vuejs/vue/blob/48acf71a01e5665f72696d44aa5a8d8f1d137172/src/core/util/next-tick.js#L20)，这里就翻译一下：

> 在vue2.5之前的版本中，nextTick基本上基于 `micro task` 来实现的，但是在某些情况下 `micro task` 具有太高的优先级，并且可能在连续顺序事件之间（例如[＃4521](https://github.com/vuejs/vue/issues/4521)，[＃6690](https://github.com/vuejs/vue/issues/6690)）或者甚至在同一事件的事件冒泡过程中之间触发（[＃6566](https://github.com/vuejs/vue/issues/6566)）。但是如果全部都改成 `macro task`，对一些有重绘和动画的场景也会有性能影响，如 issue [#6813](https://github.com/vuejs/vue/issues/6813)。vue2.5之后版本提供的解决办法是默认使用 `micro task`，但在需要时（例如在v-on附加的事件处理程序中）强制使用 `macro task`。

为什么默认优先使用 `micro task` 呢，是利用其高优先级的特性，保证队列中的微任务在一次循环全部执行完毕。

强制 `macro task` 的方法是在绑定 DOM 事件的时候，默认会给回调的 handler 函数调用 `withMacroTask` 方法做一层包装 `handler = withMacroTask(handler)`，它保证整个回调函数执行过程中，遇到数据状态的改变，这些改变都会被推到 `macro task` 中。以上实现在 [src/platforms/web/runtime/modules/events.js](https://github.com/SHERlocked93/vue-analysis/blob/12343b07f468bd4b6c2e7c078312b882cd7885ee/vue/src/platforms/web/runtime/modules/events.js#L48) 的 `add` 方法中，可以自己看一看具体代码。

刚好在写这篇文章的时候思否上有人问了个问题 [vue 2.4 和2.5 版本的@input事件不一样](https://segmentfault.com/q/1010000015663316?_ea=4018873) ，这个问题的原因也是因为2.5之前版本的DOM事件采用 `micro task` ，而之后采用 `macro task`，解决的途径参考 [< Vue.js 升级踩坑小记>](https://juejin.im/post/5a1af88f5188254a701ec230) 中介绍的几个办法，这里就提供一个在mounted钩子中用 `addEventListener` 添加原生事件的方法来实现，参见 [CodePen](https://codepen.io/SHERlocked93/pen/WKGNKJ)。

## 3. 一个例子

说这么多，不如来个例子，执行参见 [CodePen](https://codepen.io/SHERlocked93/pen/XBjOLq) 

```html
<div id="app">
  <span id='name' ref='name'>{{ name }}</span>
  <button @click='change'>change name</button>
  <div id='content'></div>
</div>
<script>
  new Vue({
    el: '#app',
    data() {
      return {
        name: 'SHERlocked93'
      }
    },
    methods: {
      change() {
        const $name = this.$refs.name
        this.$nextTick(() => console.log('setter前：' + $name.innerHTML))
        this.name = ' name改喽 '
        console.log('同步方式：' + this.$refs.name.innerHTML)
        setTimeout(() => this.console("setTimeout方式：" + this.$refs.name.innerHTML))
        this.$nextTick(() => console.log('setter后：' + $name.innerHTML))
        this.$nextTick().then(() => console.log('Promise方式：' + $name.innerHTML))
      }
    }
  })
</script>
```

执行以下看看结果：

```
同步方式：SHERlocked93 
setter前：SHERlocked93 
setter后：name改喽 
Promise方式：name改喽 
setTimeout方式：name改喽
```

为什么是这样的结果呢，解释一下：

1. **同步方式：** 当把data中的name修改之后，此时会触发name的 `setter` 中的 `dep.notify` 通知依赖本data的render watcher去 `update`，`update` 会把 `flushSchedulerQueue` 函数传递给 `nextTick`，render watcher在 `flushSchedulerQueue` 函数运行时 `watcher.run` 再走 `diff -> patch` 那一套重渲染 `re-render` 视图，这个过程中会重新依赖收集，这个过程是异步的；所以当我们直接修改了name之后打印，这时异步的改动还没有被 `patch` 到视图上，所以获取视图上的DOM元素还是原来的内容。
2. **setter前：** setter前为什么还打印原来的是原来内容呢，是因为 `nextTick` 在被调用的时候把回调挨个push进callbacks数组，之后执行的时候也是 `for` 循环出来挨个执行，所以是类似于队列这样一个概念，先入先出；在修改name之后，触发把render watcher填入 `schedulerQueue` 队列并把他的执行函数 `flushSchedulerQueue` 传递给 `nextTick` ，此时callbacks队列中已经有了 `setter前函数` 了，因为这个 `cb` 是在 `setter前函数` 之后被push进callbacks队列的，那么先入先出的执行callbacks中回调的时候先执行 `setter前函数`，这时并未执行render watcher的 `watcher.run`，所以打印DOM元素仍然是原来的内容。
3. **setter后：** setter后这时已经执行完 `flushSchedulerQueue`，这时render watcher已经把改动 `patch` 到视图上，所以此时获取DOM是改过之后的内容。
4. **Promise方式：** 相当于 `Promise.then` 的方式执行这个函数，此时DOM已经更改。
5. **setTimeout方式：** 最后执行macro task的任务，此时DOM已经更改。

注意，在执行 `setter前函数` 这个异步任务之前，同步的代码已经执行完毕，异步的任务都还未执行，所有的 `$nextTick` 函数也执行完毕，所有回调都被push进了callbacks队列中等待执行，所以在`setter前函数` 执行的时候，此时callbacks队列是这样的：[`setter前函数`，`flushSchedulerQueue`，`setter后函数`，`Promise方式函数`]，它是一个micro task队列，执行完毕之后执行macro task `setTimeout`，所以打印出上面的结果。

另外，如果浏览器的宏任务队列里面有`setImmediate`、`MessageChannel`、`setTimeout/setInterval` 各种类型的任务，那么会按照上面的顺序挨个按照添加进event loop中的顺序执行，所以如果浏览器支持`MessageChannel`， `nextTick` 执行的是 `macroTimerFunc`，那么如果 macrotask queue 中同时有 `nextTick` 添加的任务和用户自己添加的 `setTimeout` 类型的任务，会优先执行 `nextTick` 中的任务，因为`MessageChannel` 的优先级比 `setTimeout`的高，`setImmediate` 同理。



---

**本文是系列文章，随后会更新后面的部分，共同进步~**
> 1. [Vue源码阅读 - 文件结构与运行机制](https://juejin.im/post/5b38830de51d455888216675)
> 2. [Vue源码阅读 - 依赖收集原理](https://juejin.im/post/5b40c8495188251af3632dfa)
> 3. [Vue源码阅读 - 批量异步更新与nextTick原理](https://juejin.im/post/5b50760f5188251ad06b61be)

网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出~

> 参考：
> 1. [Vue2.1.7源码学习](http://hcysun.me/2017/03/03/Vue%E6%BA%90%E7%A0%81%E5%AD%A6%E4%B9%A0/)
> 2. [Vue.js 技术揭秘](https://ustbhuangyi.github.io/vue-analysis)
> 3. [剖析 Vue.js 内部运行机制](https://juejin.im/book/5a36661851882538e2259c0f/)
> 4. [Vue.js 文档](https://cn.vuejs.org/)
> 5. [记录：window.MessageChannel那些事](https://zhuanlan.zhihu.com/p/37589777)
> 6. [MDN - MessageChannel](https://developer.mozilla.org/zh-CN/docs/Web/API/MessageChannel)
> 7. [JS与Node.js中的事件循环](https://segmentfault.com/a/1190000012362096#articleHeader6)
> 8. [黄轶 - Vue.js 升级踩坑小记](https://juejin.im/post/5a1af88f5188254a701ec230)
> 9. [Vue nextTick 机制](https://juejin.im/post/5ae3f0956fb9a07ac90cf43e)

