# Hugo 博客评论系统配置指南

## 已支持的评论系统

你的博客主题 (hugo-theme-stack) 已经内置了多种评论系统支持：

### 商业评论系统
- **Disqus** - 最流行，但有广告
- **Commentix**
- **Hyvor Talk**
- **IntenseDebate**

### 开源评论系统（推荐）
- **Giscus** ⭐ - 基于 GitHub Discussions，免费无广告
- **Utterances** - 基于 GitHub Issues
- **Waline** - 基于 LeanCloud
- **Twikoo** - 基于腾讯云
- **Remark42** - 自托管
- **Cactus Comments** - 基于 Matrix 协议

---

## 推荐方案：Giscus（已配置）

### 为什么选择 Giscus？

✅ **完全免费** - 无广告、无追踪  
✅ **无需数据库** - 数据存储在 GitHub Discussions  
✅ **开源** - 代码公开透明  
✅ **自定义主题** - 支持多种主题  
✅ **多语言** - 支持中文  
✅ **自动同步** - 新评论自动显示  
✅ **可自托管** - 数据完全可控  

### 工作原理

1. 访客通过 GitHub OAuth 授权在网站上留言
2. 评论以 GitHub Discussion 的形式存储
3. 你可以在 GitHub 上管理/删除评论
4. 访客也可以直接在 GitHub 上评论

---

## 配置步骤

### 第一步：启用 GitHub Discussions

1. 打开你的博客仓库：https://github.com/HHjoker/HHjoker.github.io
2. 点击 **Settings** → **General**
3. 找到 **Features** 部分
4. 勾选 **Discussions** → 点击 **Set up discussions**
5. 选择分类（推荐用 **Announcements** 类型）

### 第二步：安装 Giscus App

1. 访问 https://github.com/apps/giscus
2. 点击 **Install**
3. 选择你的仓库 `HHjoker/HHjoker.github.io`
4. 确认安装

### 第三步：获取配置信息

1. 访问 https://giscus.app/zh-CN
2. 填写配置：
   - **仓库**: `HHjoker/HHjoker.github.io`
   - **仓库 ID**: (在仓库页面 F12 查看，或从 giscus.app 获取)
   - **分类**: `Announcements` (或你创建的分类名)
   - **分类 ID**: (在分类页面 F12 查看)
   - **映射方式**: `pathname` (推荐)
   - **语言**: `zh-CN`
   - **主题**: `preferred_color_scheme` (跟随系统)

3. 点击 **Generate** 生成配置

### 第四步：更新 Hugo 配置

修改 `hugo.yaml` 中的 `comments.giscus` 部分：

```yaml
comments:
    enabled: true
    provider: giscus
    
    giscus:
        repo: "HHjoker/HHjoker.github.io"
        repoID: "你的仓库 ID"
        category: "Announcements"
        categoryID: "你的分类 ID"
        mapping: "pathname"
        lightTheme: "light"
        darkTheme: "dark"
        reactionsEnabled: 1
        emitMetadata: 0
```

### 第五步：验证配置

1. 提交更改到 hugo-main 仓库
2. 等待自动部署到 HHjoker.github.io
3. 打开任意文章页面
4. 应该能看到评论框

---

## 其他评论系统配置

### Disqus（已配置但未启用）

```yaml
comments:
    enabled: true
    provider: disqus
    
services:
    disqus:
        shortname: "你的-disqus-shortname"
```

**步骤**:
1. 注册 https://disqus.com/
2. 创建站点获取 shortname
3. 填入配置

### Utterances（基于 GitHub Issues）

```yaml
comments:
    enabled: true
    provider: utterances
    
    utterances:
        repo: "HHjoker/HHjoker.github.io"
        issueTerm: "pathname"
        label: "comment"
```

### Waline（推荐中文博客）

```yaml
comments:
    enabled: true
    provider: waline
    
    waline:
        serverURL: "你的-waline-服务器地址"
        lang: "zh-CN"
        pageview: true
```

---

## 主题自定义

### 修改评论位置

编辑主题布局文件（如果需要）：

```bash
# 位置
hugo-main/themes/hugo-theme-stack/layouts/partials/comments.html
```

### 自定义样式

在 `assets/scss/custom.scss` 添加：

```scss
.giscus {
    margin-top: 2rem;
}

.giscus-frame {
    width: 100%;
}
```

---

## 评论管理

### 在 GitHub 上管理

1. 访问仓库的 **Discussions** 标签
2. 可以找到所有评论
3. 可以编辑、删除、隐藏评论

###  moderation 设置

在 Giscus 配置中可以设置：
- 是否需要审核
- 允许的反应类型
- 评论排序方式

---

## 故障排查

### 评论不显示

1. 检查 `comments.enabled` 是否为 `true`
2. 检查 `provider` 是否正确
3. 查看浏览器控制台错误信息
4. 确认仓库是 **public** 的

### 无法登录

1. 确认已安装 Giscus App
2. 确认 GitHub Discussions 已启用
3. 检查 OAuth 授权

### 评论框是空的

1. 第一次评论会自动创建 Discussion
2. 检查 mapping 配置是否正确
3. 尝试刷新页面

---

## 推荐配置

**对于个人博客，推荐使用 Giscus：**

```yaml
comments:
    enabled: true
    provider: giscus
    
    giscus:
        repo: "HHjoker/HHjoker.github.io"
        repoID: "R_kgDO..."  # 需要填写
        category: "Announcements"
        categoryID: "DIC_..."  # 需要填写
        mapping: "pathname"
        strict: 0
        reactionsEnabled: 1
        emitMetadata: 0
        inputPosition: "bottom"
        lang: "zh-CN"
        loading: "lazy"
```

---

## 参考资料

- [Giscus 官网](https://giscus.app/zh-CN)
- [Giscus GitHub](https://github.com/giscus/giscus)
- [Hugo 官方评论文档](https://gohugo.io/content-management/comments/)
- [Theme Stack 文档](https://stack.jimmycai.com/)

---

**最后更新**: 2026-03-04
