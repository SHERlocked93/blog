# 《JavaScript 面向对象精要》 阅读摘要

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/a2699a8f35991ee9c0f10d046bc4712064670d1c0c8beaa7ea7ae9aad7ad0c3b.jpg)

高程面向对象这块内容介绍的比较浅显，个人觉得这本小书是高程的补充，看完之后觉得收获匪浅，所以做了个笔记，以备后询

## 1. 原始类型和引用类型

Js中两种基本数据类型：`原始类型`（基本数据类型）和`引用类型`；  
`原始类型`保存为简单数据值，`引用类型`则保存为对象，其本质是指向内存位置的应用。  
其它编程语言用栈存储`原始类型`，用堆存储`引用类型`，而js则不同：它使用一个变量对象追踪变量的生存期。原始值被直接保存在变量对象里，而引用值则作为一个指针保存在变量对象内，该指针指向实际对象在内存中的存储位置。

### 1.1 原始类型（基本数据类型）

Js中一共有5种原始类型：`boolean`、`number`、`string`、`null`、`undefined`，除了`null`类型，都可以用`typeof`来判断  
原始类型的变量直接保存原始值（而不是一个指向对象的指针），当原始值被赋给一个变量，该值将被复制到变量中，每个变量有它自己的一份数据拷贝

```text
var color1='red',color2=color1
console.log(color1)    // red
console.log(color2)    // red
color1='blue'
console.log(color2)    // red
```

### 1.2 引用类型

**对象**（引用值）是引用类型的实例。对象是属性的无序列表，**属性**包含键和值，如果一个属性的值是函数，它就被称为**方法**；  
Js中的函数其实是引用值，除了函数可以运行以外，一个包含数组的属性和一个包含函数的属性没什么区别。  
Js中的构造函数用首字母大写来跟非构造函数区分：`var object = new Object()`  
因为引用类型不在变量中直接保存对象，所以`object`变量实际上并不包含对象的实例，而是一个指向内存中实际对象所在位置的指针。

```text
var object1 = new Object()
var object2 = object1
```

一个变量赋值给另一个变量时，两个变量各获得一个指针的拷贝，并且指向同一个内存中的对象实例。  
对象不使用时可以将引用解除：`object = null`，内存中的对象不再被引用时，垃圾收集器（GC）会把那块内存挪作他用，在大型项目中尤为重要

### 1.3 原始封装类型

**原始封装类型**共3种：`String`、`Number`、`Boolean`，使用起来跟对象一样方便，当读取这三种类型时，原始封装类型将被自动创建：

```text
var name = "Nicholas"
var fisrtChar = name.charAt(0)
console.log(firstChar)                        // N
```

背后发生的故事：

```text
// what js engine does
var name = "Nicholas"
var temp = new String(name)            // 字符串对象
var firstChar = temp.charAt(0)
temp = null
console.log(firstChar)                         // N
```

Js引擎创建了一个字符串的实例让charAt(0)可以工作，字符串对象的存在仅用于该语句并且在随后被销毁（一种被称为自动打包的过程）。可以测试：

```text
var name = "Nicholas"
name.last = "zakas"
console.log(name.last)                // undefined
```

原始封装类型的属性会消失是因为被添加属性的对象立刻就被销毁了。  
背后的故事：

```text
var name = "Nicholas"
var temp = new String(name)
temp.last = "zakas"
temp = null                                            // temp对象销毁

var temp = new String(name)
console.log(temp.last)                           // undefined
temp = null
```

实际上是在一个立刻就被销毁的临时对象上而不是字符串上添加了新的属性，之后试图再访问该属性，另一个不同的临时对象被创建，而新属性并不存在。虽然原始封装类型会被自动创建，在这些值上进行的`instanceof`检查对应类型的返回值却是`false`

```text
var name = 'Nicholas', count = 10, found = false
console.log(name instanceof String)                    // false
console.log(count instanceof Number)                // false
console.log(found instanceof Boolean)                // false
```

这是因为临时对象仅在值（属性）被读取时被创建，`instanceof`操作符并没有真的读取任何东西，也就没有临时对象的创建。  
如果使用手动创建对象和原始封装类型之间有一定区别，比如：

```text
var found = new Boolean(false)
if (found) {
    console.log("Found")            // 执行了，因为对象在if条件判断时总被认为是true，无论该对象是不是false，所以尽量避免手动创建原始封装类型
}
```

## 2. 函数

使函数不同于其它对象是函数存在一个`[[Call]]`的内部属性。内部属性无法通过代码访问而是定义了代码执行时的行为。ECMAScript为Js的对象定义了多种内部属性，这些内部属性都用`[[ ]]`来标注。`[[Call]]`属性表明该对象可以被执行，由于仅函数拥有该属性，ECMAScript定义typeof操作符对任何具有`[[Call]]`属性的对象返回`function`。

### 2.1 函数声明与函数表达式

函数有两种字面形式，**函数声明**和**函数表达式**，两者有个非常重要的区别，函数声明会被提升至上下文的顶部（要么是函数声明时所在函数的范围，要么是全局范围），这意味着可以先使用再声明函数。

### 2.2 函数就是值

函数可以像使用对象一样使用，可以将它们赋给变量，在对象中添加它们，将它们当成参数传递给别的函数，或从别的函数中返回，基本上只要是可以使用其它引用值的地方，就可以使用函数。

### 2.3 参数

函数的参数实际上被保存在一个`arguments`的数组中，`arguments`可以自由增长来包含任意个数的值，它的`length`属性可以告诉当前有多少个值。  
`arguments`对象自动存在于函数中。也就是说函数的命名参数不过是为了方便，并不真的限制了函数可接受参数的个数。

> **注意：** `arguments`对象不是一个数组的实例，其拥有的方法与数组不同，`Array.isArray(arguments)`返回`false`。

函数期望的参数个数保存在函数的`length`属性中。

### 2.4 重载

Js中不存在**签名**，因此也不存在重载，声明的同名函数后一个会覆盖前一个。  
不过可以对`arguments`对象获取的参数个数进行判断来决定怎么处理。

### 2.5 对象方法

可以像添加属性那样给对象添加方法，注意定义数据属性和方法的语法完全相同。

```text
var person = {
    name: "Nicholas",
    sayName: function () {
        console.log(person.name)
    }
}
```

#### 2.5.1 this对象

之前的例子的`sayName()`直接引用了`person.name`，在方法和对象之间建立了紧耦合，这种紧耦合使得一个方法很难被不同对象使用。  
Js所有函数作用域内都有一个`this`对象代表该函数的对象。在全局作用域内，`this`代表全局对象`window`，当一个函数作为对象的方法被调用时，默认`this`的值等于那个对象。改写：

