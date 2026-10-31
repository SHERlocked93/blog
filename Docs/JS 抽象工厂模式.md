# JS 抽象工厂模式

## 0. 简介

**抽象工厂模式**(Abstract Factory)就是通过类的抽象使得业务适用于一个产品类簇的创建，而不负责某一类产品的实例。

JS中是没有直接的抽象类的，abstract是个保留字，但是还没有实现，因此我们需要在类的方法中抛出错误来模拟抽象类，如果继承的子类中没有覆写该方法而调用，就会抛出错误。

```text
const Car = function() { }
Car.prototype.getPrice = function() {return new Error('抽象方法不能调用')}
```

## 1. 实现

面向对象的语言里有抽象工厂模式，首先声明一个抽象类作为父类，以概括某一类产品所需要的特征，继承该父类的子类需要实现父类中声明的方法而实现父类中所声明的功能：

```text
/**
* 实现subType类对工厂类中的superType类型的抽象类的继承
* @param subType 要继承的类
* @param superType 工厂类中的抽象类type
*/
const VehicleFactory = function(subType, superType) {
  if (typeof VehicleFactory[superType] === 'function') {
    function F() {
      this.type = '车辆'
    } 
    F.prototype = new VehicleFactory[superType]()
    subType.constructor = subType
    subType.prototype = new F()                // 因为子类subType不仅需要继承superType对应的类的原型方法，还要继承其对象属性
  } else throw new Error('不存在该抽象类')
}

VehicleFactory.Car = function() {
  this.type = 'car'
}
VehicleFactory.Car.prototype = {
  getPrice: function() {
    return new Error('抽象方法不可使用')
  },
  getSpeed: function() {
    return new Error('抽象方法不可使用')
  }
}

const BMW = function(price, speed) {
  this.price = price
  this.speed = speed
}
VehicleFactory(BMW, 'Car')        // 继承Car抽象类
BMW.prototype.getPrice = function() {        // 覆写getPrice方法
  console.log(`BWM price is ${this.price}`)
}
BMW.prototype.getSpeed = function() {
  console.log(`BWM speed is ${this.speed}`)
}

const baomai5 = new BMW(30, 99)
baomai5.getPrice()                          // BWM price is 30
baomai5 instanceof VehicleFactory.Car       // true
```

## 2. 总结

抽象类创建出的结果不是一个真实的对象实例，而是一个类簇，它指定了类的结构，这也就区别于简单工厂模式创建单一对象，工厂模式创建多类对象。

通过抽象工厂，就可以创建某个类簇的产品，并且也可以通过`instanceof`来检查产品的类别，也具备该类簇所必备的方法。

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

> 参考：[《Javascript 设计模式》 - 张荣铭](https://link.segmentfault.com/?enc=%2BWE0a5Bbk1H5DEQrVkOkqQ%3D%3D.qJ%2BhYL62dK%2B%2FOVFem0sEBscZovRkMTA5JDStXBgp0H5wBRL3IOMYDY3rmyjI5ytz)
