# vue-router 源码阅读 - 
[TOC]



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
> 1. [vue-router 源码阅读 - 文件结构与注册机制](https://segmentfault.com/a/1190000018262346)

网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出~

> 推介阅读：
>
>1. 
>
>参考：
>
>1. [Vue\.js 技术揭秘](https://ustbhuangyi.github.io/vue-analysis/vue-router/router.html)

PS：欢迎大家关注我的公众号【前端下午茶】，一起加油吧~
![](https://i.loli.net/2019/03/26/5c99d1685fff9.png)