```text
var person = {
    name: "Nicholas",
    sayName: function () {
        console.log(this.name)  
    }
}
```

所以应该在方法内引用`this`而不是直接引用对象。可以轻易改变变量名，或者将函数用在不同对象上，而不用大量改动代码。

```text
function sayNameForAll() {
    console.log(this.name)
}
var person1={
    name: "Nicholas",
    sayName: sayNameForAll
}
var person2={
    name: "Greg" ,
    sayName: sayNameForAll
}
var name = "Micheal"
person1.sayName()                            // Nicholas
person2.sayName()                            // Greg
sayNameForAll()                                // Micheal
```

`this`在函数被调用时才被设置，因此最后`sayNameForAll`函数执行时的`this`为全局对象。

#### 2.5.2 改变this

有3种方法可以改变`this`，函数是对象，而对象可以有方法，所以函数也有方法。

##### call()

第一个用于操作`this`的方法是`call()`，它以指定的`this`和参数来执行函数，第一个参数为函数执行时的`this`的值，后面的参数为需要被传入函数的参数。

```text
function sayNameForAll (label) {
    console.log(label + ':' + this.name)
}
var person1 = {name: "Nicholas"}
var person2 = {name: "Greg"}
var name = "Micheal"
sayNameForAll.call(this,"global")                        // global:Micheal
sayNameForAll.call(person1, "person1")             // person1:Nicholas
sayNameForAll.call(person2,"person2")              // person2:Greg
```

##### apply()

第二个用于操作`this`的方法时`apply()`，其工作方式与`call()`完全一样，但它只接受两个参数：`this`的值和一个数组或者类似数组的对象，内含需要被传入函数的参数（可以把`arguments`对象作为`apply`的第二个参数）。

```text
function sayNameForAll (label) {
    console.log(label + ":" + this.name)
}
var person1 =  {name:"Nicholas"}
var person2 = {name:"Greg"}
var name = "Micheal"
sayNameForAll.apply(this,["global"])                        // global:Micheal
sayNameForAll.apply(person1, ["person1"])             // person1:Nicholas
sayNameForAll.apply(person2,["person2"])              // person2:Greg
```

如果你已经有个数组，那么推介使用`apply()`，如果你有的是单独的变量，则用`call()`

##### bind()

改变`this`的第三个函数方法为`bind()`，`bind()`的第一个参数是要传给新函数的`this`的值，其他参数代表需要被**永久**设置在新函数中的命名参数，可以在之后继续设置任何非永久参数。

```text
function sayNameForAll (label) {
    console.log(label + ":" + this.name)
}
var person1 =  {name:"Nicholas"}
var person2 = {name:"Greg"}

var sayNameForPerson1 = sayNameForAll.bind(person1)
sayNameForPerson1("person1")                                                // person1:Nicholas
var sayNameForPerson2 = sayNameForAll.bind(person2,"person2")
sayNameForPerson2()                                                                // person2:Greg
person2.sayName = sayNameForPerson1;
person2.sayName("person2")                                                    // person2:Nicholas
```

`sayNameForPerson1()`没有绑定永久参数，因此可以继续传入`label`参数输出，`sayNameForPerson2()`不仅绑定了`person2`作为`this`，而且绑定了第一个参数为`person2`，因此可以使用`sayNameForPerson2()`而不用传入额外参数，但是也不能更改了。`person2.sayName`最后由于`this`的值在`sayNameForPerson1`的函数表达式中已经绑定为`person1`了，所以虽然`sayNameForPerson1`现在是`person2`的方法，它依然输出`person1.name`的值。

## 3. 理解对象

Js中的对象是动态的，可以在代码执行的任意时刻发生改变。

### 3.1 定义属性

当一个属性第一次被添加给对象时，Js在对象上隐式调用一个名为`[[Put]]`的内部方法，`[[Put]]`方法会在对象上创建一个新节点保存属性，就像第一次在哈希表上添加一个键一样。这个操作不仅指定了初试的值，也定义了属性的一些特征。  
调用`[[Put]]`的结果是在对象上创建了一个自有属性，该属性被直接保存在实例内，对该属性的所有操作都必须通过该对象进行。   
当一个已有的属性被赋予一个新值时，调用的是一个名为`[[Set]]`的方法，该方法将属性的当前值替换为新值。

### 3.2 属性探测

由于属性可以在任何时候添加，因此有时候有必要检查对象是否已有该属性：

```text
if(person1.age){            // 不可取
    // 执行
}
```

问题在于Js的类型强制会影响输出结果，如果if判断的值为null、undefined、0、false、NaN或者空字符串时则判断为假。由于一个对象属性可以包含这些假值，上例代码可能导致错误的判断，更可靠的判断是用`in`操作符。  
`in`操作符是在给定对象上查找一个给定名称的属性，如果找到则返回true，另外`in`操作符在判断的时候不会评估属性的值：

```text
var person1={
    name: "Nicholas",
    age: "111",
    sayName:function(){
        consloe.log(this.name)
    }
}
console.log('name' in person1)            // true
console.log('age' in person1)              // true
console.log('title' in person1)              // false
console.log('sayName' in person1)            // true    方法是值为函数的属性，因此同样可以用in判断
```

但是`in`操作符会检查自有属性和原型属性，因此在只想要自有属性的时候使用`hasOwnProperty()`判断一下，该方法在给定的属性存在并且为自有属性时返回true。

### 3.3 删除属性

正如属性可以在任何时候被添加，也可以在任何时候被删除。但是设置一个属性值为null并不能将其从对象中删除，只是调用`[[Set]]`将null替换了该属性原来的值。彻底的删除属性值需要`delete`操作符。  
`delete`操作符针对单个对象调用`[[Delete]]`的内部方法，可以认为该操作在哈希表中移除了一个键值对，当`delete`操作符成功时，它返回true。

> **注意：** 某些属性无法被`delete`。

```text
var person1= {name: 'Nicholas'}
console.log('name' in person1)                // true
delete person.name
console.log('name' in person1)                // false
console.log(person1.name)                          // undefined
```

### 3.4 属性枚举

所有你添加的属性默认为可枚举的，可以用`for-in`循环遍历，可枚举属性的内部特征`[[Enumerable]]`都被设置为true。`for-in`循环会枚举一个对象中所有的可枚举属性并将属性名赋给一个对象：

```text
var property
for (property in object){
    console.log('name:' + property)
    console.log('value' + object[property])
}
```

