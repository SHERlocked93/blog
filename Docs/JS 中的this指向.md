# JS 中的this指向

为什么要学习this？如果你学过面向对象编程，那你肯定知道干什么用的，如果你没有学过，那么暂时可以不用看这篇文章，当然如果你有兴趣也可以看看，毕竟这是js中必须要掌握的东西。

## 1. this指向调用他的对象

首先必须要说的是，**this的指向在函数定义的时候是确定不了的，只有函数执行的时候才能确定this到底指向谁，实际上this的最终指向的是那个调用它的对象**（这句话有些问题，后面会解释为什么会有问题，虽然网上大部分的文章都是这样说的，虽然在很多情况下那样去理解不会出什么问题，但是实际上那样理解是不准确的，所以在你理解this的时候会有种琢磨不透的感觉），那么接下来我会深入的探讨这个问题。

例子1：

```text
function a(){
    var user = "呵呵";
    console.log(this.user); //undefined
    console.log(this); //Window
}
a();
```

按照我们上面说的this最终指向的是调用它的对象，这里的函数a实际是被Window对象所点出来的，下面的代码就可以证明。

```text
function a(){
    var user = "呵呵";
    console.log(this.user);  // undefined
    console.log(this);　　// Window
}
window.a();
```

和上面代码一样吧，其实alert也是`window`的一个属性，也是`window`点出来的。

例子2：

```text
var o = {
    user:"呵呵"，
    fn:function(){
        console.log(this.user);  // 呵呵
    }
}
o.fn();
```

　　这里的this指向的是对象`o`，因为你调用这个fn是通过`o.fn()`执行的，那自然指向就是对象`o`，这里再次强调一点，this的指向在函数创建的时候是决定不了的，在调用的时候才能决定，谁调用的就指向谁，一定要搞清楚这个。

其实例子1和例子2说的并不够准确，下面这个例子就可以推翻上面的理论。

## 2. this指向最后一个调用它的对象

如果要彻底的搞懂this必须看接下来的几个例子

例子3：

```text
var o = {
    user:"呵呵"，
    fn:function(){
        console.log(this.user);  // 呵呵
    }
}
window.o.fn();
```

　　这段代码和上面的那段代码几乎是一样的，但是这里的`this`为什么不是指向`window`，如果按照上面的理论，最终`this`指向的是调用它的对象，这里先说个而外话，`window`是js中的全局对象，我们创建的变量实际上是给`window`添加属性，所以这里可以用`window`点o对象。

　　这里先不解释为什么上面的那段代码this为什么没有指向window，我们再来看一段代码。

```text
var o = {
    a:10，
    b:{
        a:12，
        fn:function(){
            console.log(this.a); //12
        }
    }
}
o.b.fn();
```

　　这里同样也是对象o点出来的，但是同样this并没有执行它，那你肯定会说我一开始说的那些不就都是错误的吗？其实也不是，只是一开始说的不准确，接下来我将补充一句话，我相信你就可以彻底的理解this的指向的问题。

- 情况1：如果一个函数中有`this`，但是它没有被上一级的对象所调用，那么`this`指向的就是window，这里需要说明的是在js的严格版中`this`指向的不是window，而是undefined。
- 情况2：如果一个函数中有`this`，这个函数有被上一级的对象所调用，那么this指向的就是上一级的对象。
- 情况3：如果一个函数中有`this`，这个函数中包含多个对象，尽管这个函数是被最外层的对象所调用，this指向的也只是它上一级的对象，例子3可以证明，如果不相信，那么接下来我们继续看几个例子。

```text
var o = {
    a:10，
    b:{
        // a:12，
        fn:function(){
            console.log(this.a); //undefined
        }
    }
}
o.b.fn();
```

尽管对象b中没有属性a，这个`this`指向的也是对象b，因为`this`只会指向它的上一级对象，不管这个对象中有没有this要的东西。

## 3. this`永远`指向最后调用它的对象

还有一种比较特殊的情况，例子4：

```text
var o = {
    a:10，
    b:{
        a:12，
        fn:function(){
            console.log(this.a); //undefined
            console.log(this); //window
        }
    }
}
var j = o.b.fn;
j();
```

这里`this`指向的是`window`，是不是有些蒙了？其实是因为你没有理解一句话，这句话同样至关重要。

**this永远指向的是最后调用它的对象**，也就是看它**执行**的时候是谁调用的，例子4中虽然函数fn是被对象b所引用，但是在将fn赋值给变量j的时候并没有执行所以最终指向的是window，这和例子3是不一样的，例子3是直接执行了fn。

## 4. 构造函数中的this

构造函数版this：

```text
function Fn(){
    this.user = "呵呵";
}
var a = new Fn();
console.log(a.user);     // 呵呵
```

这里之所以对象`a`可以点出函数Fn里面的`user`是因为`new`关键字可以改变`this`的指向，将这个`this`指向对象a，为什么我说a是对象，因为用了new关键字就是创建一个对象实例，理解这句话可以想想我们的例子3，我们这里用变量a创建了一个Fn的实例（相当于复制了一份Fn到对象a里面），此时仅仅只是创建，并没有执行，而调用这个函数Fn的是对象a，那么`this`指向的自然是对象a，为什么对象a中会有`user`，因为你已经复制了一份Fn函数到对象a中，用了new关键字就等同于复制了一份。

`new`操作符会改变函数this的指向问题，这里稍微带过一下，高程上有详细讲解可以翻阅一下。

```text
function fn(){
    this.num = 1;
}
var a = new fn();
console.log(a.num); // 1
```

