# MySQL 从入门到实践，万字详解！



[TOC]

数据库是往全栈发展不得不跨过的一道坎，大家不可避免会学到用到相关知识，最近查资料的时候发现网上很多内容要么就特别深，要么不成体系，对一些希望浅尝辄止仅仅是使用一下的人不太友好。最近刚好有机会学到 MySQL，集中一些时间学习了一下同时做了一些笔记，每个概念基本都有代码示例，每一行都是在下手打，读者可以直接复制了代码到命令行中运行，希望对大家有所帮助～  😜

本文介绍的知识都不是特别深，目标用户是对 MySQL 零基础或弱基础的小伙伴们，可以帮助建立一些概念，至少碰到相关问题知道怎么去百度，也不会碰到后端给的数据库文件看不懂。

对于 Docker 和 CentOS 相关知识不了解的小伙伴可以看看 [<手摸手带你 Docker 从入门到实践>](https://juejin.cn/post/6875323565479034894) 和 [<半小时搞会 CentOS 入门必备基础知识>](https://juejin.cn/post/6844904080972709901) 两篇文章，反正 Docker 和 CentOS 也早晚会用到 😂

所有代码保存在 [Github](https://github.com/SHERlocked93/FE_Daily/tree/20210906/20210830_mysql) 上，可以自行 Clone 下来阅读和执行。

CentOS 版本： `7.6`

MySQL 版本：`8.0.21`

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/upic/MySQL-20210906-in6J0O.png)

上面这个脑图可以加文末公众号回复 「mysql脑图」 获取 xmind 源文件。

## 1. 什么是数据库

数据库是一个以某种有组织的方式存储的数据集合，可以将其想象为一个文件柜。

### 1.1 基本信息

 MySQL 数据库隶属于MySQL AB公司，总部位于瑞典，后被 oracle 收购。是目前最流行的关系型数据库。

优点：

1. 成本低：开放源代码，一般可以免费试用；
2. 性能高：执行很快；
3. 简单：很容易安装和使用。

### 1.2 MySQL 安装

MySQL 建议使用 Docker 安装，几行命令就安装好了，参见 [<手摸手带你 Docker 从入门到实践> - 安装 MySQL](https://juejin.cn/post/6875323565479034894#heading-18)

我这里的命令是：

```bash
# 创建mysql容器
docker run -d -p 3307:3306 -e MYSQL_ROOT_PASSWORD=888888 \
-v /Users/sherlocked93/Personal/configs/mysql.d:/etc/mysql/conf.d \
-v /Users/sherlocked93/Personal/configs/data:/var/lib/mysql \
--name localhost-mysql mysql

# 创建好之后进入 mysql 容器：
docker exec -it localhost-mysql bash

# 登录 mysql
mysql -u root -p888888
```

如果你机子上安装了 navicate，可以参考一下下面这个配置

![选择 New Connection](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/image-20210830164756294-16-47-56.png)

选择 New Connection 之后填一下配置：

![navicat配置](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/image-20210830164651195-16-46-51.png)

就可以看到你数据库里面的内容了。

就可以啦，效果如下图：

![image-20210830202717904](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/image-20210830202717904-20-27-18.png)

不用 Docker 可以去官网 [MySQL Community Server](https://dev.mysql.com/downloads/mysql/) 下载对应版本的 MySQL 安装包，Community Server 社区版本是不要钱的，下载安装完毕也可以，基本一直下一步就行了。

废话少说，下面直接开始知识灌体！


## 2. MySQL  简单使用

### 2.1 数据库相关术语

数据库相关的概念和术语：

1. **数据库**(database) 保存有组织的数据的容器；
2. **表**(table) 某种特定类型数据的结构化清单；
3. **模式**(schema) 关于数据库和表的布局及特性的信息；
4. **列**(column) 表中的一个字段，所有表都是由一个或多个列组成的；
5. **数据类型**(datatype) 所容许的数据的类型；
6. **行**(row) 表中的一个记录；
7. **主键**(primary key) 一列(或一组列)，其值能够唯一区分表中每个行；
8. **外键**(foreign key) 表中的一列，它包含另一个表的主键值，定义了两个表之间的关系。
9. **子句**(clause) SQL 语句由子句构成，有些子句是必需的，而有的是可选的。比如 select 语句的 from 子句。

### 2.2 主键

主键的概念十分重要，它唯一标识表中每行的单个或者多个列称为主键。主键用来表示一个特定的行。

虽然并不总是都需要主键，但应尽量**保证每个表都定义有主键**，以便于以后的数据操纵和管理。没有主键，无法将不同的行区分开来，更新或删除表中特定行很困难。

表中的任何列都可以作为主键，只要它满足以下条件：

1. 任意两行都不具有相同的主键值；
2.  每个行都必须具有一个主键值（主键列不允许 NULL 值）。

在使用多列作为主键时，上述条件必须应用到构成主键的所有列，所有列值的组合必须是唯一的（单个列的值可以不唯一)。

几个普遍认可的最好习惯为：

1. 不更新主键列中的值；
2. 不重用主键列的值；
3. 不在主键列中使用可能会更改的值。


### 2.3 语法规范

语法规范：

1. 输入 `help` 或 `\h` 获取帮助；
2. 不区分大小写，但建议关键字大写，表名、列名小写；
3. 每条命令最好使用分号 `;` 或 `\g` 结尾，仅按 Enter 不执行命令；
4. 每条命令根据需要，可以进行缩进、换行；
5. 用 `#` 开头进行多行注释，用 `/* ... */` 进行多行注释；
6. 输入 `quit` 或 `exit` 推出 MySQL 命令行；

语法特点：

1. 大小写不敏感；
2. 可以写在一行或多行，可以分成多行以便于阅读和调试；
3. 关键字不能被缩写也不能分行；
4. 各子句一般分行写；
5. 推介使用缩进提高语句的可读性；

常见的简单命令：

```mysql
mysql -u root -p      # –h 主机名 –u 用户名 -P 端口号 –p密码，注意-p跟密码之间不能加空格其他可以加可以不加
select version();     # 查看 mysql 服务版本
show databases;       # 查看所有数据库，注意最后有 s

create database [库名]; # 创建库
use [库名];             # 打开指定的库

show tables;           # 查看当前库的所有表        
show tables from [库名];   # 查看其他库的所有表               
desc [表名];               # 查看表结构   

create table [表名] (      # 创建表            
	列名 列类型,
	列名 列类型,
);

drop database [库名];     # 删除库  
drop table [表名];        # 删除表   

exit;                    # 退出
```

### 2.4 创建表并填充数据

首先我们整点数据，方便后面的代码演示。

```bash
mysql -u root -p888888     # 输入用户名密码，进入mysql命令行
```

然后在 Github [下载文件 create.sql](https://github.com/SHERlocked93/FE_Daily/blob/20210906/20210830_mysql/mysql_scripts/create.sql) 并运行（也可以直接复制文件里的内容到 MySQL 命令行中执行）。

如果你用的是 navicate，在上一章创建到 localhost-mysql 的连接后，运行一下即可：

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/image-20210830213034657-21-30-35.png)

同理运行另一个文件 [populate.sql](https://github.com/SHERlocked93/FE_Daily/blob/20210906/20210830_mysql/mysql_scripts/populate.sql)，填充每个表中的数据。

运行之后在命令行中 `show tables` 就可以看到库中的表了，如下图：

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/image-20210830215111896-21-51-12.png)

### 2.5 关系表

简单介绍一下刚刚创建好的表。

为了数据分类处理，顾客 customers、供应商 vendors、订单 orders、订单信息 orderitems、产品记录 productnotes、产品 products 表分别存储不同的信息。

比如供应商信息表 vendors 总每个供应商都有一个唯一标识，也就是**主键** vend_id，而 products 产品表的每个产品也有一个主键 prod_id，还有一个字段 vend_id 供应商 ID 和供应商表中的 vend_id 一一对应，这就是**外键**。

如果你希望通过产品 ID 查到对应的供应商信息，那么就通过外键来找到另一个表中的信息。外键避免了每个产品都重复保存供应商的详细信息，只要保存供应商的 ID 就行，当供应商信息变了，比如邮箱、地址变更，也不用挨个改每一行的数据，只需更改供应商表中对应供应商信息。

这样做的好处：

1. 供应商信息不重复，从而不浪费时间和空间；
2. 如果供应商信息变动，可以只更新 vendors 表中的单个记录，相关表中的数据不用改动；
3. 由于数据无重复，显然数据是一致的，这使得处理数据更简单。

**可伸缩性**(scale)，能够适应不断增加的工作量而不失败。设计良好的数据库或应用程序称之为可伸缩性好(scale well)。

### 2.6 数据类型

MySQL 数据类型定义了列中可以存储什么数据以及该数据怎样存储的规则。

#### 数值型

整型：`Tinyint`、`Smallint`、`Mediumint`、`Int`（`Integer`）、`Bigint`，可以为无符号和有符号，默认有符号。

1. 如果不设置有无符号默认是有符号，如果想设置无符号，可以添加 `unsigned` 关键字；
2. 如果插入的数值超出了整型的范围，会报 out of range 异常，并且插入临界值；
3. 如果不设置长度，会有默认的长度。

小数
1. 定点数：`dec(M，D)`、`decimal(M，D)`
2. 浮点数：`float(M, D)`、`double(M, D)`


M 为整数部位+小数部位，D 为小数部位，M 和 D 都可以省略。如果是 `decimal`，则 M 默认为 10，D 默认为 0。

#### 字符型

1. 较短的文本：`char(n)`、`varchar(n)` 中的 n 代表字符的个数，不代表字节个数。
2. 较长的文本：`text`（长文本数据）、`blob`（较长的二进制数据）。
3. `binary`、`varbinary` 用于保存较短的二进制。
4. `enum` 用于保存枚举。
5. `set` 用于保存集合。

#### 日期和时间类型

1. `date` 格式 YYYY-MM-DD，保存日期；
2. `time` 格式 HH:MM:SS，保存时间；
3. `year` 格式 YYYY，保存年；
4. `datetime` 格式 YYYY-MM-DD HH:MM:SS，保存日期+时间，范围 `1000-9999`，不受时区印象；
5. `timestamp` 时间戳，格式保存日期+时间，范围 `1970-2038`，受时区影响；

## 3. 检索数据 select

用来查询的 `select` 语句大概是最常用的了，用来从一个或多个表中检索信息，一条 `select` 语句必须至少给出两条信息：想选择什么、从什么地方选择。

```mysql
# 基本语法
select [查询列表] from [表名];

# 查询单个/多个/所有字段
select cust_name from customers;
select cust_name,cust_city,cust_address from customers;
select `select` from customers;               # 如果某字段是关键字，可以用 ` 符号包起来
select * from customers;                      # * 表示所有                

# 查询常量值/表达式/函数
select 100;
select 'zhangsan';
select 100%98;
select version();
```

![](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/image-20210831105804099-11-09-53.png)

### 3.1 去重 distinct

查询出来的结果可能有多个重复值，可以使用 `distinct` 关键字来去重

```mysql
select order_num from orderitems;           # 有一些重复值
select distinct order_num from orderitems;  # 将重复值去重
```

### 3.2 限制结果 limit

select 语句返回所有匹配的行，它们可能是指定表中的每个行。为了返回第一行或前几行，可使用 `limit` 子句。

`limit m` 表示返回找出的前 m 行，`limit m,n` 表示返回第 m 行开始的 n 行，也可以使用 `limit m offset n` 含义和前面一样。

注意，检索出来的第一行的索引为 0 行。

![image-20210831110913412](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/image-20210831110913412-11-09-40.png)

### 3.3 完全限定表名与列名

在某些情况下，语句可能使用完全限定的列明与表名：

```mysql
select orderitems.order_num from mysql_demo1.orderitems;
# 上面这句等价于
select order_num from orderitems;
```


## 4. 排序检索数据 order by

上一章从 `orderitems` 这个表中检索的数据是没有排序的，一般情况下返回的顺序是在底层表中出现的顺序。可以通过 `order by` 子句来对检索后的数据进行排序。

可以用 `asc`、`desc` 关键字来指定排序方向。`order by asc` 升序、`order by desc` 降序，不写默认是升序。

`order by` 子句中可以支持单个字段、多个字段、表达式、函数、别名，一般放在句子的最后面，除了 `limit` 之外。

```mysql
select * from orderitems order by item_price;           # 按item_price升序排列

# 先按 quantity 升序排列，quantity 的值一样时按 item_price 的值升序排列
select * from orderitems order by quantity,item_price;  

# 先按 quantity 降序排列，quantity 的值一样时按 item_price 的值升序排列
select * from orderitems order by quantity desc,item_price;  

# 找到最贵订单
select * from orderitems order by item_price desc limit 1;
```

## 5. 过滤数据 where

在 `from` 子句后使用 `where` 关键字可以增加筛选条件，过滤数据。

```mysql
# 基本语法
select [查询列表] from [表名] where [筛选条件] order by [排序条件];
```

按条件表达式来筛选 `>`、`=`、`<`、`>=`、`<=`、`!=`、`<>`、`<=>`

```mysql
# 找出产品价格为 2.5 的产品名字
select prod_name, prod_price from products where prod_price=2.5;

# 找出产品价格小于等于 10 的产品名字，并按产品价格降序排列
select prod_name, prod_price from products where prod_price <= 10 order by prod_price desc;

# 找到供应商 id 不为 1003 的产品，!= 和 <> 含义一样，都是不等于
select vend_id, prod_name from products where vend_id <> 1003;
```

### 5.1 范围检查 between and

使用 `between ... and ...` 指定所需范围的开始值和结束值，可以达到范围查询的效果。

注意 `between and` 左右数字是按小大的顺序的，调过来不行。

```mysql
# 查询产品价格在 3 到 10 内的产品
select prod_name, prod_price from products where prod_price between 3 and 10;

# 单独使用 and 也可以打到这个效果
select prod_name, prod_price from products where prod_price <= 10 and prod_price >= 3;
```

### 5.2 空值检查 is (not) null

创建表时，可以指定某些列可以不包含值，即可以为 `null`，`null` 表示无值 no value，这与字段包含 0、空字符串或仅仅包含空格不同。

使用 `is null` 或 `is not null` 可以用来判断一个值是否为 `null`。

说明：

1. 等于 `=` 和不等于 `<>`、`!=` 不能用来判断 `null`，只能用 `is null` 和 `is not null` 来判断 `null`
2. `<=>` 安全等于号可以用来判断 `null`

```mysql
# 找出顾客中邮箱不是 null 的顾客信息
select * from customers where cust_email is not null;

# 使用安全等于号来判断 null 也是可以的
select * from customers where cust_email <=> null;
```

### 5.3 逻辑与操作符 and

**操作符**(operator) 用来联结或改变 where 子句中的子句的关键字，也称为**逻辑操作符**(logical operator)。

前文提到了 `and` 操作符，通过这个操作符可以增加限定条件：

```mysql
# 找出供应商为 1003 提供的价格小于等于 10 的产品
select * from products where vend_id = 1003 and prod_price <= 10;
```

### 5.4 逻辑或操作符 or

`or` 操作符和 `and` 操作符相反，这是逻辑或操作符，返回匹配任一条件的行：

```mysql
# 找出id为 1003 或 1001 的供应商
select * from products where vend_id = 1003 or vend_id = 1001;
```

在 `and` 和 `or` 同时出现时，会优先处理 `and`，比如这句：

```mysql
select * from products where vend_id = 1001 or vend_id = 1003 and prod_price >= 10;
```

这句会先处理 `and`，表示 `vend_id` 为 1003 且 `prod_price` 大于等于 10 的产品，或者 `vend_id` 为 1001 的产品。

遇到这种情况，可以通过增加圆括号：

```mysql
select * from products where (vend_id = 1001 or vend_id = 1003) and prod_price >= 10;
```

这样检索的结果就是 `vend_id` 为 1001 或 1003 的产品里，所有 `prod_price` 大于等于 10 的产品列表了。

任何时候使用具有 `and` 和 `or` 操作符的 `where` 子句，都应该使用圆括号明确地分组操作符。不要过分依赖默认计算次序，即使它确实是你想要的东西也是如此，而且使用圆括号能消除歧义，增加可读性。

### 5.5 范围操作符 in (set)

使用 `in` 操作符可以指定条件范围，范围中的每个条件都可以进行匹配。`in` 要匹配的值放在其后的圆括号中：

```mysql
# 找出id为 1003 或 1001 的供应商
select * from products where vend_id in (1001, 1003);
```

`in` 操作符可以用 `or` 来取代，在以下情况建议使用 `in` ：

1. 在选项比较多时，`in` 更清楚且更直观；
2. 使用 `in` 时，计算的次序更容易管理（因为使用的操作符更少）；
3. `in` 一般比 `or` 操作符清单执行更快；
4. `in` 的最大优点是可以包含其他 `select` 语句，使得能够更动态地建立 `where` 子句。

### 5.6 逻辑否操作符 not

`not` 否操作符可以和前面的 `in` 和 `between and` 一起使用，表示对范围取反：

```mysql
# 找出id不为 1001 1003 的产品
select * from products where vend_id not in (1001, 1003);

# 选择产品价格不在 5 到 15 之间的产品
select * from products where prod_price not between 5 and 15;
```

### 5.7 like 操作符

比如想找出名称中包含 `anvil` 的所有产品，可以通过 `like` 操作符来进行搜索。`like` 表示后面跟的搜索模式使用通配符匹配而不是直接相等匹配。

#### 操作符 %

最常使用的通配符是 `%` 操作符，`%` 表示任意多个字符，包括没有字符。

```mysql
# 找出产品名字以 jet 开头的产品
select * from products where prod_name like 'jet%';

# 找出产品名中含有 on 的产品
select * from products where prod_name like '%on%';

# 找出产品名以 s 开头，以 e 结束的产品
select * from products where prod_name like 's%e';
```

注意，`%` 是无法匹配 `null` 的。

#### 操作符 _

`_` 表示任意单个字符。

```mysql
select * from products where prod_name like '_ ton anvil';
```

另外，转译使用 `\`，比如 `\_`

```mysql
# 找到描述中有 % 的产品
select * from products where prod_desc like '%\%%';
```

注意：

1. 不要过度使用通配符。如果其他操作符能达到相同的目的，应该使用其他操作符。
2. 在确实需要使用通配符时，除非绝对有必要，否则不要把它们用在搜索模式的开始处。把通配符置于搜索模式的开始处，搜索起来是最慢的。

### 5.8 正则表达式 regexp

关于正则表达式，可以先简单看一下 [「正则表达式必知必会」](https://juejin.cn/post/6844903650054111245) 这篇博客。

使用 `regexp` 关键字来表示匹配其后的正则表达式：

```mysql
# 找到产品名以 1000 或 anvil 结尾的产品
select * from products where prod_name regexp '1000|anvil$';
```

正则表达式中转译使用 `\\`，比如希望查找 `.` 这个字符而不是正则中的 `.` 通配符，使用 `\\.`，为了转移 `\` 这个字符，使用 `\\\`

```mysql
# 找到产品名以 . 字符开头的产品
select * from products where prod_name regexp '^\\.';
```

## 6. 计算字段

有时候我们需要直接从数据库中检索出转换、计算或格式化过的数据，而不是检索出数据，然后再在客户机应用程序或报告程序中重新格式化，这时我们就需要计算字段了。

### 6.1 别名 as

查询出来的虚拟表格可以起一个别名，方便理解，可读性好，另外如果查询的字段有重名的情况，可以使用别名 `as` 来区分开来。

```mysql
# 使用 as 关键字
select cust_name as name from customers;

# as 关键字也可以直接省略
select cust_name name from customers;

# 可以给不同字段分别起别名
select cust_name name, cust_city location from customers;
```

### 6.2 拼接 concat

想把多个字段连接成一个字段，可以使用到拼接字段函数 `concat`：

```mysql
# 将供应商的名字和地点拼接好后返回，并命名为 vend
select concat(vend_name, '(', vend_country, ')') vend from vendors;
```

注意中间如果有任何一个数据为 `null`，拼接的结果也是 `null`。

所以对某些可能为 `null` 的字段要使用 `ifnull` 函数判断一下，第一个参数为要判断的字段，第二个参数是如果是 `null` 希望返回的结果：

```mysql
# 将顾客信息拼接起来
select concat(cust_name, '(', ifnull(cust_email, '-'), ')') customerInfo from customers;
```

如果表中的数据前后有空格，可以使用 `rtrim()` 函数去除右边空格，`ltrim()` 去除左边空格，或者 `trim()` 去除前后空格：

```mysql
# 将顾客信息处理后拼接起来
select concat(rtrim(vend_name), '(', trim(vend_country), ')') vend from vendors;
```

### 6.3 算术计算 +-*/

基本的算术运算符在 `select` 语句中也是支持的：

```mysql
# 计算订单每种总额，并按照总金额降序排列
select prod_id as id, quantity, quantity*item_price as totalPrice 
from orderitems order by totalPrice desc;
```

基本运算符加减乘除都是支持的 `+`、 `-`、 `*`、 `/` 。

## 7. 数据处理函数

前面介绍的去除数据首位空格的 `trim()` 函数就是数据处理函数，除此之外还有多种其他类型的数据处理函数：

1. 用于处理文本串的文本函数，如删除或填充值，转换值为大写或小写。
2. 用于在数值数据上进行算术操作的数值函数，如返回绝对值，进行代数运算。
3. 用于处理日期和时间值并从这些值中提取特定成分的日期和时间函数，例如，返回两个日期之差，检查日期有效性等。
4. 系统函数，如返回用户登录信息，检查版本细节。

在不了解如何使用一个函数的时候，可以使用 `help` 命令，比如 `help substr` 就可以获取 `substr` 的使用方式和示例。

### 7.1 字符函数

| 函数                           | 说明                                            |
| ------------------------------ | ----------------------------------------------- |
| `left()`、`right()`            | 返回串左边、右边的字符                          |
| `length()`                     | 返回串长度                                      |
| `lower()`、`upper()`           | 返回串的小写、大写                              |
| `rtrim()`、`ltrim()`、`trim()` | 去除右边、左边、两边的空格                      |
| `locate()`                     | 找出一个串的子串                                |
| `soundex()`                    | 返回串的 sundex 值                              |
| `substring()`                  | 返回子串的字符                                  |
| `subset()`                     | 返回子串的字符（和 `substring` 使用方式不一样） |
| `instr()`                      | 返回子串第一次出现的索引，没有返回 0            |
| `replace()`                    | 字符串替换                                      |
| `lpad()`、`rpad()`             | 左填充、右填充                                  |

示例：

```mysql
# upper、lower 将姓变大写，名变小写，然后拼接
select concat(upper(last_name), lower(first_name)) 姓名 from employees;

# 姓名中首字符大写，其他字符小写然后用_拼接，显示出来
select concat(upper(substr(last_name, 1, 1)), '_', lower(substr(last_name, 2))) from employees;

# substr 截取字符串，sql 中索引从 1 开始而不是0
select substr('hello world', 3);      # llo world
select substr('hello world', 2, 3);   # ell

# instr 返回子串第一次出现的索引，没找到返回 0
select instr('abcdefg', 'cd');        # 3

# trim 减去字符串首尾的空格或指定字符
select trim('   hello    ');              # hello
select trim('aa' from 'aaabaabaaaaaa');   # abaab

# lpad 用指定的字符实现左填充指定长度
select lpad('he', 5, '-');   # ---he

# rpad 用指定的字符实现左填充指定长度
select rpad('he', 5, '-*');   # he-*-

# replace 替换
select replace('abcabcabc', 'bc', '--');   # a--a--a--
```

### 7.2 数学函数

| 函数         | 说明           |
| ------------ | -------------- |
| `round()`    | 四舍五入       |
| `ceil()`     | 向上取整       |
| `floor()`    | 向下取整       |
| `truncate()` | 保留几位小数   |
| `mod()`      | 取余           |
| `abs()`      | 返回绝对值     |
| `rand()`     | 返回一个随机数 |

示例：

```mysql
# round 四舍五入，第二个参数是小数点后保留的位数
select round(-1.55);      # -2
select round(1.446, 2);   # 1.45

# ceil 向上取整
select ceil(1.001);   # 2
select ceil(1.000);   # 1
select ceil(-1.001);  # -1

# floor 向下取整
select floor(1.001);   # 1
select floor(1.000);   # 1
select floor(-1.001);  # -2

# truncate 小数点后截断几位
select truncate(1.297, 1);  # 1.2
select truncate(1.297, 2);  # 1.29

# mod 取余和%同理，符号与被除数一样
select mod(10, -3);  # 1
select mod(-10, -3); # -1
select mod(-10, 3);  # -1
select 10%3;         # 1
```

### 7.3 日期函数

| 函数                                                         | 说明                                         |
| ------------------------------------------------------------ | -------------------------------------------- |
| `now()`                                                      | 返回当前系统日期和时间                       |
| `curate()`、`current_date`                                   | 返回当前系统日期，不包括时间                 |
| `curtime()`、`current_time`                                  | 返回当前时间，不包括日期                     |
| `year()`、`month()`、`day()`、`hour()`、`minute()`、`second()` | 获取时间指定部分，年、月、日、小时、分钟、秒 |
| `str_todate()`                                               | 将日期格式的字符转换成指定格式的日期         |
| `date_format()`                                              | 将日期转换为指定格式字符                     |

示例：

```mysql
# now 返回当前系统日期和时间
select now();    # 2020-07-08 12:29:56

# curdate,current_date 返回当前系统日期，不包括时间
select curdate();  # 2020-07-08

# curtime,current_time 返回当前时间，不包括日期
select curtime();  # 12:29:56

# year... 获取时间指定部分，年、月、日、小时、分钟、秒
select year(now());      # 2020
select month(now());     # 7
select monthname(now()); # July
select day(now());       # 8
select dayname(now());   # Wednesday
select hour(now());      # 12
select minute(now());    # 29
select second(now());    # 56
select month(order_date) from orders;

# str_to_date 将日期格式的字符转换成指定格式的日期
select str_to_date('1-9-2021', '%d-%c-%Y');    # 2020-09-01
select * from orders where order_date = str_to_date('2005-09-01', '%Y-%m-%d');

# date_format 将日期转换成指定格式的字符
select date_format(now(), '%Y年%m月%d日');   # 2020年09月01日
select order_num orderId,date_format(order_date, '%Y/%m') orderMonth from orders;
```

日期格式符：

| 格式符 | 功能              |
| ------ | ----------------- |
| `%Y`   | 四位年份          |
| `%y`   | 两位年份          |
| `%m`   | 月份(01,02,...12) |
| `%c`   | 月份(1,2,...12)   |
| `%d`   | 日(01,02,...)     |
| `%e`   | 日(1,2,...)       |
| `%H`   | 小时(24小时制)    |
| `%h`   | 小时(12小时制)    |
| `%i`   | 分钟(00,01,...59) |
| `%s`   | 秒(00,01,...59)   |

### 7.4 聚集函数

**聚集函数**(aggregate function) 运行在行组上，计算和返回单个值的函数。

| 函数             | 说明                                   |
| ---------------- | -------------------------------------- |
| `avg()`          | 返回某列的平均值                       |
| `count()`        | 返回某列的行数                         |
| `max()`、`min()` | 返回某列最大值、最小值（忽略 null 值） |
| `sum()`          | 返回某列之和（忽略 null 值）           |

示例：

```mysql
# 计算产品价格平均值
select avg(prod_price) as avgPrice from products;

# 计算供应商id为 1003 提供的产品的平均价格
select avg(prod_price) as avgPrice from products where vend_id = 1003;

# 计算价格最大的产品价格
select max(prod_price) as maxPrice from products;

# 计算顾客总数
select count(*) from customers;

# 计算具有 email 的顾客数
select count(cust_email) from cutomers;

# 计算产品价格总和
select sum(prod_price) from products;

# 计算订单为 20005 的订单总额 
select sum(item_price * quantity) totalPrice from orderitems where order_num = 20005;

# 计算产品具有的不同的价格的平均数
select avg(distinct prod_price) avgPrice from products where vend_id = 1003;

# 同时计算产品总数、价格最小值、最大值、平均数
select count(*) prodNums, min(prod_price) priceMin, max(prod_price) priceMax, avg(prod_price) priceAvg from products;
```

## 8. 分组数据

之前的聚集函数都是在 `where` 子句查询到的所有数据基础上进行的计算，比如查询某个供应商的产品平均价格，但假如希望分别返回每个供应商提供的产品的平均价格，该怎么处理呢。这该用到分组了，分组允许把数据分为多个逻辑组，以便能对每个组进行聚集计算。

### 8.1 创建分组 group by

使用 `group by` 子句可以指示 MySQL 按某个数据排序并分组数据，然后对每个组而不是整个结果集进行聚集。

```mysql
# 分别查询每个供应商提供的产品种类数
select vend_id, count(*) num_prods from products group by vend_id;

# 查询每个供应商提供的产品的平均价格
select vend_id, avg(prod_price) avg_price from products group by vend_id;
```

注意：

1. `group by` 子句可以包含任意数目的列。这使得能对分组进行嵌套，为数据分组提供更细致的控制。
2. 如果在 `group by` 子句中嵌套了分组，数据将在最后规定的分组上进行汇总。换句话说，在建立分组时，指定的所有列都一起计算（所以不能从个别的列取回数据）。
3. `group by` 子句中列出的每个列都必须是检索列或有效的表达式（但不能是聚集函数）。如果在 `select` 中使用表达式，则必须在 `group by` 子句中指定相同的表达式。不能使用别名。
4. 除聚集计算语句外，`select` 语句中的每个列都必须在 `group by` 子句中给出。
5. 如果分组列中具有 null 值，则 null 将作为一个分组返回。如果列中有多行 null 值，它们将分为一组。
6. `group by` 子句必须出现在 `where` 子句之后，`order by` 子句之前。

### 8.2 过滤分组 having

除了能用 `group by` 分组数据外，MySQL 还允许使用 `having` 关键字过滤分组，指定包括哪些分组，排除哪些分组。

语法顺序如下：

```mysql
# 语法顺序
select [查询列表] from [表名] where [筛选条件] group by [分组列表] having [分组后筛选] order by [排序列表] limit [要检索行数];
```

`where` 过滤没有分组的概念，指定的是行而不是分组，针对分组的过滤使用 `having` 子句。事实上，目前为止所学过的所有类型的 `where` 子句都可以用 `having` 来替代。

关于 `having` 和 `where` 的差别，这里有另一种理解方法，`where` 在数据分组前进行过滤，`having` 在数据分组后进行过滤。`where` 排除的行不包括在分组中，这可能会改变计算值，从而影响 `having` 子句中基于这些值过滤掉的分组。

能用分组前筛选 `where` 的，优先考虑分组前筛选。

```mysql
# 找到提供大于 2 个产品的供应商，并列出其提供的产品数量，这里使用 having 来过滤掉产品数不大于2的供应商
select vend_id, count(*) prodCount from products group by vend_id having prodCount > 2;

# 找到供应商提供的商品平均价格大于 10 的供应商，并且按平均价格降序排列
select vend_id, avg(prod_price) avgPrice from products group by vend_id having avgPrice > 10 order by avgPrice desc;
```

## 9. 子查询

**子查询**(subquery)，嵌套在其他查询中的查询。

### 9.1 使用子查询进行过滤

当一个查询语句中又嵌套了另一个完整的 `select` 语句，则被嵌套的 `select` 语句称为子查询或内查询，外面的 `select` 语句称为主查询或外查询。

之前所有查询都是在同一张表中的，如果我们想获取的信息分散在两张甚至多张表呢，比如要从订单表 orders 中获取顾客 ID，然后用顾客 ID 去顾客表 custormers 找到对应顾客信息。

```mysql
# 首先在 orderitems 表中找到产品 TNT2 对应的订单编号
select order_num from orderitems where prod_id = 'TNT2'

# 然后在 orders 表中找到订单编号对应的顾客 id
select cust_id from orders where order_num in (
  select order_num from orderitems where prod_id = 'TNT2');
  
# 然后去 customers 表中找到顾客 id 对应的顾客名字
select cust_id, cust_name from customers where cust_id in ( 
  select cust_id from orders where order_num in (  
    select order_num from orderitems where prod_id = 'TNT2'));
```

这里实际上有三条语句，最里边的子查询返回订单号列表，此列表用于其外面的子查询的 `where` 子句。外面的子查询返回顾客 ID 列表，此顾客 ID 列表用于最外层查询的 where 子句。最外层查询最终返回所需的数据。

对于能嵌套的子查询的数目没有限制，不过在实际使用时由于性能的限制，不能嵌套太多的子查询。

### 9.2 相关子查询

**相关子查询**(correlated subquery) 涉及外部查询的子查询。

使用子查询的另一方法是创建计算字段。假如需要显示 customers 表中每个顾客的订单总数。订单与相应的顾客 ID 存储在 orders 表中。

```mysql
# 首先找到用户 ID 对应的订单数量
select count(*) from orders where cust_id = 10003;

# 然后将其作为一个 select 子句，将用户 id 
select cust_name, cust_state, (
  select count(*) from orders where orders.cust_id = customers.cust_id) as order_count 
  from customers order by order_count desc;
```

注意到上面这个 `where orders.cust_id = customers.cust_id`，这种类型的子查询叫做相关子查询，任何时候只要列名可能有多义性，就必须使用完全限定语法（表名和列名由一个句点分隔)。

## 10. 联结表

如果要查的数据分散在多个表中，如何使用单条 `select` 语句查到数据呢，使用联结可以做到。

联结是一种机制，用来在一条 `select` 语句中关联表，因此称之为联结。使用特殊的语法，可以联结多个表返回一组输出，联结在运行时关联表中正确的行。

**维护引用完整性** ：在使用关系表时，仅在关系列中插入合法的数据非常重要。如果在 products 表中插入拥有没有在 vendors 表中出现的供应商 ID 的供应商生产的产品，则这些产品是不可访问的，因为它们没有关联到某个供应商。

为防止这种情况发生，可指示 MySQL 只允许在 products 表的供应商 ID 列中出现合法值（即出现在 vendors 表中的供应商）。 这就是维护引用完整性，它是通过在表的定义中指定主键和外键来实现的。

### 10.1 创建联结

联结的创建非常简单，规定要联结的所有表以及它们如何关联即可。

```mysql
# 列出产品的供应商及其价格
select vend_name, prod_name, prod_price from vendors, products 
where vendors.vend_id = products.vend_id order by prod_price desc;
```

这里在 `where` 后面用完全限定列名方式指定 MySQL 匹配 vender 表的 vend_id 列和 products 表的 vend_id 字段。

当引用的列可能有歧义时，必须使用完全限定列名的方式，因为 MySQL 不知道你指的是哪个列。

在联结两个表时，实际上做的是将一个表的每一行与另一个表的每一行配对，所以 `where` 子句作为过滤条件，过滤出只包含指定联结条件的列 `where vendors.vend_id = products.vend_id`，没有 where 子句，将返回两个表的长度乘积个字段，这叫**笛卡尔积**（cartesian product），可以运行一下这句看看：

```mysql
# 返回两个表长度乘积行
select vend_name, prod_name, prod_price from vendors, products;
```

所有联结应该总是使用联结条件，否则会得出笛卡尔积。

### 10.2 联结多个表

一条 `select` 语句也可以联结多个表，比如需要把某个订单的产品信息、订单信息、供应商信息都列出来，要找的产品信息分散在供应商、产品、订单信息三个表中。

```mysql
# 将订单 20005 的产品信息、订单信息、供应商信息找出来
select prod_name, vend_name, prod_price, quantity
from orderitems,
     products,
     vendors
where products.vend_id = vendors.vend_id
  and orderitems.prod_id = products.prod_id
  and order_num = 20005;
```

这里使用 `and` 来连接多个联结条件，定义了 3 个表之间用什么作为关联。

注意：MySQL 在运行时关联多个表以处理联结可能是非常耗费资源的，不要联结不必要的表。联结的表越多，性能下降越厉害。

这里可以使用联结来实现 9.1 节的例子，之前是使用子查询来实现的，从订单表 orders 中获取顾客 ID，然后用顾客 ID 去顾客表 custormers 找到对应顾客信息。

```mysql
# 使用联结来实现 9.1 的例子
select customers.cust_id, cust_name
from orders, customers, orderitems
where orders.order_num = orderitems.order_num
  and customers.cust_id = orders.cust_id
  and prod_id = 'TNT2';        						# 由于三个表中只有一个表有 prod_id，所以不需要限定表名
```

这里提一句，不仅仅列可以起别名，表也可以起，用法跟列的别名一样：

```mysql
# 把前面这个句子起别名
select c.cust_id, cust_name
from orders o, customers c, orderitems oi
where o.order_num = oi.order_num
  and c.cust_id = o.cust_id
  and prod_id = 'TNT2';
```

这样不仅仅可以缩短 SQL 语句，也允许在单条 `select` 语句中多次使用相同的表，同时起的别名不仅可以用在 `select` 子句，也可以使用在 `where`、`order by` 子句以及语句的其他部分。

### 10.3 内部联结 inner join

目前为止所用的联结称为**等值联结**(equijoin)，它基于两个表之间的相等测试，也称为**内部联结**。其实，对于这种联结可以使用稍微不同的语法来明确指定联结的类型。下面的 `select` 语句返回与前面例子完全相同的数据：

```mysql
# 列出产品的供应商及其价格
select vend_name, prod_name, prod_price
from vendors
         inner join products
                    on vendors.vend_id = products.vend_id;
```

这里的联结条件使用 `on` 子句而不是 `where`，这两种语法都可以达到效果。尽管使用 `where` 子句定义联结的确比较简单，但使用明确的联结语法能够确保不会忘记联结条件，有时候这样做也能影响性能。

### 10.4 自联结

比如某个产品出现了质量问题，现在希望找出这个产品的供应商提供的所有产品信息。按照之前介绍的子查询，我们可以先找到对应产品的供应商，然后找到具有这个供应商 ID 的产品列表：

```mysql
# 先找到产品 ID 为 TNT1 的供应商 ID，然后找到对应供应商 ID 提供的产品列表
select prod_id, prod_name, vend_id
from products
where vend_id in (
    select vend_id
    from products
    where prod_id = 'TNT1'
);
```

使用子查询确实可以实现，使用联结也可以做到，这就是自联结：

```mysql
# 自联结
select p1.prod_id, p1.prod_name, p1.vend_id
from products p1,
     products p2
where p1.vend_id = p2.vend_id
  and p2.prod_id = 'TNT1';
```

自联结查询的两个表是同一个表，因此 products 表需要分别起别名，以作为区分，而且 `select` 子句中出现的列名也需要限定表明，因为两个表都出现了相同的字段。

自联结通常作为外部语句用来替代从相同表中检索数据时使用的子查询语句。虽然最终的结果是相同的，但有时候处理联结远比处理子查询快得多。应该试一下两种方法，以确定哪一种的性能更好。

### 10.5 自然联结

无论何时对表进行联结，应该至少有一个列出现在不止一个表中(被联结的列)。标准的联结返回所有数据，甚至相同的列多次出现。自然联结排除多次出现，使每个列只返回一次。

自然联结就是你只选择那些唯一的列，这一般是通过对表使用通配符，对所有其他表的列使用明确的子集来完成的。

```mysql
# 自选择唯一的通配符只对第一个表使用。所有其他列明确列出，所以没有重复的列被检索出来。
select v.*, p.prod_id
from vendors v,
     products p
where v.vend_id = p.vend_id;
```

### 10.6 外部链接 outer join

有些情况下，联结包含了那些在相关表中没有关联行的行，这种类型的联结称为**外部联结**。

比如：

- 对每个顾客下了多少订单进行计数，包括那些至今尚未下订单的顾客;
- 列出所有产品以及订购数量，包括没有人订购的产品；
- 计算平均销售规模，包括那些至今尚未下订单的顾客。

此时联结需要包含哪些没有关联行的那些行。

比如检索所有用户，及其所下的订单，没有订单的也要列举出来：

```mysql
# 内部联结，查找用户对应的订单
select c.cust_id, o.order_num
from customers c
         inner join orders o
                    on c.cust_id = o.cust_id;
                    
# 左外部联结，将没有下单过的顾客行也列出来
select c.cust_id, o.order_num
from customers c
         left outer join orders o
                         on c.cust_id = o.cust_id;
                         
# 右外部联结，列出所有订单及其顾客，这样没下单过的顾客就不会被列举出来
select c.cust_id, o.order_num
from customers c
         right outer join orders o
                          on c.cust_id = o.cust_id;
```

在使用 `outer join` 语法时，必须使用 `right` 或 `left` 关键字指定包括其所有行的表。`right` 指出的是 `outer join` 右边的表，而 `left` 指出的是 `outer join` 左边的表。上面使用 `left outer join` 从 `from` 子句的左边表 custermers 中选择所有行。为了从右边的表中选择所有行，应该使用 `right outer join`。

左外部联结可通过颠倒 `from` 或 `where` 子句中表的顺序转换为右外部联结，具体用哪个看你方便。

### 10.7 使用带聚集函数的联结

比如想检索一个顾客下过的订单数量，即使没有也要写 0，此时使用分组和 `count` 聚集函数来统计数量：

```mysql
# 找到每个顾客所下订单的数量，并降序排列
select c.cust_id, c.cust_name, count(o.order_num) count_orders
from customers c
         left outer join orders o on c.cust_id = o.cust_id
group by c.cust_id
order by count_orders desc;
```

因为即使顾客没有下单，也要在结果里，所以把顾客表放在左边，用左外部联结。

## 11. 组合查询

MySQL 允许执行多条select语句，并将结果作为单个查询结果集返回。这些组合查询通常称为并(union)或复合查询(compound query)。

有两种情况需要使用组合查询：

1. 在单个查询中从不同的表返回类似结构的数据；
2. 对单个表执行多个查询，按单个查询返回数据。

多数情况下，组合查询可以使用具有多个 `where` 子句条件的单条查询代替。具体场景可以尝试一下这两种方式，看看对特定的查询哪一种性能更好。

### 11.1 创建组合查询 union

当查询结果来自于多张表，但多张表之间没有关联，这个时候往往使用组合查询。在每条 `select` 语句之间放上关键字 `union` 即可。

```mysql
# 比如需要列出商品价格小于等于 10 而且是供应商 ID 为 1005 或 1003 的产品信息
select prod_id, prod_name, prod_price, vend_id from products where prod_price <= 10
union
select prod_id, prod_name, prod_price, vend_id from products where vend_id in (1005, 1003);

# 实际上这句也可以通过 where 语句代替
select prod_id, prod_name, prod_price from products where prod_price <= 10 or vend_id in (1005, 1003);
```

1. 有些情况下，比如更复杂的过滤条件、需要从多个表中检索数据的情况下，使用 `union` 可能会更简单。
2. `union` 每个查询必须包含相同的列、表达式、聚集函数，不过每个列不需要以相同的次序列出。
3. 列数据类型必须兼容，类型不必完全相同，但必须是数据库管理系统可以隐式的转换。
4. 组合查询的排序 `order by` 只能出现在最后一条 `select` 语句之后，不能对不同的 `select` 语句分别排序。

### 11.2 包含或取消重复的行 union (all)

两行 `union` 分开的语句可能会返回重复的行，但前面那个例子实际结果却并没有包含重复行，这是因为 `union` 关键字自动去除了重复的行，如果不希望去重，可以使用 `union all` 关键字。

```mysql
# 不去重重复行
select prod_id, prod_name, prod_price, vend_id from products where prod_price <= 10
union all
select prod_id, prod_name, prod_price, vend_id from products where vend_id in (1005, 1003);
```

如果需要出现重复行，此时无法使用 `where` 关键字来达成同样的效果了。

## 12. 数据的增删改

前面说的都是数据的查询，这一章将所以说数据的增删改。

### 12.1 数据插入 insert into

数据插入使用 `insert` 关键字，它可以插入一行、多行数据，也可以插入某些查询的结果。

```mysql
# 插入一条数据到顾客表中
insert into customers
values (null, 'Zhang San', '001 street', 'ShangHai', 'SH', '666666', 'ZH', null, null);
```

这里插入一条数据到顾客表中，存储到每个表列中的数据需要在 `values` 子句中给出，按照表在创建的时候的顺序依次给出。如果某个列没值就给 null。虽然第一条数据对应 cust_id 列的属性是 `not null` 的，但是这个列是 auto_increment 也就是自增的，MySQL 会自动忽略你给出的 null 并将值自动增加再填充。

但使用上面 `values` 子句这种方式并不安全，因为这种方式注入数据完全靠输入数据的顺序，如果表结构变动，就会导致输入数据错位。

安全的数据插入方式是这样的：

```mysql
# 安全但繁琐的插入方式
insert into customers(cust_name, cust_address, cust_city, cust_state, cust_zip, cust_country, cust_contact, cust_email)
values ('Zhang San', '001 street', 'ShangHai', 'SH', '666666', 'ZH', null, null);
```

这里在前一个括号给出了后面括号中数据对应的列名，这样的话即使表结构或者顺序发生变化，也能正确插入数据。

可以看到列 cust_id 被省略了，当满足下面条件时，列可以省略：

1. 列定义为允许 null 值；
2. 表定义时这个列给出了默认值，表示如果不给值则使用默认值。

如果不能省略却省略了，会报错。

`insert` 操作可能很耗时，特别是有很多索引需要更新时，而且它可能降低等待处理的 select 语句的性能。如果数据检索是最重要的，你可以通过在 `insert` 和 `into` 之间添加关键字 `low_priority` ，降低 `insert` 语句的优先级，这也同样适用于下文提到的 `update` 和 `delete` 语句。

### 12.2 插入多个行

上面介绍的 `insert` 语句可以一次插入一个行，如果想一次插入多个行，每次都列出列名就比较繁琐了，可以使用下面这种方式：

```mysql
# 插入多个行
insert into customers(cust_name, cust_address, cust_city, cust_state, cust_zip, cust_country, cust_contact, cust_email)
values ('Zhang San', '001 street', 'ShangHai', 'SH', '666666', 'ZH', null, null),
       ('Li Si', '002 street', 'BeiJing', 'BJ', '878787', 'ZH', null, '123123@163.com');
```

`values` 子句后面继续用括号将字段括起来添加新行，中间加个逗号。这可以提高数据库处理的性能，因为单条 `insert` 语句处理多个插入比使用多条 `insert` 语句快。

### 12.3 插入检索出的数据 insert select

`insert` 可以将一条 `select` 语句的结果插入表中，这就是 `insert select`。比如你想将另一个表中查询的数据插入到这个表中：

```mysql
# 从别的表中找出数据，并插入 customers 表中
insert into customers(cust_id, cust_name, cust_address, cust_city, cust_state, cust_zip, cust_country, cust_contact, cust_email)
select id, name, address, city, state, zip, country, contact, email
from custnew;
```

`select` 的新行也可以省略 cust_id，这样 `insert` 的时候也是可以自动生成新的 cust_id 的。另外可以看到 select 语句的列名跟 `insert into` 语句后的列名并不对应，这也没关系，因为 `insert select` 使用的是位置对应，select 语句返回的第一列对应 cust_id，第二列对应 cust_name，依次对应。`select` 语句后也可以加入 `where` 子句进行过滤。

### 12.4 修改数据 update

`update` 语句用来修改表中的数据，使用 `update` 的时候一定要小心，不要忘了添加 `where` 子句，因为一不小心就会更新表中所有行。

```mysql
# 更新 id 为 10005 的用户的信息
update customers set cust_email = '888@qq.com' where cust_id = 10005;
```

如果这里没有使用 `where` 子句，`update` 将会更新这个表中的所有行的 cust_email 字段，所以一定要注意。

要删除某行某列的值，可以将值修改为 null。

更新多个字段的方式也很简单：

```mysql
# 更新多个字段
update customers
set cust_email   = '666@qq.com',
    cust_contact = 'S Zhang'
where cust_id = 10005;
```

如果用 `update` 语句更新多行，并且在更新这些行中的一行或多行时出一个现错误，则整个 `update` 操作被取消 (错误发生前更新的所有行被恢复到它们原来的值)。为即使是发生错误，也继续进行更新，可以在 `update` 后使用 `ignore` 关键字。

`update` 语句可以使用子查询，用 `select` 语句检索出的数据来更新列数据。

### 12.5 删除数据 delete

`delete` 语句可以用来从表中删除特定的行或者所有行。使用 `delete` 语句的时候要小心，不要忘了添加 `where` 子句，因为一不小心就会删除表中所有行。

```mysql
# 删除顾客表中顾客 id 为 10008 的行
delete from customers where cust_id = 10008;
```

如果将 `where` 子句去掉，那么就是删除这个表中的所有行，但不是删除这个表，删除表使用的是另一个语句 `drop`。另外删除一个表中所有行更快的语句是 `truncate table`，因为 `delete` 是逐行删除数据，而 `truncate` 是删除原来的表重新建个表。

注意，在使用 `update` 和 `delete` 之前，应该非常小心，因为 MySQL 没有撤销，使用之前建议先使用 `select` 进行测试，防止 `where` 子句不正确导致数据丢失。

## 13. 创建和操作表

### 13.1 创建表 create table

我们可以打开之前为了整点数据执行的 [create.sql](https://github.com/SHERlocked93/FE_Daily/blob/20210906/20210830_mysql/mysql_scripts/create.sql) 文件看看，用 VSCode/Webstorm/Navivate/文本 都能打开，这个文件除了注释的第一行就是创建表语句：

```mysql
CREATE TABLE customers
(
  cust_id      int       NOT NULL AUTO_INCREMENT,
  cust_name    char(50)  NOT NULL ,
  cust_address char(50)  NULL ,
  cust_city    char(50)  NULL ,
  cust_state   char(5)   NULL ,
  cust_zip     char(10)  NULL ,
  cust_country char(50)  NULL DEFAULT 'ZH',  # 指定默认值
  cust_contact char(50)  NULL ,
  cust_email   char(255) NULL ,
  PRIMARY KEY (cust_id)          # 指定主键
) ENGINE=InnoDB;
```

从这里可以看到 `create table` 的格式。

如果要在一个表不存在时创建，应该在表名前、`create table` 后加上 `if not exists`。这样会先检查表名是否已存在，并且在不存在时进行创建。

对于 `auto_increment`，每个表只能有一个 `auto_increment`，而且它必须被索引。当你使用 `insert` 语句插入一个新的值，后续自动增量将从这个值重新开始增加。如果一个表创建新的列需要得到最 `auto_increment` 的值，可以使用 `last_insert_id()` 来获取最后自增的值。

上面创建语句的列名后 `null` 表示这个列在插入和修改时允许不给出值，如果是 `not null`，那么在插入或修改时就必须给值，否则会报错。默认为 `null`，如果不显式的给出 `not null`，则会默认为 `null`。

`primary key` 指示主键的值，在插入时主键值必须是不重复的，主键也可以是多个字段 `primary key (cust_id, cust_name)` 用逗号分开。作为主键的列是不能允许 null 的。

`default` 关键字可以指定默认值，如果插入行没有指定默认值，那么将默认使用默认值。

最后的 `engine` 字段指定了不同的引擎，以下是 MySQL 支持的几个常用的引擎：

1. **InnoDB** 可靠的事务处理引擎，不支持全文搜索。
2. **MEMORY** 功能等同于 MyISAM，但由于数据存储在内存，速度很快，适合于临时表。
3. **MyISAM** 默认是这个，性能高，支持全文搜索，不支持事务。

根据不同需要可以选择不同引擎。

### 13.2 修改表 alter table

修改表使用 `alter table` 语句，一般情况下，当表中开始存储数据后，就不应该再修改表。所以表在设计时需要大量时间来考虑，尽量在后期不对表进行大的改动。

```mysql
# 给供应商表增加一列 vend_phone 字段
alter table vendors
    add vend_phone char(20) default 12212341234;
    
# 删除这个添加的 vend_phone 字段
alter table vendors
    drop column vend_phone;
```

`alter table` 经常用来定义外键 `foreign key`，用于限制两个表的关系，保证该字段的值必须来自于主表的关联列的值。外键具有保持数据完整性和一致性的机制，对业务处理有着很好的校验作用。

外键用来在从表添加外键约束，用于引用主表中某列的值，比如学生表的专业编号，员工表的部门编号，员工表的工种编号，产品表的供应商编号等等。

可以从 [create.sql](https://github.com/SHERlocked93/FE_Daily/blob/20210906/20210830_mysql/mysql_scripts/create.sql#L103-L104) 文件最下面看到外键的例子，这里列举一行：

```mysql
# 将订单信息表的 order_num 设置为订单表的外键
alter table orderitems
    add constraint fk_orderitems_orders foreign key (order_num) references orders (order_num);
```

设置外键之后，如果外键已经有对应数据，就不能直接删除主表的这个外键行了：

```mysql
# 直接删除外键行报错，不允许删
delete from orders where order_num = 20009;

# 先删除 orderitems 中的关联行再删除 orders 中的外键行，就可以删了
delete from orders where order_num = 20009;
delete from orderitems where order_num = 20009;
```

所以在插入数据时，先插入主表，再插入从表。删除数据时，先删除从表，再删除主表。

注意：使用 `alter table` 要小心，最好在改动之前做一个完整的备份，数据库表的更改不能撤销。如果不小心增加了不需要的列，可能无法删除它们，如果删除了不该删除的列，可能就丢失了数据。

### 13.3 删除表 drop table

删除一个表可以使用 `drop  table` 关键字。

```mysql
drop table customers2;
```

删除表没有确认，也没有撤销，执行后将永久删除该表。

如果删除时不存在这个表会报错，可以在 `drop table` 关键字后加上 `if exists`，这样数据库会先检查这个目标表是不是存在：

```mysql
# 删除一个表，如果没加 if exists 表又不存在则会报错
drop table if exists customers2;
```

创建新表时，指定的表名必须不存在，否则会报错，所以在创建前也可以执行这个句子。

### 13.4 重命名表 rename table

重命名一个表可以使用 `rename table` 关键字。

```mysql
# 重命名一个表
rename table customers to customers2;

# 重命名多个表
rename table customers to customers2,
             vendors to vendors2;
```

## 14. 视图

视图是虚拟存在的表，行和列的数据来自定义视图的查询中使用的表，并且是在使用视图时动态生成的，只保存 SQL 逻辑，不保存查询结果。

### 14.1 创建视图 create view

比如说现在要查询购买了 TNT2 产品的顾客信息，按之前介绍的知识使用联结从三个表中查找：

```mysql
# 找到购买了 TNT2 的顾客信息
select cust_name, cust_contact, cust_email, prod_id
from customers c,
     orders o,
     orderitems oi
where c.cust_id = o.cust_id
  and o.order_num = oi.order_num
  and prod_id = 'TNT2';
```

那如果现在要换成找到购买了另一个产品的顾客信息呢，重新写一遍查询语句似乎有点重复。程序员永远不做重复的事，如果有一个虚拟表，名为 prod_cust，然后使用 `select * from prod_cust where prod_id = 'TNT1'` 就可以轻松找到对应的行了，这就是视图。

```mysql
# 创建视图
create view prod_cust as
select cust_name, cust_contact, cust_email, prod_id
from customers c,
     orders o,
     orderitems oi
where c.cust_id = o.cust_id
  and o.order_num = oi.order_num;
  
# 使用视图查询购买了产品 TNT2 的顾客信息
select cust_name, cust_email from prod_cust
where prod_id = 'TNT2';
```

使用起来挺简单的，可以根据需要编写出可重复使用的视图，方便查询。

视图的使用如下：

```mysql
create view prod_cust  as ...;       # 创建视图
show create view prod_cust;          # 查看创建视图的语句
drop view prod_cust;                 # 删除视图
create or replace view prod_cust  as ...;     # 更新视图
```

如果要修改视图，可以先删除再新建，也可以直接 `create or replace view`，如果存在则会替换，如果不存在则会新建。

视图并不直接包含数据，而是一个 SQL 查询。视图和普通表的关系，就像临时组建的歌唱团和普通班级的关系。

但也因为视图不包含数据，每次都要重新执行，所以如果使用视图的场景比较复杂比如嵌套视图等，那么你会发现性能下降的厉害，所以在大量使用视图的场景可能需要关注性能问题。

视图创建后，可以像使用表一样使用视图，对视图进行 `select`、过滤、排序、联结等等操作。

使用视图可以：

1. 复用 SQL 语句。
2. 简化复杂的 SQL 操作。在编写查询后，可以方便地重用它而不必知道它的基本查询细节。
3. 使用表的组成部分而不是整个表。
4. 保护数据。可以给用户授予表的特定部分的访问权限而不是整个表的访问权限。
5. 更改数据格式和表示。视图可返回与底层表的表示和格式不同的数据。

顺便说一句，创建视图之后，`show tables` 也会显示视图，所以你可以通过下面方式查询所有基表或者视图：

```mysql
# 显示当前database中不包括视图的所有基表
select table_name
from information_schema.tables
where table_schema = 'mysql_demo1'
  and table_type = 'BASE TABLE';

# 显示当前database中的所有视图
select table_name
from information_schema.tables
where table_schema = 'mysql_demo1'
  and table_type = 'VIEW';
```

### 14.2 使用视图重新格式化检索出的数据

比如某个场景，经常会使用到一些格式化的数据，那么就可以使用视图把数据格式化的形式先拼接好：

```mysql
# 经常用到的供应商信息，可以先组装成视图
create or replace view vend_infos as
select vend_id, concat(vend_name, '(', vend_city, ', ', vend_country, ')') vend_info
from vendors;

# 使用视图直接拿到拼好的供应商信息
select prod_id, prod_name, vend_info
from products, vend_infos
where products.vend_id = vend_infos.vend_id;
```

### 14.3 使用视图过滤不想要的数据

比如某个场景，需要找到邮箱地址不为 null 的顾客下的订单：

```mysql
# 找到 email 不是 null 的顾客下的订单
select order_num, cust_name, cust_email
from customers, orders
where customers.cust_id = orders.cust_id
  and cust_email is not null;
```

但是另一个场景又需要找到邮箱地址不为 null 的顾客购买的所有商品列表，此时我们可以使用视图，把邮箱地址不为 null 的顾客创建为一个视图，在其他场景使用：

```mysql
# 创建邮箱地址不为 null 的顾客的视图
create view cust_has_email as
select * from customers
where cust_email is not null;

# 找到 email 不是 null 的顾客下的订单
select order_num, cust_name, cust_email
from cust_has_email c, orders o
where c.cust_id = o.cust_id;

# 找到 email 不是 null 的顾客购买的所有商品列表
select c.cust_name, c.cust_email, c.cust_name, prod_name
from cust_has_email c, orders o, orderitems oi, products p
where c.cust_id = o.cust_id
  and oi.order_num = o.order_num
  and p.prod_id = oi.prod_id;
```

可以看到视图这里就完全被当成了一个表来和其他表一起使用。

### 14.4 使用视图与计算字段

视图对于简化计算字段的使用很有用，比如希望查找 20008 的订单的订单总额：

```mysql
# 查找 20008 订单的订单总额
select order_num, sum(quantity * item_price) sum_price
from orderitems
where order_num = 20008;
```

那么希望查找另一个订单总额时，可以使用视图来改造一下：

```mysql
# 查找订单总额视图
create or replace view sum_orders as
select order_num, sum(quantity * item_price) sum_price
from orderitems group by order_num;

# 找另一个订单的总金额
select order_num, sum_price
from sum_orders
where order_num = 20009;
```

看到视图十分好用，实际使用中按需使用视图可以极大方便数据库操作。

### 14.5 更新视图

视图也是可以使用 `insert`、`update`、`delete`  更新数据的，虽然视图只是一个 SQL 句子而不是实际数据。

更新视图的数据会更新其基表，但并非所有视图都可以更新的，如果数据库不冷确定被更新的基数据，则不允许更新。比如分组、联结、子查询、并、聚集函数、`distinct` 等等。

```mysql
# 比如给上面的 email 不为 null 的视图添加一行数据，插入会成功
insert into cust_has_email(cust_id, cust_name, cust_address, cust_city, cust_state, cust_zip, cust_country, cust_contact)
values (10010, 'Zhang San', '001 street', 'ShangHai', 'SH', '9999', 'ZH', 'Li S');

# 给查找订单总额视图增加一行会失败，因为这里有分组，数据库不知道在哪插入
insert into sum_orders(order_num, order_item, prod_id, quantity, item_price)
values (20009, 5, 'OL1', 2, 8.99);
```

不过一般，应该把视图用于检索数据 `select`，而不是增删改数据 `insert`、`update`、`delete`。

## 15. 存储过程

前面介绍的大部分 SQL 语句都是对一个或者多个表的单个查询，但是实际情况下一个完整的操作可能是由多个语句组合而成的，比如考虑下面这个下单流程:

1. 为了处理订单，需要核对以保证库存中有相应的物品。
2. 如果库存有物品，这些物品需要预定以便不将它们再卖给别的人，并且要减少可用的物品数量以反映正确的库存量。
3. 库存中没有的物品需要订购，需要与供应商进行一些交互。
4. 关于哪些物品入库（并且可以立即发货）和哪些物品退订，需要通知相应的客户。

可以说存储过程就是数据库 SQL 语言层面上的代码封装和重用，可以回传值，也可以接受参数。可以将其视为批文件，但作用不仅限于批处理。

存储过程简单、安全、高性能。不过有些数据库管理员会限制存储过程的创建权限，只允许用户使用，但不允许用户创建存储过程。

### 15.1 创建存储过程 create procedure

创建存储过程使用 `create procedure`，可以设置参数，存储过程体使用 `begin ... end` 分隔开，调用使用 `call`

```mysql
# 创建一个计算平均价格的存储过程
create procedure product_pricing(vend_id int)
begin
    select avg(prod_price) as priceaverage
    from products
    where products.vend_id = vend_id;
end;

# 查看创建存储过程的语句
show create procedure product_pricing;

# 调用存储过程查询平均价格
call product_pricing(1002);
```

这里的存储过程使用了参数，也可以不使用参数，和其他语言中的函数类似。

### 15.2 删除存储过程 drop procedure

删除使用 `drop` 关键字，如果不存在这个存储过程会报错，此时可以增加 `if exists` 关键字：

```mysql
# 删除存储过程    
drop procedure product_pricing;

# 先检查再删除
drop procedure if exists product_pricing;
```

### 15.3 使用参数

**变量**(variable) 内存中一个特定的位置，用来临时存储数据。

存储过程输入了 4 个参数，一个输入参数，还有三个用来存储的参数，每个参数用 `in`（传递给存储过程）、`out`（从存储过程传出）、`inout`（对存储过程传入和传出）指定参数。

MySQL 中的变量都必须以 @ 开始，存储过程中检索得到的值使用 `into` 保存到相应变量，之后可以就可以查询到变量中存储的值了。

```mysql
# 存储过程输入输出参数
create procedure product_pricing(
    in vend_id int,
    out min_price decimal(8, 2),
    out max_price decimal(8, 2),
    out avg_price decimal(8, 2)
)
begin
    select min(prod_price)
    into min_price
    from products where products.vend_id = vend_id;
    select max(prod_price)
    into max_price
    from products where products.vend_id = vend_id;
    select avg(prod_price)
    into avg_price
    from products where products.vend_id = vend_id;
end;

# 调用存储过程查询产品平均价格
call product_pricing(1002, @minprice, @maxprice, @avgprice);

# 查询刚刚输出的变量
select @minprice, @maxprice, @avgprice;
```

再试个例子，使用存储过程计算出指定订单号的总价，并输出到变量中：

```mysql
# 计算指定订单号的总价格，并输出到变量中
create procedure order_pricing(
    in order_num int,
    out total_price decimal(8, 2)
)
begin
    select sum(quantity * item_price)
    into total_price
    from orderitems
    where orderitems.order_num = order_num;
end;

# 计算订单 20005 的总价
call order_pricing(20005, @totalprice);

# 查询总价
select @totalprice;
```

### 15.4 使用条件语句

存储过程也可以使用 `if (条件) then ... elseif (条件) then ... else` 语句，比如现在要计算折扣后的商品价格，总商品数量 3 件 8 折，4 件 7 折，这里使用存储过程：

```mysql
# 首先为了方便后面计算订单总金额，创建一个查询订单总金额的视图
create or replace view sum_order_price as
select sum(quantity * item_price) as total_price, order_num
from orderitems group by order_num;

# 总商品数量 3 件 8 折，4 件 7 折,计算折扣后的产品价格，
create procedure total_discount_price(
    in order_num int,
    out discount_price decimal(8, 2)
) 
begin
    # 创建一个变量保存商品总数
    declare prod_count int;

    # 计算该订单号的商品总件数
    select sum(quantity)
    into prod_count
    from orderitems where orderitems.order_num = order_num;

    # 小于 3 件无折扣
    if prod_count < 3 then
        select total_price
        into discount_price
        from sum_order_price o
        where o.order_num = order_num;
    # 等于 3 件 8 折
    elseif prod_count = 3 then
        select total_price * 0.8
        into discount_price
        from sum_order_price o
        where o.order_num = order_num;
    # 大于等于 3 件 7 折
    else
        select total_price * 0.7
        into discount_price
        from sum_order_price o
        where o.order_num = order_num;
    end if;
end;

# 调用存储过程查询折扣后的金额
call total_discount_price(20005, @discountprice);

select @discountprice;
```

这个例子中我们使用了一个临时变量 prod_count，计算出该订单总件数之后将其赋到这个临时变量中，然后在之后的 `if else` 条件语句中对其进行判断，再通过视图计算出总金额，最后保存给输出变量。

## 16. 游标

有时，需要在检索出来的行中前进或后退一行或多行，这就是使用游标的原因。**游标**（cursor）是一个存储在 MySQL 服务器上的数据库查询，它不是一条 `select` 语句，而是被该语句检索出来的结果集。在存储了游标之后，应用可以根据需要滚动或浏览其中的数据。

游标主要用于交互式应用，其中用户需要滚动屏幕上的数据，并对数据进行浏览或做出更改。

MySQL 中的游标只能用于存储过程或函数。

游标处理分为下面几个步骤：

1. 声明游标 declare：没有检索数据，只是定义要使用的 `select` 语句；
2. 打开游标 open：打开游标以供使用，用上一步定义的 `select` 语句把数据实际检索出来；
3. 检索游标 fetch：对于填有数据的游标，根据需要取出(检索)各行；
4. 关闭游标 close：在结束游标使用时，必须关闭游标，如果你不关闭游标，MySQL 将在到达 `end` 语句时关闭游标。

下面直接看例子：

```mysql
drop procedure if exists process_orders;

# 使用游标将每个订单的实际价格填写到一个表中
create procedure process_orders()
begin
    # 定义本地变量
    declare o_num int;                    # 循环中的订单号变量
    declare d_price decimal(8, 2);        # 循环中的实际价格变量
    declare done boolean default false;   # 终止条件布尔值

    # 定义游标
    declare order_numbers cursor for
        select order_num from orders;

    # 终止条件，当没有更多行供循环时满足 not found，此时给 done 赋值 true
    declare continue handler for not found set done = true;

    # 没有则创建一个新的表，用来存订单的实际价格
    create table if not exists ordertotals
    (
        order_num   int,
        order_price decimal(8, 2),
        primary key (order_num)
    );

    open order_numbers;         # 打开游标

    # 在循环中依次给表 ordertotals 填充行
    repeat
        fetch order_numbers into o_num;
        call total_discount_price(o_num, d_price); 
        insert into ordertotals(order_num, order_price)
        values (o_num, d_price);
    until done end repeat;              # 满足 done 为真值则跳出循环

    close order_numbers;
end;

call process_orders();

select * from ordertotals;
```

首先使用 `declare` 定义了几个局部变量，这几个变量用来存中间值，其中默认值为 false 的 `done` 是循环的终止条件，将在后面的 `repeat` 语句中用来作为判断是否继续循环的标志位，当 `repeat` 没有更多行供循环时满足 `not found`，此时给 `done` 赋值 true 终止循环。在循环体中使用上一章的存储过程给表 ordertotals 填充计算的订单实际价格。

`declare` 语句是有顺序的，局部变量需要在句柄之后定义，句柄必须在游标之后定义，否则会报错。

除了 `repeat` 循环外，MySQL 还支持 `loop` 循环、`while` 循环，基本大同小异，可以自己查询学习一下。

## 17. 触发器

如果你想要某些语句在事件发生时自动执行，可以考虑触发器。

1. 只可以响应 `delete`、`insert`、`update` 语句；
2. 只有表支持触发器，临时表和视图不支持；

### 17.1 创建触发器 create trigger

创建触发器使用 `create trigger` 关键字，格式如下：

```mysql
# 语法
create trigger [触发器名]
[after/before] [insert/update/delete] on [表名]
for each row 
begin
 [sql语句]
end;

# 删除
drop trigger [if exists] [触发器名];
```
`for each row` 表示对每个插入行执行触发器。只有表

```mysql
# 创建一个触发器，在新的产品插入时给临时变量赋值
create trigger newproduct
    after insert
    on products
    for each row select 'Product added' into @newprod;

# 插入一条语句试试
insert into products(prod_id, vend_id, prod_name, prod_price, prod_desc)
values ('XP2000', 1005, 'JetPack 200', 55, 'JetPack 200, multi-use');

select @newprod;
```

### 17.2 使用触发器

触发器要谨慎使用，由于触发器是针对每一行的，对增删改非常频繁的表上切记不要使用触发器，因为会非常消耗资源。 

#### insert 触发器

1. `insert` 触发器内可以通过访问名为 `new` 的虚拟表访问被插入的行；
2. `before insert` 语句中可以通过更改 `new` 虚拟表中的值来修改插入行的数据；
3. 对于 `auto_increment` 自增列，在 `before` 中 `new` 中的值为 0，在 `after` 中为自动生成的自增值。

```mysql
# 插入用户后获取这个新用户自动生成的的 ID 并且赋值给临时变量
create trigger newcust
    after insert
    on customers
    for each row select new.cust_id
                 into @newcust_after;

# 插入用户
insert into customers(cust_name, cust_address, cust_city, cust_state, cust_zip, cust_country, cust_contact, cust_email)
values ('Zhang San', '001 street', 'ShangHai', 'SH', '666666', 'ZH', null, null);

# 查看新值
select @newcust_after;
```

`before` 经常被用于数据验证。

#### delete 触发器

1. `delete` 触发器内可以通过访问名为 `old` 的虚拟表来访问被删除的行；
2. `old` 虚拟表中的字段都是只读的，不能修改。

```mysql
drop trigger if exists deletecustomer;

# 创建触发器，当从顾客表中删除时将删除的数据插入到另一个存档表中
create trigger deletecustomer
    before delete on customers for each row
begin
    insert into customers2(cust_id, cust_name, cust_address, cust_city, cust_state, cust_zip, cust_country, cust_contact, cust_email)
    values (old.cust_id, old.cust_name, old.cust_address, old.cust_city, old.cust_state, old.cust_zip, old.cust_country, old.cust_contact, old.cust_email);
end;

# 删除刚刚创建的顾客数据
delete from customers where cust_id = 10013;

# 查询一下存档表中的顾客数据是否存在
select * from customers2;
```

这里使用 `before` 而不是 `after` 的原因是，如果因为某种原因顾客信息不能存档，`delete` 操作将会放弃，避免信息丢失。

#### update 触发器

1. `update` 触发器内可以通过访问名为 `old` 的虚拟表访问更新前的值，访问名为 `new` 的虚拟表来访问更新后的值；
2. `before update` 触发器中，`new` 中的值是可以被修改的；
3. `old` 虚拟表中的字段都是只读的，不能修改。

```mysql
drop trigger if exists updatecustomer;

# 使用触发器，将每次更新的 cust_country 转化为大写
create trigger updatecustomer
    before update
    on customers
    for each row
begin
    set new.cust_country = upper(new.cust_country);
end;

# 更改数据
update customers set cust_country ='zh' where cust_id = 10005;
```

## 18. 管理事务处理

**事务处理**(transaction processing)可以用来维护数据库的完整性，它保证成批的 MySQL 操作要么完全执行，要么完全不执行。

举个例子，如果我们要转账给别人，首先把别人账户增加钱，再把我们账户上钱扣除，如果中间出现问题，那么麻烦就大了。

或者在当前数据库中，如果我们要添加一个订单信息，分为下面几步：

1. 检查数据库中是否存在相应的客户（从customers表查询），如果不存在则添加这个用户信息。
2. 检索顾客的 ID，cust_id。
3. 添加一行订单信息到 orders 表，把它与顾客 ID 关联。
4. 检索 orders 表中赋予的新订单 ID，order_id。
5. 对于订购的每个物品在 orderitems 表中添加一行，通过检索出来的 ID 把它与 orders 表关联，以及通过产品 ID 与 products 表关联。

如果发生了某种数据库故障（超出磁盘限制、安全限制、表锁等），阻止了一个完整的流程，会出现什么情况 。如果故障出现在 1 和 2 之间，这没什么关系，因为一个顾客没有订单信息是合法的，如果出现在 3 和  4 之间，那么就会出现一个空的订单，这个订单没有包含的产品信息，这很严重，如果出现在 5 时，添加 orderitems 过程中出现问题，那么可能出现订单信息不完整的情况，也很严重。

使用事务可以避免这个情况，如果中间发生了问题，那么则回退到某个安全的状态。

### 18.1 事务处理

那么使用事务如何处理这个过程呢：

1. 检查数据库中是否存在相应的顾客，如果不存在则添加这个用户信息；
2. **提交**顾客信息；
3. 检索顾客的 ID；
4. 添加一行到 orders 表；
5. 如果在添加行到 orders 表时出现故障，**回退**；
6. 检索 orders 表中赋予的新订单 ID；
7. 对于订购的每项物品，添加新行到 orderitems 表；
8. 如果在添加新行到 orderitems 时出现故障，**回退**所有添加的 orderitems 行和 orders 行；
9. **提交**订单信息。

这里有几个概念：

- 事务（transaction）指一组 SQL 语句；
- 回退（rollback）指撤销指定 SQL 语句的过程；
- 提交（commit）指将未存储的 SQL 语句结果写入数据库表；
- 保留点（savepoint）指事务处理中设置的临时占位符，你可以对它发布回退（与回退整个事务处理不同）。

### 18.2 控制事务处理

#### 使用回退 rollback

`start transaction` 标识事务开始，使用 `rollback` 可以进行回退从 `start` 到 `rollback` 中间的所有语句。

```mysql
# 开始事务
start transaction; 
delete from customers where cust_id > 10005;   # 删除几个行
select * from customers;

# 使用 rollback 回滚 delete 语句
rollback;
```

`rollback` 可以回退 `insert`、`update`、`delete` 语句，但不能回退 `create`、`drop` 语句，事务处理块中可以使用这两个语句，但 `rollback` 无效果。

#### 使用提交 commit

MySQL 中用户的任何一个更新操作（写操作）都被视为一个事务，这就是所谓的隐含提交（implicit commit），相当于 MySQL 帮你在后台提交了。

可以针对每个连接使用 `set autocommit=0` 来设置 MySQL 不自动提交更改，设置之后，每个 SQL 语句或者语句块所在的事务都需要显式 `commit` 才能提交事务。

但在事务处理块中，提交不会隐含地进行，需要你自己来显式的调用：

```mysql
# 删除订单详情表总中 20007 相关订单详情，再删除订单表中的 20007
start transaction;
delete from orderitems where order_num = 20007;
delete from orders where order_num = 20007;
commit;
```

由于设计到订单和订单详情，所以使用事务来保证订单是完整的被删除，而不是部分删除。如果两个 `delete` 语句中发生了错误，那么 `commit` 将不会被执行。

在 `commit` 或 `rollback` 执行时，事务会被自动关闭。

#### 使用保留点 savepoint

之前的 `rollback`、`commit` 只能对整个事务处理块整体提交或回滚，某些复杂场景下可能要部分回滚或者部分恢复，比如之前例子，如果订单信息增加失败，可能要回滚到添加用户信息后。

此时可以使用保留点，这样在发生问题时回滚到保留点处即可。保留点使用比较简单：

```mysql
# 创建保留点
savepoint sav1;

# 回滚到保留点
rollback to sav1;
```

保留点可以使用多一点，当在事务完成时，他们将会被自动释放，也可以使用 `release savpoint` 来手动释放。

## 19. 安全管理

### 19.1 访问控制

对数据库来说，用户应该对他们需要的数据具有适当的访问权，既不能多也不能少。

1. 多数用户只需要对表进行读和写，少数用户需要能创建和删除表；
2. 某些用户需要读表，但可能不需要更新表；
3. 你可能想允许用户添加数据，但不允许他们删除数据；
4. 某些用户（管理员）可能需要处理用户账号的权限，但多数用户不需要；
5. 你可能想让用户通过存储过程访问数据，但不允许他们直接访问数据；
6. 你可能想根据用户登录的地点限制对某些功能的访问。

给不同的用户提供不同的访问权，这就是访问控制。

对于 root 登陆的使用需要十分谨慎小心，仅在绝对需要时才使用，不应在日常 MySQL 操作中使用 root 账户。

### 19.2 管理用户

用户信息存储在 MySQL 的 mysql 库中：

```mysql
# 查看用户列表
use mysql;
select user from user;
```

创建用户账号：

```mysql
# 创建用户及其密码
create user zhangsan identified by '888888';

# 更改用户名
rename user zhangsan to lisi;

# 删除用户
drop user if exists lisi;
```

设置权限用 `grant` 关键字：

```mysql
# 显示用户张三的权限
show grants for zhangsan;

# 设置权限，允许张三在 mysql_demo1 库上使用 select
grant select on mysql_demo1.* to zhangsan;

# 撤销权限，撤销张三在 mysql_demo1 库上使用 select 的权限
revoke select on mysql_demo1.* from zhangsan;
```

权限设置和用户设置还有很多内容，不是本文的重点，可以百度一下或者看文档。

## 20. 数据库维护

### 20.1 备份数据

数据库也是经常需要备份的，可以使用以下方法：

1. 使用命令行实用程序 mysqldump 转储所有数据库内容到某个外部文件。在进行常规备份前这个实用程序应该正常运行，以便能正确地备份转储文件。
2. 用命令行实用程序 mysqlhotcopy 从一个数据库复制所有数据，但并非所有数据库引擎都支持这个实用程序。
3. 可以使用 MySQL 的 `backup table` 或 `select into outfile` 转储所有数据到某个外部文件。这两条语句都接受将要创建的系统文件名，此系统文件必须不存在，否则会出错。数据可以用 `restore table` 来复原。

### 20.2 数据库维护

1. `analyze table` 用来检查键是否正确。
2. `check table` 用来针对许多问题对表进行检查。
3. 针对 MyISAM 表访问产生不正确和不一致的问题，可以使用  `repair table` 来修复。
4. 如果从一个表中删除大量数据，应该使用 `optimize table` 来收回所用空间，从而优化表的性能。

### 20.3 查看日志

#### 错误日志 Error Log

记录 Mysql 运行过程中的 Error、Warning、Note 等信息，系统出错或者某条记录出问题可以查看错误日志。

通过 `show variables like "log_error";` 来查看错误日志存放的位置。

#### 日常日志 General Query Log

记录包括查询、修改、更新等的每条语句。

通过 `show global variables like "%genera%";` 查看日常日志存放的地方，如果 general_log 是 off 则不能查询，可以通过 `set global general_log=on;` 打开查询，然后 `tail -f /var/lib/mysql/VM-0-17-centos.log;` 来查看。

#### 二进制日志 Binary Log

包含一些事件，描述了数据库的改动，如建表、数据改动等，主要用于备份恢复、回滚操作等。

可以通过 `show variables like "%log_bin%";` 来查看 Binlog 存在哪，会有多个文件，使用 `show master logs;` 可以看到查看所有 Binlog 日志列表，格式是 `bingo.000008` 这样，当 Binlog 日志写满或者数据库重启会产生新文件，使用 `flush logs` 可以手动产生新文件，Binlog 十分重要，产生问题要回滚用 Binlog 就可以了。

#### 缓慢查询日志 Slow Query Log

记录执行缓慢的任何查询，在优化数据库时比较有用。

可以通过  `show variables like "%slow%";` 来查看缓慢日志存放的地方。

## 21. 改善性能

性能是数据库永恒的追求，对于性能有以下 Tips：

1. 数据库对硬件是有一定要求的，在老旧主机上运行自然远不如专用服务器上。
2. MySQL 有很多配置，比如内存分配、缓存区大小等，熟练使用后通过调整配置可以获得更好的性能表现。查看配置可以使用 `show variables;` 和 `show status;` 查看配置
3. 实现同样功能的不同语句有不同的性能表现，可以找到性能更好的方法。
4. 尽量不检索不需要的数据，比如能 `select param`，就不要 `select *`。
5. 一般组合查询比在 `select` 中使用 `or` 快。
6. 一般 `fulltext` 比 `like` 快。

















---
网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出，如果本文帮助到了你，别忘了点赞支持一下哦，你的点赞是我更新的最大动力！~


> 参考文档：
>
> 1. [《MySQL必知必会》](https://book.douban.com/subject/3354490/)
> 2. [MySQL 中文文档](https://www.mysqlzh.com/)

PS：本文收录在在下的博客 [Github - SHERlocked93/blog](https://github.com/SHERlocked93/blog) 系列文章中，欢迎大家关注我的公众号 `前端下午茶`，直接搜索即可添加或者点[这里](https://cdn.jsdelivr.net/gh/SHERlocked93/pic@master/uPic/TJt4p2-19-56-21.jpg)添加，持续为大家推送前端以及前端周边相关优质技术文，共同进步，一起加油~

另外可以加入「前端下午茶交流群」微信群，微信搜索  `sherlocked_93` 加我好友，备注**加群**，我拉你入群～
