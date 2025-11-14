# Netlify 部署指南 🚀

## 推荐方案：Railway（后端）+ Netlify（前端）

由于应用使用SQLite数据库，而Netlify的Serverless环境不支持持久化SQLite，建议采用混合部署方案：

### 🎯 部署架构
- **前端** → Netlify（免费、快速、全球CDN、自动HTTPS）
- **后端** → Railway（免费、支持SQLite持久化）

---

## 🚀 部署步骤（约10分钟完成）

### 第一步：部署后端到 Railway ⚡

1. **访问并登录 Railway**
   - 打开 https://railway.app/
   - 点击 "Login" 使用GitHub账号登录

2. **创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 搜索并选择：`ruanwz/primary-school-math-for-adhd-children`
   - 授权Railway访问您的仓库

3. **配置项目**
   Railway会自动检测到Python项目，但需要设置：

   - 点击项目 → "Settings" → "Service"
   - **Root Directory**: 设置为 `backend`
   - **Start Command**: `python app.py`
   - **Environment Variables** (可选):
     ```
     FLASK_ENV=production
     ```

4. **配置端口**
   - 在 "Settings" → "Networking"
   - 找到 "Public Networking" 部分
   - 在 "Enter the port your app is listening on" 输入：`5000`
   - 或者留空（应用已配置自动读取Railway的 `PORT` 环境变量）

   > 💡 **提示**：后端代码已配置为自动读取环境变量 `PORT`，Railway会自动分配端口，通常留空即可。

5. **生成公开域名**
   - 在项目页面，点击 "Settings" → "Networking"
   - 点击 "Generate Domain"
   - 会生成一个域名，例如：`adhd-math-backend.up.railway.app`
   - **📋 复制这个域名，稍后需要使用！**

6. **等待部署完成**
   - 查看 "Deployments" 标签
   - 等待状态变为 "Success"（约2-3分钟）

7. **验证后端运行**
   ```bash
   curl https://adhd-math-backend.up.railway.app/api/health
   # 应该返回: {"status":"healthy","timestamp":"..."}
   ```

---

### 第二步：部署前端到 Netlify 🌐

#### 方式一：网页部署（推荐，最简单）

1. **访问并登录 Netlify**
   - 打开 https://app.netlify.com/
   - 点击 "Sign up" 或 "Log in" 使用GitHub账号登录

2. **导入项目**
   - 点击 "Add new site" → "Import an existing project"
   - 选择 "Deploy with GitHub"
   - 授权Netlify访问您的GitHub账户
   - 搜索并选择：`ruanwz/primary-school-math-for-adhd-children`

3. **配置构建设置**

   Netlify会自动检测到React项目，确认以下设置：

   - **Branch to deploy**: `claude/adhd-math-learning-app-01RQvWryeWi18Qdo4PomPSq3`（或您的主分支）
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`

4. **配置环境变量**

   在 "Site settings" → "Environment variables" 中添加：

   | Key | Value |
   |-----|-------|
   | `REACT_APP_API_URL` | `https://adhd-math-backend.up.railway.app` |
   | `NODE_VERSION` | `18` |

   ⚠️ 将上面的URL替换为第一步中Railway生成的实际域名！

5. **更新 netlify.toml 中的 API 地址**

   在部署前，需要更新 `netlify.toml` 文件中的 Railway 后端地址：

   ```toml
   [[redirects]]
     from = "/api/*"
     to = "https://your-railway-app.up.railway.app/api/:splat"  # 改为实际的Railway域名
     status = 200
     force = true
   ```

6. **开始部署**
   - 点击 "Deploy site"
   - 等待部署完成（约3-5分钟）

7. **获取网站地址**
   - 部署完成后，Netlify会分配一个域名，例如：
     ```
     https://amazing-curie-123abc.netlify.app
     ```
   - 您可以在 "Site settings" → "Domain management" 中自定义域名

#### 方式二：使用 Netlify CLI

```bash
# 1. 安装 Netlify CLI
npm install -g netlify-cli

# 2. 登录 Netlify
netlify login

# 3. 进入项目根目录
cd /home/user/primary-school-math-for-adhd-children

# 4. 初始化 Netlify 项目
netlify init

# 5. 按照提示配置：
# - Create & configure a new site? Yes
# - Team: 选择您的团队
# - Site name: adhd-math-learning（或其他名称）
# - Base directory: frontend
# - Build command: npm run build
# - Publish directory: frontend/build

# 6. 设置环境变量
netlify env:set REACT_APP_API_URL "https://adhd-math-backend.up.railway.app"

# 7. 部署
netlify deploy --prod
```

---

### 第三步：配置 CORS（如果需要）

如果遇到CORS错误，需要在后端配置允许Netlify域名：

编辑 `backend/app.py`:

```python
from flask_cors import CORS

# 更新CORS配置
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",  # 本地开发
            "https://*.netlify.app",   # 允许所有Netlify域名
            "https://amazing-curie-123abc.netlify.app"  # 您的具体Netlify域名
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

然后重新部署后端到Railway（Railway会自动检测到代码变化并重新部署）。

---

## ✅ 验证部署

### 1. 检查后端（Railway）

```bash
# 健康检查
curl https://adhd-math-backend.up.railway.app/api/health

