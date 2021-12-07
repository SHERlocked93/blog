# 开发微信小程序，我为什么放弃 setData，使用 upData

[TOC]

![2020-07-22-HC2B7ingmKo](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@env/uPic/2020-07-22-HC2B7ingmKo.jpg)

鉴于在下使用微信小程序开发时使用 `setData` 的蹩脚体验，开发了个库函数 `wx-updata`，项目上线之后，我把这个自用的库函数整理放到 Github 上开源出来 [wx-updata](https://github.com/SHERlocked93/wx-updata)，这个库函数在开发的时候对我很有帮助，希望也可以帮到大家 👏

如果大家在使用中遇到了问题，可以给我提 pr，提 issue，一起来改善小程序开发体验加油～

1. `wx-updata` 版本 0.0.10
2. Github 地址： https://github.com/SHERlocked93/wx-updata
3. 小程序代码片段预览地址： https://developers.weixin.qq.com/s/CcXdO1mc73jD
4. 小程序代码片段代码地址： https://github.com/SHERlocked93/wx-updata-demo

## 1. setData 不方便的地方

你在使用 `setData` 的时候，是不是有时候觉得很难受，举个简单的例子：

```javascript
// 你的 data
data: {
    name: '蜡笔小新',
    info: { height: 140, color: '黄色' }
}
```

如果要修改 `info.height` 为 155，使用 `setData` 要怎么做呢：

```javascript
// 这样会把 info 里其他属性整不见了
this.setData({ info: { height: 155 } })

// 你需要取出 info 对象，修改后整个 setData
const { info } = this.data
info.height = 155
this.setData({ info })
```

似乎并不太复杂，但如果 `data` 是个很大的对象，要把比较深且不同的对象、数组项挨个改变：

```javascript
data: {
    name: '蜡笔小新',
    info: {
        height: 140, color: '黄色',
        desc: [{ age: 8 }, '最喜欢大象之歌', '靓仔', { dog: '小白', color: '白色' }]
    }
}
```

比如某个需求，需要把 `info.height` 改为 155，同时改变 `info.desc` 数组的第 0 项的 `age` 为 12，第 3 项的 `color` 为灰色呢？

```javascript
// 先取出要改变的对象，改变数字后 setData 回去
const { info } = this.data
info.height = 155
info.desc[0].age = 12
info.desc[3].color = '灰色'
this.setData({ info })

// 或者像某些文章里介绍的，这样可读性差，也不太实用
this.setData({
    'info.height': 155,
    'info.desc[0].age': 12,
    'info.desc[3].color': '灰色'
})
```

上面这两种方法，是我们平常小程序里经常用的，和其他 Web 端的框架相比，就很蹩脚，一种浓浓的半成品感扑面而来，有没有这样一个方法：

```javascript
this.upData({
    info: {
        height: 155,
        desc: [{ age: 12 }, , , { color: '灰色' }]
    }
})
```

这个方法会帮我们深度改变嵌套对象里对应的属性值，跳过数组项里不想改变的，只设置我们提供了的属性值、数组项，岂不是省略了一大堆蹩脚的代码，而且可读性也极佳呢。

这就是为什么我在上线的项目中使用 [wx-updata](https://github.com/SHERlocked93/wx-updata)，而不是 `setData`

wx-updata 的原理其实很简单，举个例子：

```javascript
this.upData({
    info: {
        height: 155,
        desc: [{ age: 12 }]
    }
})

// 会被自动转化为下面这种格式，
// this.setData({
//    'info.height': 155,
//    'info.desc[0].age': 12,
// })
```

转化为下面这种格式的请求，原来这个工作是要我们自己手动来做，现在 wx-updata 帮我们做了，岂不美哉！

下面介绍一下 wx-updata 的优点和主要使用方法～

## 2. wx-updata 的优点

1. 支持 `setData` 对象自动合并，不用写蹩脚的对象路径了 🥳
2. 支持对象中嵌套数组，数组中嵌套对象；
3. 如果数组的某个值你不希望覆盖，请使用数组空位来跳过这个数组项，比如 `[1,,3]` 这个数组中间就是数组空位；
4. 如果数组空位你的 `Eslint` 报错，可以使用 `wx-updata` 提供的 Empty 来代替： `[1, Empty, 3]`

## 3. wx-updata 安装

> 你也可以直接把 `dist` 目录下的 `wx-updata.js` 拷贝到项目里使用

使用 `npm`、`yarn` 安装方式：


```bash
$ npm i -S wx-updata
# or
$ yarn add wx-updata
```

然后：

1. 把微信开发者工具面板右侧的 `详情 - 本地设置 - 使用npm模块` 按钮打开；
2. 点击微信开发者工具面板工具栏的 `工具 - 构建npm`；

构建后成功生成 `miniprogram_npm` 文件夹就可以正常使用了

## 4. wx-updata 使用方法

### 使用方式一

可以使用直接挂载到 `Page` 上的方式，这样就可以在 `Page` 实例中像使用 `setData` 一样使用 `upData` 了

```javascript
// app.js
import { updataInit } from './miniprogram_npm/wx-updata/index'  // 你的库文件路径


App({
    onLaunch() {
        Page = updataInit(Page, { debug: true })
    }
})
```

```javascript
// 页面代码中

this.upData({
    info: { height: 155 },
    desc: [{ age: 13 }, '帅哥'],
    family: [, , [, , , { color: '灰色' }]]
})
```

### 使用方式二

有的框架可能在 `Page` 对象上进行了进一步修改，直接替换 `Page` 的方式可能就不太好了，`wx-updata` 同样暴露了工具方法，用户可以在页面代码中直接使用工具方法进行处理：

```javascript
// 页面代码中

import { objToPath } from './miniprogram_npm/wx-updata/index'  // 你的库文件路径

Page({
    data: { a: { b: 2}, c: [3,4,5]},

    // 自己封装一下
    upData(data) {
        return this.setData(objToPath(data))
    },

    // 你的方法中或生命周期函数
    yourMethod() {
        this.upData({ a: { b: 7}, c: [8,,9]})
    }
})
```

### 使用 Empty 代替数组空位

可以使用 `wx-updata` 提供的 Empty 来代替数组空位，由于 Empty 本质上是一个 Symbol，所以只能使用 `wx-updata` 导出的，而不能自己新建。

```javascript
// 页面代码中
import { Empty } from './miniprogram_npm/wx-updata/index'

this.upData({
    info: { height: 155 },
    desc: [{ age: 13 }, '帅哥'],
    family: [Empty, Empty, [Empty, Empty, Empty, { color: '灰色' }]]
})
```

## 5. wx-updata 相关 API

`Page.prototype.upData(Object data, Function callback)`

1. `data`： 你希望设置的 data
2. `callback`： 跟 [setData](https://developers.weixin.qq.com/miniprogram/dev/reference/api/Page.html#Page.prototype.setData(Object%20data,%20Function%20callback)) 第二个参数一样，引起界面更新渲染完毕后的回调函数



`updataInit(Page, config)`

1. `Page`： 页面对象，需要在 `app.js` 中调用；
2. `config`： 若提供配置参数 `{ debug: true }`，会将路径化后的 data 打印出来，帮助用户进行调试；



`objToPath(Object data)`

1. `data`： 你希望设置的 data 对象



---
网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出~


> 参考文档：
>
> 1. [小程序开发实用技巧——扩展 Page 页面对象 - 掘金](https://juejin.im/post/5b55c1056fb9a04f951d1d4b)


PS：本人博客地址 [Github - SHERlocked93/blog](https://github.com/SHERlocked93/blog)，也欢迎大家关注我的公众号【前端下午茶】，一起加油吧~

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@env/uPic/2020-03-04-5cf08a479cd5d75372-20200304131909230.jpg)

另外可以加入「前端下午茶交流群」微信群，长按识别下面二维码即可加我好友，备注**加群**，我拉你入群～

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@env/uPic/2020-03-04-5d2986f77e9bc11533-20200304131910068.jpg)