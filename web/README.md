# Movie Ranking Web App

一个基于Vue 3的电影排名和展示应用。

## 功能特性

- 电影列表展示和排序
- 演员信息管理
- 标签分类
- 博客文章系统
- **在线Markdown编辑器** - 新增功能

## 在线Markdown编辑器

### 功能说明

新增了LiveEditor组件，允许用户直接在网页上编辑电影的正文内容：

- 使用md-editor-v3提供专业的Markdown编辑体验
- 支持实时预览
- 支持图片上传
- 支持代码高亮
- 支持表格、数学公式等高级功能

### 使用方法

1. **电影详情页面**: 点击绿色的"正文"按钮编辑电影正文内容
2. **演员详情页面**: 点击绿色的"正文"按钮编辑演员介绍内容
3. **文章详情页面**: 点击绿色的"正文"按钮编辑文章正文内容
4. 在弹出的编辑器中修改Markdown内容
5. 点击保存按钮提交更改
6. 系统会自动更新文件并刷新显示

### 技术实现

- 前端：Vue 3 + md-editor-v3 + marked
- 后端：新增API接口支持正文内容更新
- 数据：保存原始Markdown文本，前端使用marked统一渲染HTML显示

### 支持的编辑类型

- **电影正文**: `/api/update-movie-body/<id>`
- **演员正文**: `/api/update-actor-body/<actor_name>`
- **文章正文**: `/api/update-post-body/<slug>`

## 架构统一

### Markdown渲染策略

为了保持架构的一致性，所有Markdown内容现在都采用前端渲染的方式：

- **MovieDetail**: 使用marked在前端渲染电影正文
- **ActorDetail**: 使用marked在前端渲染演员介绍
- **PostsDetail**: 使用marked在前端渲染博客文章

### 优势

- **性能优化**: 减少后端计算负担，提高响应速度
- **一致性**: 所有页面使用相同的渲染逻辑
- **灵活性**: 前端可以更灵活地处理Markdown内容
- **缓存友好**: 原始Markdown内容更适合缓存

## 开发环境

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

## 依赖说明

- Vue 3 - 前端框架
- Element Plus - UI组件库
- md-editor-v3 - Markdown编辑器
- Axios - HTTP客户端
- Vite - 构建工具
