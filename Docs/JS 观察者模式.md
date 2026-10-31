# JS 观察者模式

## 1. 介绍

观察者模式又叫发布订阅模式（Publish/Subscribe），它定义了一种一对多的关系，让多个观察者对象同时监听某一个主题对象，这个主题对象的状态发生变化时就会通知所有的观察者对象，使得它们能够自动更新自己。

使用观察者模式的好处：

1. 支持简单的广播通信，自动通知所有已经订阅过的对象。
2. 目标对象与观察者存在的是动态关联，增加了灵活性。
3. 目标对象与观察者之间的抽象耦合关系能够单独扩展以及重用。

## 2. 实现一

如下例子：

- subscribers：含有不同 type 的数组，存储有所有订阅者的数组，订阅行为将被加入到这个数组中
- subscribe：方法为将订阅者添加到 subscribers 中对应的数组中
- unsubscribe：方法为在 subscribers 中删除订阅者
- publish：循环遍历 subscribers 中的每个元素，并调用他们注册时提供的方法

```text
let publisher = {
  subscribers: {
    any: []
  },
  subscribe: function(fn, type = 'any') {
    if (typeof this.subscribers[type] === 'undefined') {
      this.subscribers[type] = []
    }
    this.subscribers[type].push(fn)
  },
  unsubscribe: function(fn, type) {
    this.visitSubscribers('unsubscribe', fn, type)
  },
  publish: function(publication, type) {
    this.visitSubscribers('publish', publication, type)
  },
  visitSubscribers: function(action, arg, type = 'any') {
    this.subscribers[type].forEach((currentValue, index, array) => {
      if (action === 'publish') {
        currentValue(arg)
      } else if (action === 'unsubscribe') {
        if (currentValue === arg) {
          this.subscribers[type].splice(index, 1)
        }
      }
    })
  }
}

let funcA = function(cl) {
  console.log('msg1' + cl)
}
let funcB = function(cl) {
  console.log('msg2' + cl)
}

publisher.subscribe(funcA)
publisher.subscribe(funcB)
publisher.unsubscribe(funcB)

publisher.publish(' in publisher')     // msg1 in publisher       
```

这里可以通过一个函数 makePublisher() 将一个对象复制成 publisher ，从而将其转换成一个发布者。

```text
function makePublisher(o) {
  Object.keys(publisher).forEach((curr, index, array) => {
    if (publisher.hasOwnProperty(curr) && typeof publisher[curr] === 'function') {
      o[curr] = publisher[curr]
    }
  })
  o.subscribers={any:[]}
}

// 发行者对象
let paper = {
  daily: function() {
    this.publish('big news today')
  },
  monthly: function() {
    this.publish('interesting analysis', 'monthly')
  }
}

makePublisher(paper)

// 订阅对象
let joe = {
  drinkCoffee: function(paper) {
    console.log('Just read daily ' + paper)
  },
  sundayPreNap: function(monthly) {
    console.log('Reading this monthly ' + monthly)
  }
}

paper.subscribe(joe.drinkCoffee)
paper.subscribe(joe.sundayPreNap, 'monthly')

paper.daily()         // Just read daily big news today
paper.monthly()         // Reading this monthly interesting analysis
```

## 3. 实现二

使用ES6里的class稍微改造下：

```text
class publisher {
    constructor() {
        this.subscribers = {
            any: []
        }
    }
    subscribe(fn, type = 'any') {
        if (typeof this.subscribers[type] === 'undefined') {
            this.subscribers[type] = []
        }
        this.subscribers[type].push(fn)
    }
    unsubscribe(fn, type) {
        this.visitSubscribers('unsubscribe', fn, type)
    }
    publish(publication, type) {
        this.visitSubscribers('publish', publication, type)
    }
    visitSubscribers(action, arg, type = 'any') {
        this.subscribers[type].forEach((currentValue, index, array) => {
            if (action === 'publish') {
                currentValue(arg)
            } else if (action === 'unsubscribe') {
                if (currentValue === arg) {
                    this.subscribers[type].splice(index, 1)
                }
            }
        })
    }
}

let publish = new publisher();

let funcA = function(cl) {
    console.log('msg1' + cl)
}
let funcB = function(cl) {
    console.log('msg2' + cl)
}

publish.subscribe(funcA)
publish.subscribe(funcB)
publish.unsubscribe(funcB)

publish.publish(' in publisher')     // msg1 in publisher
```

## 4. 实现三

以上两个方法都是[《JavaScript模式》](https://link.segmentfault.com/?enc=2j1vAY45jfgHaQTSS6EBtA%3D%3D.2P04fZ5iS8lVn%2BbtdD81b3lStKk6czrBxpFoi8IK8cyRtN1WjJ5LKEm4z2%2FA%2FsBk)里介绍的，这里贴上个自己实现的，感觉看起来舒服点...

- 使用IIFE的方法：

```text
const Observer = (function() {
  const _message = {}  // 消息队列
  return {
    regist(type, fn) {          // 订阅
      _message[type]
          ? _message[type].push(fn)
          : _message[type] = [fn]
    },
    emit(type, payload) {          // 发布
      if (!_message[type]) {
        return
      }
      _message[type].forEach(event => event(payload))
    },
    remove(type, fn) {            // 退订
      if (!_message[type].includes(fn)) {return}
      const idx = _message[type].indexOf(fn)
      _message[type].splice(idx, 1)
    }
  }
})()
```

- 使用ES6的class方法

```text
class Observer {
  constructor() {
    this._message = {}
  }

  regist(type, fn) {          // 订阅
    this._message[type]
        ? this._message[type].push(fn)
        : this._message[type] = [fn]
  }

  emit(type, payload) {          // 发布
    if (!this._message[type]) {
      return
    }
    this._message[type].forEach(event => event(payload))
  }

  remove(type, fn) {            // 退订
    if (!this._message[type].includes(fn)) {return}
    const idx = this._message[type].indexOf(fn)
    this._message[type].splice(idx, 1)
  }
}
```

## 5. 总结

观察者的使用场合就是：当一个对象的改变需要同时改变其它对象，并且它不知道具体有多少对象需要改变的时候，就应该考虑使用观察者模式。

总的来说，观察者模式所做的工作就是在解耦，让耦合的双方都依赖于抽象，而不是依赖于具体。从而使得各自的变化都不会影响到另一边的变化。

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
> [设计模式之观察者模式](https://link.segmentfault.com/?enc=dOGP%2BShulksHRPKH1ihzHA%3D%3D.pFzVh5ntLisiiPURviJ2Y9rHRszTZxSm5YXZVQRbeU23nNGpSInNpDag8iyPOiUjDh1afNcjaSV%2BQ8Qw3DvsGg%3D%3D)   
> [《JavaScript模式》](https://link.segmentfault.com/?enc=976018KlG%2FNOJydH%2FeaeFw%3D%3D.4rDZLLSjGa3jWkYqeRbR9JLOR7PdD2QOAGJBVesvsuzAHTQ2jjF%2F99cRxuUuibCi)  
> [《Javascript 设计模式》 - 张荣铭](https://link.segmentfault.com/?enc=i8%2F5rcT%2FU170ACQUH6QoxA%3D%3D.3i%2FXXthaQ2I2PXNiWS2MdNykIe6Vexn42oW5ZHJKWc%2FD5eSPMCy97KEz6x%2FuuTEE)
