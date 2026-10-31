# Git学习笔记

最近公司的代码管理工具要从SVN转到Git上，因此虽然之前用过Git，但是都是一些简单的推送提交，因此还是有必要进行一些系统的学习，这里做一下笔记，以备后询，且不定期更新。

关于SVN和Git的比较已经有很多文章说过了，就不再赘述，本文的重点是如何使用**常用**的Git命令进行操作，冷门的就不说了，且比较零散，系统的学习推介廖雪峰的[Git教程](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)。

声明

1. 下面用户名都为`SHERlocked93`，请自行修改成自己的用户名

## 1. 概览

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/5ffd7a3d1d086ed11e65b270038bcb32fd924749016d39715274fc127e373363.png)

- 工作区 Workspace
- 暂存区 Stage / Index
- 本地仓库 Repository
- 远程仓库 Remote

## 2. 修改

### 2.1 暂存修改

操作一览

| 操作 | bash |
| --- | --- |
| 创建stash | git stash |
| 查看 | git stash list |
| 应用 | git stash apply stash@{`<num>`} |
| 删除 | git stash drop stash@{`<num>`} |
| 还原上一个暂存并删除暂存(如无conflict) | git stash pop |

如果在工作的时候出现了临时需要解决的问题，而你又不希望提交，那么有个`stash`功能

```text
git stash
```

在暂存后工作区会回退到最近的一个commit的状态，以便开建新分支；比如我们修复bug时，我们会通过创建新的bug分支进行修复，然后合并，最后删除；

当手头工作没有完成时，先把工作现场`git stash`一下，然后去修复bug，修复后，再`git stash pop`，回到工作现场。

### 2.2 撤销修改

#### 还未提交到暂存区

当修改还没有被`add`的时候，可以使用

```text
git checkout -- filename.txt
```

来丢弃工作区某文件的修改，当然也可以把后面的文件改成`*`来撤销所有文件的修改。这是用仓库的文件覆盖工作区的文件。注意这里用的是 `--`，如果没有 `--` 就变成切换分支。

注意这里用的是`--`，如果没有这个`--`的话就变成切换分支了。

#### 还未提交到仓库

如果你的修改已经被`add`到了暂存区，但是还没有被`commit`，那么可以使用

```text
git reset HEAD filename.txt
git checkout -- filename.txt
```

首先用`reset`来把修改撤回到工作区，再使用上面的`checkout`命令撤回工作区的修改。这里的`reset`相当于`add`的反操作。

#### 已经提交到仓库

则可以版本回退

```text
git reset --hard 15zdx2s
```

这里的`--hard`表示强制回退，丢弃本地的修改。这个回退比较野蛮，该版本号之后的提交都将不可见。

#### 撤销之前某一个提交

`git revert`撤销一个提交的同时会创建一个新的提交，这是一个安全的方法，因为它不会重写提交历史。但实现上和reset是完全不同的。它撤销这个提交引入的更改，然后在最后加上一个撤销了更改的新提交，而不是从项目历史中移除这个提交。

```text
git revert 46af7z6
```

相较于`reset` ，`revert`不会改变项目历史，对那些已经发布到共享仓库的提交来说这是一个安全的操作。其次`git revert` 可以将提交历史中的任何一个提交撤销、而`reset`会把历史上某个提交及之后所有的提交都移除掉，这太野蛮了。

相比 `reset`，它不会改变现在的提交历史。因此，`revert` 可以用在公共分支上，`reset` 应该用在私有分支上。

#### 合并commit

如果已经`commit`了怎么办，如果要撤回目前的`commit`，可以把它合并到上一个`commit`中

```text
git rebase -i HEAD~~
```

在出现的两个提交信息的`pick`改为`fixup`

## 3. 分支操作

### 3.1 创建/查看/合并分支

操作一览

| 操作 | bash |
| --- | --- |
| 查看分支 | git branch |
| 查看本地和远程分支 | git branch -a |
| 在target分支上创建分支，没有则从当前分支 | git branch `<branch-name>` `<target-branch>` |
| 创建并切换分支 | git checkout -b `<branch-name>` |
| 合并某分支到当前分支 | git merge `<branch-name>` |
| 删除分支，只能删参与了合并的 | git branch -d `<branch-name>` |
| 强行删除 | git branch -D `<branch-name>` |
| 删除远程分支 | git push origin :`<remote-branch-name>` |