# 获取年级列表
curl https://adhd-math-backend.up.railway.app/api/curriculum/grades
```

### 2. 检查前端（Netlify）

1. 访问Netlify提供的URL
2. 尝试以下操作：
   - 注册新用户
   - 登录
   - 选择年级（应该能看到一年级到六年级）
   - 选择主题（例如：一年级的"数一数、比多少"）
   - 开始练习

3. 检查浏览器Console（F12）：
   - 不应该有CORS错误
   - 不应该有404错误
   - 网络请求应该成功

### 3. 检查数据持久化

1. 注册一个测试用户
2. 完成几道练习题
3. 关闭浏览器
4. 重新打开并登录
5. 数据应该还在（说明Railway的SQLite持久化工作正常）

---

## 🎨 自定义域名（可选）

### 在 Netlify 上设置自定义域名

1. 进入 Netlify 项目 → "Domain settings"
2. 点击 "Add custom domain"
3. 输入您的域名（例如：`math.yourdomain.com`）
4. 按照提示配置DNS记录：
   - 类型：CNAME
   - 名称：math（或@用于根域名）
   - 值：您的Netlify域名（例如：amazing-curie-123abc.netlify.app）
5. 等待DNS传播（可能需要几分钟到几小时）
6. Netlify会自动配置免费的SSL证书（Let's Encrypt）

---

## 📊 部署后的完整架构

```
用户浏览器
    ↓ HTTPS
Netlify CDN（前端）
    ↓ API请求（通过代理）
Railway 服务器（后端 + SQLite）
    ↓
持久化存储（用户数据、进度、成就等）
```

**优势：**
- ✅ 全球CDN加速（Netlify提供）
- ✅ 自动HTTPS证书
- ✅ 数据持久化（Railway提供）
- ✅ 自动部署（推送代码即自动更新）
- ✅ 完全免费！

---

## 💰 成本说明

### Railway 免费额度
- **免费额度**: $5/月 使用额度
- **包含**:
  - 500小时运行时间
  - 100GB网络流量
  - 1GB RAM
  - 持久化存储
- **适用场景**: 小型到中型应用，个人项目完全够用

### Netlify 免费额度
- **带宽**: 100GB/月
- **构建分钟数**: 300分钟/月
- **并发构建**: 1个
- **站点数量**: 无限制
- **表单提交**: 100次/月
- **无服务器函数**: 125,000次请求/月
- **适用场景**: 个人项目、小型商业网站

**总成本**: 完全免费！两个平台的免费额度对于这个应用来说绰绰有余。

---

## 🔄 持续部署（CI/CD）

配置完成后，每次推送代码到GitHub：

1. **Netlify自动部署前端**
   - 检测到代码变化
   - 自动执行 `npm run build`
   - 部署到全球CDN
   - 约2-3分钟完成

2. **Railway自动部署后端**
   - 检测到backend目录变化
   - 自动重新构建
   - 重启服务
   - 约2-3分钟完成

**无需手动操作，推送代码即可自动更新线上应用！**

---

## 🐛 常见问题

### Q1: 部署成功但页面空白

**解决方案：**
- 检查浏览器Console是否有错误
- 确认 `frontend/package.json` 中有正确的 `homepage` 字段
- 检查环境变量是否正确设置

### Q2: API请求失败（CORS错误）

**解决方案：**
```python
# backend/app.py
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-site.netlify.app"]
    }
})
```

### Q3: 数据库初始化失败

**解决方案：**
- Railway会自动创建持久化卷
- 首次部署时，数据库会自动初始化
- 查看Railway日志确认初始化成功

### Q4: Railway 应用休眠

**解决方案：**
- Railway免费版应用在15分钟无请求后会休眠
- 首次唤醒可能需要5-10秒
- 可以使用 UptimeRobot 等服务定期ping保持活跃（可选）

### Q5: 构建失败

**检查清单：**
1. 确认 `netlify.toml` 配置正确
2. 确认 `frontend/package.json` 中的依赖完整
3. 查看Netlify构建日志
4. 确认Node版本兼容（推荐18）

---

## 📱 部署完成后的最终结果

### 您将获得：

1. **前端访问地址**
   ```
   https://adhd-math-learning.netlify.app
   ```
   或自定义域名：
   ```
   https://math.yourdomain.com
   ```

2. **后端API地址**
   ```
   https://adhd-math-backend.up.railway.app
   ```

3. **功能特性**
   - ✅ 全球CDN加速访问
   - ✅ 自动HTTPS安全连接
   - ✅ 持久化数据存储
   - ✅ 自动部署（推送即更新）
   - ✅ 性能监控（Netlify Analytics）
   - ✅ 错误追踪（Netlify Functions日志）

---

## 🆘 需要帮助？

### Netlify 支持
- 文档: https://docs.netlify.com/
- 社区: https://answers.netlify.com/
- 状态: https://www.netlifystatus.com/

### Railway 支持
- 文档: https://docs.railway.app/
- Discord: https://discord.gg/railway
- 状态: https://status.railway.app/

### 调试步骤

1. **查看Netlify部署日志**
   - 项目 → "Deploys" → 点击最新部署 → 查看日志

2. **查看Railway部署日志**
   - 项目 → "Deployments" → 点击最新部署 → 查看构建和运行日志

3. **查看浏览器错误**
   - 按F12打开开发者工具
   - 查看 "Console" 和 "Network" 标签
   - 截图错误信息

---

## 🎉 完成！

按照以上步骤，您的ADHD儿童数学学习应用将：

- 🌍 全球可访问
- 🚀 快速加载（CDN）
- 🔒 安全连接（HTTPS）
- 💾 数据持久化
- 🔄 自动更新
- 💰 完全免费

**立即分享给家长和孩子们，开始学习之旅吧！** 🎊

---

## 📚 相关文档

- `QUICK_DEPLOY.md` - 快速部署指南（Railway + Vercel）
- `VERCEL_DEPLOYMENT.md` - Vercel部署详细指南
- `README.md` - 项目说明
- `GRADE1_GAME_DESIGN.md` - 一年级游戏化评估设计
