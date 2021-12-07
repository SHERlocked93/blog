# JS 中的offset、scroll、client

经常碰到offset、scroll、client这几个关键字，这里总结一下。

![img](file:///C:/Users/qiany/Documents/My%20Knowledge/temp/a0b082bf-d98e-4118-83a4-5c587b923857/128/index_files/44e942d3-a4f0-48fc-9931-f2dfab61b03f.png)

![img](file:///C:\Users\qiany\Documents\My Knowledge\temp\a0b082bf-d98e-4118-83a4-5c587b923857\128\index_files\0.4192579735080717.png)

## 1. offset 

`offset` 指**偏移**，包括这个元素在文档中占用的所有显示宽度，包括滚动条、`padding`、`border`，不包括`overflow`隐藏的部分

1. `offsetParent`属性返回一个对象的引用，这个对象是距离调用`offsetParent`的父级元素中最近的（在包含层次中最靠近的），并且是已进行过CSS定位的容器元素。 如果这个容器元素未进行CSS定位, 则`offsetParent`属性的取值为根元素的引用。
   - 如果当前元素的父级元素中没有进行CSS定位（`position`为absolute/relative），`offsetParent`为body
   - 如果当前元素的父级元素中有CSS定位（`position`为absolute/relative），`offsetParent`取父级中最近的元素

2. **obj.offsetWidth** 指 obj 控件自身的绝对宽度，不包括因 `overflow` 而未显示的部分，也就是其实际占据的宽度，整型，单位：像素。
   `offsetWidth` = `border-width`*2+`padding-left`+`width`+`padding-right`

3. **obj.offsetHeight** 指 obj 控件自身的绝对高度，不包括因 overflow 而未显示的部分，也就是其实际占据的高度，整型，单位：像素。
   `offsetHeight` = `border-width`*2+`padding-top`+`height`+`padding-bottom`

4. **obj.offsetTop** 指 obj 相对于版面或由 `offsetParent` 属性指定的父坐标的计算上侧位置，整型，单位：像素。
   `offsetTop`= `offsetParent`的padding-top + 中间元素的offsetHeight + 当前元素的margin-top

5. **obj.offsetLeft** 指 obj 相对于版面或由 `offsetParent` 属性指定的父坐标的计算左侧位置，整型，单位：像素。
   `offsetLeft`= `offsetParent`的padding-left + 中间元素的offsetWidth + 当前元素的margin-left



## 2. scroll

`scroll`指**滚动**，包括这个元素没显示出来的实际宽度，包括`padding`，不包括滚动条、`border`

1. **scrollHeight** 获取对象的滚动高度，对象的实际高度；
2. **scrollLeft** 设置或获取位于对象左边界和窗口中目前可见内容的最左端之间的距离
3. **scrollTop** 设置或获取位于对象最顶端和窗口中可见内容的最顶端之间的距离
4. **scrollWidth** 获取对象的滚动宽度

## 3. client

`client`指元素本身的**可视**内容，不包括`overflow`被折叠起来的部分，不包括滚动条、`border`，包括`padding`

1. **clientWidth** 对象可见的宽度，不包括滚动条等边线，会随窗口的显示大小改变
2. **clientHeight** 对象可见的高度
3. **clientTop**、**clientLeft** 这两个返回的是元素周围边框的厚度，一般它的值就是0。因为滚动条不会出现在顶部或者左侧









---



网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出~



> 参考：
> 
> 1. [javascript的offset、client、scroll的总结笔记](https://www.jianshu.com/p/cd0567797d5e)
> 2. [轻松弄清JavaScript中的offset、scroll、client](<https://my.oschina.net/longteng2013/blog/167023)
> 3. [offset client scroll screen 关键字整理](https://zhuanlan.zhihu.com/p/22077165)

 