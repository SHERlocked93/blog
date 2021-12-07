# Egg.js入门

[TOC]

Egg.js 的一个重要原则，约定大于配置。

## 新建工程

```bash
mkdir egg-demo    # 创建demo目录
cd egg-demo       # 进入这个新建的目录
npm init          # 一直enter下去
npm i -S egg      # 安装egg.js
npm i -S egg-bin  # 安装egg-bin
```

这时候就创建了一个简单的目录，目录是这样的：

![](https://raw.githubusercontent.com/SHERlocked93/pic/env/2019/20191118134216.png)

然后在 `package.json` 文件的 `scripts` 里面加上一个 `dev` 命令，使用 `egg-bin` 来启动项目：

![](https://raw.githubusercontent.com/SHERlocked93/pic/env/2019/20191118135013.png)

现在 `npm run dev` 就可以跑起来了，但是因为你没写任何服务代码，所以访问 `http://127.0.0.1:7001/` 的时候会报 `Error in /`，所以下面我们简单写上一些代码，跑起来 `hello world`。

### HelloWorld

首先在根目录下创建文件夹 `app` 和 `config`，并新建一些文件，现在文件夹除了 `node_modules` 之外看起来是这样的：

```bash
.
├── app
│   ├── controller
│   │   └── home.js
│   └── router.js
├── config
│   └── config.default.js
└── package.json
```

这些文件夹到底是用来做什么的，后文会单独讲解。

这个 `home.js` 是 `controller`，对应于 `MVC` 框架中的 `C`：

```javascript
// app/controller/home.js
const Controller = require('egg').Controller

class HomeController extends Controller {
  async index() {
    this.ctx.body = 'Hello world, Egg ！'
  }
}

module.exports = HomeController
```

而 `router.js` 指代的是路由文件，配置路由映射

```javascript
// app/router.js
module.exports = app => {
  const { router, controller } = app
  router.get('/', controller.home.index)
}
```

最后添加一个配置文件，不加的话会报错 `Please set config.keys first`

```javascript
exports.keys = '呵呵呵'
```

下面 `npm run dev` 运行起来看看：

![](https://raw.githubusercontent.com/SHERlocked93/pic/env/2019/20191118141720.png)

再访问 `http://127.0.0.1:7001/`

![](https://raw.githubusercontent.com/SHERlocked93/pic/env/2019/20191118141753.png)

恭喜，Hello world 运行成功！

### 使用脚手架快速创建工程

上面的方法是不是看起来比较繁琐，每次都要手动创建这么多文件，麻烦不说还容易出错，这里可以使用官方的脚手架工具来生成：

```bash
mkdir egg-demo
cd egg-demo
npm init egg --type=simple   # 应用简单egg应用程序骨架，注意这里不要用cnpm，行为不一致
npm install                  # 安装依赖
```

和前端的脚手架一样，这里的 `--type` 也是负责选定脚手架类型的，有几种脚手架初始骨架可选：

| 骨架类型  | 说明                  |
| :-------- | :-------------------- |
| simple    | 简单 egg 应用程序骨架 |
| empty     | 空的 egg 应用程序骨架 |
| plugin    | egg plugin 骨架       |
| framework | egg framework 骨架    |