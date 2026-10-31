# JS 异步的实现

我们经常说JS是单线程的，比如node.js研讨会上大家都说JS的特色之一是单线程的，这样使JS更简单明了，可是大家真的理解所谓JS的单线程机制吗？单线程时，基于事件的异步机制又该当如何，这些知识在《JavaScript权威指南》并没有介绍，我也一直困惑了，直到看到一篇外文，才有了些眉目，这里与大家分享下。后来发现《JavaScript高级程序设计》高级定时器和循环定时器介绍过，不过觉得没我翻译这篇原文介绍得更透彻，觉得我写的不好的，可以查看原外文。

## 1 先看下两个例子

### 1.1. 简单的settimeout

```text
setTimeout(function () { while (true) { } }, 1000);
setTimeout(function () { alert('end 2'); }, 2000);
setTimeout(function () { alert('end 1'); }, 100);
alert('end');
```

　　执行的结果是弹出’end’、’end 1’，然后浏览器假死，就是不弹出‘end 2’。也就是说第一个settimeout里执行的时候是一个死循环，这个直接导致了理论上比它晚一秒执行的第二个settimeout里的函数被阻塞，这个和我们平时所理解的异步函数多线程互不干扰是不符的。

附计时器使用方法

```text
// 初始化一个简单的js的计时器，一段时间后，才触发并执行回调函数。 setTimeout 返回一个唯一id,可用这个id来取消这个计时器。
var id = setTimeout(fn,delay);
// 类似于setTimeout,不一样的是，每隔一段时间，会持续调用回调fn，直到被取消
var id = setInterval(fn,delay);
// 传入一个计时器的id,取消计时器。
clearInterval(id);
clearTimeout(id);
```

### 1.2 ajax请求回调

接着我们来测试一下通过xmlhttprequest实现ajax异步请求调用，主要代码如下：

```text
var xmlReq = createXMLHTTP();//创建一个xmlhttprequest对象
function testAsynRequest() {
    var url = "/AsyncHandler.ashx?action=ajax";
    xmlReq.open("post", url, true);
    xmlReq.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xmlReq.onreadystatechange = function () {
        if (xmlReq.readyState == 4) {
            if (xmlReq.status == 200) {
                var jsonData = eval('(' + xmlReq.responseText + ')');
                alert(jsonData.message);
            }
            else if (xmlReq.status == 404) {
                alert("Requested URL is not found.");
            } else if (xmlReq.status == 403) {
                alert("Access denied.");
            } else {
                alert("status is " + xmlReq.status);
            }
        }
    };
    xmlReq.send(null);
}
testAsynRequest();//1秒后调用回调函数

while (true) {
}
```

在服务端实现简单的输出：

```text
private void ProcessAjaxRequest(HttpContext context)
{
    string action = context.Request["ajax"];
    Thread.Sleep(1000);//等1秒
    string jsonObject = "{\"message\":\"" + action + "\"}";
    context.Response.Write(jsonObject);
}
```

　　理论上，如果ajax异步请求，它的异步回调函数是在单独一个线程中，那么回调函数必然不被其他线程”阻挠“而顺利执行，也就是1秒后，它回调执行弹出‘ajax’，可是实际情况并非如此，回调函数无法执行，因为浏览器再次因为死循环假死。

　　据上面两个例子，总结如下：

1. JavaScript引擎是单线程运行的,浏览器无论在什么时候都只且只有一个线程在运行JavaScript程序.
2. JavaScript引擎用单线程运行也是有意义的,单线程不必理会线程同步这些复杂的问题,问题得到简化。

## 2. JavaScript引擎

　　可JS内部究竟如何实现，我们在接下来探讨。

　　在了解计时器内部运作前，我们必须清楚一点，触发和执行并不是同一概念，计时器的回调函数一定会在指定delay的时间后被触发，但并不一定立即执行，可能需要等待。所有JavaScript代码是在一个线程里执行的，像鼠标点击和计时器之类的事件只有在JS单线程空闲时才执行。

　　我们来看一下图表，一开始你可能并没发现什么或啥都不懂，但请静下心来，在脑海里绘制出这个场景

![clipboard.png](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/3b9a8057e383ef7154cdebc8a3d39411054db9381e9b54f6f7891334260b3fae.png "clipboard.png")

