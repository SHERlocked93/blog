# JS 原型模式

## 1. 简介

**原型模式**(Prototype pattern)，用原型实例指向创建对象的类，使用于创建新的对象的类的共享原型的属性与方法。

## 2. 实现

对于原型模式，我们可以利用JavaScript特有的原型继承特性去创建对象的方式，也就是创建的一个对象作为另外一个对象的`prototype`属性值。原型对象本身就是有效地利用了每个构造器创建的对象，例如，如果一个构造函数的原型包含了一个name属性（见后面的例子），那通过这个构造函数创建的对象都会有这个属性。

在现有的文献里查看原型模式的定义，没有针对JavaScript的，你可能发现很多讲解的都是关于类的，但是现实情况是基于原型继承的JavaScript完全避免了类（class）的概念。我们只是简单从现有的对象进行拷贝来创建对象。

真正的原型继承是作为最新版的ECMAScript5标准提出的，使用`Object.create`方法来创建这样的对象，该方法创建指定的对象，其对象的`prototype`有指定的对象（也就是该方法传进的第一个参数对象），也可以包含其他可选的指定属性。例如`Object.create(prototype, optionalDescriptorObjects)`，下面的例子里也可以看到这个用法：

```text
// 因为不是构造函数，所以不用大写
var someCar = {
    drive: function () { },
    name: '马自达 3'
};

// 使用Object.create创建一个新车x
var anotherCar = Object.create(someCar);
anotherCar.name = '丰田佳美';
```

`Object.create`运行你直接从其它对象继承过来，使用该方法的第二个参数，你可以初始化额外的其它属性。例如：

```text
var vehicle = {
    getModel: function () {
        console.log('车辆的模具是：' + this.model);
    }
};

var car = Object.create(vehicle, {
    'id': {
        value: MY_GLOBAL.nextId(),
        enumerable: true // 默认writable:false, configurable:false
},
    'model': {
        value: '福特',
        enumerable: true
    }
});
```

这里，可以在`Object.create`的第二个参数里使用对象字面量传入要初始化的额外属性，其语法与`Object.defineProperties`或`Object.defineProperty`方法类似。它允许您设定属性的特性，例如`enumerable`, `writable` 或 `configurable`。

如果你希望自己去实现原型模式，而不直接使用`Object.create` 。你可以使用像下面这样的代码为上面的例子来实现：

```text
var vehiclePrototype = {
    init: function (carModel) {
        this.model = carModel;
    },
    getModel: function () {
        console.log('车辆模具是：' + this.model);
    }
};

function vehicle(model) {
    function F() { };
    F.prototype = vehiclePrototype;

    var f = new F();

    f.init(model);
    return f;
}

var car = vehicle('福特Escort');
car.getModel();
```

## 3. 总结

原型模式在JavaScript里的使用简直是无处不在，其它很多模式有很多也是基于prototype的，这里大家要注意的依然是浅拷贝和深拷贝的问题，免得出现引用问题。

原型模式适合在创建复杂对象时，对于那些需求一直在变化而导致对象结构不停地改变时，将那些比较稳定的属性与方法共用而提取的继承的实现。

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
> [设计模式之原型模式](https://link.segmentfault.com/?enc=FZ9flXSFJAtyyMol3oyvvQ%3D%3D.YL9Rkf%2F8d3uarc1YcXZQcQKKL9KcS3FNxp6D1HPLeQ%2F2N%2BhPDAudqIP7sNwlpE%2BUH3XQCyBSWtRLf%2Fw%2FOUwUMw%3D%3D)  
> [《Javascript 设计模式》 - 张荣铭](https://link.segmentfault.com/?enc=%2FdKNY%2BAdfagmphZIx53kbw%3D%3D.QB16cCXg90eWUSSkDZpGdy%2F%2BuQQ2%2BQYNo1JOfq6y1Q6CvFHACbIxzk1ih3Q6yUbo)
