+++
date = '2025-06-04T21:11:19+08:00'
draft = true
title = 'cmake'

+++

# CMKAE 

## CMake 使用方法

### 打印详细信息

``` she
make VERBOSE=1
```
### visual studio code 中使用CMake
``` 
vcproj2cmake.rb 可以根据 Visual Studio 的工程文件（后缀名是 .vcproj 或 .vcxproj）生成 CMakeLists.txt 文件。
```

## 基本语法

### cmake 编译

一个最基本的CmakeLists.txt文件最少包含以下三行：
``` cmake
cmake_minimum_required(VERSION 3.10)
project(HelloWorld)
add_executable(HelloWorld main.cpp)
# cmake_minimum_required(VERSION 3.10)：指定CMake的最低版本要求。
# project(HelloWorld)：指定项目的名称。
# add_executable(HelloWorld main.cpp)：添加可执行文件，其中HelloWorld是可执行文件的名称，main.cpp是源文件的名称。
```

cpp文件样例```Tutorial.cpp```

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stdout, "Usage: %s <number>\n", argv[0]);
        return 1;
    }

    double number = atof(argv[1]);
    double outputValue = sqrt(number);
    fprintf(stdout, "The square root of %.2f is %.2f\n", number, outputValue);
    
    return 0;
}
```



**注意**

cmake中系统指令是不区分大小写的，但是变量和字符串需要区分大小写

### 添加版本号

``` set(KEY VALUE)``` 接受两个参数，用来声明变量，cmake中需要通过```${KEY}```来获取到VALUE。

``` cmake
cmake_minimum_required(VERSION 3.10)
project(Tutorial)
# The version number.
set(Tutorial_VERSION_MAJOR 1)
set(Tutorial_VERSION_MINOR 0)

# configure a header file to pass some of the CMake settings
# to the source code
configure_file(
    "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
    "${PROJECT_BINARY_DIR}/TutorialConfig.h"
)

# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
include_directories("${PROJECT_BINARY_DIR}")

# add the executable
add_executable(Tutorial tutorial.cpp)
```

配置文件将会被写入到可执行文件的目录下，所以项目中必须包含这个文件夹来使用这些配置头文件。在工程目录下新建一个```TutorialConfig.h.in```，内容如下：

```cpp
// the configuration file for the tutorial project
// This file is used to generate the TutorialConfig.h file
#define TUTORIAL_VERSION_MAJOR @TUTORIAL_VERSION_MAJOR@
#define TUTORIAL_VERSION_MINOR @TUTORIAL_VERSION_MINOR@
```

上面的代码中的```@Tutorial_VERSION_MAJOR@```和```@Tutorial_VERSION_MINOR@```将会被替换为```CmakeLists.txt```中的0和1/然后修改```Tutorial.cpp```文件如下，用来在不输入额外参数的情况下输出版本信息

### 构建自己的库

新建一个目录```mathfunction```的子目录中，在该目录下新建```CMakeLists.txt```文件，包含以下代码：

``` cmake
add_library(MathFunctions mysqrt.cpp)
```

生成如下结构内容

```cpp
/*
.
├── CMakeLists.txt
├── MathFunctions
│   ├── CMakeLists.txt
│   ├── MathFunctions.h
│   └── mysqrt.cpp
├── TutorialConfig.h.in
└── tutorial.cpp
*/
// MathFunctions.h
double mysqrt(double x);
// mysqrt.cpp
#include "MathFunctions.h"
#include <stdio.h>

// a hack to get around the fact that we can't #include <cmath>
double mysqrt(double x) {
    if (x <= 0) {
        return 0;
    }

    double result;
    double delta;
    result = x;

    // do ten iterations
    for (int i = 0; i < 10; i++) {
        if (result <= 0) {
            result = 0.1;
        }
        delta = x - (result * result);
        result = result + 0.5 * delta / result;
        fprintf(stdout, "Iteration %d: result = %.2f\n", i, result);
    }

    return result;
}
```

跟目录下CMakeLists.txt 文件添加如下内容，引入我们自定义的库

``` cmake
include_directories ("${PROJECT_SOURCE_DIR}/MathFunctions")
add_subdirectory (MathFunctions) 
 
# add the executable
add_executable (Tutorial tutorial.cxx)
target_link_libraries (Tutorial MathFunctions)
```

### 构建可选选项

```MathFunctions```是我们自己构建的库，在构建大型项目时，有些库不需要引入，我们可以添加一个开关

在源cmake文件中添加如下代码：

```cmake
option (USE_MYMATH
				"Use tutorial provided math implementation" ON)
				
if (USE_MYMATH)
	include_directories("${PROJECT_SOURCE_DIR}/mathfunction")
	add_subdirectory(mathfunction)
	set(EXTRA_LIBS ${EXTRA_LIBS} MathFunctions)
endif (USE_MYMATH)
```

### 设置安装规则

通过下面两行可以引入静态库和头文件来进行安装

```cmake
# 安装编译生成的静态库到系统bin目录
# TARGETS指定要安装的目标(这里是MathFunctions库)
# DESTINATION指定安装路径，bin是可执行文件/库的标准安装目录
install (TARGETS MathFunctions DESTINATION bin)

# 安装头文件到系统include目录
# FILES指定要安装的头文件
# include目录是头文件的标准安装位置，便于其他项目引用
install (FILES MathFunctions.h DESTINATION include)
```