创建分支

```text
# 创建新分支
git branch bug-fix
# 查看分支，-a查看本地和远程的分支，-r查看远程分支，-l或没有只查看本地
git branch -a
# 切换到刚刚创建的分支
git checkout bug-fix
```

上面两个步骤可以合并为

```text
# 创建并切换到分支
git checkout -b bug-fix
```

如果修改一下本地文件之后在这个分支继续培育一个版本之后，怎么去合并到主分支呢

```text
git add *
git commit -m "some change"
# 切换到主分支
git checkout master
# 合并分支
git merge bug-fix
# 删除分支 (可选)
git branch -d bug-fix
```

如果master分支和新的分支都各自培育了版本，那么自动合并通常会失败，发生冲突`conflict`，此时需要打开文件解决冲突之后`commit`一个版本以完成合并

```text
git add *
git commit -m "branch merge"
```

这里提一下，`merge`的时候有几个主要模式，`--no-ff`、`fast-forward`，其中`fast-forward`是默认的

1. `fast-forward`：在master开始的新分支前进了几个版本之后如果需要merge回来，此时master并没有前进，那么这个模式就是把HEAD与master指针指向新分支上，完成合并。这种情况如果删除分支，则会丢失分支信息，因为在这个过程中并没有创建commit。
2. `--no-ff`：关闭默认的`fast-forward`模式，也就是在merge的时候生成一个新的commit，这样在分支历史上就可以看出分支信息。

### 3.2 远程仓库操作

操作一览

| 操作 | bash |
| --- | --- |
| 克隆 | git clone `<url>` |
| 添加远程仓库 | git remote add `<name>` `<url>` |
| 删除远程仓库 | git remote rm `<name>` |
| 拉取 | git pull `<remote-branch-name>` `<local-branch-name>` |
| 推送本地所有分支到远程 | git push --all origin |
| 推送到远程同名分支 | git push origin `<local-branch-name>` |
| 推送本地分支到远程master | git push origin `<local-branch-name>`:`master` |
| 把当前本地分支推送并创建到远程 | git push origin |
| 检出远程分支 | git checkout -b `<new-local-branch-name>` origin/`<remote-branch-name>` |

关于各个分支，哪些需要推送呢

1. `master`分支是主分支，因此要时刻与远程同步；
2. `dev`分支是开发分支，团队所有成员都需要在上面工作，所以也需要与远程同步；
3. `bug`分支只用于在本地修复bug，就没必要推到远程了，除非老板要看看你每周到底修复了几个bug；
4. `feature`分支是否推到远程，取决于你是否和你的小伙伴合作在上面开发。

#### 直接`clone`

在github上创建一个新的项目之后，比如叫`learn-git`，那么可以直接`clone`下来，注意创建的时候不要选择 `Initialize this repository with a README`，我们要的是一个空的仓库

```text
git clone https://github.com/SHERlocked93/learn-git.git
```

这样在本地就直接创建了一个空的文件夹`learn-git`，当然里面有`.git`文件夹。<br>
也可以使用SSH地址来clone，速度会快一些，也不用每次推送都输入口令，推介使用这种

```text
git clone git@github.com:SHERlocked93/learn-git.git
```

添加一个文件`filename.txt`之后

```text
git add filename.txt
git commit -m "add filename.txt"
git push -u origin master
```

这样就把本地新建的文件push到了远程仓库

#### 本地与远程建立关联

如果已经有了本地工程文件夹，如何分享到github远程仓库呢，当然此时我们已经在github上创建了一个新的空白项目，还是叫`learn-git`，在本地文件夹中

```text
git init
# 关联远程库
git remote add origin git@github.com:SHERlocked93/learn-git.git
git push -u origin master
```

就可以了，如果你的远程仓库已经有了提交，那么在`push`之前需要

```text
# 允许不想干库合并
git pull origin master --allow-unrelated-histories
git push -u origin master
```

先拉取远程分支，注意这里`--allow-unrelated-histories`允许两个不想干的分支强行合并，再`push`；这样在github的网站上还能看到commit记录。

也可以强硬一点直接强行推送

```text
# -f 强行推送
git push -u origin master -f
```

这样本地仓库就直接把远程仓库覆盖了，且github上也看不到历史`commit`了，如果不想被同事枪击的话，还是推介上一种做法。

