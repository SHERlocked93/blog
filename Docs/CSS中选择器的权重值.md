# CSS中选择器的权重值

CSS 具有自己的优先级计算方法，而不仅仅是行间>内部>外部、ID>class>元素

## 1. 样式类型

- 行间样式

```text
<h1 style="font-size:12px;color:#000;">我的行间CSS样式。</h1>
```

- 内联样式

```text
<style type="text/css">
  h1{font-size:12px;
      color:#000;
      }
</style>
```

- 外部样式

```text
<link rel="stylesheet" href="css/style.css">
```

## 2. 选择器类型

| 选择器 | 栗子 |
| --- | --- |
| **ID** | #id |
| **class** | .class |
| **标签** | p |
| **属性** | [type='text'] |
| **伪类** | :hover |
| **伪元素** | ::first-line |
| **相邻选择器、子代选择器** | `> +` |

## 3. 权重计算规则

1. **内联样式**，如: style="..."，权值为`1000`。
2. **ID选择器**，如：#content，权值为`0100`。
3. **类，伪类、属性选择器**，如.content，权值为`0010`。
4. **类型选择器、伪元素选择器**，如div p，权值为`0001`。
5. **通配符、子选择器、相邻选择器**等。如`* > +`，权值为`0000`。
6. **继承**的样式没有权值

## 4. 比较规则

- 1,0,0,0 > 0,99,99,99。也就是说从左往右逐个等级比较，前一等级相等才往后比。
- 无论是行间、内部和外部样式，都是按照这个规则来进行比较。而不是直观的行间>内部>外部样式；ID>class>元素。之所以有这样的错觉，是因为确实行间为第一等的权重，所以它的权重是最高的。而内部样式可能一般写在了外部样式引用了之后，所以覆盖掉了之前的。
- 在权重相同的情况下，后面的样式会覆盖掉前面的样式。
- 通配符、子选择器、相邻选择器等的。虽然权值为0000，但是也比继承的样式优先，0 权值比无权值优先。

## 5. !important

**!important** 的作用是提升优先级，换句话说。加了这句的样式的优先级是最高的（比内联样式的优先级还高)。

```text
<style>
    p{color:red !important;}
</style>
<p style="color:blue;">我显示红色</p>　
```

ie7+和别的浏览器对important的这种作用的支持度都很好。只有ie6-有些bug

```text
p{
  color:red !important;
  color:blue;    
}        //会显示blue
```

但是这并不说明ie6不支持important，只是支持上有些bug。

```text
p{color:red !important;  }
p{color:blue;}        // 这样就会显示的是red。说明ie6还是支持important的
```

当 `!important` 规则被应用在一个样式声明中时,该样式声明会覆盖CSS中任何其他的声明，无论它处在声明列表中的哪个位置。尽管如此，`!important` 规则还是与优先级毫无关系。使用 `!important` 不是一个好习惯，因为它改变了你样式表本来的级联规则，从而难以调试。  
在使用 `!important` 时需要注意：

- Never 永远不要在全站范围的 css 上使用 !important
- Only 只在需要覆盖全站或外部 css（例如引用的 ExtJs 或者YUI ）的特定页面中使用 !important
- Never 永远不要在你的插件中使用 !important
- Always 要优化考虑使用样式规则的优先级来解决问题而不是 !important

---

> 参考：
>
> 1. [CSS 选择器权重计算规则](https://link.segmentfault.com/?enc=UL%2BNNVxqbiNevbWDLbctbQ%3D%3D.MNFcqeFDtctXs6LZJWDtJz6Rb4iGDuCQpMVhkuu%2FxlSv%2F6kJKAWGN69eETqHryh7)
> 2. [MDN 优先级是如何计算的？](https://link.segmentfault.com/?enc=UryV0R%2B%2FiiFDrM1c8W5k5w%3D%3D.sp5vRks2161%2BJKS7mHVzWm8vQt%2F0gzlQiVd6XLCrSfTqjzWQ2syoQ5BwLoke0eEOAPHfRI%2FnsQpngwv8wFSBHQ%3D%3D)
