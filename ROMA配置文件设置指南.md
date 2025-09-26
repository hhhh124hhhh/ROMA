# ROMA多智能体系统配置文件设置指南

## 概述

ROMA (Research-Oriented Multi-Agent) 系统是一个基于多智能体架构的研究工具，支持复杂任务的分解、并行执行和结果聚合。本指南详细介绍了配置文件的结构、支持的任务类型以及如何创建自定义配置。

## 支持的任务类型

根据系统的 `types.py` 文件定义，ROMA支持以下6种任务类型：

### 1. WRITE (写作任务)
- **用途**: 内容创作、报告生成、文档编写
- **特点**: 专注于结构化内容输出
- **适用场景**: 
  - 研究报告撰写
  - 分析文档生成
  - 创意内容创作
  - 技术文档编写

### 2. THINK (思考分析任务)
- **用途**: 逻辑推理、数据分析、问题解决
- **特点**: 强调分析思维和推理过程
- **适用场景**: 
  - 数据分析和洞察
  - 逻辑推理和演绎
  - 问题诊断和解决
  - 策略制定和规划

### 3. SEARCH (搜索任务)
- **用途**: 信息检索、数据收集、资源查找
- **特点**: 专注于信息获取和整理
- **适用场景**: 
  - 网络信息搜索
  - 数据库查询
  - 文献调研
  - 市场调研

### 4. AGGREGATE (聚合任务)
- **用途**: 结果整合、信息合并、总结归纳
- **特点**: 将多个子任务结果进行统一处理
- **适用场景**: 
  - 多源信息整合
  - 阶段性结果汇总
  - 最终报告生成
  - 决策支持整合

### 5. CODE_INTERPRET (代码解释任务)
- **用途**: 代码分析、程序理解、技术解释
- **特点**: 专门处理编程和技术相关内容
- **适用场景**: 
  - 代码审查和分析
  - 技术文档生成
  - 程序功能解释
  - 代码优化建议

### 6. IMAGE_GENERATION (图像生成任务)
- **用途**: 图像创建、可视化内容生成
- **特点**: 处理视觉内容的创建需求
- **适用场景**: 
  - 数据可视化
  - 图表生成
  - 概念图制作
  - 演示素材创建

## 配置文件结构详解

### 基本结构

```yaml
# 配置文件注释
profile:
  name: "配置名称"
  description: "配置描述"
  
  # 根级代理配置
  root_planner_adapter_name: "根规划器名称"
  root_aggregator_adapter_name: "根聚合器名称"
  
  # 任务类型映射
  planner_adapter_names:
    SEARCH: "搜索规划器"
    WRITE: "写作规划器"
    THINK: "思考规划器"
    # 其他任务类型...
  
  executor_adapter_names:
    SEARCH: "搜索执行器"
    WRITE: "写作执行器"
    THINK: "思考执行器"
    # 其他任务类型...
  
  aggregator_adapter_names:
    SEARCH: "搜索聚合器"
    WRITE: "写作聚合器"
    THINK: "思考聚合器"
    # 其他任务类型...
  
  # 辅助代理配置
  atomizer_adapter_name: "任务原子化器"
  aggregator_adapter_name: "默认聚合器"
  plan_modifier_adapter_name: "计划修正器"
  
  # 默认配置
  default_planner_adapter_name: "默认规划器"
  default_executor_adapter_name: "默认执行器"
  default_node_agent_name_prefix: "节点前缀"

metadata:
  version: "版本号"
  description: "详细描述"
  use_case: "使用场景"
  recommended_for:
    - "推荐用途1"
    - "推荐用途2"
```

### 核心组件说明

#### 1. 规划器 (Planner)
- **作用**: 将复杂任务分解为可执行的子任务
- **根规划器**: 处理最初的任务分解
- **任务特定规划器**: 针对不同任务类型进行专门规划

#### 2. 执行器 (Executor)
- **作用**: 执行具体的任务操作
- **任务特定执行器**: 针对不同任务类型进行专门执行

#### 3. 聚合器 (Aggregator)
- **作用**: 整合多个子任务的执行结果
- **根聚合器**: 处理最终的结果整合
- **任务特定聚合器**: 针对不同任务类型进行专门聚合

#### 4. 辅助组件
- **原子化器**: 将任务分解到最小执行单元
- **计划修正器**: 根据执行情况调整计划

## 官方配置文件分析

### 1. general_agent.yaml - 通用数据分析配置
```yaml
# 特点: 专注于数据分析和统计研究
# 支持任务类型: SEARCH, WRITE, THINK
# 适用场景: 数据分析、统计研究、商业智能
```

### 2. crypto_analytics_agent.yaml - 加密货币分析配置
```yaml
# 特点: 专门针对加密货币和DeFi分析
# 支持任务类型: SEARCH, WRITE, THINK
# 适用场景: 代币分析、DeFi研究、市场情报
```

### 3. deep_research_agent.yaml - 深度研究配置
```yaml
# 特点: 综合性研究任务处理
# 支持任务类型: SEARCH, WRITE, THINK
# 适用场景: 学术研究、市场分析、技术调研
```

