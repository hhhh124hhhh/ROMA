# ROMA智能体灵活启动指南

## 概述

本指南介绍了如何灵活启动不同类型的ROMA智能体配置，包括专门的AI产品痛点收集智能体和其他专业智能体。

## 可用的启动方式

### 1. 专用启动脚本（推荐用于痛点收集）

#### Windows批处理启动
```bash
# 启动AI产品痛点收集智能体（全栈）
start_pain_point_collector.bat

# 仅启动后端服务
uv run python start_pain_point_collector_backend.py
```

#### 特点
- ✅ 专门为AI产品痛点收集智能体优化
- ✅ 详细的功能说明和使用示例
- ✅ 自动检查配置文件和环境
- ✅ 同时启动前端和后端服务

### 2. 灵活启动脚本（推荐用于多配置切换）

#### Python灵活启动（功能最全）
```bash
# 交互式选择模式
uv run python start_flexible_agent.py

# 直接指定配置启动
uv run python start_flexible_agent.py --profile 1
uv run python start_flexible_agent.py --profile ai_product_pain_point_collector

# 列出所有可用配置
uv run python start_flexible_agent.py --list
```

#### Windows批处理灵活启动
```bash
# 交互式选择启动
start_flexible_agent.bat
```

#### 特点
- ✅ 支持5种不同的智能体配置
- ✅ 交互式选择界面
- ✅ 命令行参数支持
- ✅ 完整的环境检查
- ✅ 配置文件自动验证

## 支持的智能体配置

### 🎯 1. AI产品痛点收集智能体
**配置名**: `ai_product_pain_point_collector`
**描述**: 专业的AI产品痛点收集、分析和解决方案生成系统

**专业团队**:
- 痛点发现专家 - 多渠道信息收集
- 痛点分析专家 - 深度分析和分类
- 竞品研究专家 - 对比分析
- 优先级专家 - 影响评估和排序
- 解决方案专家 - 改进方案设计
- 报告专家 - 专业报告生成

**工作流程**:
1. 痛点发现阶段
2. 痛点分类阶段
3. 深度分析阶段
4. 优先级排序阶段
5. 解决方案阶段

### ⚡ 2. GLM-4.5增强多任务智能体
**配置名**: `glm45_enhanced_multitask`
**描述**: 复杂的多层级、多类型任务工作流处理系统

**特性**:
- 智能任务分解
- 并行执行支持
- 依赖关系管理
- 结果聚合整合

### 🤖 3. GLM-4.5专业智能体
**配置名**: `glm45_professional`
**描述**: 专为智谱AI GLM-4.5模型优化的专业代理配置

**特性**:
- 中文理解优化
- 逻辑推理能力
- 创意写作支持
- 问答系统

### 🔍 4. 深度研究智能体
**配置名**: `deep_research_agent`
**描述**: 综合性研究任务处理，支持多步骤分析

**适用场景**:
- 学术研究
- 市场分析
- 技术调研
- 事实核查验证

### 💰 5. 加密货币分析智能体
**配置名**: `crypto_analytics_agent`
**描述**: 专门用于加密货币和DeFi分析的智能体

**专业能力**:
- 代币深度分析
- DeFi协议研究
- 市场情报收集
- 链上数据分析

## 环境要求

### 必需环境变量
```bash
# 智谱AI API密钥（必需）
ZHIPUAI_API_KEY=your_zhipuai_api_key

# E2B沙箱配置（可选，用于代码执行）
E2B_API_KEY=your_e2b_api_key
E2B_TEMPLATE_ID=your_e2b_template_id
```

### 软件依赖
- Python 3.8+
- UV包管理器
- Node.js（用于前端服务）

## 使用示例

### AI产品痛点收集任务示例

```
任务：请系统性收集和分析我们AI写作助手产品的用户痛点

预期输出：
1. 多渠道痛点信息收集
2. 痛点严重程度分类
3. 根因分析报告
4. 竞品对比分析
5. 优先级排序矩阵
6. 可执行的改进方案
```

```
任务：分析AI聊天机器人的用户体验问题并提供改进建议

重点关注：
- 对话质量和准确性
- 响应速度和稳定性
- 用户界面和交互体验
- 功能完整性和易用性
```

### 其他智能体任务示例

#### GLM-4.5增强多任务
```
任务：请进行一个综合性的市场研究项目
要求：分析电动汽车市场现状、技术趋势、竞争格局，并预测未来发展
```

#### 深度研究智能体
```
任务：研究人工智能在医疗诊断中的应用现状和发展趋势
要求：包括技术综述、案例分析、挑战识别和未来预测
```

#### 加密货币分析智能体
```
任务：分析比特币和以太坊的技术基础、市场表现和投资价值
要求：包括技术分析、基本面分析和风险评估
```

## 启动流程

### 方式一：专用脚本启动（痛点收集）
1. 确保在项目根目录
2. 检查环境变量配置
3. 运行 `start_pain_point_collector.bat`
4. 等待服务启动完成
5. 访问 http://localhost:3000

### 方式二：灵活脚本启动（多配置）
1. 运行 `uv run python start_flexible_agent.py`
2. 查看可用配置列表
3. 选择所需的智能体配置
4. 系统自动验证和启动
5. 访问 http://localhost:5000

### 方式三：命令行直接启动
```bash
# 设置环境变量
export SENTIENT_PROFILE="ai_product_pain_point_collector"
export SENTIENT_AGENTS_CONFIG="agents_pain_point_collector.yaml"

# 启动服务
uv run python -m sentientresearchagent.server.main
```

## 故障排除

### 常见问题

1. **配置文件不存在**
   ```
   ❌ 配置文件不存在: ai_product_pain_point_collector.yaml
   ```
   **解决方案**: 确保配置文件存在于 `src/sentientresearchagent/hierarchical_agent_framework/agent_configs/profiles copy/` 目录

2. **环境变量未设置**
   ```
   ❌ 智谱AI密钥未配置
   ```
   **解决方案**: 在 `.env` 文件中设置 `ZHIPUAI_API_KEY=your_key`

3. **UV未安装**
   ```
   ❌ UV未安装，请先安装UV
   ```
   **解决方案**: 安装UV包管理器 `pip install uv`

4. **端口占用**
   ```
   ❌ 端口5000已被占用
   ```
   **解决方案**: 停止占用端口的服务或修改配置使用其他端口

### 调试模式

启用调试模式获取更详细的日志信息：
```bash
export DEBUG=true
uv run python start_flexible_agent.py --profile 1
```

### 日志查看

查看服务运行日志：
```bash
# 查看后端日志
tail -f logs/backend.log

# 查看前端日志  
tail -f logs/frontend.log
```

## 高级配置

### 自定义端口
```bash
export PORT=8080
export FRONTEND_PORT=3001
```

### 自定义模型参数
```bash
export GLM_TEMPERATURE=0.7
export GLM_MAX_TOKENS=4000
```

### 启用额外功能
```bash
export ENABLE_WEB_SEARCH=true
export ENABLE_CODE_EXECUTION=true
export ENABLE_VISUALIZATION=true
```

## 总结

ROMA智能体灵活启动系统提供了多种启动方式，满足不同使用场景的需求：

- **专用脚本**: 适合专门使用某个特定智能体配置
- **灵活脚本**: 适合需要频繁切换不同配置的开发和测试
- **命令行**: 适合自动化脚本和高级用户

选择最适合您需求的启动方式，享受ROMA智能体系统带来的强大功能！