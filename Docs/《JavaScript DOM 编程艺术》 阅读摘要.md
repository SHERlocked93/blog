# 《JavaScript DOM 编程艺术》 阅读摘要

**概念：**

- 平稳退化
- 渐进增强
- 以用户为中心

## 第一章 js简史

可以使用`DOM`（Document Object Model）给`HTML`（HyperText Markup Language）文档增加交互能力，就像`CSS`（Cascading Style Sheet）给文档增加样式一样。`DOM`是一种`API`（Application Programing Interface），就是一种已得到各方认同的基本约定，作为一种标准可以使得人们更方便的进行交流和合作，类似于化学元素周期表、莫尔斯码，W3C联盟推出的标准化DOM理论上可以让任何一种程序设计语言对使用任何一种标记语言编写出来的任何一份文档进行操控。

W3C联盟对DOM的**定义**：一个与系统平台和编程语言无关的接口，程序和脚本可以通过这个接口动态的访问和修改文档的内容、结构和样式。

## 第二章 js语法

### 准备工作

程序语言分为解释型和编译型两大类

1. 编译型

Java、C++等语言需要一个编译器（Compiler）。编译器是一种程序，能够把用Java等解释型高级语言编写出来的源代码翻译为直接在计算机上执行的文件。  
编译型的语言编写的代码如果有错误，这些错误会在代码编译阶段就会被发现。与解释型语言相比速度更快，可移植性更高，但学习曲线也更陡峭。

1. 解释型

解释型语言不需要编译器，仅需要解释器。对于JavaScript语言，在互联网环境下Web浏览器负责完成有关的解释和执行工作。浏览器中的JavaScript解释器将直接读入源代码并执行。浏览器中如果没有解释器，JavaScript代码就无法执行。  
解释型语言编写的代码只能等到解释器执行到有关代码时才能被发现。

### 语法

每行结尾并不一定需要分号，不过为了更容易追踪JavaScript脚本的执行顺序还是推介加上；  
var不关心变量的类型，ex：

```text
var str="happy", str1 = 50;
str = 33;
```

字符串可以包括在双引号或者单引号里，如果在引号中包括引号，那么需要对这个字符进行转义（escaping）：

```text
var str="about 5'10\" tall";
```

- 数组声明：

```text
var beatles = ["John", "Paul", "George", "Ringo", true, 44, strA, [0, false, "my Dog", strB]];
var arr1 = Array();
var arr2 = [];
arr2["name"] = "John";
```

- 对象声明：

```text
var lennon = Object();
lennon.name = "Smith";
var lennon1 = {name: "Ringo", age: 78};
```

- 比较操作符：

```text
var strC = false;
if (strC == "") {
    alert("xixi");        //会输出
}
```

相等操作符 `==` 会认为false与空字符串含义相同，如果要进行严格比较，则需要全等操作符 `===`，全等操作符会执行严格的比较，不仅会比较值，还会比较变量的类型，严格不相等也类似 `!==` 。ex：

```text
var strC = false;
if (strC === "") {
    alert("xixi");        //不会输出
}
```

在if()或者while()的判断条件中，整数中0被判断为false，除了0之外都为true包括负数。

```text
while (-1.1) {
    alert("memeda");      //会一直输出
}
```

for循环:

```text
var beatles = ["John", "Paul", "George", "Ringo", true, 44, [0, false, "my Dog", strB]];
for (var strE = 0; strE < beatles.length; strE++) {
    alert(beatles[strE]);
}
```

函数：

```text
function shout(para) {
    var beatles = [para, 44];
    for (var strE = 0; strE < beatles.length; strE++) {
        alert(beatles[strE]);
    }
}
shout("xixixi");        //弹出2条alert： xixixi , 44
```

变量和函数的命名（为了能一眼看出哪些是变量，哪些是函数）：

- 变量使用下划线来分割各个单词，如`temp_celsius`；
- 函数名使用首字母小写的驼峰命名法，如`convertToCelsius`；

