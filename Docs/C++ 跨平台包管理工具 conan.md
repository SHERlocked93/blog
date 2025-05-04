# 在 C++ 的 VS 项目中引入跨平台包管理工具 conan

我们知道 C++ 不像很多其他语言有包管理工具，比如 Python 有 pip，Java 有 maven，C# 有 nuget，JS 有 npm，Go 有 go mod，Rust 有 cargo，项目中需要自己手动引入第三方库，手动维护带来了很多麻烦。现在 C++ 也有了包管理工具，比如 VCpkg 和 conan，后者 conan 是跨平台的，支持 Windows、Linux、MacOS 等平台，并且支持多种编译器，本文介绍一下如何在项目中引入 conan。

1. [nlohmann::json](https://json.nlohmann.me/)/3.11.3
2. [sqlite3](https://github.com/sqlite/sqlite)/3.48.0

## 1. 包管理器 conan
### 1.1 最小化配置
#### 1.1.1 安装
Conan 基于 Python3 的工具，安装好 python3（3.6以上） 后，用 python 的 pip [安装 conan](https://docs.conan.io/2/installation.html) 很简单：

```bash
pip install conan             # windows/linux下
brew install conan            # macos下
```

#### 1.1.2 配置
conan 的配置文件有两种，一种是 `conanfile.txt` 文本文件相当于配置：

```bash
[requires]
nlohmann_json/3.11.3
sqlite3/3.48.0

[generators]
CMakeDeps
CMakeToolchain
```

这个配置文件用来配置我们需要的第三方库，比如指定版本的 nlohmann_json 和 sqlite3。然后 `generators` 为我们指定的生成器。

另一种是 `conanfile.py` 的 python 脚本文件，我们用这个脚本文件可以结合 python 代码获得更灵活的能力：

```python
from conan import ConanFile

class MyProjectConan(ConanFile):
    name = "mytestproj"
    version = "0.1"
    settings = "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        self.requires("nlohmann_json/3.11.3")
        self.requires("sqlite3/3.48.0", options={"shared": True})
```

在项目根目录下创建 `conanfile.py` 文件，在其中的 `requirements` 配置我们需要的第三方库。

> NOTE! 这两种配置文件是互斥的，只能选择一种。

如果只是比较轻量级使用，可以用 `conanfile.txt` 配置文件，否则一般用 `conanfile.py` 脚本文件，以获得最大自由度，比如我们可以写 python 代码将生成的 `.lib`、`.dll`、`.so` 和头文件等拷贝到指定目录下。

#### 1.1.3 安装第三方库
项目根目录下执行：

```bash
conan install .
```

之后 conan 会在文件根目录生成 `.cmake`、`.sh`、`.bat` 等等一堆文件，这些文件都是 conan 生成的，用来给项目引入第三方库的脚本文件，如何引入我们在后面介绍。

上面的方式会在根目录下生成一堆文件，一般我会在根目录下放一个 thridparty 目录，将 conan 生成的文件都放在这个目录下，这样方便管理，然后一些本地的第三方库或者驱动也用 `mklink /d` 命令创建软链接，指向对应文件夹，这样方便管理。

这是最小化配置的 conan 配置，我们可以在 `conanfile.txt` 或 `conanfile.py` 中配置更多的选项，比如指定第三方库的版本、指定第三方库的构建类型、指定第三方库的构建选项等等。

下面介绍一下在项目中如何引入 conan。

## 2 VS 项目中引入 conan

### 2.1 修改配置文件

为了指定 conan 将我们的第三方库生成到指定目录，并且在生成结束后，将生成的 `.dll` 动态库文件复制到可执行文件同级目录，需要对 `conanfile.py` 进行一些改动：

```python
import os
from conan import ConanFile
from conan.tools.files import copy


class MyProjectConan(ConanFile):
    name = "cef_131_mytest"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    generators = "MSBuildDeps", "MSBuildToolchain"

    def requirements(self):
        self.requires("nlohmann_json/3.11.3")
        self.requires("sqlite3/3.48.0", options={"shared": True})

    def layout(self):
        self.folders.generators = os.path.join("thirdparty", "conan")
        self.folders.build = os.path.join("thirdparty", "conan", "build")

    def deploy(self):
        print(f"  -->deploying env: arch={self.settings.arch}, build_type={self.settings.build_type}")

        source_dir = os.path.join(self.dependencies["sqlite3"].package_folder, "bin")
        print(f"  -->deploy source_dir: {source_dir}")

        # 动态生成目标路径（如 x64/Debug 或 x64/Release）
        arch = "x64" if self.settings.arch == "x86_64" else "x86"
        target_dir = os.path.join(os.getcwd(), arch, str(self.settings.build_type))
        print(f"  -->deploy target_dir: {target_dir}")

        # 复制 DLL 到项目输出目录
        dll_files = [f for f in os.listdir(source_dir) if f.endswith(".dll")]
        for dll_file in dll_files:
            print(f"    --> Copying {dll_file}")
            copy(self, dll_file, src=source_dir, dst=target_dir)
```

由于是 VS 项目，所以配置文件的 generators 使用的是 MSBuild 构建工具链。

然后在项目根目录下：


```bash
conan install . -s build_type=Debug --build=missing --deployer-package=*
```

如果是 Release 模式：

```bash
conan install . -s build_type=Release --build=missing --deployer-package=*
```

此时会在 `thirdparty/conan` 目录下生成 `conandeps.props` 等 VS 属性表，然后我们可以通过公共配置文件的方式引入生成的 VS 属性表，关于 VS 公共配置文件的使用方式参考 [<C++ 中 VS 项目引入公共配置文件>](https://juejin.cn/post/7500070714624540682) 

我们要引入的配置文件是 conan 在 install 的时候生成的 `conandeps.props`，在项目配置 `.vcxproj` 中加入：

```xml
<Import Project="$(SolutionDir)\thirdparty\conan\conandeps.props" Condition="exists('$(SolutionDir)\thirdparty\conan\conandeps.props')" Label="conandeps" />
```

![引入](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/202505031516860.png)

这个 `conandeps.props` 文件会导入 conan 给每个引入的第三方库生成的 props 配置文件：

![conandeps.props](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/202505031506521.png)

第三方库的 props 配置文件中会分别引入其 Debug 和 Rlease 版本的目录配置和变量配置，其中指定了将第三方库目录和包含目录存放的具体位置，在项目 `.vcxproj` 中引入 `conandeps.props` 之后重启 VS，就可以从 conan 的缓存目录里直接 `#include` 相应库的头文件了。 

> NOTE! 确保你的 cmake 命令是 Win 环境下的（如果也有 Cygwin 环境下的 cmake，将环境变量中的 `C:\Program Files\CMake\bin` 移动到前面），否则 conan 会找不到你的 VS 编译器。 ex:
>
> ![](https://raw.githubusercontent.com/SHERlocked93/pic/master/picgo/202505031539713.png)



[conan使用(一)--安装和应用 - 星星,风,阳光 - 博客园](https://www.cnblogs.com/xl2432/p/11873394.html)

[chu's blog - 从零开始的C++包管理器CONAN上手指南](http://chu-studio.com/posts/2019/%E4%BB%8E%E9%9B%B6%E5%BC%80%E5%A7%8B%E7%9A%84C++%E5%8C%85%E7%AE%A1%E7%90%86%E5%99%A8CONAN%E4%B8%8A%E6%89%8B%E6%8C%87%E5%8D%97)
