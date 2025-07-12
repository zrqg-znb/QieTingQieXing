# 切听切行 - 个人空间系统

基于Django DRF和Vue3的前后端分离个人空间系统，包含知识库(wiki)和商城(shop)两个核心应用。

## 项目结构

- 后端：Django REST Framework
- 前端：Vue3 + Element UI
- 数据库：MySQL

## 环境配置

### 后端环境

1. 创建Conda环境

```bash
conda create -n QieTingQIeXing python=3.11
conda activate QieTingQIeXing
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 配置数据库

在项目根目录创建`.env`文件，配置数据库连接信息：

```
DB_NAME=qietingqiexing
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

4. 运行迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

5. 启动开发服务器

```bash
python manage.py runserver
```

### 前端环境

1. 安装依赖

```bash
cd frontend
npm install
```

2. 启动开发服务器

```bash
npm run dev
```

## 功能特性

- 单点登录：用户只需登录一次即可访问所有子系统
- 基于JWT的用户认证
- 基于角色的权限控制
- 知识库系统
- 商城系统（占位，暂未实现具体功能）
- 可扩展的项目结构，方便添加新的子应用