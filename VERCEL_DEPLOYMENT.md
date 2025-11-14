# Vercel 部署指南

## ⚠️ 重要说明

### SQLite 数据库限制

**当前应用使用SQLite数据库，但Vercel的Serverless环境有以下限制：**

1. **无状态执行环境**：每次函数调用可能在不同的容器中运行
2. **临时文件系统**：SQLite数据库文件会在每次部署或函数重启时丢失
3. **只读文件系统**：在某些情况下，无法写入数据库

### 解决方案

有两个推荐的解决方案：

#### 方案一：混合部署（推荐）

- **前端**：部署到 Vercel（快速、免费、CDN加速）
- **后端**：部署到支持持久存储的平台：
  - [Railway](https://railway.app/)（推荐，支持PostgreSQL）
  - [Render](https://render.com/)（免费tier可用）
  - [Fly.io](https://fly.io/)（支持SQLite持久卷）

#### 方案二：迁移到云数据库

将SQLite迁移到云数据库，然后全部部署到Vercel：
- PostgreSQL（推荐）：Supabase、Neon、Railway
- MySQL：PlanetScale
- MongoDB：MongoDB Atlas

---

## 🚀 方案一：混合部署步骤

### 步骤1：部署后端到 Railway

1. 访问 [Railway](https://railway.app/) 并登录
2. 创建新项目
3. 选择 "Deploy from GitHub repo"
4. 连接此仓库
5. Railway会自动检测Python项目
6. 设置根目录为 `backend`
7. 添加环境变量（如果需要）
8. 部署完成后，获取API URL（例如：https://your-app.railway.app）

### 步骤2：部署前端到 Vercel

1. 安装 Vercel CLI：
```bash
npm install -g vercel
```

2. 登录 Vercel：
```bash
vercel login
```

3. 在项目根目录运行：
```bash
vercel
```

4. 设置环境变量：
```bash
# 设置后端API URL
vercel env add REACT_APP_API_URL production
# 输入Railway的API URL，例如：https://your-app.railway.app
```

5. 重新部署：
```bash
vercel --prod
```

### 步骤3：更新前端API配置

在 `frontend/src/services/api.js` 中：

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

---

## 🔧 方案二：使用Vercel + PostgreSQL

### 步骤1：创建PostgreSQL数据库

推荐使用 [Supabase](https://supabase.com/)（免费）：

1. 创建Supabase项目
2. 获取数据库连接URL
3. 记录 `DATABASE_URL`

### 步骤2：修改后端以支持PostgreSQL

更新 `backend/app.py`：

```python
import os

# 使用环境变量获取数据库URL
database_url = os.getenv('DATABASE_URL', 'sqlite:///adhd_math.db')

# 如果是PostgreSQL，需要替换postgres://为postgresql://
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
```

更新 `requirements.txt`：

```
Flask==3.0.0
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.1.1
SQLAlchemy==2.0.23
psycopg2-binary==2.9.9  # PostgreSQL驱动
numpy==1.26.2
marshmallow==3.20.1
python-dateutil==2.8.2
```

### 步骤3：部署到Vercel

```bash
# 设置数据库URL环境变量
vercel env add DATABASE_URL production
# 输入Supabase的DATABASE_URL

# 部署
vercel --prod
```

---

## 📋 完整Vercel部署命令（如果只部署前端）

```bash
# 1. 安装Vercel CLI
npm install -g vercel

# 2. 登录
vercel login

# 3. 初始化项目
cd /path/to/primary-school-math-for-adhd-children
vercel

# 4. 按照提示操作：
# - Set up and deploy? Y
# - Which scope? 选择你的账户
# - Link to existing project? N
# - What's your project's name? adhd-math-learning
# - In which directory is your code located? ./
# - Want to override the settings? N

# 5. 生产环境部署
vercel --prod
```

---

## 🔍 验证部署

部署完成后，Vercel会提供一个URL，例如：
```
https://adhd-math-learning.vercel.app
```

访问这个URL来验证前端部署。

如果使用混合部署，确保：
1. 后端API在Railway上正常运行
2. 前端能成功连接到后端API
3. 数据能正常保存和读取

---

## 🐛 常见问题

### 1. "Module not found" 错误

确保 `requirements.txt` 包含所有依赖：
```bash
pip freeze > requirements.txt
```

### 2. 数据库初始化失败

在Vercel上，数据库初始化应该在首次部署后手动执行：
```bash
# 如果使用PostgreSQL，连接到数据库并运行迁移
```

### 3. CORS错误

确保后端的CORS配置允许Vercel域名：
```python
CORS(app, origins=['https://your-app.vercel.app'])
```

### 4. 函数超时

Vercel免费版函数有10秒超时限制。如果初始化数据耗时过长，考虑：
- 使用后台任务
- 分批初始化数据
- 使用数据库迁移脚本

---

## 📞 需要帮助？

如果遇到部署问题：
1. 查看Vercel部署日志
2. 查看浏览器Console错误
3. 检查网络请求是否成功

---

## 🎯 推荐部署配置（最简单）

**最简单的部署方式（无需修改代码）：**

1. **前端 → Vercel**（本文档的命令）
2. **后端 → Railway**（自动检测，一键部署）

这样可以保留SQLite数据库，无需迁移到PostgreSQL，且Railway提供持久存储。
