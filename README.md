# HH's Blog

基于 [Hugo](https://gohugo.io/) 和 [Hugo Theme Stack](https://github.com/CaiJimmy/hugo-theme-stack) 构建的个人博客。

## 目录结构

```
├── archetypes/        # 内容模板
├── assets/            # 静态资源（SCSS、JS、图片等）
├── content/           # 博客内容
│   ├── page/          # 页面（关于、归档、链接、搜索）
│   ├── post/          # 博客文章
│   └── categories/    # 分类页面
├── img/               # 图片资源
├── layouts/           # 布局模板
├── public/            # 生成的静态文件
├── resources/         # Hugo 资源文件
├── themes/            # 主题
└── hugo.yaml          # Hugo 配置文件
```

## 博客分类

### 主要分类

| 分类 | 目录 | 说明 |
|------|------|------|
| AI Daily | `content/post/AI-Daily/` | AI 领域每日资讯与论文解读 |
| Rust 每日学习 | `content/post/rust-daily/` | Rust 语言学习记录 |
| Rust 周刊 | `content/post/rust-weekly/` | Rust 社区周刊汇总 |
| 学习路线 | `content/post/learning-roadmap/` | 技术学习路线规划 |
| CMake | `content/post/Cmake/` | CMake 构建工具相关 |
| 编程 | `content/post/Coding/` | 编程相关文章 |
| DDD | `content/post/DDD/` | 领域驱动设计 |
| 股票日报 | `content/post/stock-daily/` | 股票分析与报告 |

### Front Matter 分类设置

在文章的 Front Matter 中使用 `categories` 字段：

```yaml
---
title: "文章标题"
date: 2026-03-05
draft: false
tags: ['标签1', '标签2']
categories: ['AI Daily']
---
```

## 构建博客

### 环境要求

- Hugo Extended (>= 0.110.0)
- Go (用于主题模块)

### 本地开发

```bash
# 启动本地服务器
hugo server -D

# 访问 http://localhost:1313
```

### 构建静态文件

```bash
# 构建生产版本
hugo --minify

# 输出目录：public/
```

## 添加新博客

### 方法一：使用 archetypes（推荐）

```bash
# 创建新文章（会使用 archetypes/default.md 模板）
hugo new content/post/分类目录/文章名.md
```

### 方法二：手动创建

1. 在 `content/post/分类目录/` 下创建新目录
2. 在新目录中创建 `index.md` 文件
3. 使用以下 Front Matter 模板：

```yaml
+++
date = '2026-03-05T20:30:00+08:00'
draft = false
title = '文章标题'
tags = ['标签1', '标签2']
categories = ['分类名称']
+++

## 文章内容

在这里编写文章内容...
```

### 添加新分类

1. 在 `content/post/` 下创建新目录
2. 创建 `_index.md` 文件作为分类索引：

```yaml
+++
title = '分类名称'
description = '分类描述'
+++
```

3. 在 `hugo.yaml` 的 `mainSections` 中添加新分类：

```yaml
params:
    mainSections:
        - post
        - learning-roadmap
        - rust-daily
        - 新分类名称
```

## 主要功能

- **多语言支持**：中文、英文、阿拉伯文
- **暗色模式**：支持自动切换
- **搜索功能**：全文搜索
- **评论系统**：Giscus (基于 GitHub Discussions)
- **数学公式**：支持 KaTeX
- **代码高亮**：支持多种语言
- **图片处理**：自动优化封面图

## 部署

博客通过 GitHub Actions 自动部署到 GitHub Pages：

1. 推送代码到 `master` 分支
2. GitHub Actions 自动构建
3. 部署到 `https://HHjoker.github.io`

## 常用命令

```bash
# 创建新文章
hugo new content/post/分类/文章名.md

# 本地预览
hugo server -D

# 构建生产版本
hugo --minify

# 清理缓存
hugo clean
```

## 参考链接

- [Hugo 官方文档](https://gohugo.io/documentation/)
- [Hugo Theme Stack](https://stack.jimmycai.com/)
- [Markdown 语法](https://www.markdownguide.org/)
