# UV环境前后端启动脚本说明

## 概述

为方便使用UV环境启动前后端服务，我们提供了多种启动脚本选择：

## 脚本类型

### 1. 完整版启动器
- **Python脚本**: `start_fullstack_uv.py`
- **批处理文件**: `start_fullstack_uv.bat`
- **特点**: 
  - 在同一个终端中监控前后端输出
  - 自动检查环境依赖
  - 自动安装缺失的依赖
  - 支持优雅停止（Ctrl+C）
  - 提供详细的日志输出

### 2. 简化版启动器
- **Python脚本**: `start_fullstack_simple.py`
- **批处理文件**: `start_fullstack_simple.bat`
- **特点**:
  - 在独立的终端窗口中启动前后端
  - 快速启动，减少复杂性
  - 适合日常开发使用
  - 可以独立控制前后端服务
  - **新增**: 窗口标题显示服务类型
  - **新增**: 启动和停止提示信息
  - **新增**: 服务停止后的友好提示

## 使用方法

### 环境要求
- ✅ UV包管理器
- ✅ Node.js (>=16.0)
- ✅ NPM
- ✅ 智谱AI API密钥配置

### 完整版启动（推荐）

#### Windows
```bash
# 方法1：直接运行批处理文件
start_fullstack_uv.bat

# 方法2：使用UV运行Python脚本
uv run python start_fullstack_uv.py
```

#### Linux/Mac
```bash
uv run python start_fullstack_uv.py
```

### 简化版启动（快速开发）

#### Windows
```bash
# 方法1：直接运行批处理文件
start_fullstack_simple.bat

# 方法2：英文版（避免编码问题）
start_fullstack_en.bat

# 方法3：使用UV运行Python脚本
uv run python start_fullstack_simple.py
```

#### Linux/Mac
```bash
uv run python start_fullstack_simple.py
```

### 编码问题解决方案

如果遇到“文件名、目录名或卷标语法不正确”错误，请使用英文版本：
```bash
start_fullstack_en.bat
```

## 服务地址

启动成功后，可以访问以下地址：

- **前端界面**: http://localhost:3000
- **后端API**: http://localhost:5000
- **系统信息**: http://localhost:5000/api/system-info
- **API文档**: http://localhost:5000/api/docs

## 停止服务

### 完整版启动器
- 按 `Ctrl+C` 优雅停止所有服务

### 简化版启动器
- 关闭对应的终端窗口
- 或在各自窗口中按 `Ctrl+C`

## 新窗口显示信息

为了解决新窗口启动时看不到启动信息的问题，我们对简化版启动器进行了优化：

### 改进特性
- ✅ **窗口标题**: 每个新窗口都有清晰的标题
  - 后端: "GLM-4.5后端服务"
  - 前端: "React前端开发服务器"
- ✅ **启动提示**: 服务启动前显示明确的提示信息
- ✅ **停止提示**: 服务停止后显示友好的停止提示
- ✅ **保持窗口**: 服务停止后窗口不会自动关闭

### 窗口显示效果
```
🚀 启动GLM-4.5后端服务...
[...服务启动日志...]
后端服务已停止，按任意键关闭窗口...
```

### 测试新窗口功能
如果您想测试新窗口启动是否正常工作：
```bash
python test_window_launch.py
```

## 最佳实践

### 窗口管理
- 使用窗口标题区分不同服务
- 关闭窗口前先停止服务（Ctrl+C）
- 可以同时运行多个实例进行测试

### 端口占用问题
如果遇到端口占用，可以：
```bash
# 查看端口占用
netstat -ano | findstr :5000
netstat -ano | findstr :3000

# 强制停止进程（Windows）
taskkill /F /PID <进程ID>
```

### 依赖问题
```bash
# 重新同步UV依赖
uv sync

# 重新安装前端依赖
cd frontend
npm install
```

### 智谱AI配置问题
确保 `.env` 文件中包含：
```
ZHIPUAI_API_KEY=your_api_key_here
```

## 开发建议

1. **日常开发**: 使用简化版启动器 `start_fullstack_simple.bat`
2. **调试问题**: 使用完整版启动器 `start_fullstack_uv.bat`
3. **生产环境**: 使用专门的部署脚本

## 技术特性

- 🚀 使用UV进行Python依赖管理
- 🎯 集成智谱AI GLM-4.5模型
- 🔧 自动环境检查和依赖安装
- 📡 WebSocket实时通信
- 🌐 现代React前端界面
- 📊 完整的API系统