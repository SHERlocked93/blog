# CSS margin合并问题

在CSS当中，相邻的两个盒子（可能是兄弟关系也可能是祖先关系）的外边距可以结合成一个单独的外边距。这种合并外边距的方式被称为折叠，并且因而所结合成的外边距称为折叠外边距。

## 1. 折叠的结果

1. 两个相邻的外边距都是正数时，折叠结果是它们两者之间较大的值。
2. 两个相邻的外边距都是负数时，折叠结果是两者绝对值的较大值。
3. 两个外边距一正一负时，折叠结果是两者的相加的和。

## 2. 条件

产生折叠的必备条件：[**margin必须是邻接的**](https://link.segmentfault.com/?enc=wdEnRFF9%2BaOH5y67Xl5RHA%3D%3D.Yhu6PQTui7OdY3k%2B2ah9FFFXakbReedzK3jVtKS0kq87HeclJuyKrzc8Sy%2BzzUYNs%2Bh%2BP0ll8Pf%2FIF%2FJLelXlw%3D%3D)  
而根据w3c规范，两个margin是邻接的必须满足以下条件：

1. 必须是处于常规文档流（非float和绝对定位）的块级盒子，并且处于同一个BFC当中。
2. 没有线盒，没有空隙（[clearance](https://link.segmentfault.com/?enc=e8ES7MCLwu7%2BPAnIG3VrCQ%3D%3D.Tem7FkztmdL46x04PYxZrUg%2B9%2F04LGt3mQxgECC7%2FGUrrh7ZWa9ElYr%2Fb6zcbsaeHPK8ONe7FHdTGyQ7uCt2ZA%3D%3D)，下面会讲到），没有padding和border将他们分隔开
3. 都属于垂直方向上相邻的外边距，可以是下面任意一种情况

   - 元素的margin-top与其第一个常规文档流的子元素的margin-top
   - 元素的margin-bottom与其下一个常规文档流的兄弟元素的margin-top
   - height为auto的元素的margin-bottom与其最后一个常规文档流的子元素的margin-bottom
   - 高度为0并且最小高度也为0，不包含常规文档流的子元素，并且自身没有建立新的BFC的元素的margin-top和margin-bottom

### 2.1 条件解读

1. 创建了新的BFC的元素（例如浮动元素或者'overflow'值为'visible'以外的元素）与它的子元素的外边距不会折叠
2. 浮动元素不与任何元素的外边距产生折叠（包括其父元素和子元素）
3. 绝对定位元素不与任何元素的外边距产生折叠
4. inline-block元素不与任何元素的外边距产生折叠
5. 一个常规文档流元素的margin-bottom与它下一个常规文档流的兄弟元素的margin-top会产生折叠，除非它们之间存在间隙（clearance）。
6. 一个常规文档流元素的margin-top 与其第一个常规文档流的子元素的margin-top产生折叠，条件为父元素不包含 padding 和 border ，子元素不包含 clearance。
7. 一个 'height:auto' 并且 'min-height:0'的常规文档流元素的 margin-bottom 会与其最后一个常规文档流子元素的 margin-bottom 折叠，条件为父元素不包含 padding 和 border ，子元素的 margin-bottom 不与包含 clearance 的 margin-top 折叠。
8. 一个不包含border-top、border-bottom、padding-top、padding-bottom的常规文档流元素，并且其 'height' 为 0 或 'auto'， 'min-height:0'，其里面也不包含行盒(line box)，其自身的 margin-top 和 margin-bottom 会折叠。

**注意：**  
浮动元素和绝对定位元素不与其他盒子产生外边距折叠是因为元素会脱离当前的文档流，违反了上面所述的两个margin是邻接的条件同时，又因为浮动和绝对定位会使元素为它的内容创建新的BFC，因此该元素和子元素所处的BFC是不相同的，因此也不会产生margin的折叠。

但是浮动元素脱离了当前的BFC并不影响它后面的兄弟元素，后面的兄弟元素与浮动元素前面的元素依然在同一个BFC当中，所以，它们之间的margin还是会折叠的。

### 2.2 空隙 clearance

当浮动元素之后的元素设置clear以闭合相关方向的浮动时，根据w3c规范规定，闭合浮动的元素会在其margin-top以上产生一定的空隙（clearance），该空隙会阻止元素margin-top的折叠，并作为间距存在于元素的margin-top的上方。关于这个间距的计算稍微有点复杂，但实际工作中你并不需要去计算它。

## 3. 如何解决

使用BFC解决margin合并问题可以参考这篇文章：[CSS中重要的BFC](https://github.com/SHERlocked93/blog/blob/master/Docs/CSS%20%E4%B8%AD%E7%9A%84%E5%B1%82%E5%8F%A0%E5%92%8C%E5%9D%97%E7%BA%A7%E6%A0%BC%E5%BC%8F%E5%8C%96%E4%B8%8A%E4%B8%8B%E6%96%87.md)

### 3.1 自身margin合并的情况

- 加个`padding`或者`border-top`/`border-bottom`

### 3.2 相邻元素的情况

1. 相邻元素中间添加一个1px的间隔元素(不推介，因为添加了冗余标签)
2. 相邻元素加上`display: inline-block;` 或者`grid`与`inline-grid`后相邻元素之间的垂直外边距不会合并，不过注意`grid`的浏览器兼容性不太好。
3. 相邻元素可以在其中一个元素外面包一层div，并设置任何能触发BFC的属性即可。codepen的DEMO
4. 浮动与绝对定位之类脱离文档流的元素不发生margin合并

### 3.3 父子元素的情况

1. 给父元素添加padding-top值，缺点：增加了一点padding的误差
2. 给父元素添加border值，比如`border-top:1px solid transparent;`，缺点同上
3. 给父元素或者子元素声明浮动float，缺点：float有时是不必要的。
4. 使父元素或子元素声明为绝对定位：`position:absolute/fixed;`
5. 给父元素添加属性 `overflow:auto/auto/scroll;`
6. 子元素的`margin`使用父元素的`padding`代替

---

> 参考：
>
> 1. [CSS外边距合并的问题](https://link.segmentfault.com/?enc=A0E1FrlbzPHl1%2BFiMWrsBg%3D%3D.azjSQZTZOhrw5kPSea30UEJTiWBPsVpyyfMotrxe6h3oY4rJ3lNJRZ27JQT6x6MKIIGWrqe3HuZwH3djO5TDqA%3D%3D)
> 2. [深入理解css中的margin属性](https://link.segmentfault.com/?enc=S6D78TAe2228GP5shy5TNw%3D%3D.oZ8AMuIAkTp3CakWeprlcPL96vuWSG%2FcAwu%2Bxtn3WrFVFjBGqH92hxNpjslPl59mAzHPbNUFlF8%2BuGR%2BtiQHyA%3D%3D)
> 3. [深入理解BFC和Margin Collapse](https://www.w3cplus.com/css/understanding-bfc-and-margin-collapse.html)
