# Vue-router应用如何做锚点定位

[TOC]

最近在做个人项目 [vue-style-codebase](https://github.com/SHERlocked93/vue-style-codebase) 的时候遇到了一个场景，根据页面内容自动生成一个目录，并且需要跟右侧内容区的滚动同步滚动显示活动链接。

因为vue-router的hash路由会与传统的锚点定位冲突，点击的时候会导航到错误的路由路径，因此。在此记录一下怎么去完善这个功能的过程。

## 1 vue-router 采用 history 模式

使用 `vue-router` 的 history 模式之后，其提供的 [scrollBehavior](https://router.vuejs.org/zh/api/#scrollbehavior) 可以获取

## 2 手动实现点击跳转



## 3 自定义指令













---

网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出~
> 参考：
>
> 1. [vue2.0中怎么做锚点定位](https://segmentfault.com/q/1010000007888351)
> 2. [Codepen - Progress Nav](https://codepen.io/hakimel/pen/BpKNPg) 