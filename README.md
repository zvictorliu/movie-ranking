# Movie Ranking

一个功能完整的影视作品与演员管理系统，支持个人影视收藏管理、评分排行、演员资料、标签分类、图床管理以及博客功能。

## 功能特性

### 核心功能

- **影片管理**
  - 影片列表展示与排行
  - 支持评分（0-5 星）和自定义排序
  - 标签分类和筛选
  - 演员关联管理
  - 详情页面支持 Markdown 编辑
  - 封面图片上传

- **演员管理**
  - 演员列表按拼音排序
  - 喜爱度评级（1-5 级）
  - 出生日期、出道时间记录
  - 主要作品自动关联
  - 演员详情页 Markdown 编辑

- **标签系统**
  - 自动统计标签使用频次
  - 按标签浏览影片
  - 支持多标签筛选

- **图床功能**
  - 图片上传和管理
  - 文件信息展示（大小、修改时间）
  - 支持多种图片格式（PNG, JPG, JPEG, GIF, WebP）

- **博客系统**
  - Markdown 文章编写
  - 文章标签和摘要
  - 按日期排序展示

### 界面特性

- 双主题切换（亮色/暗色）
- 响应式卡片布局
- 点击复制引用快捷键
- 现代化 UI 设计（基于 Element Plus）

### 数据管理

- 基于 Markdown 文件存储（Frontmatter 格式）
- 支持在线编辑和实时更新
- 文件系统持久化存储

## 技术栈

### 前端

- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite 6
- **UI 组件**: Element Plus 2.9
- **状态管理**: Pinia 3
- **路由**: Vue Router 4
- **编辑器**: md-editor-v3 (Markdown 编辑器)
- **样式**: SCSS + CSS 变量系统
- **其他**: Axios, Marked, Gray-matter

### 后端

- **框架**: Flask (Python 3.13)
- **跨域**: Flask-CORS
- **Markdown 解析**: python-frontmatter
- **中文拼音**: pypinyin

### 部署

- Docker + Docker Compose
- Nginx (静态文件服务)

## 项目结构

```
movie-ranking/
├── backend/              # Flask 后端
│   ├── app.py           # 主应用程序
│   └── requirements.txt # Python 依赖
├── web/                 # Vue 前端
│   ├── src/
│   │   ├── views/       # 页面组件
│   │   ├── components/  # 公共组件
│   │   ├── router/      # 路由配置
│   │   ├── store/       # Pinia 状态管理
│   │   ├── styles/      # 全局样式
│   │   └── main.js      # 入口文件
│   ├── package.json
│   └── vite.config.js
├── content/             # 数据存储目录（不公开）
│   ├── movies/          # 影片 Markdown 文件
│   ├── actors/          # 演员 Markdown 文件
│   ├── posts/           # 博客文章
│   ├── imgbed/          # 图床文件
│   └── covers/          # 封面图片
│       ├── movie-cover/
│       ├── actor-cover/
│       └── post-cover/
├── docker-compose.yml   # Docker Compose 配置
├── Dockerfile.backend   # 后端 Docker 配置
├── Dockerfile.frontend  # 前端 Docker 配置
└── README.md
```

## 快速开始

### 环境要求

- **本地开发**
  - Python 3.9+
  - Node.js 18+
  - npm 或 yarn

- **Docker 部署**
  - Docker 20.10+
  - Docker Compose 1.29+

### 本地开发

#### 1. 启动后端

```bash
cd backend/
pip install -r requirements.txt
python app.py
```

后端默认运行在 `http://localhost:5000`

#### 2. 启动前端

```bash
cd web/
npm install
npm run dev
```

前端默认运行在 `http://localhost:5173`（Vite 默认端口）

### Docker 部署

#### 使用 Docker Compose（推荐）

```bash
# 一次性构建并启动所有服务
docker compose up --build

# 后台运行
docker compose up -d

# 停止服务
docker compose down
```

#### 单独构建

```bash
# 构建后端
docker compose build backend

# 构建前端
docker compose build frontend

# 启动服务
docker compose up -d
```

