# 快速部署指南 🚀

## 推荐方案：混合部署（最简单）

由于应用使用SQLite数据库，而Vercel的Serverless环境不支持持久化SQLite，建议采用以下部署方案：

### 🎯 部署架构
- **前端** → Vercel（免费、快速、全球CDN）
- **后端** → Railway（免费、支持SQLite持久化）

---

## 📝 部署步骤

### 第一步：部署后端到 Railway

1. 访问 https://railway.app/ 并使用GitHub登录

2. 点击 "New Project" → "Deploy from GitHub repo"

3. 选择仓库：`ruanwz/primary-school-math-for-adhd-children`

4. 设置配置：
   - **Root Directory**: `backend`
   - **Start Command**: `python app.py`
   - Railway会自动检测Python项目

5. 等待部署完成（约2-3分钟）

6. **复制API地址**：
   - 在Railway项目页面，点击 "Settings" → "Domains"
   - 生成域名，例如：`https://adhd-math-backend.up.railway.app`
   - **保存这个地址！**

### 第二步：配置前端API地址

在本地修改 `frontend/src/services/api.js`:

```javascript
// 当前代码
const API_BASE_URL = 'http://localhost:5000';

// 修改为
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

### 第三步：部署前端到 Vercel

**方式一：使用Vercel网站（推荐，最简单）**

1. 访问 https://vercel.com/ 并使用GitHub登录

2. 点击 "Add New" → "Project"

3. 导入GitHub仓库：`ruanwz/primary-school-math-for-adhd-children`

4. 配置项目：
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

5. 设置环境变量：
   - 点击 "Environment Variables"
   - 添加变量：
     - Name: `REACT_APP_API_URL`
     - Value: `https://adhd-math-backend.up.railway.app`（从第一步复制的Railway地址）

6. 点击 "Deploy" 开始部署

7. 等待部署完成（约3-5分钟）

8. 获得Vercel URL，例如：`https://adhd-math-learning.vercel.app`

**方式二：使用Vercel CLI**

```bash
# 1. 安装Vercel CLI（如果未安装）
npm install -g vercel

# 2. 登录Vercel
vercel login

# 3. 进入前端目录
cd frontend

# 4. 部署
vercel

# 5. 设置环境变量（使用Railway的API地址）
vercel env add REACT_APP_API_URL production
# 输入: https://adhd-math-backend.up.railway.app

# 6. 生产环境部署
vercel --prod
```

---

## ✅ 验证部署

1. **检查后端**：
   ```bash
   curl https://adhd-math-backend.up.railway.app/api/health
   # 应该返回: {"status":"healthy","timestamp":"..."}
   ```

2. **检查前端**：
   - 访问Vercel URL
   - 尝试注册用户
   - 尝试选择年级和主题
   - 检查浏览器Console是否有错误

3. **检查数据持久化**：
   - 注册一个用户
   - 完成一些练习
   - 刷新页面
   - 数据应该还在

---

## 🔧 如果遇到CORS错误

在 `backend/app.py` 中更新CORS配置：

```python
# 当前代码
CORS(app)

# 修改为
from flask_cors import CORS
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "https://*.vercel.app",  # 允许所有Vercel域名
            "https://adhd-math-learning.vercel.app"  # 你的具体域名
        ]
    }
})
```

重新部署后端到Railway。

---

## 📱 最终结果

部署完成后，你将获得：

- **前端访问地址**: `https://adhd-math-learning.vercel.app`
- **后端API地址**: `https://adhd-math-backend.up.railway.app`
- **全球CDN加速**: Vercel自动提供
- **自动SSL证书**: HTTPS安全连接
- **持久化数据库**: Railway提供的SQLite存储

---

## 💰 成本

- **Railway**: 免费版提供 $5/月 使用额度，足够小型应用使用
- **Vercel**: 免费版提供 100GB 带宽/月，足够个人项目使用

两者都免费，无需信用卡！

---

## 🆘 需要帮助？

如果遇到问题：

1. **查看Railway日志**:
   - 在Railway项目页面点击 "Deployments"
   - 查看构建和运行日志

2. **查看Vercel日志**:
   - 在Vercel项目页面点击 "Deployments"
   - 点击最新的部署查看日志

3. **检查浏览器Console**:
   - 按F12打开开发者工具
   - 查看Console和Network标签页

---

## 🎉 完成！

按照以上步骤，你的ADHD儿童数学学习应用就可以在线访问了！

分享链接给朋友或家长，让孩子们开始学习吧！