内建对象（Native Object）:

- Array
- Math

```text
var num = 7.454;
num = Math.round(num);
alert(num);                    //输出四舍五入结果：7
```

- Date

```text
var current_date=new Date();
var today=current_date.getDate();
alert(today);                  //输出当天日期
```

etc...

## 第三章 DOM

DOM是针对XML但是经过扩展用于HTML的应用程序编程接口。DOM把整个页面映射为一个多层节点结构。

### DOM中的D

D指的是document，当创建了一个网页并将其加载到web浏览器中时，DOM已经被创建，它把编写的网页文档转换成一个文档对象。

### DOM中的O

O指的是对象object，js中的对象包括：

- 用户自定义对象（user-defined object）：自行创建的对象
- 内建对象（native object）：内建在js中的对象，如Array、Math、Date
- 宿主对象（host object）：由浏览器提供的对象

最基础的宿主对象：window对象：

```text
window.open("http://www.baidu.com", "","", false);    //弹出百度窗口，也可以是新窗口
```

### DOM中的M

M指的是Model，有三种DOM方法可以获取元素节点，分别是通过ID，通过标签名，和通过类名来获取。

- getElementById

返回一个有着给定ID属性值的元素节点对应的对象，它是document对象特有的函数，并且形参是要获取的id值，放在单引号或双引号里：

```text
<h1 title="memeda" id="header_h1">Hello World!</h1>
<script>
    alert(document.getElementById("header_h1").getAttribute("title"));    //弹出 memeda
</script>
```

- getElementsByTagName

返回一个对象数组，每个对象对应着文档里有着给定标签的一个元素，形参是标签，且在引号内：

```text
<ul>
    <li>Data1</li>
    <li>Data2</li>
    <li>Data3</li>
</ul>
<script>
    alert(document.getElementsByTagName("li").length);    //弹出 3
</script>
```

- getElementsByClassName

返回具有Class名的对象数组，还可以查找那些带有多个类名的元素，并不是所有浏览器都支持：

```text
<ul>
    <li class="data_1 data_2">Data1</li>
    <li class="data_1">Data2</li>
    <li class="data_2">Data3</li>
</ul>
<script>
    alert(document.getElementsByClassName("data_1 data_2").length);    //弹出 1 ，只有一个元素既有data_1也有data_2
</script>
```

如果浏览器不一定支持，那么可以使用：

```text
function getElementsByClassName(node, classname) {    //node是DOM树中搜索起点，也可以是document，不支持多个class搜索
    if (node.getElementsByClassName) {
        return node.getElementsByClassName(classname);
    } else {
        var results = [];
        var elems = node.getElementsByTagName("*");
        for (var i = 0; i < elems.length; i++) {
            if (elems[i].className.indexOf(classname) != -1) {
                results[results.length] = elems[i];
            }
        }
    }
}
```

- getAttribute & setAttribute

可以用来获取和设置节点的属性：

```text
<h1 title="memeda" id="header_h1">Hello World!</h1>
<script>
    var shop=document.getElementById("header_h1");
    alert(shop.getAttribute("title"));
    shop.setAttribute("title","xixi");
    alert(shop.getAttribute("title"));
</script>
```

通过`setAttribute`对文档作出修改后，通过查看源代码发现文档源代码仍然是改变之前的值，也就是说，`setAttribute`作出的修改并不会反映到文档本身的源代码里，原因是DOM的工作模式：**先加载文档的静态内容，再动态刷新，动态刷新不影响文档的静态内容**。  
这正是DOM的真正威力：**对页面内容进行刷新却不需要在浏览器里刷新页面。**

## 第四章 js图片库

需要说明的是，若一个站点要用到多个js文件，为了减少对站点的请求次数提高性能，应该把这些js文件合并到一个文件中。图片同理。

实例：

