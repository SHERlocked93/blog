# JS 中的 __proto__ 与 prototype

## __proto__ 探究

`__proto__`隐式原型与`prototype`显式原型是个容易令人混淆的概念，简而言之`prototype`是构造函数用来被自己的实例继承的原型，而`_proto_`是实例用来继承父类原型的载体。

### 1. 是什么

#### 显式原型 explicit prototype property

每一个函数在创建之后都会拥有一个名为`prototype`的属性，这个属性指向函数的原型对象，定义了该构造函数创建的所有实例对象共享的属性。  
**Note:**通过`Function.prototype.bind`方法构造出来的函数是个例外，它没有`prototype`属性

> NOTE Function objects created using Function.prototype.bind do not have a prototype property or the [[Code]], [[FormalParameters]], and [[Scope]] internal properties. ----- [ECMAScript Language Specification](https://link.segmentfault.com/?enc=8G85xqk%2FJunZpXAhP%2BAfxg%3D%3D.p9RiCc4qaSIkG1BbPVh1Q9s4xm5yILbUpeTQbmh7UwrsDISzLGGlcmujeoN5QLIAzTHB3hgyPeZURXf6pFzo7bFhxyD%2B8D242LC%2Bj%2Ft49AjcwO466Q4TQg8z5POgOFyB)

#### 隐式原型 implicit prototype link

JavaScript中任意对象都有一个内置属性`[[prototype]]`，在ES5之前没有标准的方法访问这个内置属性，但是大多数浏览器都支持通过`__proto__`来访问。ES5中有了对于这个内置属性标准的Get方法，`Object.getPrototypeOf()` 。  
`__proto__`是浏览器自实现的`[[prototype]]`

#### 二者的关系

隐式原型指向创建这个对象的函数（构造函数constructor）的显式原型`prototype`

```text
function Person(name) {this.name = name}
var person1 = new Person
console.log(person1.__proto__ === Person.prototype)                    // true
console.log(Object.getPrototypeOf(person1) === person1.__proto__)        // true
console.log(person1.prototype === person1.__proto__)                    // false
console.log(Object.getPrototypeOf(Person) === Person.__proto__)    // true
console.log(Person.prototype===Person.__proto__)                        // false
console.log(person1.constructor === Person)                                // true
```

### 2. 作用是什么

- 显示原型的作用：用来实现基于原型的继承与属性的共享。

> ECMAScript does not use classes such as those in C++, Smalltalk, or Java. Instead objects may be created in various ways including via a literal notation or via constructors which create objects and then execute code that initialises all or part of them by assigning initial values to their properties. Each constructor is a function that has a property named “prototype” that is used to implement prototype-based inheritance and shared properties.Objects are created by using constructors in new expressions; for example, new Date(2009,11) creates a new Date object. ---- [ECMAScript Language Specification](https://link.segmentfault.com/?enc=3KDKO73B3lBaUsQy35q0Lw%3D%3D.S5mlmuo%2BqyPPqCBy9TKXAnRa6RagO%2FO%2F%2FK8CDoB2zITm2wytsqvEbldE6Fr5ZEv2rzp%2BKU2OFFo9fjdmgbkcEIzkL8x97zUGvvuucFDgc0%2BDuefK%2BFqf%2Fcg7zcjWpOep)

- 隐式原型的作用：构成原型链，同样用于实现基于原型的继承。举个例子，当我们访问obj这个对象中的x属性时，如果在obj中找不到，那么就会沿着__proto__依次查找。

> Every object created by a constructor has an implicit reference (called the object’s prototype) to the value of its constructor’s “prototype” ---- [ECMAScript Language Specification](https://link.segmentfault.com/?enc=L20uE8fq8ITlfGC%2B%2BB01Pw%3D%3D.f9wP%2FCa1LHCNLE2WUjiyQvGuFojgI2S8u5XCvOsvzMBuqMLg%2F5JD17Lfbfj4xSdrCA46SPFu2%2BqV%2BvzJGfEwiTX8rlxOg6%2BLyG%2F%2FIMaSJXVyIvTw2enQh8LNeauRQgRs)

### 3. __proto__的指向

`__proto__`的指向到底如何判断呢？根据ECMA定义 'to the value of its constructor's "prototype" ' ----指向创建这个对象的函数（构造函数）的显式原型。所以关键的点在于找到创建这个对象的构造函数，接下来就来看一下JS中对象被创建的方式，一眼看过去似乎有三种方式：对象字面量的方式 、new 的方式 、ES5中的Object.create() 但是我认为本质上只有一种方式，也就是通过new来创建。为什么这么说呢，首先字面量的方式是一种为了开发人员更方便创建对象的一个语法糖，本质就是 `var o = new Object(); o.xx = xx;o.yy=yy;` 再来看看Object.create(),这是ES5中新增的方法，在这之前这被称为原型式继承

> 道格拉斯在2006年写了一篇文章，题为 Prototypal Inheritance In JavaScript。在这篇文章中，他介绍了一种实现继承的方法，这种方法并没有使用严格意义上的构造函数。他的想法是借助原型可以基于已有的对象创建新对象，同时还不比因此创建自定义类型，为了达到这个目的，他给出了如下函数:

```text
 function object(o){
    function F(){}
    F.prototype = o;
    return new F()
}
```

----- 《JavaScript高级程序设计》P169

所以从实现代码 return new F() 中我们可以看到，这依然是通过new来创建的。不同之处在于由 Object.create() 创建出来的对象没有构造函数，看到这里你是不是要问，没有构造函数我怎么知道它的`__proto__`指向哪里呢，其实这里说它没有构造函数是指在 Object.create() 函数外部我们不能访问到它的构造函数，然而在函数内部实现中是有的，它短暂地存在了那么一会儿。假设我们现在就在函数内部，可以看到对象的构造函数是F, 现在

```text
// 以下是用于验证的伪代码
var f = new F(); 
// 于是有
f.__proto__ === F.prototype         // true
// 又因为
F.prototype === o;            // true
// 所以
f.__proto__ === o;
```

因此由Object.create(o)创建出来的对象它的隐式原型指向o。好了，对象的创建方式分析完了，现在你应该能够判断一个对象的__proto__指向谁了。  
好吧，还是举一些一眼看过去比较疑惑的例子来巩固一下。

- 构造函数的显示原型的隐式原型：

**内建对象**(built-in object)：比如Array()，Array.prototype.__proto__指向什么？Array.prototype也是一个对象，对象就是由 Object() 这个构造函数创建的，因此`Array.prototype.__proto__ === Object.prototype //true`，或者也可以这么理解，所有的内建对象都是由Object()创建而来。

- 自定义对象

**默认情况下：**

```text
function Foo(){}
var foo = new Foo()
Foo.prototype.__proto__ === Object.prototype         // true 理由同上
```

**其他情况：**

```text
function Bar(){}
//这时我们想让Foo继承Bar
Foo.prototype = new Bar()
Foo.prototype.__proto__ === Bar.prototype //true
```

```text
//我们不想让Foo继承谁，但是我们要自己重新定义Foo.prototype
Foo.prototype = {
  a:10,
  b:-10
}
//这种方式就是用了对象字面量的方式来创建一个对象，根据前文所述 
Foo.prototype.__proto__ === Object.prototype
```

**Note：** 以上两种情况都等于完全重写了Foo.prototype，所以Foo.prototype.constructor也跟着改变了，于是乎constructor这个属性和原来的构造函数Foo（）也就切断了联系。

- 构造函数的隐式原型

既然是构造函数那么它就是Function（）的实例，因此也就指向Function.prototype,比如 `Object.__proto__ === Function.prototype`

### 4. instanceof

instanceof 操作符的内部实现机制和隐式原型、显式原型有直接的关系。instanceof的左值一般是一个对象，右值一般是一个构造函数，用来判断左值是否是右值的实例。它的内部实现原理是这样的：

```text
// 设 L instanceof R 
// 通过判断
L.__proto__.__proto__ ..... === R.prototype ？
// 最终返回true or false
```

也就是沿着L的`__proto__`一直寻找到原型链末端，直到等于R.prototype为止。知道了这个也就知道为什么以下这些奇怪的表达式为什么会得到相应的值了，所有构造函数都是`Fucntion`的实例，所有对象都是`Object`的实例

```text
Function instanceof Object // true 
Object instanceof Function // true 
Function instanceof Function //true
Object instanceof Object // true
Number instanceof Number //false
```

### 5. Js对象体系结构

![clipboard.png](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/dc60e162e994ae5834c0f65450332d6e47ff59bc4bfb65902f8646f3a4ff6a17.png "clipboard.png")

- 每一个对象都有`__proto__`，谁创建的对象（继承谁），`__proto__`就指向谁的`prototype`
- 所有的函数都是由Function()创建的，所以所有的函数的`__proto__`就指向Function的`prototype`，包括它自己
- 函数有`prototype`，普通实例对象没有，且函数的`prototype`都有一个自有属性`constructor`指向自己
- 所有的`prototype`也是对象，是由Object()创建（继承Object）而来的，所以所有的`prototype`的`__proto__`都指向Object

### 6. 谨慎操作`__proto__`

[警告:](https://link.segmentfault.com/?enc=kfEZOWKVr8g2FHEoNaH8MA%3D%3D.6A001geDiVg1jGlNO8Q9TLJPalj8451d207QnOhyL66HPcMry5eLYJL%2FXxqTnLsnnHv%2BPVtAnmRLd3Zarav%2BIPj6yWMjU0BRUYM748SAmC3YxaWMsYSfhA7hNfPQ5AmHOEPtn8LoJIP40NfARjesVQ%3D%3D) 由于现代 JavaScript 引擎优化属性访问所带来的特性的关系，更改对象的 `[[Prototype]]`在各个浏览器和 JavaScript 引擎上都是一个很慢的操作。其在更改继承的性能上的影响是微妙而又广泛的，这不仅仅限于 `obj.__proto__ = ...` 语句上的时间花费，而且可能会延伸到任何代码，那些可以访问任何`[[Prototype]]`已被更改的对象的代码。如果你关心性能，你应该避免设置一个对象的 `[[Prototype]]`。相反，你应该使用 `Object.create()`来创建带有你想要的`[[Prototype]]`的新对象。

---

> 参考：  
> 1、[js中__proto__和prototype的区别和关系？](https://link.segmentfault.com/?enc=21aql5%2B7VdlFtzWLoTIOvg%3D%3D.eb80ibBuxr09ldudsnAGR42oXj2oScNWzntFfdmnAAkFNiQVI0%2FlouTZsbtLK4FI)  
> 2、[G小调的悲伤的博客](https://link.segmentfault.com/?enc=rbSeeQAG29aBe0GRXVSoqw%3D%3D.hzV4dtIPqvzTMa2hFHvtL%2Fu8MqdTFZD8N2CovxQoYjuhPLCRNk406DrH%2F4BYdGKgu%2BlyVFOrXPoGiUkHwuPT3bm%2Bpwe5dyPdmdR4izCHXo68AgqGzkPXm%2FCtV%2Bzjx3hc4ej2RvS3Kac2nfvr7urs1A%3D%3D)  
> 3、[JavaScript instanceof 运算符深入剖析](https://link.segmentfault.com/?enc=Uo6RNOMB3EyOnaasTkkq2A%3D%3D.ovngDYDpYwYncaw7ibDieSSqYLoc%2BnrNSABwbOCHn0jEDCG9MFSWlpLbJPaqm%2B%2F62Sxt42kq7PLeFyu1BxY4h5z9HQtmCOi8dBLW5puLVvWyNndVANUHSMiSFuu0Y%2BMEyaw9cvvkhw2VULgEH37T1A%3D%3D)
