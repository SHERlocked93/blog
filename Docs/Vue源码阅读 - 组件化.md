# Vue源码阅读 - 组件化
[TOC]

vue已是目前国内前端web端三分天下之一，同时也作为本人主要技术栈之一，在日常使用中知其然也好奇着所以然，另外最近的社区涌现了一大票vue源码阅读类的文章，在下借这个机会从大家的文章和讨论中汲取了一些营养，同时对一些阅读源码时的想法进行总结，出产一些文章，作为自己思考的总结，本人水平有限，欢迎留言讨论~

目标Vue版本：`2.5.17-beta.0`

vue源码注释：[https://github.com/SHERlocked93/vue-analysis](https://github.com/SHERlocked93/vue-analysis)

声明：文章中源码的语法都使用 Flow，并且源码根据需要都有删节(为了不被迷糊 @_@)，如果要看完整版的请进入上面的[github地址](https://github.com/SHERlocked93/vue-analysis)，本文是系列文章，文章地址见底部~


## 1. 响应式系统





---

**本文是系列文章，随后会更新后面的部分，共同进步~**
> 1. [Vue源码阅读 - 文件结构与运行机制](https://juejin.im/post/5b38830de51d455888216675)
> 2. [Vue源码阅读 - 依赖收集原理](https://juejin.im/post/5b40c8495188251af3632dfa)
> 3. [Vue源码阅读 - 批量异步更新与nextTick原理](https://juejin.im/post/5b50760f5188251ad06b61be)

网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出~

> 参考：
> 1. 
