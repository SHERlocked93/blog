# JS 工厂模式

## 1. 简介

**工厂模式**的目的是为了创建对象，它通常在类或者类的静态方法中实现，具有以下目标：

- 当创建相似对象时执行重复操作
- 当编译时不知道具体类型的情况下，为工厂客户提供一个创建对象的接口

与创建型模式类似，工厂模式创建对象（视为工厂里的产品）时无需指定创建对象的具体类。

工厂模式定义一个用于创建对象的接口，这个接口由子类决定实例化哪一个类。该模式使一个类的实例化延迟到了子类。而子类可以重写接口方法以便创建的时候指定自己的对象类型。

这个模式十分有用，尤其是创建对象的流程赋值的时候，比如依赖于很多设置文件等。并且，你会经常在程序里看到工厂方法，用于让子类类定义需要创建的对象类型。

## 2. 实现

一个简单的实现，使用IIFE：

```text
var Car = (function () {
    var Car = function (model, year, miles) {
        this.model = model;
        this.year = year;
        this.miles = miles;
    };
    return function (model, year, miles) {
        return new Car(model, year, miles);
    };
})();

var tom = new Car("Tom", 2009, 20000);
var dudu = new Car("Dudu", 2010, 5000);
```

如果使用对象属性来实现：

```text
var productManager = {};

productManager.createProductA = function() {
    this.prd = 'A'
    console.log('Product ' + this.prd);
}
productManager.createProductB = function() {
    this.prd = 'B'
    console.log('Product ' + this.prd);
}

productManager.factory = function(typeType) {
    return new productManager[typeType];
}

productManager.factory("createProductA");    // Product A
productManager.factory("createProductB");    // Product B
```

以下例子中的工厂方法接受在运行时以字符串形式指定的类型，然后创建并返回所请求类型的对象。

```text
function CarMaker() {}

CarMaker.prototype.drive = function() {
  return `I have ${this.doors} doors!`
}

CarMaker.factory = function(type) {
  const constr = type
  if (typeof CarMaker[constr] !== 'function') {
    throw new Error(`${constr} doesnot exist`)
  }
  // 原型继承的方式使得原型继承父类
  if (typeof CarMaker[constr].prototype.drive !== 'function') {
    CarMaker[constr].prototype = new CarMaker()
  }
  return new CarMaker[constr]()
}

CarMaker.Compact = function() { this.doors = 4}
CarMaker.Convertible = function() { this.doors = 2}

const corolla = CarMaker.factory('Compact')
corolla.drive()    // "I have 4 doors!"
```

也可以把实际对象的创建工作放到原型中：

```text
const Factory = function(type, content) {
  return (this instanceof Factory)
      ? new this[type](content)
      : new Factory(type, content)
}

Factory.prototype.Compact = function(content) { this.doors = 4}
Factory.prototype.Convertible = function(content) { this.doors = 2}

Factory.prototype.Compact.prototype.drive = function() {
  return `I have ${this.doors} doors!`
}

const corolla = Factory('Compact')
corolla.drive()    // "I have 4 doors!"
```

## 3. 总结

那么什么时候使用工厂模式呢，以下几种情景下工厂模式特别有用：

- 对象的构建十分复杂
- 需要依赖具体环境创建不同实例
- 处理大量具有相同属性的小对象

什么时候不该用工厂模式：  
不滥用运用工厂模式，有时候仅仅只是给代码增加了不必要的复杂度，同时使得测试难以运行下去。

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
> [深入理解JavaScript系列（28）：设计模式之工厂模式](https://link.segmentfault.com/?enc=%2FacX%2F6YkK45Oc8yfYeUnBw%3D%3D.bxGQvR5lyeaAsFq1JZVQ7lKV4ffzcHBDFZGbonDTy4O2Mq4p7016OBqXE2PxLq0W21e%2FO71V0pXLkvgJF6gruA%3D%3D)   
> [《JS 模式》](https://link.segmentfault.com/?enc=myefAGS%2FGUVtBE7EuJXnMA%3D%3D.ELssUn0wJ0U96drM%2FIOMpymfkFD0JghlltoMJv4q3RZ00XGZiIiP2XeubqHEGggA)  
> [《Javascript 设计模式》 - 张荣铭](https://link.segmentfault.com/?enc=Yf5Ksnb%2B7N8OFz%2B6RuYwRw%3D%3D.xEM8fnYFzkD0kkeBZTQyq8JVo89tNpRl79lo8UCz%2FtH5hgrt365L42b5raHwhBzU)
