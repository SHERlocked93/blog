# JS 建造者模式

## 1. 简介

在软件系统中，有时候面临着“一个复杂对象”的创建工作，其通常由各个部分的子对象用一定的算法构成；由于需求的变化，这个复杂对象的各个部分经常面临着剧烈的变化，但是将它们组合在一起的算法确相对稳定。如何应对这种变化？如何提供一种“封装机制”来隔离出“复杂对象的各个部分”的变化，从而保持系统中的“稳定构建算法”不随着需求改变而改变？这就是要说的建造者模式。

**建造者模式**(Builder pattern)，将一个复杂对象的构建层与其表示层相互分离，使得同样的构建过程可以采用不同的表示。也就是说如果我们用了建造者模式，那么用户就需要指定需要建造的类型就可以得到它们，而具体建造的过程和细节就不需要知道了。

在工厂模式中，对创建的结果都是一个完整的个体，我们对参见的过程不为所知，只了解创建的结果对象。而在建造者模式中我们关心的是对象的创建过程，因此我们通常将创建对象的类模块化，这样使被创建的类的每一个模块都可以得到灵活的运用和高质量的复用。

## 2. 实现

```text
const Human = function(param) {
  this.skill = param && param.skill || '保密'
  this.hobby = param && param.hobby || '保密'
}
Human.prototype = {
  getSkill: function() {
    return this.skill
  },
  getHobby: function() {
    return this.hobby
  }
}

const Named = function(named) { 
  (function(named, that) {
    that.wholeName = named
    if (named.includes(' ')) {
      that.FirstName = named.slice(0, named.indexOf(' '))
      that.SecondeName = named.slice(named.indexOf(' '))
    }
  })(named, this)
}

const Work = function(work) {
  (function(work, that) {
    switch (work) {
      case 'code':
        that.work = '工程师'
        that.workDesc = '每天沉迷于编程'
        break
      case 'UE':
        that.work = '设计师'
        that.workDesc = '设计更像一种艺术'
        break
      default :
        that.work = work
        that.workDesc = '对不起，我们不清楚您所选择职位的描述'
    }
  })(work, this)
}

Work.prototype.changeWork = function(work) {
  this.work = work
}

const Person = function(param, name, work) {    // 构造方法，不同模块使用不同创建过程
  const _person = new Human(param)
  _person.named = new Named(name)
  _person.work = new Work(work)
  return _person
}

const xiaoming = new Person({ skill: '耍帅', hobby: '装逼' }, 'xiao ming', 'code')
xiaoming.skill    // 耍帅
xiaoming.FirstName  // xiao
xiaoming.work    // 工程师
```

根据建造者的定义，表相即是回调，也就是说获取数据以后如何显示和处理取决于回调函数，相应地回调函数在处理数据的时候不需要关注是如何获取数据的，同样的例子也可以在jquery的ajax方法里看到，有很多回调函数（比如success, error回调等），主要目的就是职责分离。

同样再来一个jQuery的例子：`$('<div class= "foo"> bar </div>')`，我们只需要传入要生成的HTML字符，而不需要关心具体的HTML对象是如何生产的。

## 3. 总结

建造者模式主要用于“分步骤构建一个复杂的对象”，在这其中“分步骤”是一个稳定的算法，而复杂对象的各个部分则经常变化，其优点是：建造者模式的“加工工艺”是暴露的，这样使得建造者模式更加灵活，并且建造者模式解耦了组装过程和创建具体部件，使得我们不用去关心每个部件是如何组装的。

这种方式对于整体对象类的拆分无疑增加了结构的复杂性，因此如果对象粒度很小，或者模块间的复用率很低并且变动不大，我们最好还是要创建整体对象。

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
> [设计模式之建造者模式](https://link.segmentfault.com/?enc=e2bDHqNlJ1bSs1GVvbX97w%3D%3D.PKeC5KRwrVat%2Fjux4aj9yiToYfyjXvWcg%2FvHwLrzx5Xqk5eHOYA00qPtcU6ceicfvoHZeAbBeuqmzl55I4lf5g%3D%3D)  
> [《Javascript 设计模式》 - 张荣铭](https://link.segmentfault.com/?enc=CMp%2Bn6NIWuJO%2FQY69LH3MA%3D%3D.EHOaFXMDnc1pvBNsVw6coq21tPN%2BgPfOo9AXAfavxeEmXkeir3NTp25d%2BWtVtB7M)
