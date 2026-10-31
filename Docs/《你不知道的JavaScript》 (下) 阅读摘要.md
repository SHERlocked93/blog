# 《你不知道的JavaScript》 (下) 阅读摘要

本书属于基础类书籍，会有比较多的基础知识，所以这里仅记录平常不怎么容易注意到的知识点，不会全记，供大家和自己翻阅；

不错，下册的知识点就这么少，非常不推介看下册；

上中下三本的读书笔记：

1. [《你不知道的JavaScript》 (上) 读书笔记](https://github.com/SHERlocked93/blog/blob/master/Docs/%E3%80%8A%E4%BD%A0%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84JavaScript%E3%80%8B%20%28%E4%B8%8A%29%20%E9%98%85%E8%AF%BB%E6%91%98%E8%A6%81.md)
2. [《你不知道的JavaScript》 (中) 读书笔记](https://github.com/SHERlocked93/blog/blob/master/Docs/%E3%80%8A%E4%BD%A0%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84JavaScript%E3%80%8B%20%28%E4%B8%AD%29%20%E9%98%85%E8%AF%BB%E6%91%98%E8%A6%81.md)
3. [《你不知道的JavaScript》 (下) 读书笔记](https://github.com/SHERlocked93/blog/blob/master/Docs/%E3%80%8A%E4%BD%A0%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84JavaScript%E3%80%8B%20%28%E4%B8%8B%29%20%E9%98%85%E8%AF%BB%E6%91%98%E8%A6%81.md)

## 第三章 代码组织

### 子类构造器

有个 ES6 子类构造器的限制是：子类构造器中调用 `super()` 之后才能访问 `this`；具体原因比较复杂，不过可以归结为初始化你的实例 `this` 的实际上是父构造器。在 ES6 之前正好相反，`this` 对象是由子类构造器创建的，然后在子类的 `this` 上下文中调用父类构造器；

```text
class Foo {
  constructor() { this.a = 1 }
}

class Bar extends Foo {
  constructor() {
    this.b = 2        // 报错，this不允许在super()之前调用
    super()            // 交换上一句位置
  }
}
```

---
