# Git

[TOC]





- 工作区 Work
- 暂存区 Stage
- 仓库 Repository

### 撤销

#### 还未提交到暂存区

当修改还没有被`add`的时候，可以使用

```bash
git checkout -- filename.txt
```

来丢弃工作区的修改，当然也可以把后面的文件改成`*`来撤销所有文件的修改。注意这里用的是`--`，如果没有这个`--`的话就变成切换分支了。

#### 还未提交到仓库

如果你的修改已经被`add`到了`Stage`暂存区，但是还没有被`commit`，那么可以使用

```bash
git reset HEAD filename.txt
git checkout -- filename.txt
```

首先用`reset`来把修改撤回到工作区，再使用上面的`checkout`命令撤回工作区的修改。

#### 已经提交到仓库

则可以版本回退

```bash
git reset --hard HEAD~
```

这里的`--hard`表示强制回退，丢弃本地的修改。







#### 合并commit

如果已经`commit`了怎么办，如果要撤回目前的`commit`，可以把它合并到上一个`commit`中

```bash
git rebase -i HEAD~~
```

在出现的两个











---


网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出~

 


> 参考：
>
> 1. [廖雪峰 - Git教程](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)