为什么`this`会指向a？首先`new`关键字会创建一个空的对象，然后会自动调用一个函数apply方法，将`this`指向这个空对象，这样的话函数内部的this就会被这个空的对象替代。  
注意: 当你new一个空对象的时候，js内部的实现并不一定是用的apply方法来改变this指向的，这里只是打个比方

除了上面的这些以外，我们还可以自行改变this的指向，关于自行改变this的指向请看JavaScript中`call，apply，bind`方法的总结性文章。

## 5. 当this碰到return时

```text
function fn()  {  
    this.user = '呵呵';  
    return {};  
}
var a = new fn;  
console.log(a.user); //undefined
```

再看一个

```text
function fn()  {  
    this.user = '呵呵';  
    return function(){};
}
var a = new fn;  
console.log(a.user); //undefined
```

再来

```text
function fn()  {  
    this.user = '呵呵';  
    return 1;
}
var a = new fn;  
console.log(a.user);    // 呵呵
```

```text
function fn()  {  
    this.user = '呵呵';  
    return undefined;
}
var a = new fn;  
console.log(a.user);    // 呵呵
```

什么意思呢？

如果返回值是一个对象，那么`this`指向的是构造函数的实例但是并没有被返回，如果返回值不是一个对象那么`this`还是指向构造函数创建的实例。

```text
function fn()  {  
    this.user = '呵呵';  
    return undefined;
}
var a = new fn;  
console.log(a);     // fn {user: "呵呵"}
```

还有一点就是虽然null也是对象，但是在这里this还是指向那个函数的实例，因为null比较特殊。

```text
function fn()  {  
    this.user = '呵呵';  
    return null;
}
var a = new fn;  
console.log(a.user); // 呵呵
```

注意：在严格版中的默认的this不再是window，而是undefined

## 6. 箭头函数中的this

箭头函数是ES6的新特性，最重要的特点是它会捕获其所在上下文的this作为自己的this，或者说，箭头函数本身并没有this，它会沿用外部环境的this。也就是说，箭头函数内部与其外部的this是保持一致的。

```text
this.a=20
var test={
    a:40，
    init:()=>{
        console.log(this.a)
        function go(){
            this.a=60
            console.log(this.a)
        }
        go.prototype.a=50
        return go
    }   
}

var p=test.init()
p()
new (test.init())()
```

输出 20 60 60 60

解释一下：

1. `this.a=20`这个this是window应该毫无疑问，这里在全局变量window上创建了个属性a并赋值为20
2. 首先执行的是`test.init()`，这是一个箭头函数，箭头函数不创建新的函数作用域直接沿用语句外部的作用域，因此`test.init()`执行时的箭头函数中this是全局window，首先打印出window上的属性a的值**20**，箭头函数返回了一个原型上有个值为50的属性a的函数对象`go`给p
3. 继续执行的是`p()`，这里执行的是刚刚箭头函数返回的`go`，`go`执行的是闭包，内部的tihs指向的还是window，因此首先`this.a`修改了window.a的值为**60**并打印出来
4. 再执行的是`test.init()`，这个箭头函数中的this指向全局window刚刚已经说了，但是这时候window.a已经被修改为60了，因此再打印一个**60**，这个箭头函数返回了一个新建的函数对象`go`，下面为了方便起见起名字叫`go1`
5. 然后执行的是`new go1()`，根据之前的表述new操作符会在`go1`函数中创建一个继承了`go1`原型的实例对象并用this指向它，随后`this.a=60`又在实例对象上创建了一个属性a，在之后的打印中已经在实例上找到了属性a，因此就不继续往对象原型上查找了，所以打印出第三个**60**

```text
this.a=20
var test={
    a:40，
    init:function (){
        console.log(this.a)
        function go(){
            this.a=60
            console.log(this.a)
        }
        go.prototype.a=50
        return go
    }

}

var p=test.init()
p()
new (test.init())()
```

输出 40 60 40 60

这里就不解释了，如果这两个例子都搞懂，基本上this的指向也就差不多掌握啦~

---

> 参考：  
> 1、[彻底理解js中this的指向，不必硬背](https://link.segmentfault.com/?enc=hwPhHfabVQYn%2B8kgZI11gw%3D%3D.6A2wMWN5ooxhn3VgNTHBWAdOb36z0BNy0zCMUQjIb371gl8LGv7iLPyLhtxp52MC)  
> 2、[偶遇this之坑](https://link.segmentfault.com/?enc=zHEHLQdFXVqbhYHshVu6Rg%3D%3D.b0jbfGt7A7oBSdhxioQMBW5hpJJOW2zB%2BtC4pig3C%2BjQot9CC0eImkLf5hv2Tn1m)  
> 3、[JS中call、apply、bind使用指南，带部分原理。](https://link.segmentfault.com/?enc=0SF%2FaAjMnhvv633dotnMzA%3D%3D.ASoiIzDyI%2BL7Ncp60L4eV2ut0dMNc%2FO7KW%2F57Qpq4V4YgqkmpilahbuIhBX1n7Sz)  
> 4、[那些年我们一起过的JS闭包，作用域，this，让我们一起划上完美的句号。](https://link.segmentfault.com/?enc=ux272gjlMjjhDyJ3ouMy9A%3D%3D.M8FG%2BNFuJkKMsIrgW4Ck%2FbP7sl4usUWmL9fHSsMszo0%2FSZsxBR4FgP4p7h6Z3pEF)  
> 5、[Nodejs中的this](https://link.segmentfault.com/?enc=WDW6gdhVrKZEXaIzb4VAJw%3D%3D.x6O36wPpumkFZnh4nT9O8YQ9341b4et41Z9OSoIIvVbh1twhDAk%2Bl%2FxfE4puvIzk)
