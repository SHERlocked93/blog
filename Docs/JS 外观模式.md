# JS 外观模式

## 1. 简介

**外观模式**（Facade）为子系统中的一组接口提供了一个一致的界面，此模块定义了一个高层接口，这个接口值得这一子系统更加容易使用。  
外观模式在JS中常常用于解决浏览器兼容性问题。

## 2. 实现

外观模式不仅简化类中的接口，而且对接口与调用者也进行了解耦。外观模式经常被认为开发者必备，它可以将一些复杂操作封装起来，并创建一个简单的接口用于调用。  
外观模式经常被用于JavaScript类库里，通过它封装一些接口用于兼容多浏览器，外观模式可以让我们间接调用子系统，从而避免因直接访问子系统而产生不必要的错误。

外观模式的优势是易于使用，而且本身也比较轻量级。但也有缺点 外观模式被开发者连续使用时会产生一定的性能问题，因为在每次调用时都要检测功能的可用性。  
下面是一段未优化过的代码，我们使用了外观模式通过检测浏览器特性的方式来创建一个跨浏览器的使用方法。

比如对`document`对象添加`click`事件的时候：

```text
function addEvent(dom, type, fn) {
  if (dom.addEventListener) {      // 支持DOM2级事件处理方法的浏览器
    dom.addEventListener(type, fn, false)
  } else if (dom.attachEvent) {    // 不支持DOM2级但支持attachEvent
    dom.attachEvent('on' + type, fn)
  } else {
    dom['on' + type] = fn      // 都不支持的浏览器
  }
}

const myInput = document.getElementById('myinput')
addEvent(myInput, 'click', function() {console.log('绑定 click 事件')})
```

还可以用来解决一些其他的浏览器兼容性问题：

```text
const getEvent = function(event) {  // 获取事件对象
  return event || window.event      // IE下window.event
}

const getTarget = function(event) {        // 获取事件元素
  const event = getEvent(event)
  return event.target || event.srcElement  // IE下event.srcElement
}

const preventDefault = function(event) {    // 阻止默认事件
  const event = getEvent(event)
  if (event.preventDefault) {event.preventDefault()}
  else {event.returnValue = false}          // IE下
}

const cancelBubble = function(event) {
  const event = getEvent(event)
  if (event.stopPropagation) {event.stopPropagation()}
  else {event.cancelBubble = true}      // IE下
}

document.onclick = function(e) {
  preventDefault(e)
  if (getTarget(e) !== document.getElementById('myinput')) {console.log('呵呵')}
}
```

## 3. 总结

那么何时使用外观模式呢？一般来说分三个阶段：

1. 在设计初期，应该要有意识地将不同的两个层分离，比如经典的三层结构，在数据访问层和业务逻辑层、业务逻辑层和表示层之间建立外观Facade。
2. 在开发阶段，子系统往往因为不断的重构演化而变得越来越复杂，增加外观Facade可以提供一个简单的接口，减少他们之间的依赖。
3. 在维护一个遗留的大型系统时，可能这个系统已经很难维护了，这时候使用外观`Facade`也是非常合适的，为系统开发一个外观`Facade`类，为设计粗糙和高度复杂的遗留代码提供比较清晰的接口，让新系统和`Facade`对象交互，`Facade`与遗留代码交互所有的复杂工作。

---

本文是系列文章，可以相互参考印证，共同进步~

> 1. [JS 抽象工厂模式](https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E6%8A%BD%E8%B1%A1%E5%B7%A5%E5%8E%82%E6%A8%A1%E5%BC%8F.md)
> 2. [JS 工厂模式](https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E5%B7%A5%E5%8E%82%E6%A8%A1%E5%BC%8F.md)
> 3. [JS 建造者模式](https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E5%BB%BA%E9%80%A0%E8%80%85%E6%A8%A1%E5%BC%8F.md)
> 4. [JS 原型模式](https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E5%8E%9F%E5%9E%8B%E6%A8%A1%E5%BC%8F.md)
> 5. [JS 单例模式](https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E5%8D%95%E4%BE%8B%E6%A8%A1%E5%BC%8F.md)
> 6. [JS 回调模式](https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E5%9B%9E%E8%B0%83%E6%A8%A1%E5%BC%8F.md)
> 7. [JS 外观模式](https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E5%A4%96%E8%A7%82%E6%A8%A1%E5%BC%8F.md)
> 8. [JS 适配器模式](https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E9%80%82%E9%85%8D%E5%99%A8%E6%A8%A1%E5%BC%8F.md)
> 9. [JS 利用高阶函数实现函数缓存(备忘模式)](https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E5%88%A9%E7%94%A8%E9%AB%98%E9%98%B6%E5%87%BD%E6%95%B0%E5%AE%9E%E7%8E%B0%E5%87%BD%E6%95%B0%E7%BC%93%E5%AD%98%28%E5%A4%87%E5%BF%98%E6%A8%A1%E5%BC%8F%29.md)
> 10. [JS 状态模式](https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E7%8A%B6%E6%80%81%E6%A8%A1%E5%BC%8F.md)
> 11. [JS 桥接模式](https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E6%A1%A5%E6%8E%A5%E6%A8%A1%E5%BC%8F.md)
> 12. [JS 观察者模式](https://github.com/SHERlocked93/blog/blob/master/Docs/JS%20%E8%A7%82%E5%AF%9F%E8%80%85%E6%A8%A1%E5%BC%8F.md)

> 参考：  
> [设计模式之外观模式](https://link.segmentfault.com/?enc=xypDAPVRnuw5WvfAgdMmFw%3D%3D.Py5agjKSFSOm0oIVefKnbVyXl5JORmJt8dtQ0Natt4X%2BBI3R9jr7swp10N5iC3hxap9hfHOyxS4DR1b5km92SQ%3D%3D)  
> [《Javascript 设计模式》 - 张荣铭](https://link.segmentfault.com/?enc=YUMO0NtmubKgpLsJ3v%2BgRQ%3D%3D.bSjEVUS0cXLRvXJCnzGqMVipgCDj0jPfpbTuJvvPpUbdhESDGWpe3etqiHLeKS8y)
