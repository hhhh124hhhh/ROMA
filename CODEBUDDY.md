# ROMA: Recursive Open Meta-Agents - CodeBuddy Guide

## 项目概述

ROMA是一个递归分层多智能体框架，用于构建能够分解复杂任务的AI智能体系统。项目采用Python 3.12+后端（基于FastAPI）和React+TypeScript前端，支持多种LLM提供商。

## 常用开发命令

### 环境设置
```bash
# 自动化设置（推荐）
./setup.sh

# Docker设置
./setup.sh --docker
make setup-docker

# 原生设置
./setup.sh --native
make setup-native

# Windows用户
setup.bat --docker
quickstart.bat
```

### 依赖管理
```bash
# 安装依赖（使用PDM）
make install
pdm install

# 开发环境安装
make install-dev
pdm install -d

# 前端依赖
cd frontend && npm install
```

### 运行服务
```bash
# 启动后端服务器（端口5000）
make run
python -m sentientresearchagent

# 调试模式
make run-debug
python -m sentientresearchagent --debug

# 前端开发服务器（端口3000）
make frontend-dev
cd frontend && npm run dev

# Docker服务
make docker-up
make docker-down
```

### 测试与代码质量
```bash
# 运行测试
make test
pdm run pytest

# 测试覆盖率
make test-coverage

# 代码检查和格式化
make lint
make format
pdm run ruff check src/
pdm run ruff format src/
```

### 清理
```bash
# 清理缓存和日志
make clean
make clean-cache
make clean-logs

# 完整清理
make clean-all
```

## 核心架构

### 递归任务分解模式
ROMA使用递归的plan-execute循环：
```python
def solve(task):
    if is_atomic(task):           # 原子化器判断
        return execute(task)      # 执行器处理
    else:
        subtasks = plan(task)     # 规划器分解
        results = []
        for subtask in subtasks:
            results.append(solve(subtask))  # 递归调用
        return aggregate(results) # 聚合器整合
```

### 关键组件
- **Atomizer**: 判断任务是否为原子任务
- **Planner**: 将复杂任务分解为子任务
- **Executor**: 执行原子任务
- **Aggregator**: 聚合子任务结果

### 项目结构
```
src/sentientresearchagent/
├── hierarchical_agent_framework/  # 核心框架
│   ├── agents/                     # 智能体实现
│   ├── node_handlers/              # 节点处理器
│   ├── orchestration/              # 编排逻辑
│   ├── toolkits/                   # 工具集
│   └── agent_blueprints.py         # 智能体蓝图
├── server/                         # FastAPI服务器
├── config/                         # 配置管理
└── core/                          # 核心功能

frontend/                          # React前端
├── src/                          # TypeScript源码
└── package.json                  # 前端依赖
```

### 智能体蓝图系统
项目包含三个预构建的智能体蓝图：
- `DeepResearchAgent`: 深度研究分析
- `GeneralAgent`: 通用任务解决
- `CryptoAnalyticsAgent`: 加密货币分析

每个蓝图定义了任务类型到处理器的映射（SEARCH、WRITE、THINK）。

### 配置系统
- 使用`SentientConfig`类进行配置管理
- 支持环境变量和配置文件
- 自动加载配置：`auto_load_config()`

### E2B沙盒集成
```bash
# 设置E2B沙盒（可选）
./setup.sh --e2b
./setup.sh --test-e2b
```

### 数据持久化
- 支持S3挂载和本地存储
- 使用goofys进行高性能S3文件系统挂载
- 包含路径注入保护和AWS凭证验证

## 开发注意事项

### 任务类型枚举
使用`TaskType`枚举定义任务类型：
- `TaskType.SEARCH`
- `TaskType.WRITE` 
- `TaskType.THINK`

### 日志系统
项目使用loguru进行日志管理，支持结构化日志和清理格式。

### 前端技术栈
- React 18 + TypeScript
- Vite构建工具
- Tailwind CSS样式
- Socket.IO实时通信
- ReactFlow图形可视化

### 测试配置
使用pytest进行测试，支持异步测试（pytest-asyncio）。

### Docker支持
完整的Docker化部署，包括开发和生产环境配置。