如果只需要获取一个对象的属性列表，ES5引入了`Object.keys()`方法，它可以获取可枚举属性的名字(key)的数组。

> **注意：**`Object.keys()`只返回自有属性不返回原型属性。

```text
var properties = Object.keys(object)
var i, len=properties.length
for (i=0; i<len; i++){
    console.log('name:' + properties[i])
    console.log('value' + object[properties[i]])
}
```

并不是每个属性都是可枚举的，可以使用`propertyIsEnumerable()`方法检查一个属性是否为可枚举，每个对象都有该方法。

```text
var person1= {name: 'Nicholas'}
var properties = Object.keys(person1)
console.log('name' in person1)                                                // true
console.log(person1.propertyIsEnumerable('name'))            // true
console.log('length' in properties)                                            // true
console.log(properties.propertiesIsEnumerable('length'))            // false
```

这里`name`为可枚举，因为它是`person1`的自有属性，而`properties`的`length`为不可枚举的，因为它是`Array.prototype`的内建属性，你会发现很多原生属性默认都是不可枚举的。

### 3.5 属性类型

属性有两种类型**数据属性**和**访问器属性**；  
**数据属性**包含一个值，例如之前的`name`属性，`[[Put]]`方法默认行为是创建一个数据属性。  
**访问器属性**不包含值而是定义了一个当属性被读取时调用的函数`getter`和一个当属性被写入时调用的函数`setter`。

```text
let person1 = {
    _name: "Nicholas" ,                        // 前置下划线是约定俗成的，表示该属性为私有的，实际上它是公开的
    get name() {
        console.log("reading me")
        return this._name
    },
    set name(val) {
        console.log(`setting name to ${val}`)
        this._name = val
    }
}
console.log(person1.name)                // reading me Nicholas
person1.name='greg'
console.log(person1.name)                // setting name to Greg
```

用于定义`name`的`getter`和`setter`的语法看上去像函数但是没有`function`关键字，注意`get`和`set`之后的`name`需要跟被访问的属性名保持一致。  
当你希望赋值操作会触发一些行为或者读取的值需要通过计算所需的返回值得到时，访问器属性将会很有用。

> **注意：** 不一定要同时定义`getter`和`setter`，可以选择其中之一，如果只定义`getter`，那么属性变为只读，在非严格下写入将失败，严格下写入报错，如果只定义`setter`，那么属性为只写，两种模式下读取都失败

### 3.6 属性特征

ES5之前无法访问属性的任何特征，也没有办法指定一个属性是否为可枚举，因此ES5引入多种方法与属性特征互动，同时也引入新的特征来支持额外的功能，现在已经可以创建出和Js内建属性一样的自定义属性。下面介绍数据属性和访问器属性的特征。

#### 3.6.1 通用特征

有两个属性时数据属性和访问器属性共有的：  
`[[Enumerable]]`决定你是否可以遍历该属性；  
`[[Configurable]]`决定该属性是否可配置；  
你可以用`delete`删除一个可配置的属性，或者随时改变它，也可以把可配置的属性从数据属性变为访问器属性，反之亦可，所有自有属性都是可枚举和可配置的。

如果你想改变属性特征，可以使用`Object.defineProperty()`方法，它接受三个参数：拥有函数的对象、属性名、包含需要设置的特征的属性描述对象。属性描述对象具有和内部特征同名的属性但名字中不包含中括号，所以可以使用`enumerable`属性来设置`[[Enumerable]]`特征，用`configurable`属性来设置`[[Configurable]]`特征。假如你想让一个对象属性变成不可枚举且不可配置：

```text
var person1 = { name: 'Nicholas' }
var properties = Object.keys(person1)

Object.defineProperty(person1, 'name', { enumerable: false })
console.log('name' in person1)                          // true
console.log(person1.propertyIsEnumerable('name'))      // false
console.log(properties.length)                            // 0
Object.defineProperty(person1, 'name', { configurable: false })
delete person1.name                                            // 属性设置为不可配置之后不能被delete，删除失败
console.log('name' in person1)                        // true
console.log(person1.name)                            // Nicholas
Object.defineProperty(person1, 'name', { configurable: true })    // error!    设置为不可配置之后就不能再设置属性特征了，包括[[Configurable]]
```

#### 3.6.2 数据属性特征

数据属性额外拥有两个访问器属性不具备的特征：  
`[[Value]]`包含属性的值，当你在对象上创建属性时该特征被自动赋值，所有属性的值都保存在`[[Value]]`中，哪怕该值是一个函数；  
`[[Writable]]`是一个布尔值，指示该属性是否可以写入，所有属性默认都是可写的，除非另外指定。  
通过这两个额外属性，可以使用`Object.defineProperty()`完整定义一个数据属性，即使该属性还不存在。

```text
var person1 = { name: 'Nicholas' }                // 等同于
Object.defineProperty(person, 'name',  {
    value: "Nicholas",
    enumerable: true,
    configurable: true,
    writable: true
}
```

当`Object.defineProperty()`被调用时，它首先检查属性是否存在，如果不存在将根据属性描述对象指定的特征创建。当使用`Object.defineProperty()`定义新属性时一定记得为**所有**的特征指定一个值，否则布尔型的特征会被默认设置为false。

```text
var person1 = {}
Object.defineProperty(person1, 'name', { value: 'Nicholas' })    // 由于没有显式指定特征，因此属性为不可枚举、不可配置、不可写的
console.log('name' in person1)                          // true
console.log(person1.propertyIsEnumerable('name'))      // false
delete person1.name
console.log('name' in person1)                    // true
person1.name = 'Greg'
console.log(person1.name)                          // Nicholas
```

> 在严格模式下视图改变不可写属性会抛出错误，而在非严格模式下会失败

#### 3.6.3 访问器属性

访问器属性拥有两个数据属性不具备的特征，访问器属性不需要储存值，因此也就没有`[[Value]]`和`[[Writable]]`，取而代之的是`[[Get]]`和`[[Set]]`属性，内含`getter`和`setter`函数，同字面量形式一样，只需要定义其中一个特征就可以创建一个访问器属性。

> 如果试图创建一个同时具有数据属性和访问器属性的属性，会报错

之前get set 例子可以被改写为：

```text
let person1 = { _name: "Nicholas" }
Object.defineProperty(person1, 'name', {
    get: function() {
      console.log("reading me")
      return this._name
    },
    set: function(val) {
      console.log(`setting name to ${val}`)
      this._name = val
    },
    enumerable: true,
    configurable: true
  }
)
console.log(person1.name)               // reading me Nicholas
person1.name = 'greg'
console.log(person1.name)                // setting name to Greg
```

