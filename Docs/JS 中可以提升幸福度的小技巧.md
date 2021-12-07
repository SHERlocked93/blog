# JS 中可以提升幸福度的小技巧

[TOC]

本文主要介绍一些JS中用到的小技巧，可以在日常Coding中提升幸福度，将不定期更新~

## 1. 类型强制转换
### 1.1 string强制转换为数字
可以用`*1`来转化为数字(实际上是调用`.valueOf`方法)
然后使用`Number.isNaN`来判断是否为`NaN`，或者使用 `a !== a` 来判断是否为`NaN`，因为 `NaN !== NaN`
```js
'32' * 1            // 32
'ds' * 1            // NaN
null * 1            // 0
undefined * 1    // NaN
1  * { valueOf: ()=>'3' }        // 3
```

**常用：**也可以使用`+`来转化字符串为数字
```js
+ '123'            // 123
+ 'ds'               // NaN
+ ''                    // 0
+ null              // 0
+ undefined    // NaN
+ { valueOf: ()=>'3' }    // 3
```

### 1.2 object强制转化为string
可以使用 `字符串+Object` 的方式来转化对象为字符串(实际上是调用 `.toString()` 方法)
```js
'the Math object:' + Math                // "the Math object:[object Math]"
'the JSON object:' + JSON              // "the JSON object:[object JSON]"
```

当然也可以覆盖对象的`toString`和`valueOf`方法来自定义对象的类型转换：
```js
2  * { valueOf: ()=>'3' }                // 6
'J' + { toString: ()=>'S' }                // "JS"
```

> 《Effective JavaScript》P11：当`+`用在连接字符串时，当一个对象既有`toString`方法又有`valueOf`方法时候，JS通过盲目使用`valueOf`方法来解决这种含糊。
对象通过`valueOf`方法强制转换为数字，通过`toString`方法强制转换为字符串

```js
'' + {toString:()=>'S',valueOf:()=>'J'}                // J
```

### 1.3 使用Boolean过滤数组中的所有假值

我们知道JS中有一些假值：`false`，`null`，`0`，`""`，`undefined`，`NaN`，怎样把数组中的假值快速过滤呢，可以使用Boolean构造函数来进行一次转换

```js
const compact = arr => arr.filter(Boolean)
compact([0, 1, false, 2, '', 3, 'a', 'e' * 23, NaN, 's', 34])             // [ 1, 2, 3, 'a', 's', 34 ]
```

### 1.4 双位运算符 ~~

可以使用双位操作符来替代 `Math.floor( )`。双否定位操作符的优势在于它执行相同的操作运行速度更快。
```js
Math.floor(4.9) === 4      //true
// 简写为：
~~4.9 === 4      //true
```
不过要注意，对整数来说 `~~` 运算结果与 `Math.floor( )` 运算结果相同，而对于负数来说不相同：
```js
~~4.5            // 4
Math.floor(4.5)        // 4
~~-4.5        // -4
Math.floor(-4.5)        // -5
```

### 1.5 短路运算符
我们知道逻辑与`&&`与逻辑或`||`是短路运算符，短路运算符就是从左到右的运算中前者满足要求，就不再执行后者了；
可以理解为：

- `&&`为取假运算，从左到右依次判断，如果遇到一个假值，就返回假值，以后不再执行，否则返回最后一个真值
- `||`为取真运算，从左到右依次判断，如果遇到一个真值，就返回真值，以后不再执行，否则返回最后一个假值

```js
let param1 = expr1 && expr2
let param2 = expr1 || expr2
```

| 运算符 | 示例 | 说明 |
| --- | --- | --- |
| `&&` | `expr1&&expr2` | 如果expr1 能转换成false则返回expr1,否则返回expr2. 因此, 在Boolean环境中使用时, 两个操作结果都为true时返回true,否则返回false. |
| `||` | `expr1||expr2` | 如果expr1能转换成true则返回expr1,否则返回expr2. 因此,在boolean环境(在if的条件判断中)中使用时, 二者操作结果中只要有一个为true,返回true;二者操作结果都为false时返回false. |
| `!` | `!expr` | 如果单个表达式能转换为true的话返回false,否则返回true. |

