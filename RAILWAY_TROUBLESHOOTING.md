# Railway 502错误故障排查指南 🔧

## 🚨 当前问题

访问 `https://primary-school-math-for-adhd-children-production.up.railway.app/api/health` 返回502错误。

---

## ✅ 必须检查的配置（按顺序）

### 1️⃣ 检查启动命令

在Railway项目页面：

1. 点击 **"Settings"** → **"Service"**
2. 找到 **"Start Command"** 字段
3. **必须**设置为以下之一：

   **选项A（推荐）**：
   ```bash
   gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   ```

   **选项B**：
   留空（Railway会自动检测 `backend/Procfile`）

4. 点击 **"Save"**

---

### 2️⃣ 检查Root Directory

在 **"Settings"** → **"Service"**：

- **Root Directory** 必须设置为：`backend`
- **不是** `./backend`
- **不是** `/backend`
- 就是 `backend`

---

### 3️⃣ 检查部署日志

1. 点击 **"Deployments"** 标签
2. 点击最新的部署
3. 查看 **"Build Logs"**

**应该看到：**
```
Successfully installed gunicorn-21.2.0 ...
```

**然后查看 "Deploy Logs"，应该看到：**
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:XXXX
[INFO] Using worker: sync
[INFO] Booting worker with pid: XXX
✅ 数据库表创建成功！
```

**如果看到错误，复制错误信息**

---

### 4️⃣ 触发重新部署

如果更改了配置：

1. 在 **"Deployments"** 页面
2. 点击右上角的 **"Redeploy"** 或 **"Deploy"**
3. 等待2-3分钟

---

## 🔍 常见错误及解决方案

### 错误1：启动命令仍然是 `python app.py`

**症状**：部署日志显示
```
WARNING: This is a development server.
```

**解决**：
更新启动命令为：
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

---

### 错误2：找不到gunicorn

**症状**：部署日志显示
```
bash: gunicorn: command not found
```

**解决**：
1. 确认最新代码已推送到GitHub
2. 在Railway点击 **"Redeploy"**
3. 确保构建日志显示安装了gunicorn

---

### 错误3：端口绑定失败

**症状**：部署日志显示
```
Error: Invalid bind address
```

**解决**：
确保启动命令中使用 `$PORT` 变量：
```bash
--bind 0.0.0.0:$PORT
```

**不要**写死端口号！

---

### 错误4：Workers启动失败

**症状**：部署日志显示workers crash

**解决**：
减少worker数量，使用：
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

---

### 错误5：数据库初始化超时

**症状**：应用启动但立即崩溃

**解决**：
这不应该发生，因为我们已经移除了启动时的数据初始化。
检查 `backend/app.py` 第83-87行是否只有：
```python
with app.app_context():
    db.create_all()
    print("✅ 数据库表创建成功！")
    print("💡 提示: 访问 /api/init 来初始化课程数据")
```

---

## 📋 完整检查清单

请逐一确认：

- [ ] Root Directory = `backend`
- [ ] Start Command = `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
- [ ] Port设置为空或5000
- [ ] 最新代码已推送到GitHub
- [ ] Railway已重新部署
- [ ] 构建日志显示安装了gunicorn
- [ ] 部署日志显示gunicorn启动
- [ ] 没有Python错误在日志中

---

## 🆘 如果仍然502

### 方案A：查看详细日志

1. 在Railway，点击项目
2. 点击 **"Observability"** 或 **"Logs"**
3. 查找红色错误信息
4. 复制完整的错误堆栈

### 方案B：检查Railway状态

访问 https://status.railway.app/
查看是否有服务中断

### 方案C：使用简化配置

临时使用1个worker测试：

```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 60
```

---

## 📞 提供以下信息以获得帮助

如果问题仍未解决，请提供：

1. **构建日志**的最后50行（从Railway复制）
2. **部署日志**的全部内容
3. **Settings** 截图（显示Root Directory和Start Command）
4. 访问 `/api/health` 时的完整错误响应

---

## 💡 成功标志

当一切正常时，您应该看到：

**部署日志：**
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:8080
[INFO] Using worker: sync
[INFO] Booting worker with pid: 123
✅ 数据库表创建成功！
💡 提示: 访问 /api/init 来初始化课程数据
```

**访问 `/api/health` 返回：**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-15T..."
}
```

**然后就可以访问 `/api/init` 初始化数据了！**

---

## 🚀 下一步

一旦后端正常运行：

1. ✅ 测试 `/api/health`
2. ✅ 访问 `/api/init` 初始化课程数据
3. ✅ 测试 `/api/curriculum/grades` 查看课程列表
4. 🚀 部署前端到Netlify

加油！我们快成功了！ 💪
