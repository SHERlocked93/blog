# 浏览器垃圾回收机制与 Vue 项目内存泄漏分析

## 1. 介绍

浏览器的 Javascript 具有自动垃圾回收机制(GC:Garbage Collecation)，也就是说，执行环境会负责管理代码执行过程中使用的内存。其原理是：**垃圾收集器会定期（周期性）找出那些不在继续使用的变量，然后释放其内存**。但是这个过程不是实时的，因为其开销比较大并且GC时停止响应其他操作，所以垃圾回收器会按照固定的时间间隔周期性的执行。

不再使用的变量也就是生命周期结束的变量，当然只可能是局部变量，全局变量的生命周期直至浏览器卸载页面才会结束。局部变量只在函数的执行过程中存在，而在这个过程中会为局部变量在栈或堆上分配相应的空间，以存储它们的值，然后在函数中使用这些变量，直至函数结束，而闭包中由于内部函数的原因，外部函数并不能算是结束。

还是上代码说明吧：

```javascript
function fn1() {
    var obj = {name: 'hanzichi', age: 10};
}
function fn2() {
    var obj = {name:'hanzichi', age: 10};
    return obj;
}

var a = fn1();
var b = fn2();
```

我们来看代码是如何执行的。首先声明了两个函数，分别叫做 `fn1` 和 `fn2`，当 `fn1` 被调用时，进入 `fn1` 的环境，会开辟一块内存存放对象 `{name: 'hanzichi', age: 10}`，而当调用结束后，出了fn1的环境，那么该块内存会被 JS 引擎中的垃圾回收器自动释放；在 `fn2` 被调用的过程中，返回的对象被全局变量 `b` 所指向，所以该块内存并不会被释放。

这里问题就出现了：到底哪个变量是没有用的？所以垃圾收集器必须跟踪到底哪个变量没用，对于不再有用的变量打上标记，以备将来收回其内存。用于标记的无用变量的策略可能因实现而有所区别，通常情况下有两种实现方式：**标记清除**和**引用计数**。引用计数不太常用，标记清除较为常用。

## 2. 标记清除

js中最常用的垃圾回收方式就是标记清除。当变量进入环境时，例如，在函数中声明一个变量，就将这个变量标记为“进入环境”。从逻辑上讲，永远不能释放进入环境的变量所占用的内存，因为只要执行流进入相应的环境，就可能会用到它们。而当变量离开环境时，则将其标记为“离开环境”。

```javascript
function test(){
var a = 10 ;       // 被标记 ，进入环境 
var b = 20 ;       // 被标记 ，进入环境
}
test();            // 执行完毕 之后 a、b又被标离开环境，被回收。
```

垃圾回收器在运行的时候会给存储在内存中的所有变量都加上标记（当然，可以使用任何标记方式）。然后，它会去掉环境中的变量以及被环境中的变量引用的变量的标记（闭包）。而在此之后再被加上标记的变量将被视为准备删除的变量，原因是环境中的变量已经无法访问到这些变量了。最后，垃圾回收器完成内存清除工作，销毁那些带标记的值并回收它们所占用的内存空间。
到目前为止，IE9+、Firefox、Opera、Chrome、Safari 的 JS 实现使用的都是标记清除的垃圾回收策略或类似的策略，只不过垃圾收集的时间间隔互不相同。

## 3. 引用计数

引用计数的含义是跟踪记录每个值被引用的次数。当声明了一个变量并将一个引用类型值赋给该变量时，则这个值的引用次数就是 1。如果同一个值又被赋给另一个变量，则该值的引用次数加 1。相反，如果包含对这个值引用的变量又取得了另外一个值，则这个值的引用次数减 1。当这个值的引用次数变成 0 时，则说明没有办法再访问这个值了，因而就可以将其占用的内存空间回收回来。这样，当垃圾回收器下次再运行时，它就会释放那些引用次数为 0 的值所占用的内存。

```javascript
function test() {
    var a = {};    // a指向对象的引用次数为1
    var b = a;     // a指向对象的引用次数加1，为2
    var c = a;     // a指向对象的引用次数再加1，为3
    var b = {};    // a指向对象的引用次数减1，为2
}
```

