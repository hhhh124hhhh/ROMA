# 智譜AI (ZhipuAI) 配置指南

本文档介绍如何在SentientResearchAgent项目中配置和使用智谱AI的GLM-4系列模型。

## 支持的配置方式

### 1. 通过OpenRouter使用智谱GLM模型（推荐）

OpenRouter提供了智谱GLM-4模型的访问，这是目前最稳定的方式：

#### 配置环境变量
```bash
# .env文件中添加
OPENROUTER_API_KEY=your_openrouter_key_here
```

#### agents.yaml配置示例
```yaml
agents:
  - name: "ZhipuGLMPlanner"
    type: "planner"
    adapter_class: "PlannerAdapter"
    description: "使用智谱GLM-4模型的规划器"
    model:
      provider: "litellm"
      model_id: "openrouter/z-ai/glm-4-32b"  # 通过OpenRouter访问GLM-4
      temperature: 0.7
      max_tokens: 4000
    prompt_source: "prompts.planner_prompts.PLANNER_SYSTEM_MESSAGE"
    response_model: "PlanOutput"
    registration:
      action_keys:
        - action_verb: "plan"
          task_type: "WRITE"
      named_keys: ["ZhipuGLMPlanner"]
    enabled: true

  - name: "ZhipuGLMExecutor"
    type: "executor"
    adapter_class: "ExecutorAdapter"
    description: "使用智谱GLM-4模型的执行器"
    model:
      provider: "litellm"
      model_id: "openrouter/z-ai/glm-4-32b"
      temperature: 0.7
      max_tokens: 2000
    prompt_source: "prompts.executor_prompts.REASONING_EXECUTOR_SYSTEM_MESSAGE"
    tools: ["PythonTools", "ReasoningTools"]
    registration:
      action_keys:
        - action_verb: "execute"
          task_type: "THINK"
      named_keys: ["ZhipuGLMExecutor"]
    enabled: true
```

### 2. 直接使用智谱AI API（实验性）

如果项目后续支持直接调用智谱AI接口：

#### 配置环境变量
```bash
# .env文件中添加
ZHIPUAI_API_KEY=your_zhipuai_key_here
```

#### agents.yaml配置示例
```yaml
agents:
  - name: "DirectZhipuPlanner"
    type: "planner"
    adapter_class: "PlannerAdapter"
    description: "直接使用智谱AI的规划器"
    model:
      provider: "zhipuai"
      model_id: "glm-4"  # 或 "glm-4-air", "glm-4-flash"
      temperature: 0.7
      max_tokens: 4000
    prompt_source: "prompts.planner_prompts.PLANNER_SYSTEM_MESSAGE"
    response_model: "PlanOutput"
    registration:
      action_keys:
        - action_verb: "plan"
          task_type: "WRITE"
      named_keys: ["DirectZhipuPlanner"]
    enabled: false  # 当前为实验性功能，默认禁用
```

## 可用的智谱AI模型

### 通过OpenRouter可用的模型
- `openrouter/z-ai/glm-4-32b` - GLM-4模型，32B参数版本

### 直接API可用的模型（当支持时）
- `glm-4` - 标准GLM-4模型
- `glm-4-air` - 轻量版GLM-4模型
- `glm-4-flash` - 快速版GLM-4模型
- `glm-4-plus` - 增强版GLM-4模型

## 获取API密钥

### OpenRouter API密钥
1. 访问 [OpenRouter](https://openrouter.ai/)
2. 注册账户并登录
3. 在控制台中生成API密钥
4. 将密钥添加到`.env`文件中

### 智谱AI API密钥
1. 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
2. 注册账户并完成实名认证
3. 在控制台中创建应用并获取API密钥
4. 将密钥添加到`.env`文件中

## 配置验证

项目已内置智谱AI的环境变量验证：

```python
# models.py中的验证逻辑
elif model_id.startswith("zhipuai/") or model_id.startswith("glm-"):
    if not os.getenv("ZHIPUAI_API_KEY"):
        raise ValueError(
            f"ZhipuAI model '{model_id}' requires ZHIPUAI_API_KEY environment variable"
        )
```

## 使用建议

1. **生产环境**：推荐使用OpenRouter方式，稳定性更高
2. **开发测试**：可以尝试直接API方式，但需要注意可能的兼容性问题
3. **模型选择**：
   - GLM-4适合复杂推理任务
   - GLM-4-Air适合快速响应场景
   - GLM-4-Flash适合大批量处理

## 故障排除

### 常见问题

1. **API密钥错误**
   ```
   ZhipuAI model 'glm-4' requires ZHIPUAI_API_KEY environment variable
   ```
   解决方案：检查`.env`文件中的`ZHIPUAI_API_KEY`配置

2. **模型不可用**
   ```
   Model 'openrouter/z-ai/glm-4-32b' not found
   ```
   解决方案：检查OpenRouter账户中是否有模型访问权限

3. **超时错误**
   - 增加`timeout`参数或降低`max_tokens`

### 调试技巧

启用详细日志：
```bash
export LOG_LEVEL=DEBUG
```

检查模型加载过程：
```bash
# 查看日志中的模型创建信息
grep "Creating.*model" logs/app.log
```

## 更新历史

- 2025-01-XX: 添加智谱AI支持
- 2025-01-XX: 完善配置验证和错误处理