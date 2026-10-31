# JS throttle与debounce的区别

一般在项目中我们会对input、scroll、resize等事件进行节流控制，防止事件过多触发，减少资源消耗；在vue的官网的[例子](https://link.segmentfault.com/?enc=MTFU8g2zVAfsS1gge6AI4g%3D%3D.VP1E3s3iOGMTcVicoP8L0tVdlKpHxj%2FGvpr%2F2u%2FVduAvPXXhrjX1AVKIAWf%2FfvPJQTfGIUfH%2FeePpyJ%2FQAaoP8dN2%2BlWHKGbhBNCX9e8rsU%3D)中就有关于lodash的debounce方法的使用，当时也提到了throttle，但一直没搞明白**节流 throttle** 与 **去抖 debounce**具体区别在哪里，所以花了点时间来搞清楚。

## 1. 区别

**节流 throttle** 与 **去抖 debounce**的区别主要在触发时机上：

- [`debounce(func, wait, options)`](https://link.segmentfault.com/?enc=x6iUnOdokn69kUL%2F6QyU7Q%3D%3D.CM61EaZXgmo8deA4cq30WWrV%2FwoRgqoHLZutUgvK3CeH%2B%2FG6PBx6bOqf4l8Ym%2Fpl)：创建并返回函数的防反跳版本，将延迟函数的执行（真正的执行）在函数最后一次调用时刻的wait毫秒之后，对于必须在一些输入（多是一些用户操作）停止之后再执行的行为有帮助。**将一个连续的调用归为一个**，如果连续在wait毫秒内调用，最后只有最后一次会执行
- [`throttle(func, wait, options)`](https://link.segmentfault.com/?enc=py%2BLhLJNZebwc29gNvaf%2FQ%3D%3D.8fmzG7oNtpGgww8B2ZGFOlAcNgKKGJiVuTM%2Bh1U3fnsbbyi13qrWNDMxoYF3EBwF)：创建并返回一个像节流阀一样的函数，当重复调用函数的时候，最多每隔指定的wait毫秒调用一次该函数；**不允许方法在每wait毫秒间执行超过一次**，如果连续在wait毫秒内调用，最后执行会均匀分布在大约每wait一次

对于[lodash](https://link.segmentfault.com/?enc=%2FMEBaRBw6yhpQgtXHIvEzg%3D%3D.%2BG5UHta%2F9KdSWUQgahw1y0JOqoLe3Gs7yuizf4MDtvQ%3D)来说，throttle是调用debounce来实现的，throttle 和 debounce 最终都会都会调用 debounce 方法。当调用 `_.debounce`lodash会返回一个函数，这个函数在被调用时会生成一个 setTimeout(delayed, delay)。其中 delayed 又是一个内部方法，在 delayed 被调用时进行如下检测：当前时间 - 上次func被调用事件 是否 小于 0 或 大于 delay ？如果是则执行一次 func，记录并返回执行结果，同时更新上次被调用时间；如果不是则调用 setTimeout 进行下一次的判断。`_.throttle` 方法只不过是多给 debounce 传了一个 `options = {maxWait: $maxWait, leading: true, trailing: true}`，这个选项的意思是至少保证在每 maxWait 时间让 func 被调用一次。

可以看下面的[栗子](https://link.segmentfault.com/?enc=Cf2Dr8YSMxNTJqbQWZrhpA%3D%3D.rzS4NOQUMStHqA%2Bq%2BZl6UqC7eULcH8%2FQ0T36uissJtVzuFi4RbCWVImCnv0vKJUtbLoGtPJB76T%2BXxYnwcHI3IPRud6%2Bjsk%2BanOPGY5pSNg%3D)：

![clipboard.png](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/b3867e190bf6e6f7cfecf8bbc919abc07434865a1978c695fd98786f239fb7ae.png "clipboard.png")

这个图中图中每个小格大约30ms，右边有原生mouseover事件、lodash与[jQuery节流去抖插件](https://link.segmentfault.com/?enc=Tcmmm5ztgdZBOGq3BNWEJQ%3D%3D.EJlD3BiRddP8HT17xKfYH4h2PGHodCJcyNaw5fMzm3355z%2FMZv0igRUKU58hZpNIVOrLeFo96dO%2FSYFYdi5T4w%3D%3D)的debounce与throttle事件。  
在图左区域移动鼠标时：对于debounce，mouseover事件一直没有被调用，直到停下来才被调用一次。而throttle是每wait毫秒就调用一次。

## 2. 使用场景

**debounce:**第一次触发后，进行倒计wait毫秒，如果倒计时过程中有其他触发，则重置倒计时；否则执行。用它来丢弃一些重复的密集操作，直到流量减慢。  
**throttle:**第一次触发后先执行fn（lodash可以通过`{leading: false}`来取消），然后wait ms后再次执行，在单位wait毫秒内的所有重复触发都被抛弃。即如果有连续不断的触发，每wait ms执行fn一次，用在每隔一定间隔执行回调的场景。

- mouse move 时减少计算次数：**debounce**
- input 中输入文字自动发送 ajax 请求进行自动补全： **debounce**
- ajax 请求合并，不希望短时间内大量的请求被重复发送：**debounce**
- resize window 重新计算样式或布局：**debounce** 或 **throttle**
- scroll 时触发操作，如随动效果：**throttle**
- 对用户输入的验证，不想停止输入再进行验证，而是每n秒进行验证：**throttle**

## 3. 简单实现

### 3.1 去抖 debounce

按照上面的说明，去抖就是连续多次delay内的操作取最后一次操作真正执行。

```text
let reduceEvent
function debounce(func, wait, imme) {
    let timer
    return function(...rest) {
        if (imme && !timer) {
            func.apply(this, rest)
        }
        timer && clearTimeout(timer)
        timer = setTimeout(() => func.apply(this, rest), wait)
    }
}

setTimeout(() => debounce(() => console.log(1), 2000), 1000)         // 打印: 1 执行啦！！
setTimeout(() => debounce(() => console.log(2), 2000), 2000)
setTimeout(() => debounce(() => console.log(3), 2000), 2000)
setTimeout(() => debounce(() => console.log(4), 2000), 4000)         // 打印: 4 执行啦！！
```

### 3.2 节流 throttle

按照上面的说明，节流就是连续多次delay内的操作按照指定的间隔来执行。

```text
function throttle(func, wait) {
    let lastTime
    return function(...rest) {
        if (!lastTime ||
          (new Date().getTime() - lastTime > wait)) {
            lastTime = +new Date()
            func.apply(this, rest)
        }
    }
}

const task = throttle(() => console.log(1), 2000)
setTimeout(task, 0)
setTimeout(task, 500)
setTimeout(task, 1000)
setTimeout(task, 2000)                 // 打印: 1 1
```

---

> 参考：
>
> 1. [lodash](https://link.segmentfault.com/?enc=g8K3LOjoadavna0jn0G6VQ%3D%3D.jhuIJUdF%2FPNo7W9kkcam9VUhTLurEwli3SaFJjIGIAM%3D)
> 2. [图解 debounce 与 throttle 的区别](https://link.segmentfault.com/?enc=IZqDBfEa5VCiZIuBXZWSLw%3D%3D.Ei30AxtMWUDikNOW3zTd7YQJMsUwIebjPlp%2Fez6o25EiOERlfXVjZO%2BHFpcxTjhSRr1WOO0%2Bw5q4r9yYo8QbHw%3D%3D)
> 3. [debounce与throttle区别](https://link.segmentfault.com/?enc=1o4BDVpTZ4mRLHVZjZGIxw%3D%3D.KzVlLwwSorpsQeXZio6xktKGg2OeYRwovEbK60oy7ugrYBgD31KVfoUqwC5J%2BbnbNmECve6V%2FtWuqpfS9hJGtg%3D%3D)
> 4. [Debouncing and Throttling Explained Through Examples](https://link.segmentfault.com/?enc=kTjp2WN%2BuOh4zkXwwakj%2BQ%3D%3D.cqGXXV22AxnsIrqy0yykSxpMV4tHed8kvbPpwbcmCi2NLVLhcLioBzoHGztO9J7JI0Cr%2FIfOcgNjS1TMGf1kIF4naFbv%2FBei12qcOvinEP8%3D)
> 5. [Debounce and Throttle: a visual explanation](https://link.segmentfault.com/?enc=zlHl2O28a1EYzcsphvZyOg%3D%3D.0yMvLmRvB%2FeT6BUBl2Ii4Ik1wFoHQXm2loDCb0Zw0ybdixfTYoec68TLHkaN42IEJuOwtcW61YQDNdgAuNWPu5mpB%2FZAxyWA5%2Bz5Stm7OLM%3D)
