# windows本地安装部署 Easy Mock

在前后端分离的开发方式下，后端如果暂时没数据，前端为了开发方便可以使用模拟数据来对付一下，目前提供模拟数据的平台已经有不少，大多数都是自带Api管理的，比如[Yapi](http://yapi.demo.qunar.com/ "http://yapi.demo.qunar.com/")、[sosoApi](http://www.sosoapi.com/ "http://www.sosoapi.com/")、[eoLinker](https://www.eolinker.com/#/ "https://www.eolinker.com/#/")、[Easy-Mock](https://easy-mock.com/ "https://easy-mock.com/")甚至我们可以本地用[Mock.js](http://mockjs.com/ "http://mockjs.com/")自己写...

其中Easy-Mock比较小清新，使用起来也方便点，缺点就是没有Api的分组功能，但平时应付应付不太大的应用、个人应用等场景足够了；如果要进行分组权限管理之类的复杂功能，则推介使用目前正在快速更新的Yapi~ 当我们快乐的在官网使用Easy-Mock的时候，天有不测之风云：

1. 官网的被不少人直接拿到开发环境用，因此经常被挤爆；
2. 有些公司/研究所限制外网；

为什么网上已经有好多介绍部署Easy-Mock的文章还要发个呢，因为我用他们的文章部署的时候趟了好多坑...所以记一下方便以后自己翻阅

因此这里介绍一下如何本地去部署 Easy-Mock

感兴趣的同学可以加文末的微信群，一起讨论吧～

**⚠️ 注意：** easy-mock 本地部署不支持 node10及以上版本 [github.com/easy-mock/e…](https://github.com/easy-mock/easy-mock/blob/dev/README.zh-CN.md#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B "https://github.com/easy-mock/easy-mock/blob/dev/README.zh-CN.md#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B")

由于这个原因，在下现在已经改用 Yapi 了，参见 [<CentOS 安装部署 Yapi>](https://github.com/SHERlocked93/blog/blob/master/Docs/CentOS%207%20%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%20Yapi.md "https://github.com/SHERlocked93/blog/blob/master/Docs/CentOS%207%20%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2%20Yapi.md")

## 1. MongoDB、Redis安装

MongoDB版本`4.0.2`，Redis版本`3.2.100`

### 1.1 MongoDB安装

MongoDB的安装要注意，如果已经有了MongoDB服务了，需要`sc delete MongoDB`把服务卸载；

[官网下载](https://www.mongodb.com/download-center#community "https://www.mongodb.com/download-center#community")安装包安装之后一直下一步，我这里是安装到`D:\MongoDB`目录下，根据自己情况自行更改；

主要有下面几步：

1. 新建文件
   `D:\MongoDB`下面新建一个配置文件`mongo.conf`

   ```text
   dbpath=D:\MongoDB\data\db
   logpath=D:\MongoDB\log\mongo.log
   logappend=true
   journal=true
   quiet=true
   port=27017
   ```

   `D:\MongoDB\data`下面新建一个文件夹`db`

   `D:\MongoDB\log`下面新建一个文件`mongo.log`
2. 创建服务
   把可执行文件的`D:\MongoDB\bin`添加到系统变量里；

   管理员权限的cmd中注册服务：`mongod --config "D:\MongoDB\mongo.conf" --install --serviceName "MongoDB"`

   cmd中开启服务：`net start mongodb`

   这时候浏览器中访问`127.0.0.1:27017`应该就已经有内容了
3. 进入mongo环境

   如果之前安装无误的话，cmd中输入`mongo`应该就可以进入mongo的可执行环境了，这时输入`db`应显示`test`

   `mongo`运行环境下：`use easymockdb`

### 1.2 Redis安装

Redis类似，在[Github-release](https://github.com/MSOpenTech/redis/releases "https://github.com/MSOpenTech/redis/releases")下载一个msi版本安装，一直下一步；

1. 添加路径

   添加安装路径`D:\Redis`到系统变量里
2. 创建服务

   cmd下`redis-server redis.windows.conf`

   如果报`bind: No error`错，则cmd上**依次**执行

   ```text
   redis-cli.exe
   shutdown
   exit
   redis-server.exe redis.windows.conf
   ```

   这时候出来一个图就是正确安装了；

   cmd中注册服务：`redis-server --service-install redis.windows-service.conf --loglevel verbose`
3. 启动服务

   cmd下：`redis-server --service-start`

常用Redis命令：

- 卸载服务：`redis-server --service-uninstall`
- 开启服务：`redis-server --service-start`
- 停止服务：`redis-server --service-stop`

## 2 安装部署Easy-Mock

1. 首先要全局安装两个库

   ```text
   npm i -g cross-env pm2
   ```

2. 具体安装从git上clone下来并`install`、`build`，我这里是安装到`E:\Official Project\Easy-Mock`

   ```text
   git clone https://github.com/easy-mock/easy-mock.git
   cd easy-mock
   npm install
   npm run build
   ```

3. 配置在`config/default.json`中自行修改，注意其中有几个地方要改一下

   1. `db`改为`mongodb://localhost:27017/easymockdb`
   2. `redis->port`应该跟之前安装的redis配置的port一致，默认`6379`
4. 在项目目录下使用pm2守护运行：

   ```text
   cd "E:\Official Project\Easy-Mock"
   cross-env NODE_ENV=production pm2 start app.js
   ```

这时候访问本地的 `http://localhost:7300/` 就可以打开Easy-Mock页面了，跟Easy-Mock官网一样的~

---

> 参考：
>
> 1. [Redis在windows下安装过程](http://www.cnblogs.com/M-LittleBird/p/5902850.html "http://www.cnblogs.com/M-LittleBird/p/5902850.html")
> 2. [Easy-mock文档 - 如何本地部署](https://easy-mock.com/docs#ru-he-ben-di-bu-shu "https://easy-mock.com/docs#ru-he-ben-di-bu-shu")
> 3. [easy-mock 本地部署(挤需体验三番钟，里造会干我一样，爱象节款mock)](https://segmentfault.com/a/1190000016389301 "https://segmentfault.com/a/1190000016389301")