```text
<ul>
    <li><a href="../imgs/aaa.jpeg" onclick="showpic(this); return false;">Data1</a></li>
    <li><a href="../imgs/step.png" onclick="showpic(this); return false;">Data2</a></li>
    <li><a href="../imgs/arrow-right-bold.png" onclick="showpic(this); return false;">Data3</a></li>
    <li><a href="../imgs/dazongdianpin_logo.png" onclick="showpic(this); return false;">Data4</a></li>
</ul>
<img id="placeholder" src="../imgs/CD.jpg" alt="My image gallery">

<script>
    function showpic(whichpic) {
        document.getElementById("placeholder").setAttribute("src", whichpic.getAttribute("href"));
    }
</script>
```

实现一个在点击a标签时把placeholder占位图片替换成a标签对应的图片，并拦截点击a时网页的默认行为。  
另外，setAttribute方法是DOM Level1 的内容，它可以设置任意元素节点的任意属性，在DOM Level1出现之前的HTML-DOM还可以通过：`element.value="value"`来直接设置元素的属性，不过不推介使用这种方式，这种方式只适用于web文档，而DOM则适用于任何一种标记语言，因为“DOM是一种适用于多种环境和多种程序设计语言的通用型API”，比如xml，为了更好的移植性，严格遵守DOM Level1可以避免很多问题。

- nodeType属性可以得到任何节点的节点属性：

  - 元素节点的nodeType值为1
  - 属性节点的nodeType值为2
  - 文本节点的nodeType值为3
- nodeValue属性：

可以用来检索节点的值，也可以用来设置节点的值。

```text
<ul>
    <li><a href="#" onclick="showa(this);return false;">xixi1</a></li>
    <li><a href="#" onclick="showa(this);return false;">xixi2</a></li>
    <li><a href="#" onclick="showa(this);return false;">xixi3</a></li>
</ul>
<p id="description">Hello</p>
<script>
    function showa(whicha) {
        document.getElementById("description").firstChild.nodeValue = whicha.firstChild.nodeValue;
    }
</script>
```

## 第五章 最佳实践

### 平稳退化

平稳退化（graceful degradation）确保网页在没有js的情况下也能正常工作；就是说，虽然某些功能无法使用，但最基本的操作仍能顺利实现。

```text
<a href="http://www.baidu.com/" onclick="openw(this.href);return false;">Example</a>
<script>
    function openw(urlStr) {
        window.open(urlStr, "ppp", "width=400,height=600");
    }
</script>
```

这种方式比JavaScript伪协议：`href="javascript:..."`和`href="#" onclick=“...”`，方式效果要好得多，即使在js功能已被禁用或者遇到爬虫的情况下，链接也是可用的，虽然功能上打了折扣，但是并没有彻底失效。

### 渐进增强

**渐进增强**（progressive enhancement）原则基于这样一种思想：实现良好的结构应该从最核心的部分，也就是从内容开始。根据内容使用标记实现良好的结构；然后再逐步加强这些内容，这些增强工作可以是通过css改进呈现效果，也可以通过DOM添加各种行为，如果使用DOM来添加核心内容，那么这是不推介的，并且也不利于网站SEO，js也没有任何空间去平稳退化，那些缺乏js支持的访问者就无法看到其内容。

### 向后兼容

确保老版本的浏览器不会因为你的js而挂掉；  
可以使用对象检测（object detection）：

```text
window.onload = function () {
    if (!document.getElementsByTagName()) return false;
}
```

检测浏览器是否支持这一方法，来避免老版本浏览器不会因为新加入的js出错。

### 分离js

把网页的结构和内容与js脚本的动作行为分开；

### 性能考虑

确保脚本执行的性能最优；

- 避免搜索浪费

```text
if(document.getElementsByTagName("a").length>0){        //不推介
    var links=document.getElementsByTagName("a");
    for(var i=0;i<links.length;i++){        
    }
}
```

这样会进行两次`.getElementsByTagName()`搜索，造成性能浪费，因此不推介。如果有多个函数重复做一件事，那么可以把搜索结果放在全局变量中，或者把一组元素直接以参数形式传递给函数，以免造成搜索浪费。