### 4. opensourcegeneralagent.yaml - 开源通用配置
```yaml
# 特点: 开源版本的通用配置
# 支持任务类型: SEARCH, WRITE, THINK
# 适用场景: 与general_agent相同，适用于开源环境
```

### 5. glm45_enhanced_multitask.yaml - GLM-4.5增强配置
```yaml
# 特点: 针对GLM-4.5模型优化的多任务配置
# 支持任务类型: SEARCH, WRITE, THINK
# 适用场景: 复杂研究项目、多步骤分析
```

## 配置文件创建指南

### 步骤1: 确定使用场景
1. 明确任务的主要类型 (SEARCH/WRITE/THINK等)
2. 确定任务的复杂程度
3. 评估所需的专业化程度

### 步骤2: 选择基础模板
- **通用任务**: 基于 `general_agent.yaml`
- **研究任务**: 基于 `deep_research_agent.yaml`
- **专业领域**: 基于 `crypto_analytics_agent.yaml`
- **多任务复杂流程**: 基于 `glm45_enhanced_multitask.yaml`

### 步骤3: 配置任务类型映射
```yaml
planner_adapter_names:
  SEARCH: "适合的搜索规划器"
  WRITE: "适合的写作规划器"
  THINK: "适合的思考规划器"
  # 根据需要添加其他任务类型

executor_adapter_names:
  SEARCH: "适合的搜索执行器"
  WRITE: "适合的写作执行器"
  THINK: "适合的思考执行器"
  # 根据需要添加其他任务类型

aggregator_adapter_names:
  SEARCH: "适合的搜索聚合器"
  WRITE: "适合的写作聚合器"
  THINK: "适合的思考聚合器"
  # 根据需要添加其他任务类型
```

### 步骤4: 设置元数据
```yaml
metadata:
  version: "1.0.0"
  description: "配置的详细描述"
  use_case: "主要使用场景"
  recommended_for:
    - "推荐使用场景1"
    - "推荐使用场景2"
```

## 重要注意事项

### ⚠️ 关键约束条件

1. **任务类型限制**: 只能使用以下6种任务类型
   - WRITE, THINK, SEARCH, AGGREGATE, CODE_INTERPRET, IMAGE_GENERATION
   - ❌ 禁止使用 ANALYZE 等其他任务类型

2. **文件命名**: 配置文件必须以 `.yaml` 结尾

3. **文件位置**: 必须放置在 `agent_configs/profiles/` 目录下

4. **引用一致性**: 配置文件中引用的适配器名称必须在系统中已定义

### 🔧 常见问题排查

1. **验证错误**: 检查任务类型是否为支持的6种类型之一
2. **适配器未找到**: 确认引用的适配器名称在系统中存在
3. **配置加载失败**: 检查YAML语法是否正确
4. **任务分解失败**: 验证规划器配置是否正确

## 最佳实践

### 1. 配置文件命名
- 使用描述性名称: `专业领域_agent.yaml`
- 避免特殊字符和空格
- 使用小写字母和下划线

### 2. 任务类型选择
- 根据实际需求选择任务类型
- 避免配置不使用的任务类型
- 确保每种任务类型都有对应的规划器、执行器和聚合器

### 3. 适配器选择
- 选择与任务类型匹配的适配器
- 考虑性能和准确性平衡
- 根据模型能力选择合适的适配器

### 4. 测试验证
- 创建配置后进行功能测试
- 验证任务分解是否正常工作
- 检查结果聚合是否符合预期

## 配置示例

### 简单研究配置示例
```yaml
# 简单研究代理配置
profile:
  name: "SimpleResearchAgent"
  description: "简单的研究任务处理配置"

  root_planner_adapter_name: "GeneralTaskSolver"
  root_aggregator_adapter_name: "RootGeneralAggregator"

  planner_adapter_names:
    SEARCH: "EnhancedSearchPlanner"
    THINK: "EnhancedThinkPlanner"
    WRITE: "EnhancedWritePlanner"

  executor_adapter_names:
    SEARCH: "OpenAICustomSearcher"
    THINK: "BasicReasoningExecutor"
    WRITE: "BasicReportWriter"

  aggregator_adapter_names:
    SEARCH: "SearchAggregator"
    THINK: "ThinkAggregator"
    WRITE: "WriteAggregator"

  atomizer_adapter_name: "default_atomizer"
  aggregator_adapter_name: "default_aggregator"
  plan_modifier_adapter_name: "PlanModifier"

  default_planner_adapter_name: "GeneralTaskSolver"
  default_executor_adapter_name: "BasicReasoningExecutor"
  default_node_agent_name_prefix: "SimpleResearch"

metadata:
  version: "1.0.0"
  description: "适用于一般研究任务的简化配置"
  use_case: "基础研究和分析任务"
  recommended_for:
    - "文献调研"
    - "基础数据分析"
    - "简单报告生成"
```

## 结论

ROMA系统通过灵活的配置文件系统支持多种任务类型和使用场景。正确理解和配置这些文件是充分发挥系统能力的关键。遵循本指南的建议，可以创建适合特定需求的高效配置文件。