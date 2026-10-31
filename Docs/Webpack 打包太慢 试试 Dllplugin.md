# Webpack 打包太慢? 试试 Dllplugin

webpack在build包的时候，有时候会遇到打包时间很长的问题，这里提供了一个解决方案，让打包如丝般顺滑~

## 1. 介绍

在用 Webpack 打包的时候，对于一些不经常更新的第三方库，比如 `react`，`lodash`，`vue` 我们希望能和自己的代码分离开，Webpack 社区有两种方案

- CommonsChunkPlugin
- DLLPlugin

对于 `CommonsChunkPlugin`，webpack 每次打包实际还是需要去处理这些第三方库，只是打包完之后，能把第三方库和我们自己的代码分开。而 `DLLPlugin` 则是能把第三方代码完全分离开，即每次只打包项目自身的代码。Dll这个概念是借鉴了Windows系统的dll，一个dll包，就是一个纯纯的依赖库，它本身不能运行，是用来给你的app引用的。

## 2. 模板webpack-simple 用法

要使用 `DLLPlugin`，需要额外新建一个配置文件。所以对于用这种方式打包的项目，一般会有下面两个配置文件

- webpack.config.js
- webpack.dll.config.js

**在项目根目录新建一个文件 webpack.dll.config.js**

```text
const path    = require('path');
const webpack = require('webpack');
module.exports = {
  entry: {
      vendor: ['vue-router','vuex','vue/dist/vue.common.js','vue/dist/vue.js','vue-loader/lib/component-normalizer.js','vue']
  },
  output: {
    path: path.resolve('./dist'),
    filename: '[name].dll.js',
    library: '[name]_library'
  },
  plugins: [
    new webpack.DllPlugin({
      path: path.resolve('./dist', '[name]-manifest.json'),
      name: '[name]_library'
    })
  ]
};
```

这是把用到的第三方插件添加到 vendor 中。  
**然后在webpack.config.js中添加代码**

```text
plugins: [
    new webpack.DllReferencePlugin({
      manifest: require('./dist/vendor-manifest.json')
    })
  ]
```

**再在入口html文件中引入 vendor.dll.js**   
`<script type="text/javascript" src="./../vendor.dll.js"></script>`

**然后在package.json文件中添加快捷命令(build:dll)**

```text
"scripts": {
    "dev": "cross-env NODE_ENV=development webpack-dev-server --open --hot",
    "build": "cross-env NODE_ENV=production webpack --progress --hide-modules",
    "build:dll": "webpack --config webpack.dll.config.js"
  },
```

最后打包的时候首先执行npm run build:dll命令会在打包目录下生成 `vendor-manifest.json` 文件与 `vendor.dll.js` 文件。   
打包dll的时候，Webpack会将所有包含的库做一个索引，写在一个manifest文件中，而引用dll的代码（dll user）在打包的时候，只需要读取这个manifest文件，就可以了。

**再执行`npm run build`**  
发现现在的webpack打包速度为2，3秒左右，与之前的20秒左右快了很多。

## 3. 模板webpack 用法

**在build下创建 webpack.dll.config.js**

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/2d2d0a2b19d067ff20d8f24bb0a9d1a2bc5cfcdac910ff1c0346495d85c80252.png)

内容：

```text
const path = require('path')
const webpack = require('webpack')
module.exports = {
  entry: {
    vendor: [
      'vue-router',
      'vuex',
      'vue/dist/vue.common.js',
      'vue/dist/vue.js',
      'vue-loader/lib/component-normalizer.js',
      'vue',
      'axios',
      'echarts'
    ]
  },
  output: {
    path: path.resolve('./dist'),
    filename: '[name].dll.js',
    library: '[name]_library'
  },
  plugins: [
    new webpack.DllPlugin({
      path: path.resolve('./dist', '[name]-manifest.json'),
      name: '[name]_library'
    }),
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false
      }
    })
  ]
}
```

建议加上代码压缩插件，否则dll包会比较大。

**在 webpack.prod.conf.js 的 plugin 后面加入配置**

```text
new webpack.DllReferencePlugin({
    manifest: require('../dist/vendor-manifest.json')
})
```

**根目录下的入口 index.html 加入引用**  
`<script type="text/javascript" src="./vendor.dll.js"></script>`

**package.json的script里加入快捷命令**  
`"build:dll": "webpack --config build/webpack.dll.config.js"`

要生成dll时运行`npm run build:dll`，即生成dist目录下两个文件 `vender-manifest.json` 与 `vender.dll.js`。  
然后正式生成 prod `npm run build:prod`，即生成除`webpack.dll.config.js`中指定包之外的其他打包文件。

在尝试在 [`vue-element-admin`](http://panjiachen.github.io/vue-element-admin) 中引入 DllPlugin 时，加入20个打包项，测试结果：  
原来的打包时间：

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/14a00d2ddad3d6c1e1fdfac95373766f7705617792a23d09ed13c71bbda82f20.png)

引入 DllPlugin 后的打包时间：

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/ab7dbfb0749bd90f91d8590564ad90c82b7b86483e69a4972942647526b5b2d7.png)

可以看到大幅缩短了打包时间~

## 4. 另一种方法 externals 选项

也可以使用 externals 让webpack不打包某部分，然后在其他地方引入cdn上的js文件，利用缓存下载cdn文件达到减少打包时间的目的。  
**配置externals选项**：

```text
// webpack.prod.config.js
// 多余代码省略
module.exports = {
    externals: {
        'vue': 'window.Vue',
        'vuex': 'window.Vuex',
        'vue-router': 'window.VueRouter'
        ...
    }
}

// 配置externals之后，webpack不会把配置项中的代码打包进去，别忘了需要在外部引入cdn上的js文件
// html
<body>
    <script src="XXX/cdn/vue.min.js"></script>
    ......
</body>
```

---

> 参考：
>
> 1. [Webpack DLL 用法](http://www.jianshu.com/p/a5b3c2284bb6)
> 2. [使用webpack.DllPlugin与webpack.DllReferencePlugin解决webpack打包慢问题](http://blog.csdn.net/hanxue_tyc/article/details/76795861)
> 3. [webpack文档](https://doc.webpack-china.org/plugins/dll-plugin/)
> 4. [Webpack的dll功能](https://segmentfault.com/a/1190000005969643)
