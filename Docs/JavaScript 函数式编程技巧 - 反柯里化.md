# JS中的反柯里化

作为函数式编程语言，JS带来了很多语言上的有趣特性，比如柯里化和反柯里化。

可以对照另外一篇介绍 [JS 柯里化](https://github.com/SHERlocked93/blog/blob/master/Docs/JavaScript%20%E5%87%BD%E6%95%B0%E5%BC%8F%E7%BC%96%E7%A8%8B%E6%8A%80%E5%B7%A7%20-%20%E6%9F%AF%E9%87%8C%E5%8C%96.md) 的文章一起看~

## 1. 简介

**柯里化**，是固定部分参数，返回一个接受剩余参数的函数，也称为部分计算函数，目的是为了缩小适用范围，创建一个针对性更强的函数。核心思想是把多参数传入的函数拆成单参数（或部分）函数，内部再返回调用下一个单参数（或部分）函数，依次处理剩余的参数。

而**反柯里化**，从字面讲，意义和用法跟函数柯里化相比正好相反，扩大适用范围，创建一个应用范围更广的函数。使本来只有特定对象才适用的方法，扩展到更多的对象。

## 2. 实现

先来看看反柯里化的通用实现吧~

```text
Function.prototype.unCurrying = function() {
  const self = this
  return function(...rest) {
    return Function.prototype.call.apply(self, rest)
  }
}
```

解释下：

1. 为Function原型添加`uncurrying`方法，并在执行的时候保存执行`unCurrying`的方法到self
2. 借用apply把要借用的函数作为this环境赋给call，并传入之后的形参作为参数执行

还有一个实现：

```text
Function.prototype.unCurrying = function() {
  return this.call.bind(this)
}
```

如果你觉得把函数放在Function.prototype上不太好，也可以这样：

```text
function unCurrying(fn) {
  return function(tar, ...argu) {
    return fn.apply(tar, argu)
  }
}
```

## 3. 使用

### 3.1 简单使用

用`unCurrying`通用实现简单的实用一下试试：

```text
Function.prototype.unCurrying = function() {
  const self = this                        // 这里的self就是Array.prototype.push方法
  return function(...rest) {              // rest为传入的两层参数[[1,2,3],4]
    return Function.prototype.call.apply(self, rest)
  }
}
const push = Array.prototype.push.unCurrying()

~function(...rest) {       // rest:[1,2,3]
  push(rest, 4)
  console.log(rest)    // [1, 2, 3, 4]
}(1, 2, 3)
```

### 3.2 借用其他方法

反柯里化其实反映的是一种思想，即扩大方法的适用范围，仍然调用刚刚的通用`unCurrying`方法借用push方法：

```text
const push = Array.prototype.push.unCurrying()

const obj = { a: '嘻嘻' }
push(obj, '呵呵', '哈哈', '嘿嘿')
console.log(obj)                    // { '0': '呵呵', '1': '哈哈', '2': '嘿嘿', a: '嘻嘻', length: 3 }
```

相当于`obj.push(...)`，obj不仅多了类似于数组一样以数字作为索引的属性，还多了个类似于数组的length属性，让引擎自动管理数组成员和length属性；(文后有V8引擎实现push方法的源码)  
这样一个数组的push方法就被借用出来，可以应用于任何其他对象了。

只要是方法，`unCurrying`就可以借用，`call`方法也可以：

```text
var call = Function.prototype.call.unCurrying();
function $(id) {
    return this.getElementById(id);
}
call($, document, 'demo')            // #demo 元素
```

相当于`document.$('demo')`，成功的借用了call方法，当然可以把document改成你希望作为this绑定到$的任何对象，比如`{ getElementById:T=>console.log(T+'呃') } // demo呃`

### 3.3 借用自己

`unCurrying`本身也是方法，也可以借用自己...-。-

```text
const unCurrying = Function.prototype.unCurrying.unCurrying()
const map = unCurrying(Array.prototype.map)
map({ 0: 4, 1: 'a', 2: null, length: 3 }, n => n + n)                    // [8, "aa", 0]
```

神奇吧~

## 4. 总结

简单说，函数柯里化就是对高阶函数的降阶处理，缩小适用范围，创建一个针对性更强的函数。举栗子：

```text
function(arg1,arg2)        // => function(arg1)(arg2)
function(arg1,arg2,arg3)        // => function(arg1)(arg2)(arg3)
function(arg1,arg2,arg3,arg4)        // => function(arg1)(arg2)(arg3)(arg4)
function(arg1,arg2,…,argn)        // => function(arg1)(arg2)…(argn)
```

而反柯里化就是反过来，增加适用范围，让方法使用场景更大。使用`unCurrying`, 可以把原生方法借出来，让任何对象拥有原生对象的方法。举个栗子：

```text
obj.func(arg1, arg2)        // => func(obj, arg1, arg2)
```

**也可以这样理解：**  
柯里化是在运算前提前传参，可以传递多个参数；  
反柯里化是延迟传参，在运算时把原来已经固定的参数或者this上下文等当作参数延迟到未来传递。

---

**附：**

V8引擎中Array.prototype.push方法源码实现：

```text
function ArrayPush() {
    var n = TO_UINT32(this.length);
    var m = %_ArgumentsLength();
    for (var i = 0; i < m; i++) {
        this[i + n] = %_Arguments(i);        // 属性拷贝
        this.length = n + m;                    // 修正length
        return this.length;
    }
}
```

---

> 参考：  
> [JS 柯里化](https://github.com/SHERlocked93/blog/blob/master/Docs/JavaScript%20%E5%87%BD%E6%95%B0%E5%BC%8F%E7%BC%96%E7%A8%8B%E6%8A%80%E5%B7%A7%20-%20%E6%9F%AF%E9%87%8C%E5%8C%96.md)  
> [前端开发者进阶之函数反柯里化unCurrying](https://www.cnblogs.com/pigtail/p/3450852.html)  
> [JavaScript中有趣的反柯里化](http://blog.jobbole.com/32059/)  
> [js柯里化适用场景，优缺点分别是什么，还有个反柯里化？](https://www.zhihu.com/question/40374792/answer/86268208)  
> [JS进阶篇--JS中的反柯里化( uncurrying)](https://segmentfault.com/a/1190000010700130)
