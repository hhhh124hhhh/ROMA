# GLM-4.5 SentientResearchAgent 启动指南

## 🚀 快速启动

### 一键启动全栈服务（推荐）
```bash
# Windows 双击运行，或命令行执行：
start_fullstack.bat
```
这将启动：
- 后端服务：http://localhost:5000
- 前端服务：http://localhost:3000

### 仅启动后端服务
```bash
# UV环境启动
uv run python start_backend.py

# 或直接Python启动
python start_backend.py
```

## 📁 保留的启动文件

### 核心启动脚本
- `start_fullstack.bat` - **主要启动脚本**，一键启动前后端
- `start_backend.py` - **后端启动脚本**，仅启动GLM-4.5后端服务

### Docker启动
- `docker/start-docker.bat` - Docker容器启动（如果使用Docker）

## 🔧 使用说明

### 1. 环境要求
- Python 3.11+
- UV包管理器
- Node.js（用于前端）
- 智谱AI API密钥

### 2. 配置检查
确保 `.env` 文件中已配置：
```
ZHIPUAI_API_KEY=你的智谱AI密钥
```

### 3. 启动服务
**推荐使用全栈启动**：
- 双击 `start_fullstack.bat`
- 或在命令行运行该脚本

### 4. 访问服务
- **Web界面**: http://localhost:3000
- **API服务**: http://localhost:5000
- **系统信息**: http://localhost:5000/api/system-info

## 🎯 API使用示例

```bash
# 研究任务
curl -X POST http://localhost:5000/api/simple/research \
     -H "Content-Type: application/json" \
     -d '{"topic": "人工智能发展趋势"}'

# 分析任务  
curl -X POST http://localhost:5000/api/simple/analysis \
     -H "Content-Type: application/json" \
     -d '{"data": "待分析的数据"}'
```

## ⚠️ 注意事项

1. **编码问题**: 如遇到Windows批处理文件编码问题，使用 `start_fullstack.bat`（英文版，无特殊字符）
2. **端口占用**: 确保5000和3000端口未被占用
3. **网络连接**: 确保能访问智谱AI API服务

## 🛑 停止服务

- **批处理启动的服务**: 关闭对应的命令行窗口
- **命令行启动的服务**: 按 `Ctrl+C`