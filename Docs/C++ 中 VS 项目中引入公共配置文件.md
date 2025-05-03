# C++ 中 VS 项目引入公共配置文件

在用 VS 做一个包含多个项目的解决方案的项目时，经常会遇到多个项目需要引入相同的配置的情况，如 C++ 版本、附加库目录、附加包含目录等，可以使用本文提供的方法来引入公共配置文件避免重复配置。

## 1. 将第三方库和驱动目录通过软连接配置到项目中

对于项目中需要引入的一些本地安装的硬件驱动和库，如 `OpenSSL` 驱动、第三方硬件驱动库等，由于每个人安装的驱动位置可能不一样，或者电脑上安装了多个版本的驱动等情况（比如我的电脑上就安装了多个版本的 OpenSSL 驱动），可以通过软连接的方式，将这些第三方库和驱动的头文件和库文件地址链接到项目目录的固定位置，这样就可以在项目中通过 VS 的宏（如解决方案目录 `SolutionDir`、运行模式 `Configuration` 等）配置的库目录和包含目录来引入这些第三方库和驱动。

比如我电脑上的 `OpenSSL@1.1.1(x64)` 的目录是 `C:\Program Files\OpenSSL-Win64-1_1_1`，可以将其放软连接到项目的 `thirdparty` 目录下：

```bash
mklink /d "C:\Projects\hello_sln\thirdparty\OpenSSL-Win64" "C:\Program Files\OpenSSL-Win64-1_1_1"
```

这样在项目中就可以通过宏 `$(SolutionDir)..\thirdparty\OpenSSL-Win64\include` 来引入 `OpenSSL-Win64` 的头文件目录。

项目文件组织：

```bash
hello_sln
├── app
    ├── CommonSettings.props
    └── hello_sln.sln
├──lib
    └──  hello_proj
        ├── hello_sln.vcxproj.filters
        └── hello_proj.vcxproj 
└── thirdparty
    ├── OpenSSL-Win64 -> C:\Program Files\OpenSSL-Win64-1_1_1
    └── boost -> C:\local\boost_1_83_0
```

## 2. 配置第三方库和驱动目录

一般在 VS 的解决方案下创建一个项目时，我们通常会需要在项目属性中对该项目的一些属性进行配置，比如要用的 C++ 语言版本、附加库目录、附加包含目录等等。

![项目属性页](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/202505031432414.png)

如果一个解决方案下有多个项目，每个项目都需要对这些属性进行配置，就会很麻烦，可不可以创建一个公共配置文件，然后在每个项目中引入这个公共配置文件，这样就可以避免重复配置呢。

答案是肯定的，VS 提供了 `.props` 公共配置文件，然后在每个项目中引入这个公共配置文件，这个配置文件可以当成项目配置文件 `.vcxproj` 的补充配置，这[两个文件的结构是一致的](https://learn.microsoft.com/zh-cn/cpp/build/reference/vcxproj-file-structure?view=msvc-170)，可以通过在 `.vcxproj` 引入我们的 `.props` 公共配置文件让 VS 加载项目的时候合并这两个文件，从而避免重复配置。

## 3. 创建 props 公共配置文件

然后在解决方案根目录下创建一个 `CommonSettings.props` 文件，内容如下：

```xml
<?xml version="1.0" ?>
<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003" ToolsVersion="4.0">
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Debug|x64'">
    <ClCompile>
       <LanguageStandard>stdcpp17</LanguageStandard>
       <PreprocessorDefinitions>_HELLO</PreprocessorDefinitions>
      <AdditionalIncludeDirectories>$(SolutionDir)..\thirdparty;$(SolutionDir)..\thirdparty\OpenSSL-Win64\include</AdditionalIncludeDirectories>
    </ClCompile>
    <Link>
      <AdditionalLibraryDirectories>$(SolutionDir)..\thirdparty\OpenSSL-Win64\lib\VC</AdditionalLibraryDirectories>
    </Link>
  </ItemDefinitionGroup>
</Project>
```

> 这里仅加入了 64 位 Debug 模式的配置，Release 模式的配置可以自己添加。

比如我们希望所有项目都用 C++17 标准，所有项目都需要预处理器定义 `_HELLO`，附加包含目录引入 `thridparty` 第三方库和驱动目录，附加库目录引入 `OpenSSL-Win64/lib/VC` 目录。就可以用 `LanguageStandard` 配置其语言，用 `PreprocessorDefinitions` 配置预处理器定义，然后用 `AdditionalIncludeDirectories` 配置附加包含目录，用 `AdditionalLibraryDirectories` 配置附加库目录，这几个是大部分项目中的重复配置。

然后在项目的配置文件 `hello_proj.vcxproj` 增加这个公共配置文件的路径配置：

```xml
  <Import Project="$(SolutionDir)\CommonSettings.props" Condition="exists('$(SolutionDir)\CommonSettings.props')" Label="LocalCommonSettings" />
```

像这样：

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/202502141035372.png)

然后我们重新加载项目，或者重启 VS，就可以看到项目的属性配置中已经引入了这个公共配置文件的配置了。

![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/202505021834557.png)

项目从我们的 `CommonSettings.props` 公共配置文件中继承了配置，后面给新增的项目的 `.vcxproj` 开头增加 `CommonSettings.props` 的配置就可以引入我们的公共配置，如果引入了新的公共第三方驱动和库，通过在 `CommonSettings.props` 中增加配置即可。

---


网上的帖子大多深浅不一，甚至有些前后矛盾，在下的文章都是学习过程中的总结，如果发现错误，欢迎留言指出，如果本文帮助到了你，别忘了点赞支持一下，你的点赞是我更新的最大动力！~

> 参考文档：
>
> 1. [.vcxproj 和 .props 文件结构 | Microsoft Learn](https://learn.microsoft.com/zh-cn/cpp/build/reference/vcxproj-file-structure?view=msvc-170)

PS：本文同步更新于在下的博客 [Github - SHERlocked93/blog](https://link.juejin.cn?target=https%3A%2F%2Fgithub.com%2FSHERlocked93%2Fblog) 系列文章中，欢迎大家关注我的公众号 `CPP下午茶`，直接搜索即可添加，持续为大家推送 CPP 以及 CPP 周边相关优质技术文，共同进步，一起加油~

另外可以加入「前端下午茶交流qun」，vx 搜索  `sherlocked_93` 加我，备注 **1**，我拉你～