注意`Object.defineProperty()`中的get和set关键字，它们是包含函数的数据属性，这里不能使用字面量形式。

#### 3.6.4 定义多重属性

如果你使用`Object.defineProperties()`而不是`Object.defineProperty()`可以为一个对象同时定义多个属性，这个方法接受两个参数：需要改变的对象、一个包含所有属性信息的对象。后者可以背看成一个哈希表，键是属性名，值是为该属性定义特征的属性描述对象。

```text
var person1 = {}
Object.defineProperties(person1, {
  _name: {
    value: 'Nicholas',
    enumerable: true,
    configurable: true,
    writable: true
  },
  name: {
    get: function() {
      console.log('reading me')
      return this._name
    },
    set: function(val) {
      console.log(`setting name to ${val}`)
      this._name = val
    },
    enumerable: true,
    configurable: true
  }
})
```

#### 3.6.5 获取属性特征

如果需要获取属性的特征，Js中可以使用`Object.getOwnPropertyDescriptor()`，这个方法只可以用于自有属性，它接受两个参数：对象、属性名。如果属性存在，它会返回一个属性描述对象，内含四个属性：configurable、enumerable、另外两个根据属性类型决定。即使你从没有为属性显式指定特征，你依然会得到包含全部这些特征值的属性描述对象。

### 3.7 禁止修改对象

对象和属性一样具有指导行为的内部特征，其中，`[[Extensible]]`是一个布尔值，它指明该对象本身是否可以被修改，你创建的所有对象默认都是可扩展的，新的属性可以随时被添加，设置`[[Extensible]]`为false则可以禁止新属性的添加。  
下面有三种方法可以用来锁定对象属性

#### 3.7.1 禁止扩展

第一种方法是`Object.preventExtensions()`创建一个不可扩展的对象。该方法接受一个参数：你希望扩展的对象。一旦在一个对象上用这个方法，就永远不能再给它添加新的属性了。

```text
let person1 = { _name: "Nicholas" }
console.log(Object.isExtensible(person1))            // true
Object.preventExtensions(person1)
console.log(Object.isExtensible(person1))            // false
person1.sayName = function(){
    console.log(this.name)
}
console.log('sayName' in person1)                // false
```

> 在严格模式下试图给一个不可扩展对象添加属性会抛出错误，而在非严格模式下会失败。应该对不可扩展对象使用严格模式，这样当一个不可扩展对象被错误使用时你就会知道

#### 3.7.2 对象封印

一个被封印的对象是不可扩展的且其所有属性都不可配置，这意味着不仅不能给对象添加属性，而且也不能删除属性或改变类型（从数据属性改变成访问属性或者反之），如果一个对象被封印，那么只能读写它的属性。  
可以用`Object.seal()`方法来封印一个对象，该方法被调用时`[[Extensible]]`特征被设置为false，其所有属性的`[[Configurable]]`特征被置为false，可以使用`Object.isSealed()`来判断一个对象是否被封印。  
这段代码封印了person1，因此不能再person1上添加或者删除属性。所有的被封印对象都是不可扩展的对象，此时对person1使用`Object.isExtensible()`方法将会返回false，且视图添加`sayName()`会失败。  
而且虽然person.name被成功改变成一个新值，但是删除它会失败。

> 确保对被封印的对象使用严格模式，这样当有人误用该对象时，会报错

#### 3.7.3 对象冻结

被冻结的对象不能添加或删除属性，不能修改属性类型，也不能写入任何数据属性。简言而之，被冻结对象是一个数据属性都为只读的被封印对象。  
`Object.freeze()` 冻结对象。  
`Object.isFrozen()` 判断对象是否被冻结。

> 被冻结对象仅仅只是对象在某个时间点上的快照，用途有限且很少被使用

## 4. 构造函数和原型对象

### 4.1 构造函数

**构造函数**就是用`new`创建对象时调用的函数，使用构造函数的好处在于所有用同一个构造函数创建的对象都具有同样的属性和方法。  
构造函数也是函数，定义的方式和普通函数一样，唯一的区别是构造函数名应该首字母大写，以此区分。

```text
function Person(){}
var person1 = new Person                        // 如果没有要传递给构造函数的参数，括号可以省略
console.log(person1 instanceof Person)        // true
console.log(person1.constructor === Person)        // true
```

即使Person构造函数没有显式返回任何东西，person1也会被认为是一个新的Person类型的对象，`new`操作符会自动创建给定类型的对象并返回它们。每个对象在创建时都会自动拥有一个构造函数属性，其中包含了一个指向其构造函数的引用。那些通过字面量形式或者Object构造函数创建出来的泛用对象，其构造函数属性`constructer`指向Object；那些通过自定义构造函数创建出来的对象，其构造函数属性指向创建它的构造函数。

虽然对象实例及其构造函数之间存在这样的关系，但是还是建议使用`instanceof`来检查对象类型，这是因为构造函数属性可以被覆盖，并不一定完全准确。  
在构造函数中只需简单的给`this`添加任何想要的属性即可：

```text
function Person(name){
    this.name =  name
    this.sayName() = function(){
        console.log(this.name)
    }
}
```

在调用构造函数时，`new`会自动创建`this`对象，且其类型就是构造函数的类型，构造函数本身不需要返回一个对象，`new`操作符会帮你返回。

```text
function Person2(name){
    this.name=name
    this.sayName=function(){
        console.log(this.name)
    }
}
var person2=new Person2('sam') 
console.log(person2.name)                    // sam
person2.sayName()                                // sam
```

每个对象都有自己的`name`属性值，所以`sayName`可以根据不同对象返回不同的值。

> 也可以在构造函数中显式调用`return`，如果返回的是一个对象，那么它会替代新创建的对象实例返回，如果返回的是一个原始类型，那么它将被忽略，新创建的对象实例将被返回。

构造函数允许使用一致的方法初始化一个类型的实例，在使用对象前设置好所有的属性，可以在构造函数中使用`Object.defineProperty()`的方法来帮助初始化。

```text
function Person(name) {
    Object.defineProperty(this, 'name', {
        get: function() {
            return name
        },
        set: function(newName) {
            name = newName
        },
        enumerable: true,
        configurable: true
    })

    this.sayName = function() {
        console.log(this.name)
    }
}

var person1 =new Person('Nicholas')                // 始终确保使用了new操作符，否则就是冒着改变全局对象的风险
console.log(person1 instanceof Person)            // true   
console.log(typeof person1)                               // object
console.log(name)                                              // undefined
```

