# Vue源码阅读 - 组件化
vue已是目前国内前端web端三分天下之一，同时也作为本人主要技术栈之一，在日常使用中知其然也好奇着所以然，另外最近的社区涌现了一大票vue源码阅读类的文章，在下借这个机会从大家的文章和讨论中汲取了一些营养，同时对一些阅读源码时的想法进行总结，出产一些文章，作为自己思考的总结，本人水平有限，欢迎留言讨论~

目标Vue版本：`2.5.17-beta.0`

vue源码注释：[https://github.com/SHERlocked93/vue-analysis](https://github.com/SHERlocked93/vue-analysis)

声明：文章中源码的语法都使用 Flow，并且源码根据需要都有删节(为了不被迷糊 @_@)，如果要看完整版的请进入上面的[github地址](https://github.com/SHERlocked93/vue-analysis)，本文是系列文章，文章地址见底部~

## 1. 响应式系统

---

**本文是系列文章，随后会更新后面的部分，共同进步~**
> 1. [Vue源码阅读 - 文件结构与运行机制](https://github.com/SHERlocked93/blog/blob/master/Docs/Vue%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%20-%20%E6%96%87%E4%BB%B6%E7%BB%93%E6%9E%84%E4%B8%8E%E8%BF%90%E8%A1%8C%E6%9C%BA%E5%88%B6.md)
> 2. [Vue源码阅读 - 依赖收集原理](https://github.com/SHERlocked93/blog/blob/master/Docs/Vue%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%20-%20%E4%BE%9D%E8%B5%96%E6%94%B6%E9%9B%86%E5%8E%9F%E7%90%86.md)
> 3. [Vue源码阅读 - 批量异步更新与nextTick原理](https://github.com/SHERlocked93/blog/blob/master/Docs/Vue%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%20-%20%E6%89%B9%E9%87%8F%E5%BC%82%E6%AD%A5%E6%9B%B4%E6%96%B0%E4%B8%8EnextTick.md)

> 参考：
> 1.