因此可以用来做很多有意思的事，比如给变量赋初值：
```js
let variable1
let variable2 = variable1  || 'foo'    
```
如果variable1是真值就直接返回了，后面短路就不会被返回了，如果为假值，则会返回后面的`foo`。

也可以用来进行简单的判断，取代冗长的`if`语句：
```js
let variable = param && param.prop
```
如果`param`如果为真值则返回`param.prop`属性，否则返回`param`这个假值，这样在某些地方防止`param`为`undefined`的时候还取其属性造成报错。


### 1.6 取整 `| 0`
对一个数字`| 0`可以取整，负数也同样适用，`num | 0 `
```js
1.3 | 0         // 1
-1.9 | 0        // -1
```

### 1.7 判断奇偶数 `& 1`
对一个数字`& 1`可以判断奇偶数，负数也同样适用，`num & 1 `
```js
const num=3;
!!(num & 1)					// true
!!(num % 2)					// true
```




## 2. 函数
### 2.1 函数默认值
```js
func = (l, m = 3, n = 4 ) => (l * m * n);
func(2)             //output: 24
```
注意，传入参数为`undefined`或者不传入的时候会使用默认参数，但是传入`null`还是会覆盖默认参数。

### 2.2 强制参数
默认情况下，如果不向函数参数传值，那么JS 会将函数参数设置为`undefined`。其它一些语言则会发出警告或错误。要执行参数分配，可以使用`if`语句抛出未定义的错误，或者可以利用`强制参数`。
```js
mandatory = ( ) => {
  throw new Error('Missing parameter!');
}
foo = (bar = mandatory( )) => {            // 这里如果不传入参数，就会执行manadatory函数报出错误
  return bar;
}
```

### 2.3 隐式返回值
返回值是我们通常用来返回函数最终结果的关键字。只有一个语句的箭头函数，可以隐式返回结果（函数必须省略大括号`{ }`，以便省略返回关键字）。

要返回多行语句（例如对象文本），需要使用`( )`而不是`{ }`来包裹函数体。这样可以确保代码以单个语句的形式进行求值。
```js
function calcCircumference(diameter) {
  return Math.PI * diameter
}
// 简写为：
calcCircumference = diameter => (
  Math.PI * diameter;
)
```

### 2.4 惰性载入函数

在某个场景下我们的函数中有判断语句，这个判断依据在整个项目运行期间一般不会变化，所以判断分支在整个项目运行期间只会运行某个特定分支，那么就可以考虑惰性载入函数

```js
function foo(){
    if(a !== b){
        console.log('aaa')
    }else{
        console.log('bbb')
    }
}

// 优化后
function foo(){
    if(a != b){
        foo = function(){
            console.log('aaa')
        }
    }else{
        foo = function(){
            console.log('bbb')
        }
    }
    return foo();
}
```

那么第一次运行之后就会覆写这个方法，下一次再运行的时候就不会执行判断了。当然现在只有一个判断，如果判断很多，分支比较复杂，那么节约的资源还是可观的。

### 2.5 一次性函数

跟上面的惰性载入函数同理，可以在函数体里覆写当前函数，那么可以创建一个一次性的函数，重新赋值之前的代码相当于只运行了一次，适用于运行一些只需要执行一次的初始化代码

```js
var sca = function() {
    console.log('msg')
    sca = function() {
        console.log('foo')
    }
}
sca()        // msg
sca()        // foo
sca()        // foo
```





## 3. 代码复用

