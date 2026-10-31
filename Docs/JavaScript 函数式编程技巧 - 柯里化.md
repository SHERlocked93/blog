# JS中的柯里化

作为函数式编程语言，JS带来了很多语言上的有趣特性，比如柯里化和反柯里化。

这里可以对照另外一篇介绍 [JS 反柯里化](https://github.com/SHERlocked93/blog/blob/master/Docs/JavaScript%20%E5%87%BD%E6%95%B0%E5%BC%8F%E7%BC%96%E7%A8%8B%E6%8A%80%E5%B7%A7%20-%20%E5%8F%8D%E6%9F%AF%E9%87%8C%E5%8C%96.md) 的文章一起看~

## 1. 简介

**柯里化**（Currying），又称部分求值（Partial Evaluation），是把接受多个参数的函数变换成接受一个单一参数（最初函数的第一个参数）的函数，并且返回接受余下的参数而且返回结果的新函数的技术。

核心思想是把多参数传入的函数拆成单参数（或部分）函数，内部再返回调用下一个单参数（或部分）函数，依次处理剩余的参数。

按照Stoyan Stefanov --《JavaScript Pattern》作者 的说法，所谓“柯里化”就是**使函数理解并处理部分应用**

柯里化有3个常见作用：

1. 参数复用
2. 提前返回
3. 延迟计算/运行

talk is cheap，看看怎么实现吧~

## 2. 实现

### 2.1 通用实现

一个通用实现：

```text
function currying(fn, ...rest1) {
  return function(...rest2) {
    return fn.apply(null, rest1.concat(rest2))
  }
}
```

注意这里concat接受非数组元素参数将被当做调用者的一个元素传入

用它将一个sayHello函数柯里化试试：

```text
function sayHello(name, age, fruit) {
  console.log(console.log(`我叫 ${name},我 ${age} 岁了, 我喜欢吃 ${fruit}`))
}

const curryingShowMsg1 = currying(sayHello, '小明')
curryingShowMsg1(22, '苹果')            // 我叫 小明,我 22 岁了, 我喜欢吃 苹果

const curryingShowMsg2 = currying(sayHello, '小衰', 20)
curryingShowMsg2('西瓜')               // 我叫 小衰,我 20 岁了, 我喜欢吃 西瓜
```

嘻嘻，感觉还行~

### 2.2 高阶柯里化函数

以上柯里化函数已经能解决一般需求了，但是如果要多层的柯里化总不能不断地进行currying函数的嵌套吧，我们希望经过柯里化之后的函数每次只传递一个或者多个参数，那该怎么做呢：

```text
function curryingHelper(fn, len) {
  const length = len || fn.length  // 第一遍运行length是函数fn一共需要的参数个数，以后是剩余所需要的参数个数
  return function(...rest) {
    return rest.length >= length    // 检查是否传入了fn所需足够的参数
        ? fn.apply(this, rest)
        : curryingHelper(currying.apply(this, [fn].concat(rest)), length - rest.length)        // 在通用currying函数基础上
  }
}

function sayHello(name, age, fruit) { console.log(`我叫 ${name},我 ${age} 岁了, 我喜欢吃 ${fruit}`) }    

const betterShowMsg = curryingHelper(sayHello)
betterShowMsg('小衰', 20, '西瓜')      // 我叫 小衰,我 20 岁了, 我喜欢吃 西瓜
betterShowMsg('小猪')(25, '南瓜')      // 我叫 小猪,我 25 岁了, 我喜欢吃 南瓜
betterShowMsg('小明', 22)('倭瓜')      // 我叫 小明,我 22 岁了, 我喜欢吃 倭瓜
betterShowMsg('小拽')(28)('冬瓜')      // 我叫 小拽,我 28 岁了, 我喜欢吃 冬瓜
```

如此实现一个高阶的柯里化函数，使得柯里化一个函数的时候可以不用嵌套的currying，当然是因为把嵌套的地方放到了curryingHelper里面进行了...-。-

### 2.3 疯狂柯里化函数

尽管柯里化函数已经很牛了，但是它也让你必须花费点小心思在你所定义函数的参数顺序上。在一些函数式编程语言中，会定义一个特殊的“占位变量”。通常会指定下划线来干这事，如果作为一个函数的参数被传入，就表明这个是可以“跳过的”，是尚待指定的参数。比如：

```text
var sendAjax = function (url, data, options) { /* ... */ }
var sendPost = function (url, data) {                    // 当然可以这样
    return sendAjax(url, data, { type: "POST", contentType: "application/json" })
}
// 也可以使用下划线来指定未确定的参数
var sendPost = sendAjax( _ , _ , { type: "POST", contentType: "application/json" })        
```

JS不具备这样的原生支持，可以使用一个全局占位符变量`const _ = { }`并且通过===来判断是否是占位符，当然你如果使用了lodash的话可以使用别的符号代替。那么可以这样改造柯里化函数：

```text
const _ = {}
function crazyCurryingHelper(fn, length, args, holes) {
  length = length || fn.length    // 第一遍是fn所需的参数个数，以后是
  args = args || []
  holes = holes || []

  return function(...rest) {
    let _args = args.slice(),
        _holes = holes.slice(),
        argLength = _args.length,        // 存储接收到的args和holes的长度
        holeLength = _holes.length,
        arg, i = 0
    for (; i < rest.length; i++) {
      arg = rest[i]
      if (arg === _ && holeLength) {
        holeLength--                      // 循环_holes的位置
        _holes.push(_holes.shift())      // _holes最后一个移到第一个
      } else if (arg === _) {
        _holes.push(argLength + i)          // 存储_hole就是_的位置
      } else if (holeLength) {              // 是否还有没有填补的hole
        holeLength--
        _args.splice(_holes.shift(), 0, arg)           // 在参数列表指定hole的地方插入当前参数
      } else {
        _args.push(arg)            // 不需要填补hole,直接添加到参数列表里面
      }
    }

    return _args.length >= length                          // 递归的进行柯里化
        ? fn.apply(this, _args)
        : crazyCurryingHelper.call(this, fn, length, _args, _holes)
  }
}

function sayHello(name, age, fruit) { console.log(`我叫 ${name},我 ${age} 岁了, 我喜欢吃 ${fruit}`) }

const betterShowMsg = crazyCurryingHelper(sayHello)
betterShowMsg(_, 20)('小衰', _, '西瓜')          // 我叫 小衰,我 20 岁了, 我喜欢吃 西瓜
betterShowMsg(_, _, '南瓜')('小猪')(25)          // 我叫 小猪,我 25 岁了, 我喜欢吃 南瓜
betterShowMsg('小明')(_, 22)(_, _, '倭瓜')          // 我叫 小明,我 22 岁了, 我喜欢吃 倭瓜
betterShowMsg('小拽')(28)('冬瓜')          // 我叫 小拽,我 28 岁了, 我喜欢吃 冬瓜
```

牛B闪闪

## 3. 柯里化的常见用法

### 3.1 参数复用

通过柯里化方法，缓存参数到闭包内部参数，然后在函数内部将缓存的参数与传入的参数组合后apply/bind/call给函数执行，来实现参数的复用，降低适用范围，提高适用性。

参看以下栗子，官员无论添加后续老婆，都能和合法老婆组合，通过柯里化方法，getWife方法就无需添加多余的合法老婆...

```text
var currying = function(fn) {
  var args = [].slice.call(arguments, 1)      // fn 指官员消化老婆的手段,args 指的是那个合法老婆
  return function(...rest) {
    var newArgs = args.concat(...rest)        // 已经有的老婆和新搞定的老婆们合成一体，方便控制
    return fn.apply(null, newArgs)        // 这些老婆们用 fn 这个手段消化利用，完成韦小宝前辈的壮举并返回
  }
}

var getWife = currying(function() {
  console.log([...arguments].join(';'))          // allwife 就是所有的老婆的，包括暗渡陈仓进来的老婆
}, '合法老婆')

getWife('老婆1', '老婆2', '老婆3')      // 合法老婆;老婆1;老婆2;老婆3
getWife('超越韦小宝的老婆')             // 合法老婆;超越韦小宝的老婆
getWife('超级老婆')                    // 合法老婆;超级老婆
```

### 3.2 提高适用性

**通用函数**解决了兼容性问题，但同时也会再来，使用的不便利性，不同的应用场景往，要传递很多参数，以达到解决特定问题的目的。有时候应用中，同一种规则可能会反复使用，这就可能会造成代码的重复性。

```text
// 未柯里化前
function square(i) { return i * i; }
function dubble(i) { return i * 2; }
function map(handler, list) { return list.map(handler); }

map(square, [1, 2, 3, 4, 5]);        // 数组的每一项平方
map(square, [6, 7, 8, 9, 10]);
map(dubble, [1, 2, 3, 4, 5]);        // 数组的每一项加倍
map(dubble, [6, 7, 8, 9, 10]);
```

同一规则重复使用，带来代码的重复性，因此可以使用上面的通用柯里化实现改造一下：

```text
// 柯里化后
function square(i) { return i * i; }
function dubble(i) { return i * 2; }
function map(handler, ...list) { return list.map(handler); }

var mapSQ = currying(map, square);
mapSQ([1, 2, 3, 4, 5]);
mapSQ([6, 7, 8, 9, 10]);

var mapDB = currying(map, dubble);
mapDB([1, 2, 3, 4, 5]);
mapDB([6, 7, 8, 9, 10]);
```

可以看到这里柯里化方法的使用和偏函数比较类似，顺便回顾一下偏函数~

**偏函数**是创建一个调用另外一个部分(参数或变量已预制的函数)的函数，函数可以根据传入的参数来生成一个真正执行的函数。比如：

```text
const isType = function(type) {
  return function(obj) {
    return Object.prototype.toString.call(obj) === `[object ${type}]`
  }
}
const isString = isType('String')
const isFunction = isType('Function')
```

这样就用偏函数快速创建了一组判断对象类型的方法~

**偏函数**固定了函数的某个部分，通过传入的参数或者方法返回一个新的函数来接受剩余的参数，数量可能是一个也可能是多个  
**柯里化**是把一个有n个参数的函数变成n个只有1个参数的函数，例如：`add = (x, y, z) => x + y + z`→`curryAdd = x => y => z => x + y + z`  
当偏函数接受一个参数并且返回了一个只接受一个参数的函数，与两个接受一个参数的函数curry()()的柯里化函数，这时候两个概念类似。(个人理解不知道对不对)

### 3.3 延迟执行

柯里化的另一个应用场景是延迟执行。不断的柯里化，累积传入的参数，最后执行。例如累加：

```text
const curryAdd = function(...rest) {
  const _args = rest
  return function cb(...rest) {
    if (rest.length === 0) {
      return _args.reduce((sum, single) => sum += single)
    } else {
      _args.push(...rest)
      return cb
    }
  }
}()                        // 为了保存添加的数，这里要返回一个闭包
curryAdd(1)
curryAdd(2)
curryAdd(3)
curryAdd(4)
curryAdd()               // 最后计算输出:10
```

更通用的写法，将处理函数提取出来：

```text
const curry = function(fn) {
  const _args = []
  return function cb(...rest) {
    if (rest.length === 0) {
      return fn.apply(this, _args)
    }
    _args.push(...rest)
    return cb
  }
}

const curryAdd = curry((...T) => 
  T.reduce((sum, single) => sum += single)
)
curryAdd(1)
curryAdd(2)
curryAdd(3)
curryAdd(4)
curryAdd()               // 最后计算输出:10
```

## 4. Function.prototype.bind 方法也是柯里化应用

与 call/apply 方法直接执行不同，bind 方法将第一个参数设置为函数执行的上下文，其他参数依次传递给调用方法（函数的主体本身不执行，可以看成是延迟执行），并动态创建返回一个新的函数， 这符合柯里化特点。

```text
var foo = {x: 888};
var bar = function () {
    console.log(this.x);
}.bind(foo);              // 绑定
bar();                    // 888
```

下面是一个 bind 函数的模拟，testBind 创建并返回新的函数，在新的函数中将真正要执行业务的函数绑定到实参传入的上下文，延迟执行了。

```text
Function.prototype.testBind = function(scope) {
  return () => this.apply(scope)
}
var foo = { x: 888 }
var bar = function() {
  console.log(this.x)
}.testBind(foo)              // 绑定
bar()                    // 888
```

---

> 参考：  
> [JS高级程序设计](https://book.douban.com/subject/10546125/)  
> [JS中的柯里化(currying)](http://www.zhangxinxu.com/wordpress/2013/02/js-currying/)  
> [前端开发者进阶之函数柯里化Currying](https://www.cnblogs.com/pigtail/p/3447660.html)  
> [浅析 JavaScript 中的 函数 currying 柯里化](https://www.cnblogs.com/zztt/p/4142891.html)  
> [掌握JavaScript函数的柯里化](https://segmentfault.com/a/1190000006096034)  
> [函数式JavaScript（4）：函数柯里化](http://blog.jobbole.com/77956/)
