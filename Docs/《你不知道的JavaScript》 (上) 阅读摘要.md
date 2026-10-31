# 《你不知道的JavaScript》 (上) 阅读摘要

本书属于基础类书籍，会有比较多的基础知识，所以这里仅记录平常不怎么容易注意到的知识点，不会全记，供大家和自己翻阅；

上中下三本的读书笔记：

1. [《你不知道的JavaScript》 (上) 读书笔记](https://github.com/SHERlocked93/blog/blob/master/Docs/%E3%80%8A%E4%BD%A0%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84JavaScript%E3%80%8B%20%28%E4%B8%8A%29%20%E9%98%85%E8%AF%BB%E6%91%98%E8%A6%81.md "https://github.com/SHERlocked93/blog/blob/master/Docs/%E3%80%8A%E4%BD%A0%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84JavaScript%E3%80%8B%20%28%E4%B8%8A%29%20%E9%98%85%E8%AF%BB%E6%91%98%E8%A6%81.md")
2. [《你不知道的JavaScript》 (中) 读书笔记](https://github.com/SHERlocked93/blog/blob/master/Docs/%E3%80%8A%E4%BD%A0%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84JavaScript%E3%80%8B%20%28%E4%B8%AD%29%20%E9%98%85%E8%AF%BB%E6%91%98%E8%A6%81.md "https://github.com/SHERlocked93/blog/blob/master/Docs/%E3%80%8A%E4%BD%A0%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84JavaScript%E3%80%8B%20%28%E4%B8%AD%29%20%E9%98%85%E8%AF%BB%E6%91%98%E8%A6%81.md")
3. [《你不知道的JavaScript》 (下) 读书笔记](https://github.com/SHERlocked93/blog/blob/master/Docs/%E3%80%8A%E4%BD%A0%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84JavaScript%E3%80%8B%20%28%E4%B8%8B%29%20%E9%98%85%E8%AF%BB%E6%91%98%E8%A6%81.md "https://github.com/SHERlocked93/blog/blob/master/Docs/%E3%80%8A%E4%BD%A0%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84JavaScript%E3%80%8B%20%28%E4%B8%8B%29%20%E9%98%85%E8%AF%BB%E6%91%98%E8%A6%81.md")

## 第一部分 作用域和闭包

### 第二章 词法作用域

#### 词法查找

全局变量会自动成为**全局对象**(浏览器中是 `window`) 的属性，因此是不可以直接通过全局对象的此法名称，而是间接地通过全局对象属性的应用来对其进行访问 `window.a`，通过这种方法可以访问那些被同名变量所遮蔽的全局变量。但是如果非全局的变量如果被遮蔽了，无论如何都无法被访问到。

#### 欺骗词法

如果词法作用域完全由写代码期间函数所生命的位置来定义，那么可以通过几种方法来欺骗(修改)词法作用域，比如 `eval`、`with` 但是要注意：**欺骗词法作用域会导致性能下降**。

因为JS引擎会在编译阶段进行性能优化，其中有些优化依赖于能够根据代码的词法进行静态分析，并预先确定所有变量和函数的定义位置，才能在执行过程中快速找到标识符。但是如果引擎在代码中找到 `eval`、`with` ，就会**完全不做**任何优化。

### 第三章 函数作用域和块作用域

#### 函数作用域

包装函数的声明以 `function` 关键字开始，那么就是函数声明，而下面这个例子是以 `(function` 开始，那么就是函数表达式：

```js
const a = 1;

function foo() {        // 函数声明
  const a = 4;
  console.log(a);
}

(function foo() {        // 函数表达式
  const a = 3;
  console.log(a);
}())
console.log(a);
```

所以上面的 `IIFE` 将会被当做函数表达式而不是一个函数声明来处理；

**函数声明**和**函数表达式**之间最重要的区别是他们的名称标识符会绑定在何处。

函数声明的名称标识符 `foo` 会被绑定在所在作用域中，可以直接通过 `foo()` 来调用；而函数表达式的 `foo` 被绑定在函数表达式只剩的函数中而不是所在作用域中；

同时，即使是具名的函数表达式，名称标识符在赋值之前也无法在所在作用域中使用。

`try/catch` 结构的 `catch` 分句中具有块级作用域。

### 第四章 提升

#### 编译器

**函数声明**会被提升，而**函数表达式**不会被提升。

#### 函数优先

函数声明和变量声明都会被提升，但是函数会首先被提升，然后才是变量。

```js
foo()        // 1
var foo

function foo() {
  console.log(1)
}

foo = function() {
  console.log(2)
}
```

函数声明 `foo` 会首先被提升，然后打印出 `1`，后面的 `var` 声明会被认为是重复声明而被忽略；但是注意如果后面出现同名函数声明，则会覆盖前面的：

```js
foo()        // 2
function foo() { console.log(1) }
function foo() { console.log(2) }
```

## 第二部分 this和对象原型

### 第一章 关于this

#### this到底是什么

`this` 实际上是在函数被调用时发生的绑定，它指向什么完全取决于函数在哪里被调用，并不是在编写时绑定。当一个函数被调用时，会创建一个执行上下文，它包含函数在哪里被调用(调用栈)、函数的调用方式、传入的参数等信息，`this` 就是这个记录的一个属性，会在函数执行的过程中用到。

#### 判断this

我们可以根据优先级来判断 `this`：

1. **new 绑定：** 函数是否是在 `new` 中调用，如果是的话， `this` 绑定的是新创建的对象；

   `var bar = new foo()`
2. **显式绑定：** 函数是否通过 `call`、`apply` 或者硬绑定调用，如果是的话，`this` 绑定的是指定的对象；

   `var bar = foo.call(obj)`
3. **隐式绑定：** 函数是否在某个上下文对象中调用，如果是的话 `this` 绑定的是那个上下文对象；

   `var bar = obj.foo()`
4. **默认绑定：** 如果都不是的话，在严格模式下绑定到 `undefined` ，非严格模式绑定到全局对象；

   `var bar = foo()`

#### 例外

1. **被忽略的情况：** 比如把 `null`、`undefined` 作为 `this` 的绑定对象传入 `call`、`apply`、`bind` ，那么这些值在调用时会被忽略，实际应用的是默认绑定；
2. **箭头函数：** 箭头函数根据外层作用域来决定 `this`，且箭头函数的绑定无法被修改，`new` 也不可以；

---