　　这个图表中有许多数据信息等着我们去理解，当你完全理解了这个图，你会对js的异步运行机制（即JavaScript引擎如何实现异步事件）有很好的了解。这个图是一维的，垂直线上是以毫秒计位，蓝色块代表被划分的不同的js区域执行代码。例如，第一个JS区块执行了18毫秒，鼠标点击事件被阻塞了将近11毫秒，等等。

　　由于JavaScript引擎同一时间只执行一段代码（这是由JavaScript单线程的性质决定的），所以每个JS代码块阻塞了其它异步事件的进行。这意味着当一个异步事件（像鼠标点击、计时器、Ajax）发生时，这些事件的回调函数将排在队列后面等待执行（如何排队完全取决于各浏览器，而我们可以忽视它们内部差异，作一个简化处理）。

　　我们首先从第一个JS代码块开始，有两个计时器被初始化：一个10ms的`setTimeout`和一个10ms的`setInterval`观察计时器初始化位置，（计时器初始化完毕后就会开始计时），发现setTimeout计时器的回调实际上会在第一个代码块执行完毕前被触发。但是这里注意的是，它不会立即执行（单线程不能这样做）。实际上，触发的回调将被排成一个队列，等待下一个可执行时间。

　　此外，在第一个JS代码块，我们发现一个鼠标点击事件被触发。这个鼠标点击JS回调被绑定在异步队列上（我们从来不知道用户什么时候执行这个操作，所以它被认为是异步的）且不能马上执行。像初始化的计时器一样,排队等待执行。

　　执行完初始化JS代码块后，浏览器就有个疑问：谁在等待执行？此时，鼠标点击回调和`setTimeout`计时器的回调都在等待。浏览器将选一个（实际上选择了“鼠标点击事件的处理函数”，因为由图可知它是先进队的）并立马执行。而计时器的回调将等待下一合适时机执行。

　　注意，鼠标点击事件执行过程中，`interval`的回调第一次被触发，与`setTimeout`的回调一样，排队等待执行。随着时间推移，等到`setTimeout`计时器的回调执行时候，`setInterval`的回调再次被触发，这次被触发的回调将被抛弃(因为已经有个同样的回调在排队了)。如果一大段代码块正在执行，所有的`setInterval`的回调都将要排队，一旦大段代码块执行完毕，这些一连串的`setInterval`的回调相互间将被无延迟地执行。实际上，浏览器处理`setInterval`被触发的回调排队等待执行时，除非队列中`setInterval`回调为空，才允许新的`setInterval`的回调加入。

　　我们发现，`setInterval`的第一个被触发的回调执行时，`setInterval`的回调又被触发且排到队列。这向我们传达一个重要的消息：setInterval不关心目前JS正在执行的内容，setInterval的被触发的回调都将会无差别地排队，这意味着两次setInterval回调函数之间的时间间隔会被牺牲掉（缩减）。

　　最后，当setInterval的回调执行两次后，我们发现没有javascript引擎要执行东西。这意味着浏览器将等待着一个新的异步事件发生。我们知道，在50ms时候，setInterval的回调再次被触发，但这次并没有东西阻塞，所以回调就立马执行了。

