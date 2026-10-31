# vue-router 源码阅读 - 
前端路由是我们前端开发日常开发中经常碰到的概念，在下在日常使用中知其然也好奇着所以然，因此对 vue-router 的源码进行了一些阅读，也汲取了社区的一些文章优秀的思想，于本文记录总结作为自己思考的输出，本人水平有限，欢迎留言讨论~

目标 vue-rouer 版本：`3.0.2`

vue-router源码注释：[vue\-router\-analysis](https://github.com/SHERlocked93/vue-router-analysis)

声明：文章中源码的语法都使用 Flow，并且源码根据需要都有删节(为了不被迷糊 @_@)，如果要看完整版的请进入上面的 [github地址](https://github.com/SHERlocked93/vue-router-analysis) ~ 

本文是系列文章，链接见底部 ~

### 1. VueRouter 实例化

createMatcher的的初始化就是根据路由的配置描述创建映射表,包括path、name到路由record的映射关系。

match会根据传入的位置和路径计算出新的位置，并匹配到对应的路由record，然后根据新的位置和record创建新的路径并返回。

---
本文是**系列文章**，随后会更新后面的部分，共同进步~
> 1. [vue-router 源码阅读 - 文件结构与注册机制](https://github.com/SHERlocked93/blog/blob/master/Docs/vue-router%20%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%20-%20%E6%96%87%E4%BB%B6%E7%BB%93%E6%9E%84%E4%B8%8E%E6%B3%A8%E5%86%8C%E6%9C%BA%E5%88%B6.md)

> 推介阅读：
>
>1. 
>
>参考：
>
>1. [Vue\.js 技术揭秘](https://ustbhuangyi.github.io/vue-analysis/vue-router/router.html)