当Person不是被`new`调用时候，构造函数中的`this`指向全局对象，由于Person构造函数依靠`new`提供返回值，person1变量为undefined。没有`new`，Person只不过是一个没有返回语句的函数，对`this.name`的赋值实际上创建了一个全局对象name。

> 严格模式下，不通过`new`调用Person构造函数会出现错误，这是因为严格模式并没有为全局对象设置this，this保持为undefined，而试图给undefined添加属性时都会出错

构造函数允许给对象配置同样的属性，当构造函数并没有消除代码冗余，每个对象都有自己的`sayName()`方法，这意味着100个对象实例就有100个函数做相同的事情，只是使用的数据不同。如果所有的对象实例共享同一个方法会更有效率，该方法可以使用`this.name`来访问对应的数据，这就需要用到**原型对象**。

### 4.2 原型对象

原型对象可以看做对象的基类，几乎所有函数（除了一下内建函数）都有一个名为`prototype`的属性，该属性是一个原型对象用来创建新的对象实例。  
所有创建的对象实例共享该原型对象，且这些对象实例可以访问原型对象的属性。例如，`hasOwnProperty()`方法被定义在泛用对象`Object`的原型对象中，但却可以被任何对象当做自己的属性访问。

```text
var book = {title: "the principles of object-oriented js"}
console.log('title' in book)
console.log(book.hasOwnProperty('title'))                        // true
console.log('hasOwnProperty' in book)                            // true
console.log(book.hasOwnProperty('hasOwnProperty'))             // false
console.log(Object.prototype.hasOwnProperty('hasOwnProperty'))            // true
```

即使`book`中没有`hasOwnProperty()`方法的定义，但仍然可以通过`book.hasOwnProperty()`访问该方法，这是因为该方法存在于`Object.prototype`中。  
可以使用这样一个方法来判断一个属性是否为原型属性：

```text
function hasPrototypeProperty(object, name){
    return name in object && !object.hasOwnProperty(name)
}
```

#### 4.2.1 [[Prototype]]属性

