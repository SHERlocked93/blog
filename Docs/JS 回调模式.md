# JS 回调模式

## 1. 回调示例

如果有个模块 `findeNodes()` ，任务是找到期望的 DOM 元素并使用 `hide()` 处理：

```text
function findNodes() {
    var i = 10000, nodes = [], found
    while (i--) {
        // ...复杂逻辑，筛选出符合的元素 found
        nodes.push(found)
    }
    return nodes
}

function hide(nodes) {
    for (let i = 0, max = nodes.length; i < max; i++) {
        nodes[i].style.display = 'none'
    }
}
hide(findNodes())
```

## 2. 改进

可以看到函数 `findNodes()` 和 `hide()` 分别两次进行了循环，这是十分低效的，如果要避免这种重复循环，并且只要在 `findNodes()` 中选择的时候就进行 `hide()` 那么将是高效的实现方式。如果在 `findNodes()` 中实现修改逻辑，由于检索和修改逻辑耦合，那么它将不再是一个通用函数。对这种问题的解决方法是采用**回调模式**。

可以将节点隐藏逻辑以回调函数的方式传递给 `findNodes()` 并委托执行：

```text
function findNodes(callback) {
    var i = 10000, nodes = [], found

    if (typeof callback !== 'function') {    // 检查参数是否为可调用
        callback = false
    }

    while (i--) {
        // ...复杂逻辑，筛选出符合的元素 found
        if (callback) {
            callback(found)
        }
        nodes.push(found)
    }
    return nodes
}

function hide(nodes) {
    nodes[i].style.display = 'none'
}

findNodes(hide)
```

那么现在回调函数可选，重构后加入回调函数参数的 `findNodes()` 仍然可以像以前一样使用，而不会破坏旧 API 的原始代码。

## 3. 回调与作用域

前面的例子中，回调执行的语句：`callback(para)`，在多数情况下有效，但是如果传递的函数是对象的方法且有 `this` 那么回调方法里的 `this` 将指向的是全局对象，从而发生意外。

解决这个问题的方法是传递回调函数，并且还传递该回调函数所属的对象：

```text
function findNodes (callback, callback_obj){
    ...
    if (typeof callback === 'function'){
        callback.call(callback_obj, found)
    }
    ...
}
findNodes (obj.sayName, obj)
```

当然，可以把方法作为字符串来传递，避免重复两次输入该对象的名称：

```text
findNodes (callback, callback_obj){
    if (typeof callback === 'string'){
        callback = callback_obj[callback]
    }
    if (typeof callback === 'function'){
        callback.call(callback_obj, found)
    }
}
findNodes('sayName', Obj)
```

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

> 参考：[<JavaScript 模式> P65](https://link.segmentfault.com/?enc=TNrAzwdAR%2BF3nRwkp%2Fgq5Q%3D%3D.LX81tmFa85RSxjU%2FrVpz4lIwsTMOaHhrboXxN6nIWqWsiwc1B6W8RGMkJE92aDON)