## 配置说明

### 后端配置

在 `backend/app.py` 中修改以下配置：

```python
# 端口配置
app.run(debug=True, port=5000, host="0.0.0.0")

# 用户认证（建议修改默认密码）
USERS = {
    'hector': hash_password('your_password_here'),
}

# 内容文件夹路径
CONTENT_FOLDER = os.path.join(os.getcwd(), '../content')
```

### 前端配置

修改 `web/src/` 下的配置文件：

- API 地址配置：检查组件中的 axios 请求地址
- 路由配置：`router/index.js`
- 主题配置：`styles/` 目录下的 CSS 变量

### Docker 配置

在 `docker-compose.yml` 中：

```yaml
environment:
  - UID=${UID}  # 设置用户 ID（避免权限问题）
  - GID=${GID}  # 设置组 ID
```

运行前设置环境变量：

```bash
export UID=$(id -u)
export GID=$(id -g)
docker compose up -d
```

## 使用说明

### 登录

默认用户名和密码配置在 `backend/app.py` 中，登录后可以进行内容编辑。

### 创建影片

1. 进入"影片"页面
2. 点击"新建影片"按钮
3. 填写影片信息（标题、演员、标签、描述、评分等）
4. 上传封面图片
5. 保存后在详情页可继续编辑 Markdown 内容

### 创建演员

1. 进入"演员"页面
2. 点击"新建演员"按钮
3. 填写演员信息（姓名、出生日期、出道时间、喜爱度等）
4. 上传头像图片
5. 保存后可在详情页编辑个人简介

### 使用图床

1. 进入"图床"页面
2. 上传图片文件
3. 点击图片标题可复制引用路径
4. 在 Markdown 编辑器中使用

### 编写博客

1. 进入"博客"页面
2. 点击"新建文章"按钮
3. 填写标题、作者、标签等信息
4. 使用 Markdown 编辑器编写正文
5. 保存并发布

### shortcut

1. 在图床页面可复制图片引用
2. 在影片排行页面点击标题可复制影片引用

## 开发指南

### 添加新的 API 端点

在 `backend/app.py` 中添加新的路由：

```python
@app.route('/api/your-endpoint', methods=['GET', 'POST'])
def your_endpoint():
    # 实现逻辑
    return jsonify(data), 200
```

### 添加新的前端页面

1. 在 `web/src/views/` 创建新的 Vue 组件
2. 在 `web/src/router/index.js` 添加路由配置
3. 在导航菜单中添加链接

### 代码规范

```bash
# 前端代码检查
cd web/
npm run lint

# 代码格式化
npm run format

# 格式检查
npm run format:check
```

## 数据格式示例

### 影片 Markdown 文件

```markdown
---
title: "电影标题"
actors: "演员1, 演员2"
tags: ["标签1", "标签2"]
description: "简短描述"
order: 1
rating: 5
cover: "电影标题.jpg"
---

这里是影片的详细介绍内容，支持 Markdown 格式。

<img title="剧照1.png" />

<img title="剧照2.png" />
```

### 演员 Markdown 文件

```markdown
---
name: "演员名字"
birth: "1990-01-01"
debut: "2010-01-01"
favorite: 5
cover: "演员名字.jpg"
---

## 个人简介

这里是演员的详细介绍。

<img title="生活照.png" />

## 主要作品

<movie title="电影1" />
<movie title="电影2" />
```

## 注意事项

- 出于隐私考虑，`content/` 目录不包含在版本控制中
- 首次运行需要手动创建 `content/` 目录及子目录
- 建议定期备份 `content/` 目录中的数据
- Docker 部署时注意文件权限问题（使用 UID/GID 环境变量）

## 许可证

本项目仅供个人学习和使用。

## 致谢

- [Vue.js](https://vuejs.org/)
- [Element Plus](https://element-plus.org/)
- [Flask](https://flask.palletsprojects.com/)
- [md-editor-v3](https://github.com/imzbf/md-editor-v3)
