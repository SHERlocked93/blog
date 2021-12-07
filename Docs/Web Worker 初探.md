# Web Worker 初探

[TOC]

以前我们总说，JS是单线程没有多线程，当JS在页面中运行长耗时同步任务的时候就会导致页面假死影响用户体验，从而需要设置把任务放在任务队列中；执行任务队列中的任务也并非多线程进行的，然而现在HTML5提供了我们前端开发这样的能力 - [Web Workers API](https://developer.mozilla.org/zh-CN/docs/Web/API/Web_Workers_API)，我们一起来看一看 Web Worker 是什么，怎么去使用它，在实际生产中如何去用它来进行产出。

## 1. 概述 
Web Workers 使得一个Web应用程序可以在与主执行线程分离的后台线程中运行一个脚本操作。这样做的好处是可以在一个单独的线程中执行费时的处理任务，从而允许主（通常是UI）线程运行而不被阻塞。

它的作用就是给JS创造多线程运行环境，允许主线程创建worker线程，分配任务给后者，主线程运行的同时worker线程也在运行，相互不干扰，在worker线程运行结束后把结果返回给主线程。这样做的好处是主线程可以把计算密集型或高延迟的任务交给worker线程执行，这样主线程就会变得轻松，不会被阻塞或拖慢。这并不意味着JS语言本身支持了多线程能力，而是浏览器作为宿主环境提供了JS一个多线程运行的环境。

不过因为worker一旦新建，就会一直运行，不会被主线程的活动打断，这样有利于随时响应主线程的通性，但是也会造成资源的浪费，所以不应过度使用，用完注意关闭。或者说：如果worker无实例引用，该worker空闲后立即会被关闭；如果worker实列引用不为0，该worker空闲也不会被关闭。

看一看它的[兼容性](https://caniuse.com/#search=webworker)

| Browser | IE | Edge | FireFox | Chrome | Safari |
| ------- | :--: | :--: | :-----: | :----: | :----: |
| version | 10+ | 12+ | 3.5+ | 4+ | 4+ |

## 2. 使用
### 2.1 限制
worker线程的使用有一些注意点
1. 同源限制
   worker线程执行的脚本文件必须和主线程的脚本文件同源，这是当然的了，总不能允许worker线程到别人电脑上到处读文件吧

2. 文件限制
   为了安全，worker线程无法读取本地文件，它所加载的脚本必须来自网络，且需要与主线程的脚本同源

3. DOM操作限制
   worker线程在与主线程的window不同的另一个全局上下文中运行，其中无法读取主线程所在网页的DOM对象，也不能获取 `document`、`window`等对象，但是可以获取`navigator`、`location(只读)`、`XMLHttpRequest`、`setTimeout族`等浏览器API。

4. 通信限制
   worker线程与主线程不在同一个上下文，不能直接通信，需要通过`postMessage`方法来通信。

5. 脚本限制
   worker线程不能执行`alert`、`confirm`，但可以使用 `XMLHttpRequest` 对象发出ajax请求。



### 2.2 例子 

在主线程中生成 Worker 线程很容易：

```js
var myWorker = new Worker(jsUrl, options)
```


Worker()构造函数，第一个参数是脚本的网址（必须遵守同源政策），该参数是必需的，且只能加载 JS 脚本，否则报错。第二个参数是配置对象，该对象可选。它的一个作用就是指定 Worker 的名称，用来区分多个 Worker 线程。

```js
// 主线程

var myWorker = new Worker('worker.js', { name : 'myWorker' });

// Worker 线程
self.name 		// myWorker

```

关于api什么的，直接上例子大概就能明白了，首先是worker线程的js文件：

```js
// workerThread1.js

let i = 1

function simpleCount() {
  i++
  self.postMessage(i)
  setTimeout(simpleCount, 1000)
}

simpleCount()

self.onmessage = ev => {
  postMessage(ev.data + ' 呵呵~')
}
```

在HTML文件中的body中：

```html
<!--主线程，HTML文件的body标签中-->

<div>
  Worker 输出内容：<span id='app'></span>
  <input type='text' title='' id='msg'>
  <button onclick='sendMessage()'>发送</button>
  <button onclick='stopWorker()'>stop!</button>
</div>

<script type='text/javascript'>
  if (typeof(Worker) === 'undefined')	// 使用Worker前检查一下浏览器是否支持
    document.writeln(' Sorry! No Web Worker support.. ')
  else {
    window.w = new Worker('workerThread1.js')
    window.w.onmessage = ev => {
      document.getElementById('app').innerHTML = ev.data
    }
    
    window.w.onerror = err => {
      w.terminate()
      console.log(error.filename, error.lineno, error.message)       // 发生错误的文件名、行号、错误内容
    }
    
    function sendMessage() {
      const msg = document.getElementById('msg')
      window.w.postMessage(msg.value)
    }
    
    function stopWorker() {
      window.w.terminate()
    }
  }
</script>
```

可以自己运行一下看看效果，上面用到了一些常用的api

主线程中的api，`worker`表示是 Worker 的实例：
- `worker.postMessage`: 主线程往worker线程发消息，消息可以是任意类型数据，包括二进制数据
- `worker.terminate`: 主线程关闭worker线程
- `worker.onmessage`: 指定worker线程发消息时的回调，也可以通过`worker.addEventListener('message',cb)`的方式
- `worker.onerror`: 指定worker线程发生错误时的回调，也可以 `worker.addEventListener('error',cb)`

Worker线程中全局对象为 `self`，代表子线程自身，这时 `this`指向`self`，其上有一些api：
- `self.postMessage`: worker线程往主线程发消息，消息可以是任意类型数据，包括二进制数据
- `self.close`: worker线程关闭自己
- `self.onmessage`: 指定主线程发worker线程消息时的回调，也可以`self.addEventListener('message',cb)`
- `self.onerror`: 指定worker线程发生错误时的回调，也可以 `self.addEventListener('error',cb)`

注意，`w.postMessage(aMessage, transferList)` 方法接受两个参数，`aMessage` 是可以传递任何类型数据的，包括对象，这种通信是拷贝关系，即是传值而不是传址，Worker 对通信内容的修改，不会影响到主线程。事实上，浏览器内部的运行机制是，先将通信内容串行化，然后把串行化后的字符串发给 Worker，后者再将它还原。一个可选的 [Transferable](https://developer.mozilla.org/zh-CN/docs/Web/API/Transferable)对象的数组，用于传递所有权。如果一个对象的所有权被转移，在发送它的上下文中将变为不可用（中止），并且只有在它被发送到的worker中可用。可转移对象是如ArrayBuffer，MessagePort或ImageBitmap的实例对象，`transferList`数组中不可传入null。

更详细的API参见 [MDN - WorkerGlobalScope](https://developer.mozilla.org/zh-CN/docs/Web/API/WorkerGlobalScope)。

worker线程中加载脚本的api：
```js
importScripts('script1.js')	// 加载单个脚本
importScripts('script1.js', 'script2.js')	// 加载多个脚本
```



## 3. 实战场景

个人觉得，Web Worker我们可以当做计算器来用，需要用的时候掏出来摁一摁，不用的时候一定要收起来~

1. 加密数据

   有些加解密的算法比较复杂，或者在加解密很多数据的时候，这会非常耗费计算资源，导致UI线程无响应，因此这是使用Web Worker的好时机，使用Worker线程可以让用户更加无缝的操作UI。

2. 预取数据

   有时候为了提升数据加载速度，可以提前使用Worker线程获取数据，因为Worker线程是可以是用 `XMLHttpRequest ` 的。

3. 预渲染

   在某些渲染场景下，比如渲染复杂的canvas的时候需要计算的效果比如反射、折射、光影、材料等，这些计算的逻辑可以使用Worker线程来执行，也可以使用多个Worker线程，这里有个[射线追踪的示例](https://nerget.com/rayjs-mt/rayjs.html)。

4. 复杂数据处理场景

   某些检索、排序、过滤、分析会非常耗费时间，这时可以使用Web Worker来进行，不占用主线程。

5. 预加载图片

   有时候一个页面有很多图片，或者有几个很大的图片的时候，如果业务限制不考虑懒加载，也可以使用Web Worker来加载图片，可以参考一下[这篇文章的探索](https://juejin.im/post/5a0875fcf265da431f4a8ddc)，这里简单提要一下。

   ```js
   // 主线程
   let w = new Worker("js/workers.js");
   w.onmessage = function (event) {
     var img = document.createElement("img");
     img.src = window.URL.createObjectURL(event.data);
     document.querySelector('#result').appendChild(img)
   }
   
   // worker线程
   let arr = [...好多图片路径];
   for (let i = 0, len = arr.length; i < len; i++) {
       let req = new XMLHttpRequest();
       req.open('GET', arr[i], true);
       req.responseType = "blob";
       req.setRequestHeader("client_type", "DESKTOP_WEB");
       req.onreadystatechange = () => {
         if (req.readyState == 4) {
         postMessage(req.response);
       }
     }
     req.send(null);
   }
   ```

   

在实战的时候注意

- 虽然使用worker线程不会占用主线程，但是启动worker会比较耗费资源
- 主线程中使用XMLHttpRequest在请求过程中浏览器另开了一个异步http请求线程，但是交互过程中还是要消耗主线程资源



在 Webpack 项目里面使用 Web Worker 请参照：[怎么在 ES6+Webpack 下使用 Web Worker](https://juejin.im/post/5acf348151882579ef4f5a77)



至于还有Shared Worker、Service Worker什么的，我们就不看了，IE不喜欢



---

网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出~
> 参考：
>
> 1. [MDN - Web Workers 概念与用法](https://developer.mozilla.org/zh-CN/docs/Web/API/Web_Workers_API)
> 2. [阮一峰 - Web Worker 使用教程](http://www.ruanyifeng.com/blog/2018/07/web-worker.html)
> 3. [JavaScript 工作原理之七－Web Workers 分类及 5 个使用场景](https://segmentfault.com/a/1190000014938305)
> 4. [Web Worker在项目中的妙用](https://juejin.im/post/5a0875fcf265da431f4a8ddc)
> 5. [怎么在 ES6+Webpack 下使用 Web Worker](https://juejin.im/post/5acf348151882579ef4f5a77)