# JS 桥接模式

## 1. 简介

**桥接模式**（Bridge）将抽象部分与它的实现部分分离，使它们都可以独立地变化。  
其实就是函数的封装，比如要对某个DOM元素添加`color`和`backgroundColor`，可以封装个`changeColor`函数，这样可以在多个相似逻辑中提升智商...

## 2. 实现

有时候在多维的变化中**桥接模式**更加实用，比如可以提取多个底层功能模块，比如提取运动，着色，说话模块，球类可以具有运动和着色模块，人类可以具有运动和说话模块，这样可以实现模块的快速组装，不仅仅是实现与抽象部分相分离了，而是更进一步功能与抽象相分离，进而 ~~提升逼格~~ 灵活的创建对象。

```text
class Speed {            // 运动模块
  constructor(x, y) {
    this.x = x
    this.y = y
  }
  run() {  console.log(`运动起来 ${this.x} + ${this.y}`)  }
}

class Color {            // 着色模块
  constructor(cl) {
    this.color = cl
  }
  draw() {  console.log(`绘制颜色 ${this.color}`)  }
}

class Speak {
  constructor(wd) {
    this.word = wd
  }
  say() {  console.log(`说话 ${this.word}`)  }
}

class Ball {                     // 创建球类，可以着色和运动
  constructor(x, y, cl) {
    this.speed = new Speed(x, y)
    this.color = new Color(cl)
  }
  init() {
    this.speed.run()
    this.color.draw()
  }
}

class Man {                    // 人类，可以运动和说话
  constructor(x, y, wd) {
    this.speed = new Speed(x, y)
    this.speak = new Speak(wd)
  }
  init() {
    this.speed.run()
    this.speak.say()
  }
}

const man = new Man(1, 2, 'hehe?')
man.init()                                // 运动起来 1 + 2      说话 hehe?
```

## 3. 总结

桥接模式的优点也很明显，我们只列举主要几个优点：

- 分离接口和实现部分，一个实现未必不变地绑定在一个接口上，抽象类（函数）的实现可以在运行时刻进行配置，一个对象甚至可以在运行时刻改变它的实现，同将抽象和实现也进行了充分的解耦，也有利于分层，从而产生更好的结构化系统。
- 提高可扩充性
- 对客户隐藏实现细节。

同时桥接模式也有自己的缺点：

- 大量的类将导致开发成本的增加，同时在性能方面可能也会有所减少。

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
> [设计模式之桥接模式](https://link.segmentfault.com/?enc=1rwGOJWWIJg7Gvqbblf34w%3D%3D.1RcSguHYrZV89NiPr8VToZNM7ib964kujO65oCERhKnfrhqaq0%2Bpw6gIZaknRSX%2Ft1xI1Fldmq2vDwMmZmE%2FEQ%3D%3D)  
> [《Javascript 设计模式》 - 张荣铭](https://link.segmentfault.com/?enc=%2BiNfYxYbGTIRUahEcbZzSw%3D%3D.uwovNXfd85qcTzRvBtwjSpRzkJ3BBGG6oRpIhAYW%2FASv9lX%2Bo1hQiSiOE4sunt21)
