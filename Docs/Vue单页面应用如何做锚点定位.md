# Vue-router应用如何做锚点定位

最近在做个人项目 [vue-style-codebase](https://github.com/SHERlocked93/vue-style-codebase) 的时候遇到了一个场景，根据页面内容自动生成一个目录，并且需要跟右侧内容区的滚动同步滚动显示活动链接。

因为vue-router的hash路由会与传统的锚点定位冲突，点击的时候会导航到错误的路由路径，因此。在此记录一下怎么去完善这个功能的过程。

## 1 vue-router 采用 history 模式

使用 `vue-router` 的 history 模式之后，其提供的 [scrollBehavior](https://router.vuejs.org/zh/api/#scrollbehavior) 可以获取

## 2 手动实现点击跳转

## 3 自定义指令

---
