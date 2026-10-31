# JS 状态模式

## 1. 简介

**状态模式**(State)允许一个对象在其内部状态改变的时候改变它的行为，对象看起来似乎修改了它的类。  
其实就是用一个对象或者数组记录一组状态，每个状态对应一个实现，实现的时候根据状态挨个去运行实现。

## 2. 实现

比如超级玛丽，就可能同时有好几个状态比如 跳跃，移动，射击，蹲下 等，如果对这些动作一个个进行处理判断，需要多个`if-else`或者`switch`不仅丑陋不说，而且在遇到有组合动作的时候，实现就会变的更为复杂，这里可以使用状态模式来实现。

状态模式的思路是：首先创建一个状态对象或者数组，内部保存状态变量，然后内部封装好每种动作对应的状态，然后状态对象返回一个接口对象，它可以对内部的状态修改或者调用。

```text
const SuperMarry = (function() {    
  let _currentState = [],        // 状态数组
      states = {
        jump() {console.log('跳跃!')},
        move() {console.log('移动!')},
        shoot() {console.log('射击!')},
        squat() {console.log('蹲下!')}
      }

  const Action = {
    changeState(arr) {  // 更改当前动作
      _currentState = arr
      return this
    },
    goes() {
      console.log('触发动作')
      _currentState.forEach(T => states[T] && states[T]())
      return this
    }
  }

  return {
    change: Action.changeState,
    go: Action.goes
  }
})()

SuperMarry
    .change(['jump', 'shoot'])
    .go()                    // 触发动作  跳跃!  射击!
    .go()                    // 触发动作  跳跃!  射击!
    .change(['squat'])
    .go()                    // 触发动作  蹲下!
```

这里可以使用`ES6`的`class`优化一下：

```text
class SuperMarry {
  constructor() {
    this._currentState = []
    this.states = {
      jump() {console.log('跳跃!')},
      move() {console.log('移动!')},
      shoot() {console.log('射击!')},
      squat() {console.log('蹲下!')}
    }
  }

  change(arr) {  // 更改当前动作
    this._currentState = arr
    return this
  }

  go() {
    console.log('触发动作')
    this._currentState.forEach(T => this.states[T] && this.states[T]())
    return this
  }
}

new SuperMarry()
    .change(['jump', 'shoot'])
    .go()                    // 触发动作  跳跃!  射击!
    .go()                    // 触发动作  跳跃!  射击!
    .change(['squat'])
    .go()                    // 触发动作  蹲下!
```

## 3. 总结

状态模式的使用场景也特别明确，有如下两点：

1. 一个对象的行为取决于它的状态，并且它必须在运行时刻根据状态改变它的行为。
2. 一个操作中含有大量的分支语句，而且这些分支语句依赖于该对象的状态。状态通常为一个或多个枚举常量的表示。

简而言之，当遇到很多同级`if-else`或者`switch`的时候，可以使用**状态模式**来进行简化。

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
> [《Javascript 设计模式》 - 张荣铭](https://link.segmentfault.com/?enc=EIG2FrIQPUgZbjWVOMfrpg%3D%3D.Kb%2FK0NYE3LRbnlM6BMjJC0ldrQFt45610jt7opu4n72U1%2BtfHKGbWhtSnY%2FVxzfg)  
> [设计模式之状态模式](https://link.segmentfault.com/?enc=4Yn5hcrWzVwjE8dFYY%2Fc8g%3D%3D.wLwYG66P7nUAdTQber1WSuNqVh2d8iBkifQK3QVFQHlWgtOvlLwDIt5uFJRkGo9%2B54ddowVZtB2xb%2BgMRYNlLw%3D%3D)