- 合并与放置脚本

在`<head>`部分的脚本会导致浏览器无法并行加载其他文件，因此推介在文档末尾`</body>`之前引入`script`元素，可以让页面变得更快；根据HTTP规范，浏览器每次从同一个域名最多只能同时下载两个文件，而在下载脚本期间，浏览器不会下载其他任何文件，即使是来自不同域名的文件也不会下载，所有其他资源要等脚本加载完毕后才能下载。

- 压缩脚本

可以使用压缩工具来删除脚本文件中不必要的字节，比如空格和注释，有的压缩工具设置会重写部分代码，使用更短的变量名，从而减少整体文件大小。精简后的代码不易看懂，但会大幅减小文件大小，一般会在压缩后的文件名后加上`.min.`，比如 `scriptName.min.js` 。

## 第六章 案例：图片库改进

ex：

```text
<ul id="imagegallery">
    <!--平稳退化-->
    <li><a href="../imgs/aaa.jpeg">Data1</a></li>
    <li><a href="../imgs/step.png">Data2</a></li>
    <li><a href="../imgs/arrow-right-bold.png">Data3</a></li>
    <li><a href="../imgs/dazongdianpin_logo.png">Data4</a></li>
</ul>
<img id="placeholder" src="../imgs/CD.jpg" alt="My image gallery">

<script>
    addLoadEvent(prepareGallery);
    function prepareGallery() {
        if (!document.getElementById) alert("1");
        if (!document.getElementsByTagName) alert("2");               //检查浏览器是否支持这个DOM方法
        if (!document.getElementById("imagegallery")) alert("3");     //即使在网页上删除了这个img或者id，js也不会出错

        var gallery = document.getElementById("imagegallery");
        var links = gallery.getElementsByTagName("a");
        for (var i = 0; i < links.length; i++) {
            links[i].onclick = function () {
                return !showpic(this);                                //由showpic返回值决定是否取消浏览器执行链接被点击时的默认操作
            }
        }
    }
    function showpic(whichpic) {
        if (!document.getElementById("placeholder")) return false;

        whichpic.getAttribute("href").setAttribute("src", whichpic.getAttribute("href"));
        return true;                                                  //setAttribute成功才会返回true
    }
    function addLoadEvent(func) {                                     //将函数添加到页面加载时执行
        var oldonload = window.onload;
        if (typeof window.onload != 'function') {
            window.onload = func;
        } else {
            window.onload = function () {
                oldonload();
                func();
            }
        }
    }
</script>
```

## 第七章 动态创建标记

### 传统方法

`document.write`可以方便的把字符串插入文档（不推介）

```text
<div id="test-div"></div>
<script>
    document.write("<p>This is a <em>content</em> script!;</p>");
</script>
```

`innerHTML`方法会替换元素内的所有内容。

```text
<div id="test-div"></div>
<script>
    window.onload = function () {
        var testdiv = document.getElementById("test-div");
        testdiv.innerHTML = "<p>This is a <em>content</em> script;</p>"
    }
</script>
```

### DOM方法

插入节点的子元素后

```text
<div id="test-div"></div>
<script>
    var newE = document.createElement("p");                        //创建新元素节点，不可以使用.firstChild.nodeValue赋值，因为创建的标签的nodeValue是null
    var newT = document.createTextNode("hello world~");            //创建新文本节点
    newE.appendChild(newT);                                        //把文本节点插入元素节点的最后面
    document.getElementById("test-div").appendChild(newE);         //把元素节点插入原有节点的最后面
</script>
```

插入元素后：

```text
var place = document.createElement("p");
place.appendChild(document.createTextNode("百度"));
var tar = document.getElementById("tar");

tar.parentNode.insertBefore(place, tar);
```

插入元素前：

