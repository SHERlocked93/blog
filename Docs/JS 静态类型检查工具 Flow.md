# JS 静态类型检查工具 Flow

本文主要介绍了解决JS作为弱类型语言没有类型检查痛点的静态类型检查工具 `Flow` ，并且介绍了在WebStorm中使用Flow的方法，最后介绍了一些常用的Flow语法。

## 1. 简介

JS作为一种脚本语言是没有类型检测的，这个特点有时候用着很方便，但在一个较大的项目中就会发现这其实是一件挺糟糕的特性，因为和你协作的程序员往往不太清楚你所写的代码到底哪种类型才是正确的，等到代码重构就比较麻烦。于是基于这个需求有了Typescript和Flow的产生，今天这里主要介绍`Flow`。

[Flow](https://link.segmentfault.com/?enc=YMZRHiNtY4l6SHevEVcKhw%3D%3D.WgPgtkt2babBqCuFwg6sXRMw3f6K1KvjYr7JaM7DMpSJASL2KbQ6TJKdizpJ%2BOkF)是一个由Facebook出品的JavaScript静态类型检查工具，它与Typescript不同的是，它可以部分引入，不需要完全重构整个项目，所以对于一个已有一定规模的项目来说，迁移成本更小，也更加可行。除此之外，Flow可以提供实时增量的反馈，通过运行Flow server不需要在每次更改项目的时候完全从头运行类型检查，提高运行效率。Flow和Typescript都是给Javascript增加类型检查的优秀解决方案，两者的简单对比如下：

| 工具 | Flow | TypeScript |
| --- | --- | --- |
| 公司 | Facebook | 微软 |
| star | 16k | 33k |
| 文档支持程度 | 中等 | 多 |
| 优点 | 自由度高，老项目迁移成本低 | 工程化强，社区活跃，官方支持力度高 |

对于两者使用场景差别，可以简单总结为：对于新项目，可以考虑使用TypeScript或者Flow，对于已有一定规模的项目则建议使用Flow进行较小成本的逐步迁移来引入类型检查。Flow可以帮助找出由于不合理的类型操作引起的错误，包括运算符操作，函数参数类型和返回值类型等。Flow也支持自定义类型声明，泛型声明等类型语言相关的操作，详细的内容可以参考[文档](https://link.segmentfault.com/?enc=AMjmbIsaMYO61YEHbGTxKA%3D%3D.y355RBWwxkTZ6HjwQV8aUzMHYaUfqPPisCnaZYLBmDk%3D)。

**引入方法：**在需要使用 Flow 进行类型检查的 js 文件开头加入 `// @flow` 或者 `/* @flow */`，即可引入Flow，一个简单例子：

```text
// @flow
function square(n: number): number {
  return n * n;
}

square("2"); // Error!
```

## 2. 安装方法

npm安装：

```text
npm install --save-dev babel-cli babel-preset-flow flow-babel-webpack-plugin babel-preset-es2015 babel-preset-env babel-plugin-transform-class-properties
```

我是全局安装的：

```text
npm install -g babel-cli babel-preset-flow flow-bin flow-babel-webpack-plugin babel-preset-es2015  babel-preset-env babel-plugin-transform-class-properties
```

在`.babelrc`文件加入：

```text
{
  "presets": ["flow", "es2015"],
  "plugins": [
    "transform-vue-jsx",
    "transform-runtime",
    "transform-class-properties"
  ]
}
```

设置一下WebStorm：通过 `File>Settings>Languages&Frameworks>JavaScript` 选择Flow，Flow package可以选择你项目下的flow-bin，当然你也可以全局安装flow-bin，然后在这里设置后就可以在每个项目中都使用Flow了 。  
但是flow不能直接在node或浏览器环境中使用，所以我们必须用babel编译后才能使用，使用File watcher：

![clipboard.png](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/493a46c7d666a77caf86536022b2bc7f0c59d69bf263068f1dd9746d7a347b93.png "clipboard.png")

在项目目录下运行`flow init`，会自动生成一个文件`.flowconfig`，这个文件可以配置flow，我的配置：

```text
[ignore]
.*/node_modules/.*
<PROJECT_ROOT>/build/.*
<PROJECT_ROOT>/config/.*

[options]
module.file_ext=.js
module.file_ext=.vue
```

现在当我们在项目中使用Flow时WebStorm可以给出智能的提示了。

![clipboard.png](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/cc55cc174c407ecbace986f98e9fea9b10860852a5d5409a8563a1c5c029fce2.png "clipboard.png")

并且多了一个窗口 Flow 给出文档中所有提示：

![clipboard.png](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/87e386150859f7d0ab340c14f25ef55cef1b4f05ac8ca45f73cad8dc9b219a66.jpg "clipboard.png")

## 3. 使用

最新的 ECMAScript 标准定义了 7 种数据类型: 6种原始类型:Boolean、Null、Undefined、Number、String、Symbol 和 Object

在Flow中也是使用这几种类型作为标注:

使用原始类型：

```text
// @flow
function method(x: number, y: string, z: boolean) {
  // ...
}

method(3.14, "hello", true);
```

使用对象类型：

```text
// @flow
function method(x: Number, y: String, z: Boolean) {
  // ...
}

method(new Number(42), new String("world"), new Boolean(false));
```

这里需要注意的是大小写，小写的 number 是原始类型，而大写的 Number 是JavaScript的构造函数，是对象类型的。

#### Boolean

在Flow中，默认并不会转换类型，如果你需要转换类型请使用显示或隐式转换，例如：

```text
// @flow
function acceptsBoolean(value: boolean) {
  // ...
}

acceptsBoolean(true); // Works!
acceptsBoolean(false); // Works!
acceptsBoolean("foo"); // Error!
acceptsBoolean(Boolean("foo")); // Works!
acceptsBoolean(!!("foo")); // Works!
```

#### Number

```text
// @flow
function acceptsNumber(value: number) {
  // ...
}

acceptsNumber(42); // Works!
acceptsNumber(3.14); // Works!
acceptsNumber(NaN); // Works!
acceptsNumber(Infinity); // Works!
acceptsNumber("foo"); // Error!
```

#### null和void

JavaScript兼有 null 和 undefined。Flow将这些视为单独的类型：null 和 void（void表示undefined类型）

```text
// @flow
function acceptsNull(value: null) {
  /* ... */
}

function acceptsUndefined(value: void) {
  /* ... */
}

acceptsNull(null); // Works!
acceptsNull(undefined); // Error!
acceptsUndefined(null); // Error!
acceptsUndefined(undefined); // Works!
```

#### 也许类型

也许类型是用于可选值的地方，你可以通过在类型前添加一个问号（如 ?string 或者 ?number）来创建它们。

除了问号 ? 后跟着的类型，也许类型也可以是 null 或者 void 类型。

```text
// @flow
function acceptsMaybeString(value: ?string) {
  // ...
}

acceptsMaybeString("bar"); // Works!
acceptsMaybeString(undefined); // Works!
acceptsMaybeString(null); // Works!
acceptsMaybeString(); // Works!
```

#### 可选的对象属性

对象类型可以具有可选属性，问号 ? 位于属性名称后面。

```text
{ propertyName?: string }
```

除了它们的设定值类型之外，这些可选属性也可以被 void 完全省略。但是，他们不能 null。

```text
// @flow
function acceptsObject(value: { foo?: string }) {
  // ...
}

acceptsObject({ foo: "bar" }); // Works!
acceptsObject({ foo: undefined }); // Works!
acceptsObject({ foo: null }); // Error!
acceptsObject({}); // Works!
```

#### 可选的函数参数

函数可以具有可选参数，其中问号 ? 出现在参数名称后面。同样，该参数不能为 null。

```text
// @flow
function acceptsOptionalString(value?: string) {
  // ...
}

acceptsOptionalString("bar"); // Works!
acceptsOptionalString(undefined); // Works!
acceptsOptionalString(null); // Error!
acceptsOptionalString(); // Works!
```

#### 文字类型

文字类型使用一个具体的值作为类型：

```text
function foo(value: 2) {}

foo(2); // Work!
foo(3); // Error!
foo('2'); // Error!
```

您可以使用这些类型的原始值：

- 布尔值： true 或 false
- 数字：像 42 或 3.14
- 字符串：像 "foo" 或 "bar"

```text
// @flow
function getColor(name: "success" | "warning" | "danger") {
  switch (name) {
    case "success" : return "green";
    case "warning" : return "yellow";
    case "danger" : return "red";
  }
}

getColor("success"); // Works!
getColor("danger"); // Works!
// $ExpectError
getColor("error"); // Error!
```

#### 混合类型 mixed

有时候我们并不能确定需要的值到底是哪种类型，这时候我们可以使用混合类型来表示，但在使用该值之前，我们需要判断该值到底是哪种类型，否则会引起错误：

```text
// @flow
function stringify(value: mixed) {
  // $ExpectError
  return "" + value; // Error!
}

stringify("foo");
```

```text
// @flow
function stringify(value: mixed) {
  if (typeof value === 'string') {
    return "" + value; // Works!
  } else {
    return "";
  }
}

stringify("foo");
```

#### 任意类型 any

如果你想要一种方法来选择不使用类型检查器，any 是做到这一点的方法。使用any是完全不安全的，应尽可能避免。

例如，下面的代码不会报告任何错误：

```text
// @flow
function add(one: any, two: any): number {
  return one + two;
}

add(1, 2); // Works.
add("1", "2"); // Works.
add({}, []); // Works.
```

#### 接口类型 interface

你可以使用 interface 以声明您期望的类的结构。

```text
// @flow
interface Serializable {
  serialize(): string;
}

class Foo {
  serialize() { return '[Foo]'; }
}

class Bar {
  serialize() { return '[Bar]'; }
}

const foo: Serializable = new Foo(); // Works!
const bar: Serializable = new Bar(); // Works!
```

你也可以使用 implements 告诉Flow，你希望类匹配一个接口。这可以防止编辑类时发生不兼容的更改。

```text
// @flow
interface Serializable {
  serialize(): string;
}

class Foo implements Serializable {
  serialize() { return '[Foo]'; } // Works!
}

class Bar implements Serializable {
  // $ExpectError
  serialize() { return 42; } // Error!
}
```

#### 数组类型 Array

要创建一个数组类型，可以使用 `Array<Type>` 类型，其中 Type 是数组中元素的类型。例如，为你使用的数字数组创建一个类型 `Array<number>`。

```text
let arr: Array<number> = [1, 2, 3];
```

暂时就介绍这么多，还有一些类型文章中没有提到，更多更详细的内容请在[Flow官网](https://link.segmentfault.com/?enc=%2FSjLBEyY9tseMPOip8B5cw%3D%3D.o04navpAipMgMFg2Hs4Za3QRUqtnIUBf%2Fe9AYzWQrZ4%3D)中查看。

## 4. 移除Flow内容

因为Flow的语法并不是标准的JavaScript语法，所以我们要在代码最终上线前移除Flow相关的代码（主要是那些固定类型的描述，如果只是添加了@flow，直接应用即可）

### flow-remove-types

这个程序会将你所有标有@flow的内容进行移除。。然后将移除后的代码生成后指定的目录下

```text
npm i -g flow-remove-types
flow-remove-types src/ --out-dir dist/
# src 源文件地址
# dist 生成后的地址
```

### babel+webpack

安装一个webpack插件

```text
npm i -D flow-babel-webpack-plugin
```

然后我们修改 `.babelrc` 文件，添加如下配置：

```text
{
  "plugins": [
      "transform-flow-comments"
  ]
}
```

然后在`webpack.config.js`或 `webpack.dev.config.js`、 `webpack.prod.config.js`、文件中添加：

```text
const FlowBabelWebpackPlugin= require('flow-babel-webpack-plugin')
module.exports = {
  plugins: [
      new FlowBabelWebpackPlugin()
  ]
}
```

在babel编译JavaScript的同时也就会将Flow内容进行移除了。

---

> 参考：  
> [使用Flow来检测你的JS](https://link.segmentfault.com/?enc=HOUk0HumEkH2NlnCvGKGcw%3D%3D.WMzLtgW7Lm5RqzCx59l%2F%2FXHrTDRPRMsjBvRtYA32Vi%2F1QMItDJKZdqOHLNCrQFDl)   
> [vue2.0项目配置flow类型检查](https://link.segmentfault.com/?enc=96QjSWVcLvB%2BdGn16fLEfQ%3D%3D.af0U2M%2Be1%2FufxxwmO%2B8kvJKLvgMZVBKMsasDhL7Lt3liJGn%2FU%2B0ViR87MmpyfMEL)  
> [用flow.js提升前端开发的体验](https://segmentfault.com/a/1190000006983211)   
> [Flow静态类型检查及在Vue项目中的使用](https://link.segmentfault.com/?enc=E38xMrTiRVTmfqo%2Ba6zqvg%3D%3D.0JFkN6hu2OpfBUYNhftljZ4URWEPP7KAoJfEzmAw06JyD3N8NwNhhpaIY%2BfoALIh)   
> [如何在项目中使用 flow js](https://link.segmentfault.com/?enc=fTbcxWt3Zn8pksxVGtl8eA%3D%3D.wJYSf%2Fz7l75MzlMO17%2BLnAL6p8g2T8TP%2BmlGNJUBc%2FqY2%2Bj6DdJnyRxvIOS7ojLB)