### 3.1 Object [key]
虽然将 `foo.bar` 写成 `foo ['bar']` 是一种常见的做法，但是这种做法构成了编写可重用代码的基础。许多框架使用了这种方法，比如element的[表单验证](http://element-cn.eleme.io/#/zh-CN/component/form#biao-dan-yan-zheng)。

请考虑下面这个验证函数的简化示例：
```js
function validate(values) {
  if(!values.first)
    return false;
  if(!values.last)
    return false;
  return true;
}
console.log(validate({first:'Bruce',last:'Wayne'})); // true
```
上面的函数完美的完成验证工作。但是当有很多表单，则需要应用验证，此时会有不同的字段和规则。如果可以构建一个在运行时配置的通用验证函数，会是一个好选择。
```js
// object validation rules
const schema = {
  first: {
    required:true
  },
  last: {
    required:true
  }
}

// universal validation function
const validate = (schema, values) => {
  for(field in schema) {
    if(schema[field].required) {
      if(!values[field]) {
        return false;
      }
    }
  }
  return true;
}
console.log(validate(schema, {first:'Bruce'})); // false
console.log(validate(schema, {first:'Bruce',last:'Wayne'})); // true
```
现在有了这个验证函数，我们就可以在所有窗体中重用，而无需为每个窗体编写自定义验证函数。

## 4. 数字字面量
### 4.1 不同进制表示法

ES6中新增了不同进制的书写格式，在后台传参的时候要注意这一点。

```js
29            // 10进制
035            // 8进制29      原来的方式
0o35            // 8进制29      ES6的方式
0x1d            // 16进制29
0b11101            // 2进制29
```

### 4.2 精确到指定位数的小数

将数字四舍五入到指定的小数位数。使用 `Math.round()` 和模板字面量将数字四舍五入为指定的小数位数。 省略第二个参数 `decimals` ，数字将被四舍五入到一个整数。

```js
const round = (n, decimals = 0) => Number(`${Math.round(`${n}e${decimals}`)}e-${decimals}`)
round(1.345, 2) 				// 1.35
round(1.345, 1) 				// 1.3
```



### 4.3 数字补0操作
感谢网友 @JserWang @vczhan 提供 这个小技巧
有时候比如显示时间的时候有时候会需要把一位数字显示成两位，这时候就需要补0操作，可以使用`slice`和string的`padStart`方法
```js
const addZero1 = (num, len = 2) => (`0${num}`).slice(-len)
const addZero2 = (num, len = 2) => (`${num}`).padStart( len   , '0')
addZero1(3) // 03
 
addZero2(32,4)  // 0032
```






## 5. 数组

### 5.1 reduce方法同时实现map和filter
假设现在有一个数列，你希望更新它的每一项（map的功能）然后筛选出一部分（filter的功能）。如果是先使用map然后filter的话，你需要遍历这个数组两次。
在下面的代码中，我们将数列中的值翻倍，然后挑选出那些大于50的数。
```js
const numbers = [10, 20, 30, 40];
const doubledOver50 = numbers.reduce((finalList, num) => {
  num = num * 2;
  if (num > 50) {
    finalList.push(num);
  }
  return finalList;
}, []);
doubledOver50;            // [60, 80]
```

### 5.2 统计数组中相同项的个数
很多时候，你希望统计数组中重复出现项的个数然后用一个对象表示。那么你可以使用reduce方法处理这个数组。

下面的代码将统计每一种车的数目然后把总数用一个对象表示。
```js
var cars = ['BMW','Benz', 'Benz', 'Tesla', 'BMW', 'Toyota'];
var carsObj = cars.reduce(function (obj, name) {
  obj[name] = obj[name] ? ++obj[name] : 1;
  return obj;
}, {});
carsObj; // => { BMW: 2, Benz: 2, Tesla: 1, Toyota: 1 }
```

### 5.3 使用解构来交换参数数值
有时候你会将函数返回的多个值放在一个数组里。我们可以使用数组解构来获取其中每一个值。

```js
let param1 = 1;
let param2 = 2;
[param1, param2] = [param2, param1];
console.log(param1) // 2
console.log(param2) // 1
```

当然我们关于交换数值有不少其他办法：

```js
var temp = a; a = b; b = temp                
b = [a, a = b][0]                         
a = a + b; b = a - b; a = a - b			
```

### 5.4 接收函数返回的多个结果

在下面的代码中，我们从/post中获取一个帖子，然后在/comments中获取相关评论。由于我们使用的是async/await，函数把返回值放在一个数组中。而我们使用数组解构后就可以把返回值直接赋给相应的变量。
```js
async function getFullPost(){
  return await Promise.all([
     fetch('/post'),
     fetch('/comments')
  ]);
}
const [post, comments] = getFullPost();
```

### 5.5 将数组平铺到指定深度

使用递归，为每个深度级别 `depth` 递减 1 。 使用 `Array.reduce()` 和 `Array.concat()` 来合并元素或数组。 基本情况下，`depth` 等于 1 停止递归。 省略第二个参数，`depth` 只能平铺到 1 (单层平铺) 的深度。

```js
const flatten = (arr, depth = 1) =>
  depth != 1
    ? arr.reduce((a, v) => a.concat(Array.isArray(v) ? flatten(v, depth - 1) : v), [])
    : arr.reduce((a, v) => a.concat(v), []);
flatten([1, [2], 3, 4]);                    		 // [1, 2, 3, 4]
flatten([1, [2, [3, [4, 5], 6], 7], 8], 2);           // [1, 2, 3, [4, 5], 6, 7, 8]
```
### 5.6 数组的对象解构

数组也可以对象解构，可以方便的获取数组的第n个值

```js
const csvFileLine = '1997,John Doe,US,john@doe.com,New York';
const { 2: country, 4: state } = csvFileLine.split(',');

country			// US
state			// New Yourk
```












## 6. 对象
### 6.1 使用解构删除不必要属性
有时候你不希望保留某些对象属性，也许是因为它们包含敏感信息或仅仅是太大了（just too big）。你可能会枚举整个对象然后删除它们，但实际上只需要简单的将这些无用属性赋值给变量，然后把想要保留的有用部分作为剩余参数就可以了。

下面的代码里，我们希望删除_internal和tooBig参数。我们可以把它们赋值给internal和tooBig变量，然后在cleanObject中存储剩下的属性以备后用。
```js
let {_internal, tooBig, ...cleanObject} = {el1: '1', _internal:"secret", tooBig:{}, el2: '2', el3: '3'};

console.log(cleanObject);                         // {el1: '1', el2: '2', el3: '3'}
```

### 6.2 在函数参数中解构嵌套对象
在下面的代码中，engine是对象car中嵌套的一个对象。如果我们对engine的vin属性感兴趣，使用解构赋值可以很轻松地得到它。
```js
var car = {
  model: 'bmw 2018',
  engine: {
    v6: true,
    turbo: true,
    vin: 12345
  }
}
const modelAndVIN = ({model, engine: {vin}}) => {
  console.log(`model: ${model} vin: ${vin}`);
}
modelAndVIN(car); // => model: bmw 2018  vin: 12345
```



## 7. 代码复用

### 7.1 Object [key]

虽然将 `foo.bar` 写成 `foo ['bar']` 是一种常见的做法，但是这种做法构成了编写可重用代码的基础。许多框架使用了这种方法，比如element的[表单验证](http://element-cn.eleme.io/#/zh-CN/component/form#biao-dan-yan-zheng)。

请考虑下面这个验证函数的简化示例：

```js
function validate(values) {
  if(!values.first)
    return false;
  if(!values.last)
    return false;
  return true;
}
console.log(validate({first:'Bruce',last:'Wayne'})); // true
```

上面的函数完美的完成验证工作。但是当有很多表单，则需要应用验证，此时会有不同的字段和规则。如果可以构建一个在运行时配置的通用验证函数，会是一个好选择。

```js
// object validation rules
const schema = {
  first: {
    required:true
  },
  last: {
    required:true
  }
}
 
// universal validation function
const validate = (schema, values) => {
  for(field in schema) {
    if(schema[field].required) {
      if(!values[field]) {
        return false;
      }
    }
  }
  return true;
}
console.log(validate(schema, {first:'Bruce'})); // false
console.log(validate(schema, {first:'Bruce',last:'Wayne'})); // true
```

现在有了这个验证函数，我们就可以在所有窗体中重用，而无需为每个窗体编写自定义验证函数。



---
网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出~

> 参考：
> 1. [JavaScript 开发人员需要知道的简写技巧](https://my.oschina.net/powertoolsteam/blog/1555271)
> 2. [《Effective Javascript》](https://book.douban.com/subject/25786138/)
> 3. [不得不知的ES6小技巧](http://mp.weixin.qq.com/s/NAbvosbJ4utOgFaM-6wO4Q "不得不知的ES6小技巧")
> 4. [js运算符的一些特殊应用](https://www.cnblogs.com/daysme/p/6492398.html)
> 5. [JS高级技巧(简洁版)](https://juejin.im/post/5aeff683f265da0ba351f786)

> 推介阅读：
> [ES6演示小网站](http://es6-features.org)