Netscape Navigator3 是最早使用引用计数策略的浏览器，但很快它就遇到一个严重的问题：**循环引用**。循环引用指的是对象 A 中包含一个指向对象B的指针，而对象 B 中也包含一个指向对象 A 的引用。

```javascript
function fn() {
    var a = {};
    var b = {};
    a.pro = b;
    b.pro = a;
}
fn();
```

以上代码 `a` 和 `b` 的引用次数都是 2，`fn` 执行完毕后，两个对象都已经离开环境，在标记清除方式下是没有问题的，但是在引用计数策略下，因为 `a` 和 `b` 的引用次数不为 0，所以不会被垃圾回收器回收内存，如果 `fn` 函数被大量调用，就会造成内存泄露。在 IE7 与 IE8 上，内存直线上升。

我们知道，IE 中有一部分对象并不是原生 JS 对象。例如，其内存泄露 DOM 和 BOM 中的对象就是使用 C++ 以 COM 对象的形式实现的，而 COM 对象的垃圾回收机制采用的就是引用计数策略。因此，即使IE的js引擎采用标记清除策略来实现，但 JS 访问的**COM对象依然是基于引用计数策略**的。换句话说，只要在 IE 中涉及 COM 对象，就会存在循环引用的问题。

```javascript
var element = document.getElementById("some_element");
var myObject = new Object();
myObject.e = element;
element.o = myObject;
```

这个例子在一个 DOM 元素 `element` 与一个原生js对象 `myObject` 之间创建了循环引用。其中，变量 `myObject` 有一个属性 `e` 指向 `element` 对象；而变量 `element` 也有一个属性 `o` 回指 `myObject`。由于存在这个循环引用，即使例子中的 DOM 从页面中移除，它也永远不会被回收。

举个栗子：
![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/e21348cabaef6010cf96a1e3cb40ad85af1eee67e95769ff0bc44ae2b044bc57.webp)

- 黄色是指直接被 js变量所引用，在内存里
- 红色是指间接被 js变量所引用，如上图，refB 被 refA 间接引用，导致即使 refB 变量被清空，也是不会被回收的
- 子元素 refB 由于 `parentNode` 的间接引用，只要它不被删除，它所有的父元素（图中红色部分）都不会被删除

另一个例子：

```javascript
window.onload=function outerFunction(){
    var obj = document.getElementById("element");
    obj.onclick=function innerFunction(){};
};
```

这段代码看起来没什么问题，但是 obj 引用了 `document.getElementById('element')`，而 `document.getElementById('element')` 的 `onclick` 方法会引用外部环境中的变量，自然也包括 obj，是不是很隐蔽啊。(在比较新的浏览器中在移除Node的时候已经会移除其上的event了，但是在老的浏览器，特别是 IE 上会有这个 bug)

**解决办法：**

最简单的方式就是自己手工解除循环引用，比如刚才的函数可以这样

```javascript
myObject.element = null;
element.o = null;

window.onload=function outerFunction(){
    var obj = document.getElementById("element");
    obj.onclick=function innerFunction(){};
    obj=null;
};
```

将变量设置为 null 意味着切断变量与它此前引用的值之间的连接。当垃圾回收器下次运行时，就会删除这些值并回收它们占用的内存。

要注意的是，IE9+ 并不存在循环引用导致 DOM 内存泄露问题，可能是微软做了优化，或者 DOM 的回收方式已经改变。

## 4. 内存管理

### 4.1 什么时候触发垃圾回收？

垃圾回收器周期性运行，如果分配的内存非常多，那么回收工作也会很艰巨，确定垃圾回收时间间隔就变成了一个值得思考的问题。IE6的垃圾回收是根据内存分配量运行的，当环境中存在256个变量、4096个对象、64k 的字符串任意一种情况的时候就会触发垃圾回收器工作，看起来很科学，不用按一段时间就调用一次，有时候会没必要，这样按需调用不是很好吗？但是如果环境中就是有这么多变量等一直存在，现在脚本如此复杂，很正常，那么结果就是垃圾回收器一直在工作，这样浏览器就没法儿玩儿了。

