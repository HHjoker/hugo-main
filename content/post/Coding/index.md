+++
date = '2025-02-09T22:07:19+08:00'
lastmod = '2026-03-04T16:15:00+08:00'
draft = false
title = 'Cpp Testing: GTest & GMock 完整指南'
tags = ['C++', 'Testing', 'GTest', 'GMock', 'Unit Test']
categories = ['Programming', 'C++']
+++

# C++ 测试框架：GTest & GMock 完整指南

本文结合 [GoogleTest 官方文档](https://google.github.io/googletest/) 整理，涵盖 GTest 基础断言、测试fixture、GMock 模拟对象等核心内容。

---

## 目录

1. [为什么使用 GoogleTest](#为什么使用-googletest)
2. [基本概念](#基本概念)
3. [断言 (Assertions)](#断言-assertions)
4. [简单测试](#简单测试)
5. [测试 Fixture](#测试-fixture)
6. [GMock 模拟对象](#gmock-模拟对象)
7. [MOCK_METHOD 语法](#mock_method-语法)
8. [EXPECT_CALL 详解](#expect_call-详解)
9. [完整示例](#完整示例)
10. [最佳实践](#最佳实践)

---

## 为什么使用 GoogleTest?

GoogleTest 是 Google 开发的 C++ 测试框架，它帮助你编写更好的 C++ 测试。

**好的测试应该是：**

- **独立且可重复** - 每个测试应该独立运行，不依赖其他测试
- **组织良好** - 测试应该反映被测代码的结构
- **可移植和可复用** - 跨平台、跨编译器工作
- **提供详细信息** - 失败时提供尽可能多的问题信息
- **自动化** - 自动跟踪所有测试，无需手动枚举
- **快速** - 可以在测试间共享资源，减少设置/清理开销

---

## 基本概念

### 术语对照

| GoogleTest 术语 | ISTQB 标准术语 | 含义 |
|----------------|---------------|------|
| `TEST()` | Test Case (测试用例) | 执行特定程序路径并验证结果 |
| `TEST_SUITE` | Test Suite (测试套件) | 相关测试的分组 |

> ⚠️ **注意**: GoogleTest 早期使用 `TestCase` 术语，现在推荐使用 `TestSuite`。

### 核心概念层次

```
测试程序 (Test Program)
  └── 测试套件 (Test Suite)
      └── 测试 (Test)
          └── 断言 (Assertion)
```

- **断言 (Assertion)**: 检查条件是否为真的语句
- **测试 (Test)**: 包含多个断言的函数
- **测试套件 (Test Suite)**: 包含多个相关测试的组
- **测试程序**: 包含多个测试套件的可执行文件

---

## 断言 (Assertions)

### ASSERT_* vs EXPECT_*

| 类型 | 失败时行为 | 使用场景 |
|------|-----------|---------|
| `ASSERT_*` | **致命失败**，立即中止当前函数 | 后续代码依赖此断言成功时使用 |
| `EXPECT_*` | **非致命失败**，继续执行 | 希望一次测试报告多个错误时使用 |

**推荐**: 优先使用 `EXPECT_*`，除非断言失败后继续执行没有意义。

### 常用断言宏

#### 布尔条件

```cpp
EXPECT_TRUE(condition);    // 验证条件为真
EXPECT_FALSE(condition);   // 验证条件为假
```

#### 数值比较

```cpp
EXPECT_EQ(expected, actual);    // expected == actual
EXPECT_NE(val1, val2);          // val1 != val2
EXPECT_LT(val1, val2);          // val1 < val2
EXPECT_LE(val1, val2);          // val1 <= val2
EXPECT_GT(val1, val2);          // val1 > val2
EXPECT_GE(val1, val2);          // val1 >= val2
```

#### 字符串比较

```cpp
EXPECT_STREQ(str1, str2);   // C 字符串相同
EXPECT_STRNE(str1, str2);   // C 字符串不同
EXPECT_STRCASEEQ(str1, str2);  // 忽略大小写
```

#### 自定义失败消息

```cpp
ASSERT_EQ(x.size(), y.size()) << "Vectors x and y are of unequal length";

for (int i = 0; i < x.size(); ++i) {
    EXPECT_EQ(x[i], y[i]) << "Vectors x and y differ at index " << i;
}
```

---

## 简单测试

使用 `TEST()` 宏定义测试：

```cpp
TEST(TestSuiteName, TestName) {
    // ... test body ...
}
```

### 示例：阶乘函数测试

```cpp
// 被测函数
int Factorial(int n); // Returns the factorial of n

// 测试套件
TEST(FactorialTest, HandlesZeroInput) {
    EXPECT_EQ(Factorial(0), 1);
}

TEST(FactorialTest, HandlesPositiveInput) {
    EXPECT_EQ(Factorial(1), 1);
    EXPECT_EQ(Factorial(2), 2);
    EXPECT_EQ(Factorial(3), 6);
    EXPECT_EQ(Factorial(8), 40320);
}
```

**命名规则**: 
- 第一个参数是测试套件名（一般性）
- 第二个参数是测试名（具体性）
- 都不应包含下划线 `_`

---

## 测试 Fixture

当多个测试需要使用相似数据时，使用测试夹具 (Test Fixture)。

### 创建步骤

1. 从 `testing::Test` 派生一个类
2. 在 `protected:` 部分声明要使用的对象
3. 编写 `SetUp()` 函数准备每个测试
4. 必要时编写 `TearDown()` 函数清理资源

### 示例：队列测试

```cpp
template <typename E>
class Queue {
public:
    Queue();
    void Enqueue(const E& element);
    E* Dequeue();  // Returns NULL if empty
    size_t size() const;
};

// 定义测试夹具
class QueueTest : public testing::Test {
protected:
    QueueTest() {
        // q0_ 保持空
        q1_.Enqueue(1);
        q2_.Enqueue(2);
        q2_.Enqueue(3);
    }

    Queue<int> q0_;
    Queue<int> q1_;
    Queue<int> q2_;
};

// 使用 TEST_F 运行测试
TEST_F(QueueTest, IsEmptyInitially) {
    EXPECT_EQ(q0_.size(), 0);
}

TEST_F(QueueTest, DequeueWorks) {
    int* n = q0_.Dequeue();
    EXPECT_EQ(n, nullptr);

    n = q1_.Dequeue();
    ASSERT_NE(n, nullptr);
    EXPECT_EQ(*n, 1);
    EXPECT_EQ(q1_.size(), 0);
    delete n;
}
```

**重要**: 
- 每个测试都有独立的 fixture 对象
- GoogleTest 在测试间不重用 fixture
- 一个测试对 fixture 的修改不影响其他测试

---

## GMock 模拟对象

### 什么是 Mock?

**Mock 对象**是预先编程的对象，其行为规范了它们预期接收的调用。

| 类型 | 说明 |
|------|------|
| **Fake** | 有工作实现但走捷径（如内存文件系统） |
| **Mock** | 预先编程期望值，形成调用规范 |

### 为什么使用 gMock?

- 移除测试中不必要的依赖
- 使测试更快、更可靠
- 测试难以触发的错误场景
- 验证模块间的交互方式

---

## MOCK_METHOD 语法

### 现代语法 (推荐)

```cpp
MOCK_METHOD(返回类型，方法名，(参数列表), (限定符));
```

### 示例

```cpp
class MockTurtle : public Turtle {
public:
    MOCK_METHOD(void, PenUp, (), (override));
    MOCK_METHOD(void, PenDown, (), (override));
    MOCK_METHOD(void, Forward, (int distance), (override));
    MOCK_METHOD(void, Turn, (int degrees), (override));
    MOCK_METHOD(void, GoTo, (int x, int y), (override));
    MOCK_METHOD(int, GetX, (), (const, override));
    MOCK_METHOD(int, GetY, (), (const, override));
};
```

### 参数说明

```cpp
MOCK_METHOD(ReturnType, MethodName, (Arg1, Arg2, ...), (Qualifiers));
```

| 参数位置 | 说明 |
|---------|------|
| 1 | 返回类型 |
| 2 | 方法名称 |
| 3 | 参数类型列表 (必须用括号包裹) |
| 4 | 限定符：`override`, `(const)`, `(const, override)` 等 |

### 旧语法 (不推荐，但兼容)

```cpp
MOCK_METHOD0(MethodName, ReturnType());      // 0 个参数
MOCK_METHOD1(MethodName, ReturnType(Arg1));  // 1 个参数
MOCK_METHOD2(MethodName, ReturnType(Arg1, Arg2)); // 2 个参数
```

---

## EXPECT_CALL 详解

### 基本语法

```cpp
EXPECT_CALL(mock_object, method_name(matchers))
    .Times(cardinality)
    .WillOnce(action)
    .WillRepeatedly(action);
```

### 调用次数 (Cardinality)

| 修饰符 | 说明 |
|--------|------|
| `.Times(n)` | 恰好调用 n 次 |
| `.Times(AtLeast(n))` | 至少调用 n 次 |
| `.Times(AtMost(n))` | 最多调用 n 次 |
| `.Times(AnyNumber())` | 任意次数 |
| `.WillOnce(action)` | 下一次调用的行为 |
| `.WillRepeatedly(action)` | 之后所有调用的行为 |

### 常用 Action

```cpp
Return(value)           // 返回值
ReturnNull()            // 返回 nullptr
ReturnRef(variable)     // 返回引用
Throw(exception)        // 抛出异常
SetArgPointee<n>(value) // 设置第 n 个指针参数的值
```

### Matcher (匹配器)

```cpp
Eq(value)        // 等于
Ne(value)        // 不等于
Lt(value)        // 小于
Gt(value)        // 大于
Le(value)        // 小于等于
Ge(value)        // 大于等于
IsNull()         // 是 nullptr
NotNull()        // 不是 nullptr
_                // 通配符 (任意值)
```

---

## 完整示例

### 被测代码

```cpp
// turtle.h - 原始接口
#ifndef _TURTLE_H_
#define _TURTLE_H_

class Turtle {
public:
    virtual ~Turtle() {}
    virtual void PenUp() = 0;
    virtual void PenDown() = 0;
    virtual void Forward(int distance) = 0;
    virtual void Turn(int degrees) = 0;
    virtual void GoTo(int x, int y) = 0;
    virtual int GetX() const = 0;
    virtual int GetY() const = 0;
};

#endif
```

```cpp
// painter.h - 使用 Turtle 的类
#ifndef _PAINTER_H_
#define _PAINTER_H_

class Painter {
private:
    Turtle* turtle_;
public:
    Painter(Turtle* t) : turtle_(t) {}
    
    bool DrawCircle(int x, int y, int radius) {
        turtle_->PenDown();
        turtle_->GoTo(x, y);
        // ... 画圆逻辑
        return true;
    }
    
    int DrawXandY() {
        return turtle_->GetX() + turtle_->GetY();
    }
};

#endif
```

### Mock 类定义

```cpp
// mock_turtle.h
#ifndef _MOCK_TURTLE_H_
#define _MOCK_TURTLE_H_

#include "turtle.h"
#include <gmock/gmock.h>

class MockTurtle : public Turtle {
public:
    MOCK_METHOD(void, PenUp, (), (override));
    MOCK_METHOD(void, PenDown, (), (override));
    MOCK_METHOD(void, Forward, (int distance), (override));
    MOCK_METHOD(void, Turn, (int degrees), (override));
    MOCK_METHOD(void, GoTo, (int x, int y), (override));
    MOCK_METHOD(int, GetX, (), (const, override));
    MOCK_METHOD(int, GetY, (), (const, override));
};

#endif
```

### 测试代码

```cpp
// painter_test.cpp
#include "painter.h"
#include "mock_turtle.h"
#include <gtest/gtest.h>
#include <gmock/gmock.h>

using ::testing::AtLeast;
using ::testing::Return;
using ::testing::Eq;

TEST(PainterTest, DrawCircleTest) {
    // 创建 mock 对象
    MockTurtle turtle;
    
    // 设置期望：PenDown 至少调用 1 次
    EXPECT_CALL(turtle, PenDown())
        .Times(AtLeast(1));
    
    // 设置期望：GoTo 调用 1 次，参数为 (0, 0)
    EXPECT_CALL(turtle, GoTo(0, 0))
        .Times(1);
    
    Painter painter(&turtle);
    EXPECT_TRUE(painter.DrawCircle(0, 0, 10));
}

TEST(PainterTest, DrawXandYTest) {
    MockTurtle turtle;
    
    // 设置返回值
    EXPECT_CALL(turtle, GetX())
        .WillOnce(Return(10));
    EXPECT_CALL(turtle, GetY())
        .WillOnce(Return(20));
    
    Painter painter(&turtle);
    EXPECT_EQ(30, painter.DrawXandY());
}

TEST(PainterTest, MultipleCallsTest) {
    MockTurtle turtle;
    
    // 第一次调用返回 5，之后都返回 10
    EXPECT_CALL(turtle, GetX())
        .WillOnce(Return(5))
        .WillRepeatedly(Return(10));
    
    Painter painter(&turtle);
    EXPECT_EQ(5, painter.DrawXandY());   // 第一次
    EXPECT_EQ(10, painter.DrawXandY());  // 第二次
    EXPECT_EQ(10, painter.DrawXandY());  // 第三次
}
```

### CMakeLists.txt 配置

```cmake
enable_testing()

# 查找 GTest
find_package(GTest REQUIRED)
find_package(GMock REQUIRED)

# 创建测试可执行文件
add_executable(painter_test
    painter_test.cpp
    painter.cpp
)

# 链接库
target_link_libraries(painter_test
    GTest::gtest
    GTest::gtest_main
    GTest::gmock
    GTest::gmock_main
)

# 包含 GTest
include(GoogleTest)
gtest_discover_tests(painter_test)
```

---

## 最佳实践

### 1. 期望值设置时机

> ⚠️ **重要**: gMock 要求在调用 mock 函数**之前**设置期望值，否则行为未定义。

```cpp
// ✅ 正确
EXPECT_CALL(turtle, GetX()).WillOnce(Return(10));
int x = turtle.GetX();

// ❌ 错误
int x = turtle.GetX();
EXPECT_CALL(turtle, GetX()).WillOnce(Return(10));
```

### 2. 不要交替使用 EXPECT_CALL 和调用

```cpp
// ❌ 错误
EXPECT_CALL(turtle, GetX()).WillOnce(Return(10));
int x1 = turtle.GetX();
EXPECT_CALL(turtle, GetX()).WillOnce(Return(20));  // 不应该在调用后再次设置
int x2 = turtle.GetX();

// ✅ 正确
EXPECT_CALL(turtle, GetX())
    .WillOnce(Return(10))
    .WillOnce(Return(20));
int x1 = turtle.GetX();
int x2 = turtle.GetX();
```

### 3. 使用 EXPECT_* 而非 ASSERT_*

```cpp
// ✅ 推荐：可以继续测试其他条件
EXPECT_EQ(x.size(), y.size());
for (int i = 0; i < x.size(); ++i) {
    EXPECT_EQ(x[i], y[i]);
}

// ⚠️ 仅在必要时使用 ASSERT_*
ASSERT_NE(ptr, nullptr);  // 如果 ptr 为 null，后续代码会崩溃
EXPECT_EQ(*ptr, 10);
```

### 4. Mock 类放置位置

- 如果接口是你自己的：放在 `_test.cc` 或单独的测试头文件
- 如果接口是别人的：放在接口的包/目录中，避免接口变更导致测试破裂

### 5. 测试命名规范

```cpp
// 好的命名
TEST(FactorialTest, HandlesZeroInput)
TEST(FactorialTest, HandlesPositiveInput)
TEST(FactorialTest, HandlesNegativeInput)

// 避免的命名
TEST(FactorialTest, test1)  // 无意义
TEST(FactorialTest, test_factorial)  // 冗余
```

---

## 参考资源

- [GoogleTest 官方文档](https://google.github.io/googletest/)
- [GoogleTest Primer](https://google.github.io/googletest/primer.html)
- [gMock for Dummies](https://google.github.io/googletest/gmock_for_dummies.html)
- [gMock Cookbook](https://google.github.io/googletest/gmock_cook_book.html)
- [断言参考](https://google.github.io/googletest/reference/assertions.html)

---

**最后更新**: 2026-03-04
