# JS与Node.js中的事件循环

这两天跟同事同事讨论遇到的一个问题，js中的`event loop`，引出了chrome与node中运行具有`setTimeout`和`Promise`的程序时候执行结果不一样的问题，从而引出了Nodejs的`event loop`机制，记录一下，感觉还是蛮有收获的

```text
console.log(1)
setTimeout(function() {
  new Promise(function(resolve, reject) {
    console.log(2)
    resolve()
  })
      .then(() => {
        console.log(3)
      })
}, 0)

setTimeout(function() {
  console.log(4)
}, 0)

// chrome中运行：1 2 3 4
// Node中运行： 1 2 4 3
```

chrome和Node执行的结果不一样，这就很有意思了。

## 1. JS 中的任务队列

JavaScript语言的一大特点就是单线程，也就是说，同一个时间只能做一件事。那么，为什么JavaScript不能有多个线程呢？这样能提高效率啊。  
JavaScript的单线程，与它的用途有关。作为浏览器脚本语言，JavaScript的主要用途是与用户互动，以及操作DOM。这决定了它只能是单线程，否则会带来很复杂的同步问题。比如，假定JavaScript同时有两个线程，一个线程在某个DOM节点上添加内容，另一个线程删除了这个节点，这时浏览器应该以哪个线程为准？  
所以，为了避免复杂性，从一诞生，JavaScript就是单线程，这已经成了这门语言的核心特征，将来也不会改变。  
为了利用多核CPU的计算能力，HTML5提出Web Worker标准，允许JavaScript脚本创建多个线程，但是子线程完全受主线程控制，且**不得操作DOM**。所以，这个新标准并没有改变JavaScript单线程的本质。

## 2. 任务队列 event loop

单线程就意味着，所有任务需要排队，前一个任务结束，才会执行后一个任务。如果前一个任务耗时很长，后一个任务就不得不一直等着。  
于是，所有任务可以分成两种，一种是**同步任务**（synchronous），另一种是**异步任务**（asynchronous）。同步任务指的是，在主线程上排队执行的任务，只有前一个任务执行完毕，才能执行后一个任务；异步任务指的是，不进入主线程、而进入"任务队列"（task queue）的任务，只有"任务队列"通知主线程，某个异步任务可以执行了，该任务才会进入主线程执行。  
具体来说，异步执行的运行机制如下。（同步执行也是如此，因为它可以被视为没有异步任务的异步执行。）

1. 所有同步任务都在主线程上执行，形成一个执行栈（execution context stack）。
2. 主线程之外，还存在一个"任务队列"（task queue）。只要异步任务有了运行结果，就在"任务队列"之中放置一个事件。
3. 一旦"执行栈"中的所有同步任务执行完毕，系统就会读取"任务队列"，看看里面有哪些事件。那些对应的异步任务，于是结束等待状态，进入执行栈，开始执行。
4. 主线程不断重复上面的第三步。

![bg2014100801.jpg](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/8077b39bcd7ddd4cb16a1838bf3742e6d3b080940fa6f7085a3bb0df75ec92c4.jpg "bg2014100801.jpg")

只要主线程空了，就会去读取"任务队列"，这就是JavaScript的运行机制。这个过程会不断重复。

## 3. 定时器 `setTimeout`与`setInterval`

定时器功能主要由`setTimeout()`和`setInterval()`这两个函数来完成，它们的内部运行机制完全一样，区别在于前者指定的代码是一次性执行，后者则为反复执行。  
`setTimeout(fn,0)`的含义是，指定某个任务在主线程最早可得的空闲时间执行，也就是说，尽可能早得执行。它在"任务队列"的尾部添加一个事件，因此要等到同步任务和"任务队列"现有的事件都处理完，才会得到执行。  
`HTML5`标准规定了`setTimeout()`的第二个参数的最小值（最短间隔），不得低于`4`毫秒，如果低于这个值，就会自动增加。在此之前，老版本的浏览器都将最短间隔设为`10`毫秒。对于那些DOM的变动（尤其是涉及页面重新渲染的部分），通常不会立即执行，而是每16毫秒执行一次。这时使用`requestAnimationFrame()`的效果要好于`setTimeout()`。  
另外，浏览器内的计时器可能会因为很多原因而减慢速度：

