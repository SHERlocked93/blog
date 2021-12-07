# CentOS 安装部署 Yapi

[TOC]

![2020-05-04-NV4YaqJ2eZY](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@env/uPic/2020-05-04-NV4YaqJ2eZY.jpg)

之前自己部署过 easy-mock，还专门整了篇博客 [<Windows 本地安装部署 Easy Mock>](https://juejin.im/post/5b9b6f79e51d450e6e039766)，但现在大搜车已经两年多没有对 easy-mock 进行有效 commit 了，最重要的是，easy-mock 对 NodeJs@10.x 及以上的版本[不支持](https://github.com/easy-mock/easy-mock/blob/dev/README.zh-CN.md#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)，这就比较坑了，所以我找了一下有没有其他的 Api 管理/Mock 平台 [YApi](https://hellosean1025.github.io/yapi/index.html)，准备以后转战 YApi 了，我把 YApi 部署到我自己的服务器上，以后就用它了。

CentOS 版本： `7.6`

Nginx 版本： `1.16.1`

Yapi 版本： `1.19.1`

MongoDB 版本： `4.2.6`

## 1. MongoDB 配置

### 1.1 配置 yum 并安装 MongoDB

MongoDB 和其他挺多直接用 yum 安装的软件不一样，它不能直接用 `yum install`，这种方式安装的 MongoDB 版本很低，需要先配置一下 yum：

```bash
# 创建 yum 配置文件
vim /etc/yum.repos.d/mongodb-org-4.2.repo

# 在文件中填入以下内容，然后 :wq 退出
[mongodb-org-4.2]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/4.2/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc

# 退出后就可以使用 yum 进行安装了
yum install -y mongodb-org
```

### 1.2 MongoBD 常用命令

```bash
systemctl start mongod.service        # 开启 MongoDB
systemctl enable mongod               # 开机自启
systemctl list-unit-files|grep mongod # 查看 MongoDB 是不是开机自启

service mongod restart          # 重启
service mongod stop             # 停止
service mongod start            # 运行

rpm -ql mongodb-org-server      # 查看 MongoDB 相关文件
```

### 1.3 MongoDB 配置

然后我们修改配置文件，让 MongoDB 在外部也可以访问

```bash
# 修改 MongoDB 配置文件
vim /etc/mongod.conf

# 找到这里，修改后 :wq
net:
  port: 27017
  bindIp: 0.0.0.0    # 原来是 127.0.0.1，只允许本地连接，改成 0.0.0.0 允许外部连接，如果只需要本地连接就不用改
  
security:            # 为了安全，启用身份验证
  authorization: "enabled"   # disable or enabled

  
# 保存后重启服务
service mongod restart
```

修改完配置之后，在网页上访问 `<你的服务器地址>:27017` 就可以访问到了，如果不修改 `bindIp` 的话，就只可以进行本地连接。

如果你 `mongod` 访问的时候抱如下的情况：

![image-20200503152859106](https://i.loli.net/2020/05/03/7rkX8OQVWlDmUF6.png)

那你需要新建一个 `/data/db` 数据目录 `mkdir /data/db` ，然后再访问就可以了。

### 1.4 卸载 MongoDB

这里保留一下卸载的方法，以后可能换其他方式安装 MongoDB：

```bash
systemctl disable mongod # 停止开机自启
service mongod stop      # 停止服务
sudo yum erase $(rpm -qa | grep mongodb-org)   # 删除安装包

sudo rm -r /var/log/mongodb     # 删除日志文件
sudo rm -r /var/lib/mongo       # 删除数据文件
```

## 2. Yapi 安装部署

### 2.1 本地部署

首先安装官方提供的 `yapi-cli` 工具，顺带安上 `pm2` 回头启服务的时候可以用来守护和管理进程：

```bash
npm install -g yapi-cli pm2 --registry https://registry.npm.taobao.org
yapi server
```

然后进行可视化配置，我是下面这样配置的：

![image-20200503152036407](https://i.loli.net/2020/05/03/FHlWRk7Osfcu1vZ.png)

点击「开始部署」，就开始 Yapi 部署的过程了，经过两三分钟的等待，看到最后几行提示了管理员账户名和密码，记下来后面有用

![image-20200503154305831](https://i.loli.net/2020/05/03/6Otpml82vSzRB9X.png)

然后

```bash
cd  <部署路径>               # 刚刚的配置是 /usr/share/my-Yapi
node vendors/server/app.js  # 跑起来

# 推介用 pm2 跑，这里给 yapi 赋一个引用名称，以后操作方便，并设置当超过 200MB 内存上限后自动重启
pm2 start /usr/share/my-yapi/vendors/server/app.js -n yapi --max-memory-restart 500M
pm2 stop yapi        # pm2 停止
pm2 list             # pm2 查看运行状态
```

此时可以看到 pm2 运行的脚本状态：

![image-20200503171421872](https://i.loli.net/2020/05/03/iXegnVIOoRb5xrZ.png)

现在到浏览器访问 `<你服务器ip>:9001` （注意这里的端口是你刚刚自己设置的端口号）就可以访问到 Yapi 的服务目录了，目录看起来跟官网比较类似

![image-20200503161917956](https://i.loli.net/2020/05/03/lqSedHtMGQ12vyF.png)

这样就完成了本地的部署了～ 👏

注册一个新账号，登录后就可以正常使用了。

### 2.2 安装 cross-request 插件

安装上 Yapi 之后，还需要在浏览器安装一个 cross-request 插件，来进行页面跨域请求。

首先我们去 `https://github.com/YMFE/cross-request` 仓库，下载 `zip` 包并解压缩。

![image-20200503164553266](https://i.loli.net/2020/05/03/BegahfsxNEWp8kC.png)

然后在 Chrome 右上角三个点的菜单中选择 `更多工具 -> 扩展程序 -> 加载以解压的扩展程序 -> 选中压缩包内容`，记得先把右上角 `开发者模式` 打开。

![image-20200503164926925](https://i.loli.net/2020/05/03/qndXjyY9bxlA5c2.png)

然后查看 `接口 -> 运行` 就可以发送命令了～

⚠️ **注意：** 安装完之后，解压缩的插件文件夹不能删除！！！

后面的使用，可以参考官方文档： [YApi\-教程](https://hellosean1025.github.io/yapi/documents/index.html)

但要提一句的是，我在将 swagger2.0 的接口文档导入 Yapi 的时候，发现出现了一点问题 😅，这里给 Yapi 的仓库提了 [<导入swagger2\.0版本的配置文件后接口的编辑按钮点击进入空白页 · Issue \#1739>](https://github.com/YMFE/yapi/issues/1739) 这样一个 issue，希望官方早点解决呀～

---
网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出~


> 参考文档：
>
> 1. [Install MongoDB Community Edition on Red Hat or CentOS — MongoDB Manual](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat/)
> 2. [Linux Centos 7安装MongoDB（简单！详细！）](https://juejin.im/post/5cbe73f86fb9a0320b40d687)


PS：本人博客地址 [Github - SHERlocked93/blog](https://github.com/SHERlocked93/blog)，也欢迎大家关注我的公众号【前端下午茶】，一起加油吧~

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@env/uPic/2020-05-01-2020-03-04-5cf08a479cd5d75372-20200304131909230.jpg)

另外可以加入「前端下午茶交流群」微信群，长按识别下面二维码即可加我好友，备注**加群**，我拉你入群～

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@env/uPic/2020-03-04-5d2986f77e9bc11533-20200304131910068.jpg)