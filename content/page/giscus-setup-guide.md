# Giscus 评论系统快速配置指南

## ✅ 已完成

- [x] Hugo 配置已更新 (`hugo.yaml`)
- [x] 评论系统已切换为 Giscus
- [x] 中文语言支持已启用
- [x] 配置指南已创建

## ⏳ 待完成（需要手动操作）

### 第 1 步：启用 GitHub Discussions

1. 打开 https://github.com/HHjoker/HHjoker.github.io
2. 点击 **Settings** 标签
3. 在 **General** 页面找到 **Features** 部分
4. ✅ 勾选 **Discussions**
5. 点击 **Set up discussions**
6. 选择 **Announcements** 类型（推荐）
7. 点击 **Create categories**

### 第 2 步：安装 Giscus App

1. 访问 https://github.com/apps/giscus
2. 点击绿色按钮 **Install**
3. 选择 **Only select repositories**
4. ✅ 勾选 `HHjoker/HHjoker.github.io`
5. 点击 **Install**

### 第 3 步：获取配置 ID

1. 访问 https://giscus.app/zh-CN
2. 填写配置：
   ```
   仓库：HHjoker/HHjoker.github.io
   分类：Announcements
   映射方式：pathname
   语言：zh-CN
   主题：preferred_color_scheme
   ```
3. 点击 **Generate** 生成配置
4. 复制生成的 `data-repo-id` 和 `data-category-id`

### 第 4 步：更新配置文件

编辑 `hugo.yaml`，找到 `giscus` 部分：

```yaml
giscus:
    repo: "HHjoker/HHjoker.github.io"
    repoID: "R_kgDO..."      # ← 粘贴这里
    category: "Announcements"
    categoryID: "DIC_kwDO..."  # ← 粘贴这里
    mapping: "pathname"
    strict: 0
    lightTheme: "preferred_color_scheme"
    darkTheme: "preferred_color_scheme"
    reactionsEnabled: 1
    emitMetadata: 0
    inputPosition: "bottom"
    lang: "zh-CN"
    loading: "lazy"
```

### 第 5 步：提交并推送

```bash
cd ~/.openclaw/workspace/hugo-main
git add hugo.yaml
git commit -m "config: 填写 Giscus repoID 和 categoryID"
git push origin master
```

### 第 6 步：验证

1. 等待自动部署（约 1-2 分钟）
2. 打开博客任意文章页面
3. 滚动到页面底部
4. 应该能看到评论框

---

## 🔍 如何获取 repoID 和 categoryID

### 方法 1：使用 giscus.app（推荐）

1. 访问 https://giscus.app/zh-CN
2. 填写仓库和分类
3. 页面会自动显示 ID

### 方法 2：从 GitHub 获取

**获取 repoID:**
1. 打开仓库页面
2. 按 F12 打开开发者工具
3. 点击 **Network** 标签
4. 刷新页面
5. 找到 `graphql` 请求
6. 查看响应中的 `repository.id`

**获取 categoryID:**
1. 打开 Discussions 页面
2. 按 F12 打开开发者工具
3. 点击 **Network** → **graphql**
4. 查看响应中的 `discussionCategory.id`

---

## 📝 评论管理

### 在 GitHub 上管理评论

1. 访问 https://github.com/HHjoker/HHjoker.github.io/discussions
2. 可以看到所有评论
3. 可以编辑、删除、隐藏评论

### 在网站上管理

访客可以直接：
- 发表评论
- 点赞/反应
- 回复他人

需要 GitHub 账号登录。

---

## ⚙️ 高级配置

### 修改评论位置

```yaml
giscus:
    inputPosition: "top"  # 或 "bottom"
```

### 禁用反应

```yaml
giscus:
    reactionsEnabled: 0
```

### 使用严格匹配

```yaml
giscus:
    strict: 1  # 避免标题相似的讨论匹配错误
```

### 自定义主题

```yaml
giscus:
    lightTheme: "light"
    darkTheme: "dark"
```

可用主题：
- `light` / `dark`
- `light_protanopia` / `dark_protanopia`
- `noborder_light` / `noborder_dark`
- `transparent_dark`
- `preferred_color_scheme` (跟随系统)

---

## 🐛 故障排查

### 评论框不显示

1. 检查浏览器控制台是否有错误
2. 确认仓库是 **public** 的
3. 确认 Discussions 已启用
4. 确认 Giscus App 已安装

### 无法登录

1. 清除浏览器缓存
2. 重新授权 Giscus App
3. 检查 GitHub OAuth 设置

### 评论不更新

1. 刷新页面
2. 检查网络连接
3. 查看 GitHub Discussions 是否正常

---

## 📚 参考资料

- [Giscus 官网](https://giscus.app/zh-CN)
- [Giscus GitHub](https://github.com/giscus/giscus)
- [Giscus 高级配置](https://github.com/giscus/giscus/blob/main/ADVANCED-USAGE.md)
- [GitHub Discussions 文档](https://docs.github.com/en/discussions)

---

**配置完成后，记得删除这个文件**

```bash
rm content/page/giscus-setup-guide.md
```

---

最后更新：2026-03-04
