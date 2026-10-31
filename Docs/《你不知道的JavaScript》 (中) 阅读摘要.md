# 《你不知道的JavaScript》 (中) 阅读摘要

本书属于基础类书籍，会有比较多的基础知识，所以这里仅记录平常不怎么容易注意到的知识点，不会全记，供大家和自己翻阅；

上中下三本的读书笔记：

1. [《你不知道的JavaScript》 (上) 读书笔记](https://github.com/SHERlocked93/blog/blob/master/Docs/%E3%80%8A%E4%BD%A0%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84JavaScript%E3%80%8B%20%28%E4%B8%8A%29%20%E9%98%85%E8%AF%BB%E6%91%98%E8%A6%81.md "https://github.com/SHERlocked93/blog/blob/master/Docs/%E3%80%8A%E4%BD%A0%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84JavaScript%E3%80%8B%20%28%E4%B8%8A%29%20%E9%98%85%E8%AF%BB%E6%91%98%E8%A6%81.md")
2. [《你不知道的JavaScript》 (中) 读书笔记](https://github.com/SHERlocked93/blog/blob/master/Docs/%E3%80%8A%E4%BD%A0%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84JavaScript%E3%80%8B%20%28%E4%B8%AD%29%20%E9%98%85%E8%AF%BB%E6%91%98%E8%A6%81.md "https://github.com/SHERlocked93/blog/blob/master/Docs/%E3%80%8A%E4%BD%A0%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84JavaScript%E3%80%8B%20%28%E4%B8%AD%29%20%E9%98%85%E8%AF%BB%E6%91%98%E8%A6%81.md")
3. [《你不知道的JavaScript》 (下) 读书笔记](https://github.com/SHERlocked93/blog/blob/master/Docs/%E3%80%8A%E4%BD%A0%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84JavaScript%E3%80%8B%20%28%E4%B8%8B%29%20%E9%98%85%E8%AF%BB%E6%91%98%E8%A6%81.md "https://github.com/SHERlocked93/blog/blob/master/Docs/%E3%80%8A%E4%BD%A0%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84JavaScript%E3%80%8B%20%28%E4%B8%8B%29%20%E9%98%85%E8%AF%BB%E6%91%98%E8%A6%81.md")

## 第一部分 类型和语法

### 第二章 值

```js
43.toFixed(3)
// 报错: Invalid or unexpected token
43..toFixed(3)
// "43.000"
```

这是因为`42.toFixed(3)`这里因为`.`被视为常量`42`的一部分，所以没有`.`属性访问运算符来调用`toFixed`方法。而`42..toFixed`则没有问题。

### 第四章 强制类型转换

`JSON.stringify`在对象中遇到`undefined`、`function`、`symbol`时会自动将其忽略，在数组中则会返回`null`，比如：

```js
JSON.stringify([1, 23, 4, null, undefined, function(){ return 123 }])
// "[1,23,4,null,null,null]"
```

JS中的假值 `undefined`、`null`、`false`、`+0`、`-0`、`NaN`、`""`

1. 除了空字符串外的所有字符串都是真值
2. 所有对象都是真值

关于真假值的判断：

```js
new Boolean(false)       // true
new Number(0)            // true
new String("")           // true
Boolean("false")         // true
Boolean("0")             // true
Boolean("''")            // true
Boolean([])              // true
Boolean({})              // true
Boolean(function() {})   // true
```

### 第五章 语法

#### 结果值

语句都有个结果值：

1. 赋值表达式 `b = a` 的结果值是`a`的值
2. 规范定义 `var` 的结果值是 `undefined`
3. 代码块 `{ ... }` 的结果值是其最后一个语句\表达式的结果

标签语句

`{ foo: bar() }` 这里的 `foo` 是**标签语句**，带标签的循环跳转可以使用 `continue\break` 来实现执行标签所在循环的下一轮循环或跳出标签所在循环；

```js
foo: for (var i = 0; i < 4; i++){
    for (var j = 0; j < 4 ; j++){
        if ((i * j) === 3){
            console.log('stoping', i, j)
            break foo;
        }   
        console.log(i, j)
    }
}
// 0 0
// 0 1
// 0 2
// 0 3
// 1 0
// 1 1
// 1 2
// stoping 1 3
```

这里的 `break foo` 不是指跳转到标签 `foo` 所在位置继续执行，而是跳出标签 `foo` 所在的循环/代码块，继续执行后面的代码。因此这里的标签语句并非传统意义上的 `goto`；

关联

运算符有优先级，那么如果多个相同优先级的运算符同时出现，执行的顺序就和关联顺序有关了，JS默认的执行顺序是从左到右，但是有时候不是，比如：

1. `? :` 三元运算符是右关联，比如`? : ? :` ，其实是`? : (? :)` 这样的顺序
2. `= =` 连等是右关联，比如 `a=b=c=2`，其实是 `(a=(b=(c=2)))`

#### 函数参数

像函数传递参数时，`arguments` 数组中对应单元会和命名参数建立关联(linkage)以得到相同的值；相反，不传递参数就不会建立关联：

```js
function foo(a){
    a=42
    console.log(arguments[0])
}
foo(2)             // 42
foo()            // undefined
```

注意：严格模式没有建立关联一说；

#### try...finally

`finally` 中的代码总是会在 `try` 之后执行，即使 `try` 中已经 return 了，如果有 `catch` 的话则在 `catch` 之后执行；

```js
function foo(){
    try{
        return('returned')
    } finally {
        console.log('finally')
    }
}
console.log(foo())
// finally
// returned
```

1. 如果 `finally` 中抛出异常，函数会终值，如果之前 `try` 中已经 return 了返回值，则返回值会被丢弃；
2. `finally` 中的 return 会覆盖 `try` 和 `catch` 中 return 的返回值；
3. `finally` 中如果没有 return，则会返回前面 return 的返回值；

#### switch

`switch` 中的 `case` 执行的匹配是 `===` 严格相等的，也就是说如果不是 true，是真值也是不通过的：

```js
switch(true) {
    case ('hello' || 10):
        console.log('world')    // 不会执行
        break;
    default:
        console.log('emmm')
}
// emmm
```

所以这里的字符串即使是真值，也是不被匹配，所以可以通过强制表达式返回 Boolean 值，比如 `!!('hell0' || 10)`

`default` 是可选的，无需放在最后一个，且并非必不可少：

```js
switch(10){
    case 1:
    case 2:
    default:
        console.log('hello')
    case 3:
        console.log(3)
        break;
    case 4:
        console.log(4)
}
// hello
// 3
```

上面这个例子的逻辑是：首先找匹配的 case，没找到则运行 `default`，因为其中没有 break，所以继续执行 `case 3` 中的代码，然后 break；

### 附录

#### 全局 DOM 变量

由于浏览器历史遗留问题，在创建带有 `id` 属性的 DOM 元素的时候也会创建同名的全局变量：

```html
<div id='foo'><div>
<scripts>
   console.log(foo)     // 打印出DOM元素
</scripts>
```

所以说 HTML 中尽量少用 id 属性...

## 第二部分 异步和性能

### 第一章 异步：现在和将来

#### 异步控制台

某些浏览器的 `console.log` 并不会把传入的内容立即输出，原因是在许多程序(不只是JS)中，I/O 是非常低速的阻塞部分，所以，从页面\UI的角度来说，浏览器在后台异步处理控制台 I/O 能够提高性能，这时用户可能根本意识不到其发生。

```js
var a = { b: 1 }
console.log(a)
a.b++
```

这时候控制台看到的是 a 对象的快照 `{b:1}`，然而点开看详情的话是 `{b:2}` ；这段代码在运行的时候，浏览器可能会认为需要把控制台 I/O 延迟到后台，这种情况下，等到浏览器控制台输出对象内容时，`a.b++` 可能已经运行，因此会在点开的时候显示 `{b:2}`，这是 I/O 的异步化造成的。

如果遇到这种情况：

1. 使用JS调试器中的断点，而不要依赖控制台输出；
2. 把对象序列化到一个字符串中，以强制执行一次快照，比如通过 `JSON.stringify`；

### 第三章 Promise

#### 回调未调用

如果 Promise 状态一直未改变，怎么得到通知呢，这里可以使用 `Promise.race` 竞态，如果在设置时间内还未返回，那么 Promise 将会被 `reject`；

```js
function timeoutPromise(delay) {
  return new Promise((resolve, reject) => {
    setTimeout(() => { reject('Timeout!') }, delay)
  })
}

Promise.race([foo(), timeoutPromise(3000)])
  .then(() => console.log('Promise 及时完成'))
  .catch(() => console.log('Promise 超时了'))
```

### 第四章 生成器

#### 输入和输出

```js
function* foo(x) {
  return x * (yield 'hello')
}
const it = foo(6)

let res = it.next()
res.value       // hello

res = it.next(7)
res.value       // 42
```

可以看到第一个 `next` 并没有传参，因为只有暂停的 `yield` 才能接受这样一个通过 `next` 传递的参，而在生成器刚生成还没有 `next()` 这时候还没有暂停的 `yield` 来接受这样一个值，所以会默默丢弃传递给第一个 `next` 的任何参数。

#### 生成器中的 Promise 并发

```js
function* foo() {
  const r1 = yield request('http://some.url.1')
  const r2 = yield request('http://some.url.2')
}
```

这种方式的两个请求是串行的，`yield` 只是代码中一个单独的暂停点，不能同时在两个点上暂停，如果希望并行的发送，那么考虑：

```js
function* foo() {
  const p1 = request('http://some.url.1')
  const p2 = request('http://some.url.2')
  const r1 = yield p1
  const r2 = yield p2
}
```

---