#### 同步远程仓库

那么已经clone的仓库如果希望同步原仓库新的提交怎么办

```text
# 从远程分支拉取代码到本地
git pull upstream master
# push到自己的库里
git push  origin master
```

### 3.3 多人协作

多人协作的工作模式通常是这样：

1. 首先，可以试图用`git push origin <branch-name>`推送自己的修改；
2. 如果推送失败，则因为远程分支比你的本地更新，需要先用git pull试图合并；
3. 如果合并有冲突，则解决冲突，并在本地提交；
4. 没有冲突或者解决掉冲突后，再用`git push origin <branch-name>`推送就能成功

从远程抓取分支，使用`git pull`，如果有冲突，要先处理冲突，`add->commit->push`。如果`git pull`提示no tracking information，则说明本地分支和远程分支的链接关系没有创建，用命令`git branch --set-upstream-to <branch-name> origin/<branch-name>`。

## 4. 标签操作

操作一览

| 操作 | bash |
| --- | --- |
| 查看所有标签 | git tag |
| 新建标签 | git tag `<tagname>` |
| 新建并制定说明 | git tag `<tagname>` -m `<message>` `<bash>` |
| 查看标签说明 | git show `<tagname>` |
| 删除标签 | git tag -d `<tagname>` |
| 推送某个标签到远程 | git push origin `<tagname>` |
| 推送所有未推送到远程的本地标签 | git push origin --tags |
| 合并远程仓库的标签到本地 | git pull origin --tags |
| 删除远程标签 | git push origin :refs/tags/`<tagname>` |

如果要删除远程分支，需要

```text
# 首先删除本地tag，假如tag是v0.9
git tag -d v0.9
# 再从远程删除
git push origin :refs/tags/v0.9
```

## 5. 提交格式

type：

- feat: 新特性，添加功能
- fix: 修改bug
- refactor: 代码重构
- docs: 文档修改
- style: 代码格式修改, 注意不是 css 修改
- test: 测试用例修改
- chore: 其他修改, 比如构建流程, 依赖管理.

---

> 推介阅读：
>
> 1. [廖雪峰 - Git教程](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)
> 2. [github实现本地仓库与远程仓库同步](https://link.segmentfault.com/?enc=EoWzU6QyRP8Gg9SjvPGjMQ%3D%3D.9OxS4CXuWHY4yQKKag3pLPqLy2JpT7gXMKVVlTc84m2FvNYLigH2uYoSlQc%2F6koAucJOEuT2s30BcW4IHtyqmQ%3D%3D)
> 3. [图解 Git 命令](https://link.segmentfault.com/?enc=D3r2gDnAxJID5Ja1%2BdP3dg%3D%3D.P%2FXbEQHWwN%2FN3uhJSx1%2Bjjnf59TadYxbcNkMSas70oKykUnlN4A36DUP3XUS7yQz%2FAqAlJ5FAqaME9L9JPDQQvtzHyR0d%2B6wNA6aZon6vVh7GLisBJJyNp5pPxU4LW0V)
> 4. [git基本操作，一篇文章就够了！](https://link.segmentfault.com/?enc=ItPpcjfBV%2Be8oADwsWaS%2FQ%3D%3D.o31RhRqM5T0Q7A22eNhYRYKYkb9mGxnLkssCLw5n90%2F5aFWTizpretxKIYCZBEkc)
> 5. [团队协作中的 Github flow 工作流程](https://link.segmentfault.com/?enc=KHhFIAguh%2BPC0BXpEYhEuw%3D%3D.VjgLAj4WRw6qaRBbxnZXScbSGJg0E0vQzhsQifix%2FY2jTdcZFxgIY7fXIMsxjn%2F0)
> 6. [git 命令大全](https://link.segmentfault.com/?enc=3A8pv3O2tCsvurSUqIKCWA%3D%3D.sBIUmrRbDb40BSMGoMbTNCdDHGOTtRr9xmuptPfUMl%2Fs89yCnigcsc7%2BTVLQxCzauSmILFsXE%2FhpDqqnQerQ8Q%3D%3D)

附件

1. Git常用命令速查表：<br>
   ![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/c3cfcb45dec46f4a0e59385078a94c092645f77b392508e9b7d02211e030e9f2.png)