- CPU超载
- 浏览器选项卡处于后台模式
- 笔记本电脑使用电池

所有这些都可能将最小延迟提高到300ms甚至1000ms，具体取决于浏览器和设置。参考 [Scheduling: setTimeout and setInterval](https://link.segmentfault.com/?enc=7JNLQmwyP9FLd2r53Jcj2w%3D%3D.Ne%2FAzXLXMRA2wROR6vhE6Fi5BzpfgileXttNYFVUGGiPYWeEEIbRWNXQIVAJ1E0j)  
需要注意的是，setTimeout()只是将事件插入了"任务队列"，必须等到当前代码（执行栈）执行完，主线程才会去执行它指定的回调函数。要是当前代码耗时很长，有可能要等很久，所以并没有办法保证，回调函数一定会在setTimeout()指定的时间执行。

## 4. Nodejs特点

![Nodejs架构](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/525896a4dba8cc2f96cbf0c77f3c9458e75ed62fdf74e4d23a1719aa3f1df391.png "Nodejs架构")

NodeJS的显著特点：**异步机制**、**事件驱动**。  
事件轮询的整个过程没有阻塞新用户的连接，也不需要维护连接。基于这样的机制，理论上陆续有用户请求连接，NodeJS都可以进行响应，因此NodeJS能支持比Java、php程序更高的并发量。

虽然维护事件队列也需要成本，再由于NodeJS是单线程，事件队列越长，得到响应的时间就越长，并发量上去还是会力不从心。

RESTful API是NodeJS最理想的应用场景，可以处理数万条连接，本身没有太多的逻辑，只需要请求API，组织数据进行返回即可。

## 5. Node.js的Event Loop

关于Nodejs中的事件循环还有[另一篇文章](https://github.com/SHERlocked93/blog/blob/master/Docs/Node%E4%B8%AD%E7%9A%84%E4%BA%8B%E4%BB%B6%E5%BE%AA%E7%8E%AF%E5%92%8C%E5%BC%82%E6%AD%A5API.md)详细探讨了下，可以参考阅读。

事件轮询主要是针对事件队列进行轮询，事件生产者将事件排队放入队列中，队列另外一端有一个线程称为事件消费者会不断查询队列中是否有事件，如果有事件，就立即会执行，为了防止执行过程中有堵塞操作影响当前线程读取队列，事件消费者线程会委托一个线程池专门执行这些堵塞操作。

![时间轮询](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/26d8e282c91da3eafd9ab325ce7c76d214cb7d6a32a49e334e03431373cf2758.png "时间轮询")

Javascript前端和Node.js的机制类似这个事件轮询模型，有的人认为Node.js是单线程，也就是事件消费者是单线程不断轮询，如果有堵塞操作怎么办，不是堵塞了当前单线程的执行吗？  
其实Node.js底层也有一个线程池，线程池专门用来执行各种堵塞操作，这样不会影响单线程这个主线程进行队列中事件轮询和一些任务执行，线程池操作完以后，又会作为事件生产者将操作结果放入同一个队列中。  
总之，一个事件轮询Event Loop需要三个组件：

1. 事件队列Event Queue，属于FIFO模型，一端推入事件数据，另外一端拉出事件数据，两端只通过这个队列通讯，属于一种异步的松耦合。
2. 队列的读取轮询线程，事件的消费者，Event Loop的主角。
3. 单独线程池Thread Pool，专门用来执行长任务，重任务，干繁重体力活的。

Node.js也是单线程的Event Loop，但是它的运行机制不同于浏览器环境。

![Node.js结构](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/871e1444916724d5b37fcc4d59264c4721f1a498c9f67ae6bb6c865e4cf272fd.png "Node.js结构")

根据上图，Node.js的运行机制如下。

1. V8引擎解析JavaScript脚本。
2. 解析后的代码，调用Node API。
3. libuv库负责Node API的执行。它将不同的任务分配给不同的线程，形成一个Event Loop（事件循环），以异步的方式将任务的执行结果返回给V8引擎。
4. V8引擎再将结果返回给用户。

我们可以看到node.js的核心实际上是`libuv`这个库。这个库是c写的，它可以使用多线程技术，而我们的Javascript应用是单线程的。

**Nodejs 的异步任务执行流程：**

![图片描述](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/326b880f3eb4c4e7d27018cbcf90ac025138ee269b9f3ff93cc9523eab2a9fa3.png "图片描述")

用户写的代码是单线程的，但nodejs内部并不是单线程！

**事件机制：**  
Node.js不是用多个线程为每个请求执行工作的，相反而是它把所有工作添加到一个事件队列中，然后有一个单独线程，来循环提取队列中的事件。事件循环线程抓取事件队列中最上面的条目，执行它，然后抓取下一个条目。当执行长期运行或有阻塞I/O的代码时，注意这里：~~它不会被阻塞，会继续提取下一个事件，而对于被阻塞的事件Node.js会从线程池中取出一个线程来运行这个被阻塞的代码，同时把当前事件本身和它的回调事件一同添加到事件队列（callback嵌套callback）。~~

在Node.js中，因为只有一个单线程不断地轮询队列中是否有事件，对于数据库文件系统等I/O操作，包括HTTP请求等等这些容易堵塞等待的操作，如果也是在这个单线程中实现，肯定会堵塞影响其他工作任务的执行，Javascript/Node.js会委托给底层的线程池执行，并会告诉线程池一个回调函数，这样单线程继续执行其他事情，当这些堵塞操作完成后，其结果与提供的回调函数一起再放入队列中，当单线程从队列中不断读取事件，读取到这些堵塞的操作结果后，会将这些操作结果作为回调函数的输入参数，然后激活运行回调函数。

请注意，Node.js的这个单线程不只是负责读取队列事件，还会执行运行回调函数，这是它区别于多线程模式的一个主要特点，多线程模式下，单线程只负责读取队列事件，不再做其他事情，会委托其他线程做其他事情，特别是多核的情况下，一个CPU核负责读取队列事件，一个CPU核负责执行激活的任务，这种方式最适合很耗费CPU计算的任务。反过来，Node..js的执行激活任务也就是回调函数中的任务还是在负责轮询的单线程中执行，这就注定了它不能执行CPU繁重的任务，比如JSON转换为其他数据格式等等，这些任务会影响事件轮询的效率。

## 6. 实例

看一个具体实例：

```text
console.log('1')
setTimeout(function() {
  console.log('2')
  new Promise(function(resolve) {
    console.log('4')
    resolve()
  }).then(function() {
    console.log('5')
  })
  setTimeout(() => { console.log('6') })
  new Promise(function(resolve) {
    console.log('7')
    resolve()
  }).then(function() {
    console.log('8')
  })
})
setTimeout(function() {
  console.log('9')
}, 0)
new Promise(function(resolve) {
  console.log('10')
  resolve()
}).then(function() {
  console.log('11')
})
setTimeout(function() {
  console.log('12')
  new Promise(function(resolve) {
    console.log('13')
    resolve()
  }).then(function() {
    console.log('14')
  })
})
new Promise(function(resolve) {
  console.log('15')
  resolve()
}).then(function() {
  console.log('16')
})

// node1  : 1,10,15,11,16,2,4,7,9,12,13,5,8,14,6        // 结果不稳定
// node2  : 1,10,15,11,16,2,4,7,9,5,8,12,13,14,6        // 结果不稳定
// node3  : 1,10,15,11,16,2,4,7,5,8,9,12,13,14,6        // 结果不稳定
// chrome : 1,10,15,11,16,2,4,7,5,8,9,12,13,14,6
```

chrome的运行比较稳定，而node环境下运行不稳定，可能会出现两种情况。  
chrome运行的结果的原因是`Promise`、`process.nextTick()`的微任务Event Queue运行的权限比普通宏任务Event Queue权限高，如果取事件队列中的事件的时候有微任务，就先执行微任务队列里的任务，除非该任务在下一轮的Event Loop中，微任务队列清空了之后再执行宏任务队列里的任务。

关于Node中的事件循环和异步API的内容，具体可以参见另一篇[帖子](https://github.com/SHERlocked93/blog/blob/master/Docs/Node%E4%B8%AD%E7%9A%84%E4%BA%8B%E4%BB%B6%E5%BE%AA%E7%8E%AF%E5%92%8C%E5%BC%82%E6%AD%A5API.md)，有具体讨论。

## 7. 浏览器中的事件循环

浏览器中和Node中的事件循环的执行顺序并不一致，在浏览器中，我们可以按性质把任务分为两类，macrotask（宏任务）和 microtask（微任务）。

- **macrotask**: script (同步代码), setTimeout, setInterval, setImmediate, MessageChannel, postMessage, I/O, UI渲染
- **microtask**: process.nextTick, Promises（这里指浏览器原生实现的 Promise）, Object.observe, MutationObserver

![clipboard.png](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/ee8295141f1d7c7a67a4c6a629cf1c2664374017fafe09ff2bcdc9f2c141336e.png "clipboard.png")

执行顺序：

- 引擎首先从`macrotask queue`中取出第一个任务，执行完毕后，将`microtask queue`中的所有任务取出，按顺序全部执行；
- 然后再从`macrotask queue`中取下一个，执行完毕后，再次将`microtask queue`中的全部取出；
- 循环往复，直到两个queue中的任务都取完。

---

> 参考：
>
> 1. [Node.js的事件轮询Event Loop原理解释](https://link.segmentfault.com/?enc=VgQ5EFA2%2FMMC4UFqGpfueQ%3D%3D.WGWJrlOQOWpPsthFP53dpU%2B%2F5s3UN%2F%2FMzYdWa%2F6DTITxtDeX%2BmnIlIdJnhLbScJL)
> 2. [JavaScript 运行机制详解：再谈Event Loop](https://link.segmentfault.com/?enc=R0iRK0NvVU2wt8o9wqWSBw%3D%3D.dKWBziWNWAQI4SMewK3EsS5XGP4mx%2F7qvD2Bsewp0yyAuMRAO%2Bp6eHRPoNQXpZYJCQSlSHm%2FRQQo1wqSqObIfw%3D%3D)
> 3. [js与Nodejs的单线程和异步--初探](https://link.segmentfault.com/?enc=%2ByBGREaWogvPNdA9KVAqwA%3D%3D.oC%2B2zwnu145Pne50bgWr0imIM2XQlJOB5Nw7OG%2FdCdNp28vh1T9JNxu0XdJkaBEkc6exy%2Fay5myVKXzBsJ7FqQ%3D%3D)
> 4. [这一次，彻底弄懂 JavaScript 执行机制](https://link.segmentfault.com/?enc=ftYxRRMZhHUi%2B%2BEAh9O4xg%3D%3D.5z71Nwcz4YAHkiBT2oWclXfkHNtOXoiLUG2Tbi4soTG%2BbI%2BslBKIU0zLLAVm%2BvolAs2fJWALB6FJz5%2BbR4X92Q%3D%3D)
> 5. [JavaScript任务队列的顺序机制（事件循环）](https://link.segmentfault.com/?enc=QbPE8mkb1B5iTTtXNGxUXg%3D%3D.yvvysSl7qxSm0MyOFuphldQSvmTmqA7KCsVEI%2BuhJYR1ZmgKdd4I12LGP4GCC0VJ)