```text
var place = document.createElement("p");
place.appendChild(document.createTextNode("百度"));
var tar = document.getElementById("tar");

insertAfter(place, hhh);

function insertAfter(newElement, targetElement) {       //插入目标元素后
    var parent = targetElement.parentNode;
    if (parent.lastChild === targetElement) {
        parent.appendChild(newElement);
    } else {
        parent.insertBefore(newElement, targetElement.nextElementSibling);
    }
}
```

### Ajax

Ajax的主要优势是对页面的请求以异步的方式发送到服务器。而服务器不会用整个页面来响应请求，它会在后台处理请求，与此同时用户还能继续浏览页面并与页面交互脚本则可以按需加载和创建页面内容，而不会打断用户的浏览体验。  
Ajax的核心是XMLHttpRequest对象，这个对象充当浏览器中的客户端与服务器之间的桥梁角色，以往的请求由浏览器发出，而js通过这个对象可以自己发送请求，同事也自己处理响应。

```text
<div id="new"></div>

<script>
    function getNewContent() {
        var request = new getHTTPObject();
        if (request) {
            request.open("GET", "test.txt", true);
            request.onreadystatechange = function () {
                if (request.readyState === 4) {
                    var para = document.createElement("p");
                    var txt = document.createTextNode(request.responseText);
                    para.appendChild(txt);
                    document.getElementById("new").appendChild(para);
                }
            };
            request.send(null);
        } else {
            alert('sorry, your browser doesn\'t support XMLHttpRequest');
        }
        alert("func done!");
    }

    addLoadEvent(getNewContent);

    function addLoadEvent(func) {                                   //  将函数添加到页面加载时执行
        var oldonload = window.onload;
        if (typeof window.onload !== 'function') {
            window.onload = func;
        } else {
            window.onload = function () {
                oldonload();
                func();
            };
        }
    }

    function getHTTPObject() {
        if (typeof XMLHttpRequest === "undefined")
            XMLHttpRequest = function () {
                try {return new ActiveXObject("Msxml2.XMLHTTP.6.0");}
                catch (e) {}
                try {return new ActiveXObject("Msxml2.XMLHTTP.3.0");}
                catch (e) {}
                try {return new ActiveXObject("Msxml2.XMLHTTP");}
                catch (e) {}
                return false;
            };
            return new XMLHttpRequest();
    }
</script>
```

## 第八章 充实文档内容

js脚本只应该用来充实文档的内容，而避免使用DOM来创建核心内容；  
遍历快捷键，ex：

```text
<ul id="navigation">
    <li><a href="#" accesskey="1">home</a></li>
    <li><a href="#" accesskey="2">contact</a></li>
    <li><a href="#" accesskey="3">search</a></li>
</ul>
<script>
    function displayAccesskeys() {
        if (!document.getElementsByTagName) return false;
        var links = document.getElementsByTagName("a");
        var tags = [];
        if (links.length < 1) return false;
        for (var i = 0; i < links.length; i++) {
            if (!links[i].getAttribute("accesskey")) continue;
            var source = links[i].lastChild.nodeValue;
            var key = links[i].getAttribute("accesskey");
            tags[key] = source;
        }
        var list = document.createElement("ul");
        for (key in tags) {
            var txt = key + " : " + tags[key];
            var li = document.createElement("li");
            var li_txt = document.createTextNode(txt);
            li.appendChild(li_txt);
            list.appendChild(li);
        }
        insertAfter(list, document.getElementById("navigation"));
    }
    addLoadEvent(displayAccesskeys);
    function addLoadEvent(func) {                           //将函数添加到页面加载时执行
        var oldonload = window.onload;
        if (typeof window.onload !== 'function') {
            window.onload = func;
        } else {
            window.onload = function () {
                oldonload();
                func();
            };
        }
    }
    function insertAfter(newElement, targetElement) {       //插入目标元素后
        var parent = targetElement.parentNode;
        if (parent.lastChild === targetElement) {
            parent.appendChild(newElement);
        } else {
            parent.insertBefore(newElement, targetElement.nextElementSibling);
        }
    }
</script>
```

---
