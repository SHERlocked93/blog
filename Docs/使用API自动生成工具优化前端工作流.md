# 使用API自动生成工具优化前端工作流

在工作中，我们的前端工作流一般开始于前后端协商好Api文档之后，再针对这个Api文档做mock模拟数据，然后用做好的mock进行开发，后端开发完毕之后再改一下API数据的BaseURL切换到正式API进行联调；如下

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/2e92bbdef8316d80ed7c225061454285c8b37d6329a2cc864f47c23e1e1dbd9b.webp)

本文介绍的一个工具(或者说方法)，来将这个工作流优化一下，也是我平时工作正在用的方法，当做自己的笔记，也跟大家一起分享一下~

这个方法的主要思路就是开发人员在某个api工具中按要求填好文档，然后导出swagger.json配置文件，再把这个配置文件导入到easy-mock中，再用工具自动生成前端api的js文件以供调用。

本文中所使用的工具：[sosoApi](http://www.sosoapi.com/ "http://www.sosoapi.com/")、[Easy-mock](https://www.easy-mock.com/ "https://www.easy-mock.com/")、[Swagger](https://swagger.io/ "https://swagger.io/")、[Easy-mock-api-template](https://github.com/SHERlocked93/easy-mock-api-template "https://github.com/SHERlocked93/easy-mock-api-template")、[axios](https://github.com/axios/axios "https://github.com/axios/axios")

感兴趣的同学可以加文末的微信群，一起讨论吧～

## 1. 使用Api管理平台导出swagger.json文件

一般我们前后端通过各种平台或者工具来管理Api，比如免费的可视化Api管理平台 [sosoApi](http://www.sosoapi.com/ "http://www.sosoapi.com/")、[Yapi](http://yapi.demo.qunar.com/ "http://yapi.demo.qunar.com/")等，一般来说这些工具都可以生成`swagger.json`的Api，我们可以用它来直接生成一个漂亮的[可视化Api文档](http://petstore.swagger.io/#/api-docs "http://petstore.swagger.io/#/api-docs")，也可以用它来作为配置文件导入其他工具中，比如Easy-mock；

比如在sosoApi中就可以导出为swagger文档(`swagger.json`)：

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/a98029640b14b67226511bd1bd37c9b3847cb4b76c1f95d78611712ef9080ac6.webp)

我们先导出一个`swagger.json`备用；

## 2. 使用swagger.json导入easy-mock

Mock平台我们可以使用Easy-mock，轻量又简洁，虽然没有Api的分组功能，但平时应付应付不太大的应用、个人应用等场景足够了；Easy-mock官网的服务被不少人直接拿到开发环境用，经常被挤爆，这个情况可以用本地部署来解决这个问题，参考 [windows本地安装部署 Easy Mock](https://github.com/SHERlocked93/blog/blob/master/Docs/windows%E6%9C%AC%E5%9C%B0%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%20Easy%20Mock.md "https://github.com/SHERlocked93/blog/blob/master/Docs/windows%E6%9C%AC%E5%9C%B0%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%20Easy%20Mock.md") 。

我们将Api管理平台中导出的`swagger.json`文件在新建project的时候导入：

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/85dacae0140d98344bb26282b729331be48a4c6d8449c019c44405457a449db8.webp)

这样刚刚Api平台中配置的Api就被同步到我们的Easy-mock配置中了，比如sosoApi的示例[项目](http://www.sosoapi.com/auth/doc/inter/tree/list.htm?projId=1&docId=1 "http://www.sosoapi.com/auth/doc/inter/tree/list.htm?projId=1&docId=1")导出的结果就是：

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/d237548f79eb17432f89a5cb3950e38c800dcf884f1b6ea1bbb923aa29098fc0.webp)

这时我们就可以用它来进行数据mock了，怎么样，是不是很轻松~

easy-mock项目面板上面会有个 Project ID，这个记下来后面要用；

## 3. 使用easy-mock-cli生成js格式Api

有了easy-mock之后一般情况下我们要写前端的api文件了，一般api工具用axios，这里提供一个封装：

```js
// utils/fetch.js
import axios from 'axios'

const service = axios.create({
  baseURL: 'https://easy-mock.com/project/5bf6a23c92b5d9334494e884',
  timeout: 5000
})

// request拦截器
service.interceptors.request.use( config => {...},  err => {...})

// respone拦截器
service.interceptors.response.use( res => {...},  err => {...})

export default service
```

我们可以用[easy-mock-cli](https://easy-mock.github.io/easy-mock-cli/ "https://easy-mock.github.io/easy-mock-cli/")来生成api，模板文件如果不想用[原来的模板](https://github.com/easy-mock-templates/axios "https://github.com/easy-mock-templates/axios")的话，可以使用我fork之后改写的一个模板[easy-mock-api-template](https://github.com/SHERlocked93/easy-mock-api-template "https://github.com/SHERlocked93/easy-mock-api-template")，生成的Api文件是这样的：

```js
// api/index.js
import fetch from 'utils/fetch';

/* 活动查询 */
const activityQuery = ({ activityDate }) => fetch({
  method: 'get',
  url: '/activity/query',
  params: { activityDate }
});

/** 活动保存 */
const activitySave = () => fetch({
  method: 'post',
  url: '/activity/save'
});

/** 活动提交 */
const activitySubmit = ({ activityId, content }) => fetch({
  method: 'post',
  url: '/activity/submit',
  data: { activityId, content }
});

export {
  activityQuery,   // 活动查询
  activitySave,    // 活动保存
  activitySubmit   //  活动提交
};
```

然后在文件中就可以：

```js
import * as Api from 'api/index.js';

// 调用
Api.activitySubmit({ activityId: 2 })
    .then(...)
```

简单介绍一下配置文件，更复杂的配置要参考[原来的文档](https://github.com/easy-mock/easy-mock-cli/blob/master/docs/README.md "https://github.com/easy-mock/easy-mock-cli/blob/master/docs/README.md")；

```js
// .easy-mock.js 配置文件

{
  host: 'http://localhost:8080/',        // easy-mock的源，没有本地部署的话不用写，本地部署则填本地服务地址
  output: "../",                       // 生成 API 的基础目录
  template: "../",                       // 指定模板，这里用本地写的模板
  projects: [                           // 可以有多个模板来源
    {
      "id": "你要创建的 Easy Mock 项目的 id",    // 刚刚记下来的 Project ID
      "name": "api"                         // 生成的output目录下的文件名
    }
  ]
}
```

然后

```bash
npm run create-api
```

就可以在根目录下生成一个`api/index.js`文件了~

---

> 参考：
>
> 1. [用swagger.json自动生成axios api访问代码 - 简书](https://www.jianshu.com/p/b6577a0eb9fc "https://www.jianshu.com/p/b6577a0eb9fc")
> 2. [Easy-mock-cli/README.md](https://github.com/easy-mock/easy-mock-cli/blob/master/docs/README.md "https://github.com/easy-mock/easy-mock-cli/blob/master/docs/README.md")
>
> 推介阅读：
>
> 1. [windows本地安装部署 Easy Mock - 掘金](https://github.com/SHERlocked93/blog/blob/master/Docs/windows%E6%9C%AC%E5%9C%B0%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%20Easy%20Mock.md "https://github.com/SHERlocked93/blog/blob/master/Docs/windows%E6%9C%AC%E5%9C%B0%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%20Easy%20Mock.md")