微软在IE7中做了调整，触发条件不再是固定的，而是动态修改的，初始值和 IE6 相同，如果垃圾回收器回收的内存分配量低于程序占用内存的15%，说明大部分内存不可被回收，设的垃圾回收触发条件过于敏感，这时候把临街条件翻倍，如果回收的内存高于85%，说明大部分内存早就该清理了，这时候把触发条件置回。这样就使垃圾回收工作职能了很多

### 4.2 合理的GC方案

#### 1. 基础方案

Javascript引擎基础GC方案是（simple GC）：mark and sweep（标记清除），即：

1. 遍历所有可访问的对象。
2. 回收已不可访问的对象。

#### 2. GC的缺陷

和其他语言一样，JS 的 GC 策略也无法避免一个问题：GC 时，停止响应其他操作，这是为了安全考虑。而 Javascript 的 GC 在 100ms 甚至以上，对一般的应用还好，但对于 JS 游戏，动画对连贯性要求比较高的应用，就麻烦了。这就是新引擎需要优化的点：避免GC造成的长时间停止响应。

#### 3. GC优化策略

David 大叔主要介绍了2个优化方案，而这也是最主要的2个优化方案了：

1. **分代回收**（Generation GC）
   这个和Java回收策略思想是一致的，也是V8所主要采用的。目的是通过区分“临时”与“持久”对象；多回收“临时对象”区（young generation），少回收“持久对象”区（tenured generation），减少每次需遍历的对象，从而减少每次GC的耗时。如图：

   ![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/b16cfdad78ec749c2e2f07ced002ea9c0caaa607d19c33b7da519fb4e4233e73.webp)
   这里需要补充的是：对于 tenured generation 对象，有额外的开销：把它从 young generation 迁移到 tenured generation，另外，如果被引用了，那引用的指向也需要修改。
   这里主要内容可以参考[深入浅出Node](https://book.douban.com/subject/25768396/ "https://book.douban.com/subject/25768396/")中关于内存的介绍，很详细~
2. **增量GC**
   这个方案的思想很简单，就是“每次处理一点，下次再处理一点，如此类推”。如图：
   ![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/74dd753616d4cd51f8f52a076d363900e02e6a758c7e0a01f19ef0260d746f89.webp)

   这种方案，虽然耗时短，但中断较多，带来了上下文切换频繁的问题。因为每种方案都其适用场景和缺点，因此在实际应用中，会根据实际情况选择方案。

   比如：低 (对象/s) 比率时，中断执行GC的频率，simple GC更低些；如果大量对象都是长期“存活”，则分代处理优势也不大。

## 5. Vue 中的内存泄漏问题

JS 程序的内存溢出后，会使某一段函数体永远失效（取决于当时的 JS 代码运行到哪一个函数），通常表现为程序突然卡死或程序出现异常。

这时我们就要对该 JS 程序进行内存泄漏的排查，找出哪些对象所占用的内存没有释放。这些对象通常都是开发者以为释放掉了，但事实上仍被某个闭包引用着，或者放在某个数组里面。

### 5.1 泄漏点

1. DOM/BOM 对象泄漏；
2. script 中存在对 DOM/BOM 对象的引用导致；
3. JS 对象泄漏；
4. 通常由闭包导致，比如事件处理回调，导致 DOM 对象和脚本中对象双向引用，这个是常见的泄漏原因；

### 5.2 代码关注点

主要关注的就是各种事件绑定场景，比如：

1. DOM 中的 `addEventLisner` 函数及派生的事件监听，比如 Jquery 中的 `on` 函数，Vue 组件实例的 `$on` 函数;
2. 其它 BOM 对象的事件监听， 比如 websocket 实例的 on 函数;
3. 避免不必要的函数引用；
4. 如果使用 `render` 函数，避免在 HTML 标签中绑定 DOM/BOM 事件;

### 5.3 如何处理

1. 如果在 `mounted/created` 钩子中使用 JS 绑定了 DOM/BOM 对象中的事件，需要在 `beforeDestroy` 中做对应解绑处理；
2. 如果在 `mounted/created` 钩子中使用了第三方库初始化，需要在 `beforeDestroy` 中做对应销毁处理（一般用不到，因为很多时候都是直接全局 `Vue.use`）；
3. 如果组件中使用了 `setInterval`，需要在 `beforeDestroy` 中做对应销毁处理；

### 5.4 在 vue 组件中处理 addEventListener

调用 `addEventListener` 添加事件监听后在 `beforeDestroy` 中调用 `removeEventListener` 移除对应的事件监听。为了准确移除监听，尽量不要使用匿名函数或者已有的函数的绑定来直接作为事件监听函数。

```javascript
mounted() {
    const box = document.getElementById('time-line')
    this.width = box.offsetWidth
    this.resizefun = () => {
      this.width = box.offsetWidth
    }
    window.addEventListener('resize', this.resizefun)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizefun)
    this.resizefun = null
  }
```

### 5.5 观察者模式引起的内存泄漏

在 spa 应用中使用观察者模式的时候如果给观察者注册了被观察的方法，而没有在离开组件的时候及时移除，可能造成重复注册而内存泄漏；

举个栗子：
进入组件的时候 `ob.addListener("enter", _func)`，如果离开组件 `beforeDestroy` 的时候没有 `ob.removeListener("enter", _func)`，就会导致内存泄漏

更详细的栗子参考：[德州扑克栗子](http://frontenddev.org/link/js-memory-leak-screening-method-chrome-profiles.html#heading-2-7 "http://frontenddev.org/link/js-memory-leak-screening-method-chrome-profiles.html#heading-2-7")

### 5.6 上下文绑定引起的内存泄漏

有时候使用 `bind/apply/call` 上下文绑定方法的时候，会有内存泄漏的隐患。

```javascript
var ClassA = function(name) {
  this.name = name
  this.func = null
}

var a = new ClassA("a")
var b = new ClassA("b")

b.func = bind(function() {
  console.log("I am " + this.name)
}, a)

b.func()    // 输出: I am a

a = null           // 释放a
//b = null;        // 释放b
//b.func = null;   // 释放b.func

function bind(func, self) {    // 模拟上下文绑定
  return function() {
    return func.apply(self)
  }
}
```

使用 `chrome dev tool > memory > profiles` 查看内存中 ClassA 的实例数，发现有两个实例，`a` 和 `b`。虽然 `a` 设置成 null 了，但是 `b` 的方法中 bind 的闭包上下文 self 绑定了 `a`，因此虽然 `a` 释放，但是 `b/b.func` 没有释放，闭包的 self 一直存在并保持对 `a` 的引用。

---

> 参考：
>
> 1. [跟我学习javascript的垃圾回收机制与内存管理](http://www.jb51.net/article/75292.htm "http://www.jb51.net/article/75292.htm")
> 2. [App之性能优化](http://www.cnblogs.com/stenson/p/3951035.html "http://www.cnblogs.com/stenson/p/3951035.html")
> 3. [Vue Web App 内存泄漏-调试和分析](https://www.cnblogs.com/alongWind/p/7683624.html "https://www.cnblogs.com/alongWind/p/7683624.html")
> 4. [搞定JavaScript内存泄漏](http://boke.io/gao-ding-nei-cun-xie-lou/ "http://boke.io/gao-ding-nei-cun-xie-lou/")

> 推介阅读：
>
> 1. [雅虎网站页面性能优化的34条黄金守则](http://www.cnblogs.com/li0803/archive/2009/09/20/1570581.html "http://www.cnblogs.com/li0803/archive/2009/09/20/1570581.html")
> 2. [用 Chrome 开发者工具分析 javascript 的内存回收（GC）](http://mp.weixin.qq.com/s/zDFl58bxseZGsUvS3PjP0w "http://mp.weixin.qq.com/s/zDFl58bxseZGsUvS3PjP0w")
> 3. [JS内存泄漏排查方法——Chrome Profiles](http://frontenddev.org/link/js-memory-leak-screening-method-chrome-profiles.html "http://frontenddev.org/link/js-memory-leak-screening-method-chrome-profiles.html")
> 4. [Javascript典型内存泄漏及chrome的排查方法](https://segmentfault.com/a/1190000008901861 "https://segmentfault.com/a/1190000008901861")
