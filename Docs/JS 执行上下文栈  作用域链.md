# JS 执行上下文栈 / 作用域链

## 0、自己理解

代码执行或函数调用生成执行上下文(只有当前执行上下文有执行权)，该执行上下文内只能访问当前执行上下文的变量、函数和上一级执行上下文中的变量、函数，激活下一个执行上下文的时候执行权转移到新的执行上下文，形成执行上下文栈。

作用域是当前执行上下文中能访问的变量、函数的集合，执行上下文中只能访问当前作用域和其上执行上下文的作用域，由此形成作用域链

## 1、执行上下文（栈）

每一次代码执行和函数调用都会产生一个执行环境，称为**执行上下文**(context stack)。  
一个执行上下文`caller`又可以激活（调用）另一个执行上下文`callee`，这时`caller`会暂停自身的执行把控制权交给`callee`进入`callee`的执行上下文，`callee`执行完毕后将控制权交回`caller`，`callee`可以用`return`或者抛出`Exception`来结束自己的执行。  
多个执行上下文会形成执行上下文栈，最顶层是当前执行上下文，底层是全局执行上下文。

![clipboard.png](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/94ae129078741447f713bb4a6689fa545fcb08a8bd1dd1b14be220395dbd0512.png "clipboard.png")

## 2、作用域（链）

**作用域**(scope chain)是每一个执行上下文自身持有的活动对象的集合，如在本执行上下文中声明的变量和函数以及方法参数传入的对象。  
每一个执行上下文可以访问的对象包括自身的作用域和父执行上下文的作用域和父父执行上下文作用域直到全局作用域，这就产生了**作用域链**。作用域链的用途是保证对执行环境有权访问的所有变量和函数的有序访问。

作用域链的工作原理跟原型链十分相似：如果本身的作用域中查找不到标识符，那么就查找父作用域，直到顶层。  
目前假设作用域的联动是用的__parent__对象，它指向作用域链的下一个对象。（在ES5中，确实有一个outer链接）

![clipboard.png](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/dbf640d943b08763008e1d3d28769987476ece9cd76b88fe8fb3acc6d290be47.png "clipboard.png")

全局上下文的作用域包含Object.prototype中的对象，with和catch会改变作用域链，在with中，查询__parent__之前会先去查询__proto__，会使作用域链增大。

### 2.1 作用域链中的名称解析顺序

javascript中一个名字(name)以四种方式进入作用域(scope)，其优先级顺序如下：

1. 语言内置：所有的作用域中都有 this 和 arguments 关键字
2. 形式参数：函数的参数在函数作用域中都是有效的
3. 函数声明：形如function foo() {}
4. 变量声明：形如var bar;

名字声明的优先级如上所示，也就是说如果一个变量的名字与函数的名字相同，那么函数的名字会覆盖变量的名字，无论其在代码中的顺序如何；形式参数会覆盖变量声明。但名字的初始化却是按其在代码中书写的顺序进行的，不受以上优先级的影响。

```text
(function(){
    var foo;
    console.log(typeof foo); //function

    function foo(){}

    foo = "foo";
    console.log(typeof foo); //string
})();
```

如果形参中有多个同名变量,那么最后一个同名参数会覆盖其他同名参数,即使最后一个同名参数未定义;以上的名字解析优先级存在例外，比如可以覆盖语言内置的名字arguments。

### 2.2 with改变作用域链

with语句主要用来临时扩展作用域链，将语句中的对象添加到作用域的头部。

```text
person={name:"yhb",age:22,height:175,wife:{name:"lwy",age:21}};
with(person.wife){
    console.log(name);
}
```

with语句将`person.wife`添加到当前作用域链的头部，所以输出的就是`lwy`。with语句结束后，作用域链恢复正常。

## 3、二维作用域链查找

源于ECMAScript的原型特性。如果一个属性在对象中没有直接找到，查询将在原型链中继续。即常说的二维链查找。

1. 作用域链环节；
2. 每个作用域链－深入到原型链环节

---

> 参考：   
> 1、[执行上下文（栈）/作用域（链）/with](https://link.segmentfault.com/?enc=SaWI9rnAoLfviwFJsnSB5g%3D%3D.6uQzMi0IbSSJpn4hlxeAHHao%2BhEA9ufdQJrcQcQfF5mwhyncoj814VolBvpGskUFizZxSeWFv4QYcgUBn0rF7w%3D%3D)  
> 2、[Js 作用域与作用域链与执行上下文不得不说的故事](https://link.segmentfault.com/?enc=eJ6sN9hAwOz1pvMt3p4OWQ%3D%3D.vZcLIsOI8iqxM3D%2BsX39y2Absi1evGHjD%2FwdzmlXStYSWdRaY4SpNHIJJKc6P57J)
