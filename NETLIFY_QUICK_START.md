# Netlify 快速部署指南 ⚡

**只需3步，10分钟完成部署！**

---

## 🎯 部署方案

- **前端（React）** → Netlify（全球CDN）
- **后端（Flask）** → Railway（数据持久化）

---

## 📋 步骤1：部署后端（Railway）

### 1.1 访问Railway并登录
👉 打开 https://railway.app/ → 用GitHub账号登录

### 1.2 创建项目
1. 点击 **"New Project"**
2. 选择 **"Deploy from GitHub repo"**
3. 选择仓库：`ruanwz/primary-school-math-for-adhd-children`

### 1.3 配置设置
1. 点击项目名称进入设置
2. 找到 **"Settings"** → **"Service"**
3. 设置：
   - **Root Directory**: `backend`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - 或留空让Railway自动检测Procfile

### 1.4 配置端口（重要！）
1. 在 **"Settings"** → **"Networking"**
2. 找到 **"Public Networking"** 部分
3. 在 **"Enter the port your app is listening on"** 输入：`5000`
4. 或者留空（Railway会自动使用环境变量 `PORT`，应用已配置支持）

> 💡 **说明**：应用代码已配置为自动读取Railway的 `PORT` 环境变量，通常留空即可。

### 1.5 生成域名
1. 在 **"Settings"** → **"Networking"**
2. 点击 **"Generate Domain"**
3. 📋 **复制生成的域名**（例如：`https://xxx.up.railway.app`）

### 1.6 验证
```bash
curl https://你的域名.up.railway.app/api/health
# 应该返回: {"status":"healthy"...}
```

✅ **后端部署完成！记下这个域名，下一步要用。**

---

## 📋 步骤2：部署前端（Netlify）

### 2.1 访问Netlify并登录
👉 打开 https://app.netlify.com/ → 用GitHub账号登录

### 2.2 导入项目
1. 点击 **"Add new site"** → **"Import an existing project"**
2. 选择 **"Deploy with GitHub"**
3. 选择仓库：`ruanwz/primary-school-math-for-adhd-children`

### 2.3 配置构建设置
确认以下设置（Netlify会自动填充大部分）：

| 设置项 | 值 |
|--------|-----|
| **Base directory** | `frontend` |
| **Build command** | `npm run build` |
| **Publish directory** | `frontend/build` |

### 2.4 设置环境变量
点击 **"Show advanced"** → **"New variable"**

添加环境变量：
- **Key**: `REACT_APP_API_URL`
- **Value**: `https://你的Railway域名.up.railway.app`（步骤1.4中复制的）

例如：`https://adhd-math-backend.up.railway.app`

### 2.5 开始部署
点击 **"Deploy site"** → 等待3-5分钟

✅ **前端部署完成！**

---

## 📋 步骤3：更新配置文件

### 3.1 更新 netlify.toml

在本地编辑 `netlify.toml` 文件，找到这一行：

```toml
[[redirects]]
  from = "/api/*"
  to = "https://your-railway-app.up.railway.app/api/:splat"  # 👈 修改这里
```

将 `https://your-railway-app.up.railway.app` 替换为您的实际Railway域名。

### 3.2 更新 frontend/public/_redirects

编辑 `frontend/public/_redirects` 文件第一行：

```
/api/*  https://你的Railway域名.up.railway.app/api/:splat  200
```

### 3.3 提交并推送

```bash
git add netlify.toml frontend/public/_redirects
git commit -m "Update Railway backend URL for Netlify deployment"
git push
```

Netlify会自动检测到更新并重新部署（约2分钟）。

---

## ✅ 验证部署

### 访问您的网站

Netlify会提供一个URL，例如：
```
https://amazing-name-123456.netlify.app
```

### 测试功能

1. ✅ 打开网站
2. ✅ 注册一个测试用户
3. ✅ 选择年级（应该看到1-6年级）
4. ✅ 选择主题（例如：一年级的"数一数、比多少"）
5. ✅ 开始练习
6. ✅ 刷新页面，数据应该还在

### 检查浏览器Console

按 `F12` 打开开发者工具：
- ❌ 不应该有CORS错误
- ❌ 不应该有404错误
- ✅ 网络请求应该成功

---

## 🎨 自定义域名（可选）

### 在Netlify设置自定义域名

1. 进入站点 → **"Domain settings"**
2. 点击 **"Add custom domain"**
3. 输入域名：`math.yourdomain.com`
4. 按提示在域名提供商处添加DNS记录：
   ```
   类型: CNAME
   名称: math
   值: amazing-name-123456.netlify.app
   ```
5. 等待DNS生效（5分钟-24小时）
6. Netlify自动配置免费SSL证书

---

## 🐛 遇到问题？

### ❌ CORS错误

编辑 `backend/app.py`，更新CORS配置：

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "https://*.netlify.app",
            "https://你的实际域名.netlify.app"
        ]
    }
})
```

推送到GitHub，Railway会自动重新部署。

### ❌ 页面空白

1. 检查浏览器Console错误
2. 确认环境变量 `REACT_APP_API_URL` 设置正确
3. 在Netlify查看部署日志

### ❌ API请求失败

1. 确认Railway后端正在运行
2. 测试后端健康检查：`curl https://你的域名.up.railway.app/api/health`
3. 检查 `netlify.toml` 中的重定向配置

---

## 💰 成本

- **Railway**: 免费 $5/月 额度（够用）
- **Netlify**: 免费 100GB 带宽/月（够用）
- **总成本**: **完全免费** 🎉

---

## 🎊 完成！

恭喜！您的应用现已上线：

🌍 **全球访问**: 通过Netlify CDN快速加载
🔒 **安全连接**: 自动HTTPS证书
💾 **数据持久**: Railway SQLite存储
🔄 **自动更新**: 推送代码即自动部署

**分享链接给家长和孩子们，开始学习之旅吧！** 🚀

---

## 📚 更多文档

- `NETLIFY_DEPLOYMENT.md` - 详细部署指南
- `GRADE1_GAME_DESIGN.md` - 一年级游戏设计
- `README.md` - 项目说明

---

**需要帮助？**
- Netlify文档: https://docs.netlify.com/
- Railway文档: https://docs.railway.app/