　　在浏览器中，JavaScript引擎是基于事件驱动的，这里的事件可看作是浏览器派给它的各种任务，这些任务可能源自当前执行的代码块，如调用setTimeout()，也可能来自浏览器内核，如onload()、onclick()、onmouseover()、setTimeOut()、setInterval()、Ajax等。如果从代码的角度来看，所谓的任务实体就是各种回调函数，由于“单线程”的原因，这些任务会进行排队，一个接着一个等待着被引擎处理。(这段说法来源于[PaulGuo](https://link.segmentfault.com/?enc=%2Fk%2FBNTXtM3MLlbLaRP3tsQ%3D%3D.sWmCpOM7EocT15JBSU3T3mP4dnM3EMea9%2FZWdOKy6mt7cGNRh7KIeVH92mBZQwAx))

**注意：**

一秒一次的`setInterver()`执行时插入一个耗时10s的setTimeout，可以看到setInterver是继续执行的，而不是一下蹦出10个setInterver()的回调。

## 3. 浏览器的三个常驻线程

浏览器是多线程的，它们在内核制控下相互配合以保持同步。一个浏览器至少实现三个常驻线程：JavaScript引擎线程，GUI渲染线程，浏览器事件触发线程（UI线程）。

1. javascript引擎是基于事件驱动单线程执行的。JS引擎一直等待着event loop中任务的到来，然后加以处理（只有当前函数执行栈执行完毕，才会去任务队列中取任务执行）。浏览器无论什么时候都只有一个JS线程在运行JS程序。
2. UI渲染线程负责渲染浏览器界面，当界面需要重绘（Repaint）或由于某种操作引发回流(reflow)时,该线程就会执行。但是 GUI渲染线程与JS引擎是互斥的，当JS引擎执行时GUI线程会被挂起，JS对页面的操作即GUI的更新也会被保存在一个队列中，等到JS引擎空闲时才有机会被执行。这就是JS阻塞页面加载。
3. 事件触发线程，当一个事件被触发时该线程会把事件添加到任务队列的队尾，等待JS引擎的处理。这些事件可以来自JavaScript引擎当前执行的代码块调用setTimeout/ajax添加一个任务,也可以来自浏览器其他线程如鼠标点击添加的任务。但由于JS的单线程关系，所有这些事件都得排队等待JS引擎处理。

javascript要等主线程空了才会去查看子线程有没有回调内容。异步的任务执行的顺序是不固定的，主要看返回的速度。

## 4. JavaScript引擎线程和其它侦听线程

　　浏览器内核实现允许多个线程异步执行，这些线程在内核制控下相互配合以保持同步。假如某一浏览器内核的实现至少有三个常驻线程: javascript引擎线程,界面渲染线程,浏览器事件触发线程,除些以外,也有一些执行完就终止的线程,如Http请求线程,这些异步线程都会产生不同的异步事件,下面通过一个图来阐明单线程的JavaScript引擎与另外那些线程是怎样互动通信的.虽然每个浏览器内核实现细节不同,但这其中的调用原理都是大同小异.

![clipboard.png](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/bc33fc32e56e50bac04934bdfd8f285bced45f2389e443346e27ce1de984d19f.png "clipboard.png")

上图中，定时器和事件都按时触发了，这表明JavaScript引擎的线程和计时器触发线程、事件触发线程是三个单独的线程，即使JavaScript引擎的线程被阻塞，其它两个触发线程都在运行。

**线程间通信：**JavaScript引擎执行当前的代码块,其它诸如setTimeout给JS引擎添加一个任务,也可来自浏览器内核的其它线程,如界面元素鼠标点击事件,定时触发器时间到达通知,异步请求状态变更通知等.从代码角度看来任务实体就是各种回调函数,JavaScript引擎一直等待着任务队列中任务的到来.由于单线程关系,这些任务得进行排队,一个接着一个被引擎处理

**~~GUI渲染也是在引擎线程中执行的~~(准确描述见下)，脚本中执行对界面进行更新操作,如添加结点,删除结点或改变结点的外观等更新并不会立即体现出来,这些操作将保存在一个队列中,待JavaScript引擎空闲时才有机会渲染出来。**来看例子（这块内容还有待验证,个人觉得当Dom渲染时，才可阻止渲染）

渲染线程与JavaScript引擎线程是互斥的,这容易理解,因为JavaScript脚本是可操纵DOM元素,在修改这些元素属性同时渲染界面,那么渲染线程前后获得的元素数据就可能不一致了.见[深入理解JavaScript定时机制](https://link.segmentfault.com/?enc=8NPHF9eXAy4bjPQ54TvYUQ%3D%3D.Kvqm9wAvgf08t1q2XJIUB%2BJQ1Ld6NhRl8BAQVYYM5s%2FWd%2Bx8u%2BeP64BUjGCkdFKg)

```text
<div id="test">test</div>
<script type="text/javascript" language="javascript">
var i=0;
while(1) {
    document.getElementById("test").innerHTML+=i++ + "<br />";
}
</script>
```

　　这段代码的本意是从0开始顺序显示数字，它们将一个接一个出现，现在我们来仔细研究一下代码，while(1)创建了一个无休止的循环，但是对于单线程的JavaScript引擎而言，在实际情况中就会造成浏览器暂停响应并处于假死状态。

　　alert()会停止JS引擎的执行，直到按确认键，在JS调试的时候，查看当前实时页面的内容。

## 5. setTimeout和 setInterval

回到文章开头，我们来看下setTimeout和setsetInterval的区别。

```text
setTimeout(function(){
    /* Some long block of code ... */
    setTimout(arguments.callee,10);
},10);

setInterval(function(){
    /* Some long block of code ... */
},10);
```

　　这两个程序段第一眼看上去是一样的，但并不是这样。setTimeout代码至少每隔10ms以上才执行一次；然而setInterval固定每隔10ms将尝试执行，不管它的回调函数的执行状态。

我们来总结下：

- JavaScript引擎只有一个线程，强制异步事件排队等待执行。
- setTimeout和setInterval在异步执行时，有着根本性不同。
- 如果一个计时器被阻塞执行，它将会延迟，直到下一个可执行点（这可能比期望的时间更长）
- setInterval的回调可能被不停的执行，中间没间隔（如果回调执行的时间超过预定等待的值）

《JavaScript高级程序设计》中，针对setInterval说法如下：

当使用setInterval()时，仅当没有该定时器的任何其他代码实例时，才将定时器代码添加到队列中。还要注意两问题：

1. 某些间隔会被跳过（抛弃）；
2. 多个定时器的代码执行之间的间隔可能会比预期小。此时可采取 setTimeout和setsetInterval的区别 的例子方法。

## 5. Ajax异步

　　很多同学朋友搞不清楚，既然说JavaScript是单线程运行的，那么XMLHttpRequest在连接后是否真的异步？其实请求确实是异步的，不过这请求是由浏览器新开一个线程请求(参见上图)，当请求的状态变更时，如果先前已设置回调，这异步线程就产生状态变更事件放到JavaScript引擎的处理队列中等待处理，当任务被处理时，JavaScript引擎始终是单线程运行回调函数，具体点即还是单线程运行onreadystatechange所设置的函数。

　　Tip:理解JavaScript引擎运作非常重要，特别是在大量异步事件（连续）发生时，可以提升程序代码的效率。

---

> 参考：  
> [深入理解JavaScript定时机制](https://link.segmentfault.com/?enc=TKz%2Bq9uY3KTxpN6OGdhtmw%3D%3D.UiFYFDJTEdiufp08SPgmjRPeLaBDWqxRYQVRfk7eLSO4cOQ0gqL71uHiSG0X4ONG)  
> [原外文](https://link.segmentfault.com/?enc=hw4JdrylnJiAxH37FshOow%3D%3D.06IvJ9%2FypMU1pZNAVPDBxLtSz1ijVqDdtrqUpDtW0L8F2Rp6M142i3GSoDeRdsYGUam8mJhoMtptJcZ2ybyuwA%3D%3D)  
> [翻译参考](https://link.segmentfault.com/?enc=zhubicJeSNs%2B3ck9gspmag%3D%3D.0bB8wQ%2F0cUDo%2B97QqFsx1IsA90%2BAJmMOaKxFPCcrvatSql5YmI8IoAh7iX58PvVte66qjbPMbJTxm1%2BUCU%2FdJw%3D%3D)  
> [部分示例](https://link.segmentfault.com/?enc=JFmhlUzHx8lZKGUU9rfpUg%3D%3D.pHpYYn5lC0RNR2wxyvYv9P8OaY1%2BnFdGXl%2FBMv1AJmV%2B%2BUJFGtVmlsXmu3jbSO0TTJGlwjlPpCAJKvUG7O7IRb4mRmbIV%2BKbbgh7HvpyEVo%3D)  
> [其它参考1](https://link.segmentfault.com/?enc=VQifC7I4cSGHv4NjXHnMVQ%3D%3D.CClIJWiuVwp94hkdWkX8aW8al4ZCiHeYlb%2Ftc5xnULWIouSpdDjmwelqLwln3qBl)，[参考2](https://link.segmentfault.com/?enc=3o%2BMIkeLQcKDNn3KtY6T4g%3D%3D.lvohvS45fzwlNGxh0%2FfSsnIngUCQwwnuTKdktEAiNb6saONkwMAgCktM9AYWersD)
