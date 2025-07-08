# 个人知识与工具库系统

一个基于Django和Vue.js的前后端分离系统，集成了个人博客、数据可视化等功能。

## 项目结构

```
├── personal_toolbox_backend/  # Django后端项目
│   ├── core/                  # 核心应用（用户认证、权限等）
│   ├── blog/                  # 博客应用
│   ├── data_viz/             # 数据可视化应用
│   └── requirements.txt       # Python依赖
│
└── personal_toolbox_frontend/ # Vue前端项目
    ├── src/
    │   ├── api/              # API请求封装
    │   ├── assets/           # 静态资源
    │   ├── components/       # 通用组件
    │   ├── router/           # 路由配置
    │   ├── stores/           # Pinia状态管理
    │   └── views/            # 页面组件
    └── package.json          # npm依赖
```

## 技术栈

### 后端

- Django 5.x
- Django REST Framework
- PyMySQL (MySQL连接)
- JWT认证

### 前端

- Vue 3 (Composition API)
- Element Plus
- Vue Router 4
- Pinia
- Axios

## 功能特性

### 用户系统

- 用户注册、登录、退出
- 基于JWT的身份认证
- 基于角色的权限控制
- 用户个人信息管理

### 博客系统

- 文章的创建、编辑、删除
- Markdown编辑器支持
- 文章分类和标签管理
- 评论功能

### 数据可视化

- 多种图表类型支持
- 数据源管理
- 自定义仪表盘
- 实时数据更新

## 安装指南

### 后端设置

1. 创建并激活Python虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 配置数据库：

- 创建MySQL数据库
- 更新`settings.py`中的数据库配置

4. 运行数据库迁移：

```bash
python manage.py makemigrations
python manage.py migrate
```

5. 创建超级用户：

```bash
python manage.py createsuperuser
```

6. 启动开发服务器：

```bash
python manage.py runserver
```

### 前端设置

1. 安装依赖：

```bash
cd personal_toolbox_frontend
npm install
```

2. 启动开发服务器：

```bash
npm run dev
```

## API文档

### 认证API

- POST `/api/auth/login/` - 用户登录
- POST `/api/auth/register/` - 用户注册
- POST `/api/auth/logout/` - 用户退出
- GET `/api/auth/profile/` - 获取用户信息
- PATCH `/api/auth/profile/` - 更新用户信息

### 博客API

- GET `/api/blog/articles/` - 获取文章列表
- GET `/api/blog/articles/{slug}/` - 获取文章详情
- POST `/api/blog/articles/` - 创建文章
- PUT `/api/blog/articles/{slug}/` - 更新文章
- DELETE `/api/blog/articles/{slug}/` - 删除文章

### 数据可视化API

- GET `/api/data-viz/sources/` - 获取数据源列表
- GET `/api/data-viz/charts/` - 获取图表列表
- GET `/api/data-viz/dashboards/` - 获取仪表盘列表

## 开发指南

### 代码规范

- 使用Black格式化Python代码
- 使用ESLint和Prettier格式化JavaScript代码
- 遵循PEP 8 Python代码风格指南
- 遵循Vue.js风格指南

### 提交规范

提交信息格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型（type）：
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

## 安全注意事项

1. 不要在代码中硬编码敏感信息
2. 使用环境变量存储密钥
3. 定期更新依赖包
4. 实施CORS策略
5. 使用HTTPS
6. 实施速率限制
7. 验证所有用户输入

## 许可证

[MIT License](LICENSE)