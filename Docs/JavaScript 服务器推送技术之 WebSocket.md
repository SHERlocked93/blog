# JavaScript服务器推送技术之 WebSocket

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/bc8acf28f268442a0a98544c876f35e1eb3904d8370dc7d2eeaeffc3c1444ae9.jpg)  
最近在工作中遇到了需要服务器推送消息的场景，这里总结一下收集整理WebSocket相关资料的收获。

## 1. 概述

### 1.1 服务器推送

**WebSocket**作为一种通信协议，属于[服务器推送技术](https://en.wikipedia.org/wiki/Push_technology)的一种，IE10+支持。

[服务器推送技术不止一种](http://www.daimajiayuan.com/sitejs-65893-1.html)，有短轮询、长轮询、WebSocket、Server-sent Events（SSE）等，他们[各有优缺点](https://mp.weixin.qq.com/s/unagcn33kfCnMrlI-Oslig)：

| # | 短轮询 | 长轮询 | Websocket | sse |
| --- | --- | --- | --- | --- |
| 通讯方式 | http | http | 基于TCP长连接通讯 | http |
| 触发方式 | 轮询 | 轮询 | 事件 | 事件 |
| 优点 | 兼容性好容错性强，实现简单 | 比短轮询节约资源 | 全双工通讯协议，性能开销小、安全性高，有一定可扩展性 | 实现简便，开发成本低 |
| 缺点 | 安全性差，占较多的内存资源与请求数 | 安全性差，占较多的内存资源与请求数 | 传输数据需要进行二次解析，增加开发成本及难度 | 只适用高级浏览器 |
| 适用范围 | b/s服务 | b/s服务 | 网络游戏、银行交互和支付 | 服务端到客户端单向推送 |

**短轮询**最简单，在一些简单的场景也会经常使用，就是隔一段时间就发起一个ajax请求。那么长轮询是什么呢？

**长轮询**(Long Polling)是在Ajax轮询基础上做的一些改进，在没有更新的时候不再返回空响应，而且把连接保持到有更新的时候，客户端向服务器发送Ajax请求，服务器接到请求后hold住连接，直到有新消息才返回响应信息并关闭连接，客户端处理完响应信息后再向服务器发送新的请求。它是一个解决方案，但不是最佳的技术方案。

如果说短轮询是客户端不断打电话问服务端有没有消息，服务端回复后立刻挂断，等待下次再打；长轮询是客户端一直打电话，服务端接到电话不挂断，有消息的时候再回复客户端并挂断。

**SSE**(Server-Sent Events)与长轮询机制类似，区别是每个连接不只发送一个消息。客户端发送一个请求，服务端保持这个连接直到有新消息发送回客户端，仍然保持着连接，这样连接就可以支持消息的再次发送，由服务器单向发送给客户端。然而IE直到11都不支持，不多说了....

### 1.2 WebSocket的特点

为什么已经有了轮询还要WebSocket呢，是因为短轮询和长轮询有个缺陷：通信只能由客户端发起。

那么如果后端想往前端推送消息需要前端去轮询，不断查询后端是否有新消息，而轮询的效率低且浪费资源（必须不停 setInterval 或 setTimeout 去连接，或者 HTTP 连接始终打开），WebSocket提供了一个文明优雅的全双工通信方案。一般适合于对数据的实时性要求比较强的场景，如通信、股票、直播、共享桌面，特别适合于客户端与服务频繁交互的情况下，如聊天室、实时共享、多人协作等平台。

#### 特点

1. 建立在 TCP 协议之上，服务器端的实现比较容易。
2. 与 HTTP 协议有着良好的兼容性。默认端口也是80和443，并且握手阶段采用 HTTP 协议，因此握手时不容易屏蔽，能通过各种 HTTP 代理服务器。
3. 数据格式比较轻量，性能开销小，通信高效。服务器与客户端之间交换的标头信息大概只有2字节;
4. 可以发送文本，也可以发送二进制数据。
5. 没有同源限制，客户端可以与任意服务器通信。
6. 协议标识符是`ws`（如果加密，则为wss），服务器网址就是 URL。ex：`ws://example.com:80/some/path`
7. 不用频繁创建及销毁TCP请求，减少网络带宽资源的占用，同时也节省服务器资源;
8. WebSocket是纯事件驱动的，一旦连接建立，通过监听事件可以处理到来的数据和改变的连接状态，数据都以帧序列的形式传输。服务端发送数据后，消息和事件会异步到达。
9. 无超时处理。

#### HTTP与WS协议结构

WebSocket协议标识符用`ws`表示。`wss协议表示加密的WebSocket协议，对应HTTPs协议。结构如下：

- **HTTP**: TCP > HTTP
- **HTTPS**: TCP > TLS > HTTP
- **WS**: TCP > WS
- **WSS**: TCP > TLS > WS

## 2 WebSocket的通信过程

首先，Websocket是一个持久化的协议，相对于HTTP这种非持久的协议来说。

一个HTTP的通信生命周期通过 Request 来界定，也就是一个 Request 一个 Response ，那么在 HTTP1.0 中，这次HTTP请求就结束了。   
在HTTP1.1中进行了改进，有了一个`keep-alive`，在一个HTTP连接中，可以发送多个Request，接收多个Response，也就是合并多个请求。但是一个Request只能对应一个Response，而且这个Response是被动的，不能主动发起。

Websocket 其实是一个新协议，但是为了兼容现有浏览器的握手规范而借用了HTTP的协议来完成一部分握手。

WebSocket是纯事件驱动的，一旦连接建立，通过监听事件可以处理到来的数据和改变的连接状态，数据都以帧序列的形式传输。服务端发送数据后，消息和事件会异步到达。WebSocket编程遵循一个异步编程模型，只需要对WebSocket对象增加回调函数就可以监听事件。

### 2.1 WebSocket通信流程图

![传统HTTP传输与WebSocket传输的通信流程上的区别](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/7e66a0ff1e57a38e48397f8c0a884672736620cd78b0b37b642f8418c7763647.png "传统HTTP传输与WebSocket传输的通信流程上的区别")

这里可以看出传统HTTP通讯与WebSocket通讯的通信流程上的区别，下图显示WebSocket主要的三步中浏览器和服务器端分别做了哪些事情。

![通信过程中发生的事](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/b0b0c2e99ec1304a60a5317febee0f031873e23236a2c0bfe0d1ec4278063e0a.png "通信过程中发生的事")

### 2.2 建立连接的握手

当Web应用程序调用`new WebSocket(url)`接口时，客户端就开始了与地址为url的WebServer建立握手连接的过程。

1. 客户端与服务端通过TCP三次握手建立连接，如果这个建立连接失败，那么后面的过程就不会执行，Web应用程序将收到错误消息通知。
2. 在TCP建立连接成功后，客户端通过HTTP协议传送WebSocket支持的版本号、协议的字版本号、原始地址、主机地址等等一些列字段给服务器端。
3. 服务端收到客户端发送来的握手请求后，如果数据包数据和格式正确、客户端和服务端的协议版本号匹配等等，就接受本次握手连接，并给出相应的数据回复，同样回复的数据包也是采用HTTP协议传输。
4. 客户端收到服务端回复的数据包后，如果数据包内容、格式都没有问题的话，就表示本次连接成功，触发`onopen`，此时Web开发者就可以在此时通过`send()`向服务器发送数据。否则握手连接失败，Web应用程序触发`onerror`，并且能知道连接失败的原因。

这个握手很像HTTP，但是实际上却不是，它允许服务器以HTTP的方式解释一部分handshake的请求，然后切换为websocket。

### 2.3 WebSocket握手报文

一个浏览器发出的WebSocket请求报文类似于：

```text
GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==
Sec-WebSocket-Protocol: chat, superchat
Sec-WebSocket-Version: 13
Origin: http://example.com
```

HTTP1.1协议规定，Upgrade头信息表示将通信协议从HTTP/1.1转向该项所指定的协议。

- `Connection: Upgrade`表示浏览器通知服务器，如果可以，就升级到webSocket协议。
- `Origin`用于验证浏览器域名是否在服务器许可的范围内。
- `Sec-WebSocket-Key`则是用于握手协议的密钥，是浏览器生成的Base64编码的16字节随机字符串。
- `Sec-WebSocket-Protocol`是一个用户定义的字符串，用来区分同URL下，不同的服务所需要的协议。
- `Sec-WebSocket-Version`是告诉服务器所使用的协议版本。

服务端WebSocket回复报文：

```text
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: HSmrc0sMlYUkAGmm5OPpG2HaGWk=
Sec-WebSocket-Protocol: chat
Sec-WebSocket-Origin: null
Sec-WebSocket-Location: ws://example.com/
```

- 服务器端同样用`Connection: Upgrade`通知浏览器，服务端已经成功切换协议。
- `Sec-WebSocket-Accept`是经过服务器确认并且加密过后的`Sec-WebSocket-Key`。
- `Sec-WebSocket-Location`表示进行通信的WebSocket网址。
- `Sec-WebSocket-Protocol`表示最终使用的协议。

在这样一个类似于HTTP通信的握手结束之后，下面就按照WebSocket协议进行通信了。客户端与服务器之间不会再发生HTTP通信，一切由WebSocket 协议接管。

## 3. WebSocket API

浏览器提供了一个[WebSocket](https://developer.mozilla.org/zh-CN/docs/Web/API/WebSocket)对象的实现，可以用这个对象来创建和管理WebSocket连接，并且可以通过该连接发送和接受数据。WebSocket是事件驱动的，因此只需要对WebSocket对象增加回调函数就可以监听事件的发生。

跟[XMLHttpRequest](https://developer.mozilla.org/zh-CN/docs/Web/API/XMLHttpRequest)一样，通过该构造函数先new出来对象实例`const ws = new WebSocket('ws://localhost:8080')`，再使用对象下挂载的属性与方法来操作。后文都用**ws**来指代WebSocket的实例。

[查看DEMO](https://codepen.io/SHERlocked93/pen/payNzm)

### 3.1 ws上常用属性

#### ws.readyState

WebSocket实例对象类似于XHR有个的只读属性`readyState`来指示连接的当前状态：

| 状态 | 值 | 描述 |
| --- | --- | --- |
| CONNECTING | 0 | 连接还没开启。 |
| OPEN | 1 | 连接已开启并准备好进行通信。 |
| CLOSING | 2 | 连接正在关闭的过程中。 |
| CLOSED | 3 | 连接已经关闭，或者连接无法建立。 |

一个示例：

```text
switch (ws.readyState) {
  case WebSocket.CONNECTING:
    // ...
    break;
  case WebSocket.OPEN:
    // ...
    break;
  case WebSocket.CLOSING:
    // ...
    break;
  case WebSocket.CLOSED:
    // ...
    break;
  default:
    //  this never happens
    break;
}
```

#### ws.onopen / ws.onclose

实例对象的`onopen`属性，用于指定连接成功后的回调函数。

```text
ws.onopen = function () {
  ws.send('Hello Server!');
}
```

如果要指定多个回调函数，可以`addEventListener`。

```text
ws.addEventListener('open', function (event) {
  ws.send('Hello Server!');
});
```

实例对象的`onclose`属性，用于指定连接关闭后的回调函数。

```text
ws.onclose = function(event) {
    const { code, reason, wasClean} = event
    // ...
};
ws.addEventListener('close', function(event) {
    const { code, reason, wasClean} = event
    // ...
})
```

#### ws.onmessage

实例对象的`onmessage`属性，用于指定收到服务器数据后的回调函数。

```text
ws.onmessage = function(event) {
  const { data } = event;
  // ...
};
ws.addEventListener('message', function(event) {
  const { data } = event; 
  // ...
});
```

注意，服务器数据可能是文本，也可能是二进制数据（blob对象或Arraybuffer对象）。

```text
ws.onmessage = function(event){
  if(typeof event.data === String) {
    // string
  }
  if(event.data instanceof ArrayBuffer){
    const { data: buffer } = event;
    // array buffer
  }
}
```

除了动态判断收到的数据类型，也可以使用`binaryType`属性，显式指定收到的二进制数据类型。`binaryType`取值应当是'blob'或者'arraybuffer'，'blob'表示使用 Blob 对象，而'arraybuffer'表示使用 ArrayBuffer 对象。

```text
ws.binaryType = 'blob';                // 收到的是 Blob 数据
ws.onmessage = function(e) {
  console.log(e.data.size);
};

ws.binaryType = 'arraybuffer';            // 收到的是 ArrayBuffer 数据
ws.onmessage = function(e) {
  console.log(e.data.byteLength);
};
```

[查看DEMO](https://codepen.io/SHERlocked93/pen/EQKZab)

#### ws.bufferedAmount

实例对象的`bufferedAmount`只读属性，表示还有多少字节的二进制数据没有发送出去。它可以用来判断发送是否结束。 该值会在所有队列数据被发送后重置为 0，而当连接关闭时不会设为0。如果持续调用send()，这个值会持续增长。

```text
var data = new ArrayBuffer(10000000);
ws.send(data);
if (ws.bufferedAmount === 0) {
  // 发送完毕
} else {
  // 发送还没结束
}
```

#### ws.onerror

实例对象的`onerror`属性，用于指定报错时的回调函数。

```text
ws.onerror = function(event) {
  // handle error event
};
ws.addEventListener("error", function(event) {
  // handle error event
});
```

### 3.2 ws上常用方法

#### ws.close()

关闭WebSocket连接或停止正在进行的连接请求。如果连接的状态已经是closed，这个方法不会有任何效果。

#### ws.send()

实例对象的`send()`方法用于向服务器发送数据。

```text
ws.send('your message');                // 发送文本的例子

var file = document
  .querySelector('input[type="file"]')
  .files[0];
ws.send(file);                            // 发送 Blob 对象的例子

// Sending canvas ImageData as ArrayBuffer   
var img = canvas_context.getImageData(0, 0, 400, 320);
var binary = new Uint8Array(img.data.length);
for (var i = 0; i < img.data.length; i++) {
  binary[i] = img.data[i];
}
ws.send(binary.buffer);                // 发送 ArrayBuffer 对象的例子
```

最后一个ArrayBuffer对象栗子中的canvas_context实例是[CanvasRenderingContext2D](https://developer.mozilla.org/zh-CN/docs/Web/API/CanvasRenderingContext2D/getImageData)类型的对象，其上的`.getImageData()`方法返回一个[ImageData](https://developer.mozilla.org/zh-CN/docs/Web/API/ImageData)对象。

---

> 参考：  
> [阮一峰 - WebSocket 教程](http://www.ruanyifeng.com/blog/2017/05/websocket.html)  
> [几种web服务器端推送技术的简单介绍](http://www.daimajiayuan.com/sitejs-65893-1.html)  
> [干货 | 长连接/websocket/SSE等主流服务器推送技术比较](https://mp.weixin.qq.com/s/unagcn33kfCnMrlI-Oslig)  
> [sf - WebSocket 详解](https://segmentfault.com/a/1190000012948613)  
> [WebSocket实战之——JavaScript例子](https://www.cnblogs.com/tinywan/p/5894403.html)  
> [JavaScript之WebSocket 技术](http://blog.csdn.net/BaiHuaXiu123/article/details/53208935?locationNum=7&fps=1)  
> [知乎 - WebSocket 是什么原理？为什么可以实现持久连接？](https://www.zhihu.com/question/20215561)  
> [Socket 与 WebSocket](https://blog.zengrong.net/post/2199.html)  
> **官方文档：**  
> [MDN - WebSocket](https://developer.mozilla.org/zh-CN/docs/Web/API/WebSocket)  
> [W3C - The WebSocket API](https://www.w3.org/TR/websockets/)  
> [RFC - WebSocket协议栈](https://tools.ietf.org/html/rfc6455)  
> **工具：**  
> [WebSocket 在线测试](http://www.blue-zero.com/WebSocket/)