一个对象实例通过内部属性`[[Prototype]]`追踪其原型对象，该属性是一个指向该实例使用的原型对象的指针。当你使用`new`创建一个新的对象时，构造函数的原型对象会被赋给该对象的`[[Prototype]]`属性 ([JS __proto__ 探究.md](http://acd4a5c2.wiz03.com/share/s/2IRan20FtAg22uF57q2gr5tu2LCow03BtAW-2iwDTe34tG-X) )。你可以调用`Object.getPropertyOf()`方法读取`[[prototype]]`属性的值。

> Object.prototype.__proto__ === null

```text
var object={}
Object.getPrototypeOf(object) === Object.prototype                // true
Object.prototype.isPrototypeOf(object)                    // true
```

任何一个泛用对象（字面量形式或者`new Object()`），其`[[Prototype]]`对象始终指向`Object.prototype`。也可以用`isPrototypeOf()`方法检查某个对象是否是另一个对象的原型对象，该方法被包含在所有对象中。

> **Note:**大部分Js引擎在所有对象上都支持一个`__proto__`的属性，该属性使你可以直接读写`[[Prototype]]`属性。包括Firefox、Safari、Chrome、Node.js

在读取一个对象的属性时，Js引擎会首先在对象的自有属性中查找属性名字，如果找到则返回，如果没有则Js会搜索`[[Prototype]]`中的对象，如果找到则返回，找不到则返回`undefined`。

```text
var object = {}
console.log(object.toString())                    // [object Object]
object.toString = function() {return "[object Custom]"}
console.log(object.toString())                    // [object Custom]
delete object.toString
console.log(object.toString())                    // [object Object]
delete object.toString
console.log(object.toString())                    // [object Object]
```

上例可以看出，`delete`运算符只对只有属性起作用，无法删除一个对象的原型属性。并且也不可以给一个对象的原型属性赋值，对`.toString`的赋值只是在对象上创建了一个新的自有属性，而不是改变原型属性。

#### 4.2.2 在构造函数中使用原型对象

原型对象的共享机制使得它们成为一次性为所有对象定义所有方法的理想手段，因为一个方法对所有的对象实例做相同的事，没理由每个实例都要有一份自己的方法。将方法放在原型对象中并使用`this`方法当前实例是更有效的做法。

```text
function Person(name) {this.name = name}
Person.prototype.sayName = function() {console.log(this.name)};
var person1 = new Person("Nicholas")
console.log(person1.name)                        // Nicholas
person1.sayName()                                // Nicholas
```

也可以在原型对象上存储其他类型的数据，但是在存储引用值时要注意，因为这些引用值会被多个实例共享，可能大家不希望一个实例能够改变另一个实例的值。

```text
function Person(name) {this.name = name}
Person.prototype.favorites = []
var person1 = new Person("Nicholas")
var person2 = new Person("Greg")
person1.favorites.push("pizza")
person2.favorites.push("quinoa")

console.log(person1.favorites)                // ["pizza", "quinoa"]
console.log(person2.favorites)                // ["pizza", "quinoa"]
```

`favorites`属性被定义到原型对象上，意味着`person1.favorites`和`person2.favorites`指向同一个数组，你对任意Person对象的favorites插入的值都将成为原型对象上数组的元素。也可以使用字面量的形式替换原型对象：

```text
function Person(name) {this.name=name}
Person.prototype= {
    sayName: function() {console.log(this.name)},
    toString: function(){return `[Person ${this.name} ]`}
}
```

虽然用这种字面量的形式定义原型非常简洁，但是有个副作用需要注意。

```text
var person1 = new Person('Nicholas')
console.log(person1 instanceof Person)                // true
console.log(person1.constructor === Person)                // false
console.log(person1.constructor === Object)                // true
```

使用字面量形式改写原型对象改写了构造函数的属性，因此现在指向`Object`而不是`Person`，这是因为原型对象具有个`constructor`属性，这是其他对象实例所没有的。当一个函数被创建时，其`prototype`属性也被创建，且该原型对象的`constructor`属性指向该函数自己，当使用字面量形式改写原型对象`Person.prototype`时，其`constructor`属性将被复写为泛用对象`Object`。为了避免这一点，需要在改写原型对象时手动重置其`constructor`属性：

```text
function Person(name) {this.name = name}
Person.prototype = {
    constructor: Person,             // 为了不忘记赋值，最好在第一个属性就把constructor重置为自己
    sayName() {console.log(this.name)},
    toString() {return `[Person ${this.name} ]`}
}

var person1 = new Person('Nicholas')
console.log(person1 instanceof Person)                    // true
console.log(person1.constructor === Person)                // true
console.log(person1.constructor === Object)                // false
```

构造函数、原型对象、对象实例之间：对象实例和构造函数之间没有直接联系。不过对象实例和原型对象之间以及原型对象和构造函数之间都有直接联系。

这样的连接关系也意味着，如果打断对象实例和原型对象之间的联系，那么也将打断对象实例及其构造函数之间的关系。

#### 4.2.3 改变原型对象

给定类型的所有对象实例共享一个原型对象，所以可以一次性扩充所有对象实例。`[[Prototype]]`属性只是包含了一个指向原型对象的指针，任何对原型对象的改变都将你可反映到所有引用它的对象实例上。这意味着给原型对象添加的新成员都可以立刻被所有已经存在的对象实例使用。

```text
function Person(name) {this.name = name}
Person.prototype = {
    constructor: Person,
    sayName() {console.log(this.name)},
    toString() {return `[Person ${this.name} ]`}
}
var person1 = new Person('Nicholas')
var person2 = new Person('Greg')
console.log('sayHi' in person1)                // false
console.log('sayHi' in person2)                // false
Person.prototype.sayHi = () => console.log("Hi")
person1.sayHi()                // Hi
person2.sayHi()                // Hi
```

当对一个对象使用`Object.seal()`或`Object.freeze()`封印和冻结对象的时候是在操作对象的自有属性，无法添加封印对象的自有属性和更改冻结对象的自有属性，但是仍然可以通过在原型对象上添加属性来扩展对象实例：

```text
function Person(name) {this.name = name}
var person1 = new Person("Nicholas")
Object.freeze(person1)
Person.prototype.sayHi = function() {console.log("Hi")};
person1.sayHi()            // Hi
```

其实，`[[Prototype]]`是实例对象的自有属性，属性本身`person1.[[Prototype]]`被冻结，但是指向的值`Person.prototype`并没有冻结。

#### 4.2.4 内建对象的原型对象

所有内建对象都有构造函数，因此也都有原型对象可以去改变，例如要在数组上添加一个新的方法只需要改变`Array.prototype`即可

```text
Array.prototype.sum = function() {
    return this.reduce((privious, current) => privious + current)
}
var numbers = [1, 2, 3, 4, 5, 6]
var result = numbers.sum()
console.log(result)                    // 21
```

sum()函数内部，在调用时`this`指向数组的对象实例`numbers`，因此`this`也可以调用该数组的其他方法，比如reduce()。  
改变原始封装类型的原型对象，就可以给这些原始值添加更多功能，比如：

```text
String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.substring(1)
}
var message = 'hello world!'
console.log(message.capitalize())            // Hello world!
```

## 5. 继承

### 5.1 原型对象链和Object.prototype

Js内建的继承方法被称为原型对象链，又称为原型对象继承。原型对象的属性可以由对象实例访问。实例对象集成了原型对象的属性，因为原型对象也是一个对象，它也有自己的原型对象并继承其属性。这就是原型继承链：**对象继承其原型对象，而原型对象继承它的原型对象，以此类推。**  
所有的对象，包括自定义的对象都继承自`Object`，除非另有指定。更确切的说，所有对象都继承自`Object.prototype`，任何以字面量形式定义的对象，其`[[Prototype]]`的值都被设为`Object.prototype`，这意味着它继承Object.prototype的属性。

```text
var book = {title: 'a book'}
console.log(Object.getPrototypeOf(book) === Object.prototype)            // true
```

#### 5.1.1 继承自Object.prototype的方法

前几张用到的几个方法都是定义在Object.prototype上的，因此可以被其他对象继承：

| Methods | Usage |
| --- | --- |
| hasOwnProperty() | 检查是否存在一个给定名字的自有属性 |
| propertyIsEnumerable() | 检查一个自有属性是否为可枚举 |
| isPrototypeOf() | 检查一个对象是否是另一个对象的原型对象 |
| valueOf() | 返回一个对象的值表达 |
| toString() | 返回一个对象的字符串表达 |

这几种方法由继承出现在所有的对象中，当你需要对象在Js中以一致的方式工作时，最后两个尤为重要。

1. **valueOf()**  
   每当一个操作符被用于一个对象时就会调用`valueOf()`方法，其默认返回对象实例本身。原始封装类型重写了`valueOf()`以使得它对String返回一个字符串，对Boolean返回一个布尔，对Number返回一个数字；类似的，对Date对象的valueOf()返回一个epoch时间，单位是毫秒（正如Data.prototype.getTime()）。

   ```text
   var now = new Date                // now.valueOf()  === 1505108676169
   var earlier = new Date(2010,1,1)            // earlier.valueOf() === 1264953600000
   console.log(now>earlier)                // true
   console.log(now-earlier)                 // 240155076169
   ```

   now是一个代表当前时间的Date，而earlier是过去的时间，当使用操作符`>`时，两个对象上都调用了`valueOf()`方法，你甚至可以用两个Date相减来获得它们在epoch时间上的差值。如果你的对象也要这样使用操作符，你可以定义自己的`valueOf()`方法，定义的时候你并没有改变操作符的行为，仅仅应了操作符默认行为所使用的值。
2. **toString()**  
   一旦`valueOf()`返回的是一个引用而不是原始值的时候，就会回退调用`toString()`方法。另外，当Js期望一个字符串时也会对原始值隐式调用`toString()`。例如当加号操作符的一边是一个字符串时，另一边就会被自动转换成字符串，如果另一边是一个原始值，会自动转换成一个字符串表达（true => "true"），如果另一边是一个引用值，则会调用`valueOf()`，如果其返回一个引用值，则调用`toString()`。

   ```text
   var book = {title: 'a book'}
   console.log("book = " + book)                // "book = [object Object]"
   ```

   因为book是一个对象，因此调用它的`toString()`方法，该方法继承自Object.prototype，大部分Js引擎返回默认值[object Object]，如果对这个值不满意可以复写，为此类字符串提供包含跟多信息。

   ```text
   var book = {title: 'a book',
   toString(){return `[Book = ${this.title} ]`}}
   console.log("book = " + book)                 // book = [Book = a book ]
   ```

#### 5.1.2 修改Object.prototype

所有的对象都默认继承自Object.prototype，所以改变它会影响到所有的对象，这是非常危险的。  
如果给Obejct.prototype添加一个方法，它是可枚举的，可以粗现在for-in循环中，一个空对象依然会输出一个之前添加的属性。尽量不要修改Object.prototype。

### 5.2 对象继承

对象字面量形式会隐式指定Object.prototype为其`[[Prototype]]`，也可以用Object.create()方式显示指定。Object.create()方法接受两个参数：需要被设置为新对象`[[Prototype]]`的对象、属性描述对象，格式如在Object.defineProperties()中使用的一样（第三章）。

```text
var book = {title: 'a book'}
// ↑ 等价于 ↓
var book = Object.create(Object.prototype, {
    title: {
        configurable: true,
        enumerable: true,
        value: 'a book',
        writable: true
    }
})
```

第一种写法中字面量形式定义的对象自动继承Object.prototype且其属性默认设置为可配置、可写、可枚举。第二种写法显示使用Object.create()做了相同的操作，两个book对象的行为完全一致。

```text
var person = {
    name: "Jack",
    sayName: function(){
        console.log(this.name);
    }
}

var student = Object.create(person, {
    name:{value: "Ljc"},
    grade: {
        value: "fourth year of university",
        enumerable: true,
        configurable: true,
        writable: true
    }
});

person.sayName(); // "Jack"
student.sayName(); // "Ljc"

console.log(person.hasOwnProperty("sayName")); // true
console.log(person.isPrototypeOf(student)); // true
console.log(student.hasOwnProperty("sayName")); // false
console.log("sayName" in student); // true

console.log(student.__proto__===person)                                      // true
console.log(student.__proto__.__proto__===Object.prototype)      // true
```

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/7ad3688ddd56dc3e0f9f71f4e68c675bb222cb4d29b77dcf0fb056593251d8c3.png)

对象person2继承自person1，也就集成了person1的name和sayName()，然而又通过重写name属性定义了一个自有属性，隐藏并替代了原型对象中的同名属性。所以person1.sayName()输出Nicholas而person2.sayName()输出Greg。  
在访问一个对象的时候，Js引擎会执行一个搜索过程，如果在对象实例上发现该属性，该属性值就会被使用，如果没有发现则搜索`[[Prototype]]`，如果仍然没有发现，则继续搜索该原型对象的`[[Prototype]]`，知道继承链末端，末端通常是一个Object.prototype，其`[[prototype]]`为null。这就是**原型链**。  
当然也可以通过Object.create()创建`[[Prototype]]`为null的对象：`var obj=Object.create(null)`。该对象obj是一个没有原型链的对象，这意味着`toString()`和`valueOf`等存在于Object原型上的方法都不存在于该对象上。

### 5.3 构造函数继承

Js中的对象继承也是构造函数继承的基础，第四章提到：几乎所有的函数都有`prototype`属性（通过`Function.prototype.bind`方法构造出来的函数是个例外），它可以被替换和修改。该`prototype`属性被自动设置为一个继承自Object.prototype的泛用对象，该对象有个自有属性`constructor`。

```text
// 构造函数
function YourConstructor() {}
// Js引擎在背后做的：
YourConstructor.prototype = Object.create(Object.prototype, {
    constructor: {
        configurable: true,
        enumerable: true,
        value: YourConstructor,
        writable: true
    }
})
console.log(YourConstructor.prototype.__proto__===Object.prototype)            // true
```

你不需要做额外工作，Js引擎帮你把构造函数的`prototype`属性设置为一个继承自Object.prototype的对象，这意味着YourConstructor创建出来的任何对象都继承自Object.prototype，YouConstructor是Object的子类。  
由于prototype可写，可以通过改写它来改变原型链：

```text
function Rectangle(length, width) {
    this.length = length
    this.width = width
}
Rectangle.prototype.getArea = function() {return this.length * this.width};
Rectangle.prototype.toString = function() {return `[ Rectangle ${this.length}x${this.width} ]`};

function Square(size) {
    this.length = size
    this.width = size
}
Square.prototype = new Rectangle()
Square.prototype.constructor = Square
Square.prototype.toString = function() {return `[ Square ${this.length}x${this.width} ]`}

var rect = new Rectangle(5, 10)
var squa = new Square(6)
console.log(rect instanceof Rectangle)        // true
console.log(rect instanceof Square)        // false
console.log(rect instanceof Object)        // true
console.log(squa instanceof Rectangle)        // true
console.log(squa instanceof Square)        // true
console.log(squa instanceof Object)        // true
```

> MDN:instanceof 运算符可以用来判断某个构造函数的 prototype 属性是否存在另外一个要检测对象的原型链上。

Square构造函数的prototype属性被改写为Rectagle的一个实例，此时不需要给Rectangle的调用提供参数，因为它们不需要被使用，而且如果提供了，那么所有的Square对象实例都会共享这样的维度。如果用这种方式改写原型链，需要确保构造函数不会再参数缺失时抛出错误（很多构造函数包含的初始化逻辑）且构造函数不会改变任何全局状态。

```text
// inherits from Rectangle
function Square(size){
    this.length = size;
    this.width = size;
}

Square.prototype = new Rectangle(); // 尽管是 Square.prototype 是指向了 Rectangle 的对象实例，即Square的实例对象也能访问该实例的属性（如果你提前声明了该对象，且给该对象新增属性）。
// Square.prototype = Rectangle.prototype; // 这种实现没有上面这种好，因为Square.prototype 指向了 Rectangle.prototype，导致修改Square.prototype时，实际就是修改Rectangle.prototype。
console.log(Square.prototype.constructor); // 输出 Rectangle 构造函数

Square.prototype.constructor = Square; // 重置回 Square 构造函数
console.log(Square.prototype.constructor); // 输出 Square 构造函数

Square.prototype.toString = function(){
    return "[Square " + this.length + "x" + this.width + "]";
}

var rect = new Rectangle(5, 10);
var square = new Square(6);

console.log(rect.getArea()); // 50
console.log(square.getArea()); // 36

console.log(rect.toString()); // "[Rectangle 5 * 10]", 但如果是Square.prototype = Rectangle.prototype，则这里会"[Square 5 * 10]"
console.log(square.toString()); // "[Square 6 * 6]"

console.log(square instanceof Square); // true
console.log(square instanceof Rectangle); // true
console.log(square instanceof Object); // true
```

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/77190fa29e95dda022951849943f2c795e5540c48b6bad5ba491500ba2e159da.png)

