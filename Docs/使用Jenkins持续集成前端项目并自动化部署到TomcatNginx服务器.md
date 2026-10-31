# 使用Jenkins持续集成前端项目并自动化部署到Tomcat/Nginx服务器
上午折腾了一下Jenkins持续集成，由于公司使用自己搭建的svn服务器来进行代码管理，因此这里Jenkins是针对svn服务器来进行的配置，后面稍微介绍了下针对Github管理的项目的Jenkins配置

之前项目每次修改之后都需要本地`npm run build`一次手动发布到服务器上方便测试和产品查看，有了Jenkins持续集成之后只要svn或者git提交之后就会自动打包，很方便，此次记录以备后询。

声明：
1. 后面的项目地址与打包地址都是使用 `my-demo`，自行修改；
2. 另外还有路径等，根据自己情况自行修改；

## 1. 安装
### 1.1 安装 Nginx
可以直接去[官网](http://nginx.org/en/download.html)下直接下载，解压缩`start nginx`就可以使了，常用命令：

```bash
start nginx  # 启动
nginx -s reload  # 修改配置后重新加载生效
nginx -s reopen  # 重新打开日志文件
nginx -t  # 配置文件检测是否正确
```

### 1.2 安装**Jenkins**
从官网下载文件安装之后，我这里安装到 `C:\Jenkins`（Mac 不用在意），默认端口 8080，这时候浏览器访问 `localhost:8080` 就能访问 Jenkins 首页，这里注意如果不安装到 C 盘根目录[有些插件安装会出错](https://stackoverflow.com/questions/44403642/jenkins-plugin-installation-failing)
![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/0eb8b4765b22ea0d25fb85a904b2e93d4d48870e9e67155082ed88fb06e892c8.png)
这里会让你去某个地方找一个初始密码文件打开并填到下面的密码框里，验证成功之后进入页面，选择 `Install suggested plugins` 推介安装的插件
![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/4ca71524cd428e1a2bee81425742d2b760968ee5ed066020f5c0b426bad7baf7.png)
插件都安装完成之后进入用户登录界面，设定用户名、密码及邮箱。

然后提示 Jenkins is ready！ →   Start using Jenkins ~
![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/7747e9dfaeb609342c92d410e07cef5f650a711150b3d4a3c220c2ae7e335be9.png)

注意这里因为要使用node的命令来执行创建后操作，所以还需要安装插件：` NodeJS Plugin`、`Deploy to container`、`Github`、`Post build task`

这里顺便记录一下启动和关闭Jenkins服务的命令行：

```bash
net start jenkins            // 启动Jenkins服务
net stop jenkins             // 停止Jenkins服务
```

## 2. 创建svn项目的Jenkins任务
### 2.1 新建
左边栏新建一个任务，输入一个任务名称，这里随便写一个
![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/648f790641f19bca0137c859db203941464a2afad259cf4db5dda3a5fb8e4a34.png)

### 2.2 配置
#### General
这里才是重头戏，进入刚刚创建的任务的配置页面的 **General**

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/96e11230af0a84b31d3349b0d01db036376d4415b8333eb743fa4c12a7f05c81.png)

丢弃旧的构建就是检测到新的版本之后把旧版本的构建删除

#### 源码管理
这里采用的是svn来管理代码，
![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/2f1e437ca9ea5902e04d9ccfb330266968621b61c40c72c27459e80b9612f803.png)

#### 构建触发器
![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/ce341a474f41db35fec555059d443efda5f5891430fdbfded9654f3a1c4d9698.png)

这里的Poll SCM表示去检测是否更新构建的频率，`*****` 表示每分钟，`H****` 表示每小时

#### 构建

```bash
cd cd C:\Jenkins\workspace\my-demo
node -v
npm -v
cnpm i
npm run build
```

#### 构建后操作
安装插件 `Post build task` 后，可以在 增加构建后操作步骤中选择 `Post build task` 选项，增加构建后执行的script，具体也可以参考文章：jenkins部署maven项目构建后部署前执行shell脚本 - https://blog.csdn.net/minebk/article/details/73294785

我这里的 `Log text` 是 `Build complete`

Script：

```bash
rmdir /q/s C:\nginx-1.14.0\html\my-demo
xcopy /y/e/i C:\Jenkins\workspace\my-demo\my-demo C:\nginx-1.14.0\html\my-demo
```

复制生成好的文件到Nginx的目录下，路径自行修改

## 3. 创建Github项目的Jenkins任务
Jenkins 不仅可以持续集成 svn 项目，Git 项目也是可以的，这里以 Github 上的项目为例：

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/b29603c3f1868ecbd17ea7714ebe5602cfd2948a0e9f1aa8961f61626549fdfc.png)

其他配置和上面一章一样

这样如果 github 有新的 push 请求，都会自动化部署到之前的服务器上，可以说很方便了。

### 试一试
配置好了我们试一试，在刚刚 github 项目中随便 commit 一版到 github ：
![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/27c7dcd97f6b01abb1f62800775bce5484b94f68aaaaede8f8f76d8e53d5ddcc.png)

稍等片刻去本地 Jenkins 地址 `http://localhost:8080/job/vue-element-template/` 就能看到 Jenkins 已经在构建中了
![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/7a950d55cf09be6a5a992f07ace8334867e8baca343ba005a11e159019b509c2.png)
50秒之后：
![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/f33069413d9396e064ba5daf87e7472155c3d37c1b461ee4880a4fb8de7057b3.png)

构建成功！构建用时 54 秒，现在访问本地服务器地址 `http://localhost:8282/vue-element-template`，已经能看到编译后的发布版本啦~

如果你希望发布的是测试版本，可以自行修改构建后操作的 script

---

> 参考：

> 1. [使用Jenkins自动编译部署web应用](http://blog.csdn.net/gavid0124/article/details/53463831)
> 2. [Jenkins+github 前端自动化部署](https://segmentfault.com/a/1190000010200161)
> 3. [配置Jenkins邮件通知](https://zhuanlan.zhihu.com/p/22810691)
> 4. [jenkins部署maven项目构建后部署前执行shell脚本](https://blog.csdn.net/minebk/article/details/73294785)