`Square.prototype` 并不真的需要被改成为一个 `Rectangle` 对象。事实上，是 `Square.prototype` 需要指向 `Rectangle.prototype` 使得继承得以实现。这意味着可以用 `Object.create()` 简化例子。

```text
// inherits from Rectangle
function Square(size){
    this.length = size;
    this.width = size;
}

Square.prototype= Object.create(Rectangle.prototype, {
    constructor: {
        configurable: true,
        enumerable: true,
        value: Square,
        writable: true
    }
})
```

> 在对原型对象添加属性前要确保你已经改写了原型对象，否则在改写时会丢失之前添加的方法（因为继承是将被继承对象赋值给需要继承的原型对象，相当于重写了需要继承的原型对象）。

### 5.4 构造函数窃取

由于JavaScript中的继承是通过原型对象链来实现的，因此不需要调用对象的父类的构造函数。如果确实需要在子类构造函数中调用父类构造函数，那就可以在子类的构造函数中利用 call、apply方法调用父类的构造函数。

```text
function Rectangle(length, width) {
    this.length = length
    this.width = width
}
Rectangle.prototype.getArea = function() {return this.length * this.width};
Rectangle.prototype.toString = function() {return `[ Rectangle ${this.length}x${this.width} ]`};

function Square(size) {Rectangle.call(this, size, size)}
Square.prototype = Object.create(Rectangle.prototype, {
    constructor: {
        value: Square,
        enumerable: true,
        configurable: true,
        writable: true
    }
})
Square.prototype.toString = function() {return `[ Square ${this.length}x${this.width} ]`}

var rect = new Rectangle(5, 10)
var squa = new Square(6)
console.log(rect.getArea())
console.log(rect.toString())
console.log(squa.getArea())
console.log(squa.toString())
```

一般来说，需要修改 `prototype` 来继承方法并用构造函数窃取来设置属性，由于这种做法模仿了那些基于类的语言的类继承，所以这通常被称为**伪类继承**。

### 5.5 访问父类方法

其实也是通过指定 `call` 或 `apply` 的子对象调用父类方法。

## 6. 对象模式

可以使用继承或者混入等其他技术令对象间行为共享，也可以利用Js高级技巧阻止对象结构被改变。

### 6.1 私有成员和特权成员

#### 6.1.1 模块模式

**模块模式**是一种用于创建拥有私有数据的单件对象的模式。  
基本做法是使用立即调用函数表达式（IIFE）来返回一个对象。原理是利用闭包。

```text
var yourObj = (function(){
    // private data variables   
    return {
        // public methods and properties
    }
}());
```

模块模式还有一个变种叫**暴露模块模式**，它将所有的变量和方法都放在 IIFE 的头部，然后将它们设置到需要被返回的对象上。

```text
//  一般写法
var yourObj = (function(){
    var age = 25;    
    return {
        name: "Ljc",      
        getAge: function(){
            return age 
        }
    }
}());

// 暴露模块模式，保证所有变量和函数声明都在同一个地方
var yourObj = (function(){
    var age = 25;                            // 私有变量，外部无法访问
    function getAge(){
        return age
    };
    return {
        name: "Ljc",                          // 公共变量外部可以访问
        getAge: getAge                    // 外部可以访问的对象
    }
}());
```

#### 6.1.2 构造函数的私有成员

模块模式在定义单个对象的私有属性十分有效，但对于那些同样需要私有属性的自定义类型呢？你可以在构造函数中使用类似的模式来创建每个实例的私有数据。

```text
function Person(name){
    // define a variable only accessible inside of the Person constructor
    var age = 22;   
    this.name = name;
    this.getAge = function(){return age;};
    this.growOlder = function(){age++;}
}

var person = new Person("Ljc");
console.log(person.age);         // undefined
person.age = 100;
console.log(person.getAge());         // 22
person.growOlder();
console.log(person.getAge());         // 23
```

构造函数在被new的时候创建了一个本地作用于并返回this对象。这里有个问题：如果你需要对象实例拥有私有数据，就不能将相应方法放在 `prototype`上。  
如果你需要所有实例共享私有数据（就好像它被定义在原型对象里那样），则可结合模块模式和构造函数，如下：

```text
var Person = (function(){
    var age = 22;
    function InnerPerson(name){this.name = name;}
    InnerPerson.prototype.getAge = function(){return age;}
    InnerPerson.prototype.growOlder = function(){age++;};
    return InnerPerson;
}());

var person1 = new Person("Nicholash");
var person2 = new Person("Greg");
console.log(person1.name); // "Nicholash"
console.log(person1.getAge()); // 22
console.log(person2.name); // "Greg"
console.log(person2.getAge()); // 22

person1.growOlder();
console.log(person1.getAge()); // 23
console.log(person2.getAge()); // 23
```

### 6.2 混入

这是一种伪继承。一个对象在不改变原型对象链的情况下得到了另外一个对象的属性被称为“混入”。因此，和继承不同，混入让你在创建对象后无法检查属性来源。

```text
function mixin(receiver, supplier){
    for(var property in supplier){
        if(supplier.hasOwnProperty(property)){
            receiver[property] = supplier[property];
        }
    }
}
```

这是浅拷贝，如果属性的值是一个引用，那么两者将指向同一个对象。  
要注意一件事，使用这种方式，`supplier`的访问器属性会被复制为`receiver`的数据属性。

```text
function mixin(reciver, supplier) {
    if (Object.getOwnPropertyDescriptor) {                    // 检查是否支持es5
        Object.keys(supplier).forEach(property => {
            var descriptor = Object.getOwnPropertyDescriptor(supplier, property)
            Object.defineProperty(reciver, property, descriptor)
        })
    } else {
        for (var property in supplier) {                        // 否则使用浅复制
            if (supplier.hasOwnProperty(property)) {
                reciver[property] = supplier[property]
            }
        }
    }
}
```

### 6.3 作用域安全的构造函数

构造函数也是函数，所以不用 new 也能调用它们来改变 `this` 的值。在非严格模式下， `this` 被强制指向全局对象。而在严格模式下，构造函数会抛出一个错误（因为严格模式下没有为全局对象设置 this，this 保持为 undefined）。  
而很多内建构造函数，例如 Array、RegExp 不需要 new 也能正常工作，这是因为它们被设计为作用域安全的构造函数。  
当用 new 调用一个函数时，this 指向的新创建的对象已经属于该构造函数所代表的自定义类型。因此，可在函数内用 instanceof 检查自己是否被 new 调用。

```text
function Person(name){
    if(this instanceof Person){
        // called with "new"
    }else{
        // called without "new"
    }
}
```

具体案例：

```text
function Person(name){
    if(this instanceof Person){
        this.name = name;
    }else{
        return new Person(name);
    }
}
```

---
