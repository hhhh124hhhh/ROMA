# GLM-4.5 集成指南

本指南帮助您快速配置和启动基于智谱AI GLM-4.5模型的SentientResearchAgent。

## 🚀 快速启动

### 1. 配置API密钥

确保在 `.env` 文件中配置了智谱AI API密钥：

```bash
# 智谱AI API密钥 (必需)
ZHIPUAI_API_KEY=你的智谱AI密钥

# 可选：OpenRouter密钥 (作为备用)
OPENROUTER_API_KEY=你的OpenRouter密钥
```

### 2. 一键启动

Windows用户：
```bash
# 双击运行或在命令行执行
start_glm45.bat
```

或直接使用Python：
```bash
python start_glm45.py
```

### 3. 访问服务

- **Web界面**: http://localhost:5000
- **API文档**: http://localhost:5000/api/system-info
- **WebSocket**: ws://localhost:5000

## 📋 配置文件说明

### agents_glm45.yaml
专门为GLM-4.5优化的代理配置，包含：

- **GLM45MasterPlanner**: 主规划器，负责任务分解
- **GLM45SmartExecutor**: 智能执行器，处理搜索和分析
- **GLM45ProWriter**: 专业写作器，生成高质量内容
- **GLM45MasterAggregator**: 结果聚合器，整合信息
- **GLM45AtomizerMaster**: 任务原子化器，分解复杂任务
- **GLM45PlanModifier**: 计划修正器，动态调整策略

### profiles/glm45_profile.yaml
GLM-4.5专业配置档案，定义了：

- 任务类型到代理的映射关系
- 默认代理配置
- 针对中文优化的参数设置

### sentient_glm45.yaml
系统级配置文件，包含：

- 默认使用GLM45Professional配置档案
- Web服务器配置
- 日志和缓存设置
- 执行参数优化

## 🎯 API使用示例

### 研究任务
```bash
curl -X POST http://localhost:5000/api/simple/research \
  -H "Content-Type: application/json" \
  -d '{"topic": "人工智能在医疗领域的应用前景"}'
```

### 分析任务
```bash
curl -X POST http://localhost:5000/api/simple/analysis \
  -H "Content-Type: application/json" \
  -d '{"data": "需要分析的数据或文本", "analysis_type": "trend"}'
```

### 通用执行
```bash
curl -X POST http://localhost:5000/api/simple/execute \
  -H "Content-Type: application/json" \
  -d '{"goal": "写一份关于区块链技术发展的报告"}'
```

## ⚙️ 高级配置

### 模型参数调优

针对不同任务类型的推荐参数：

| 任务类型 | temperature | max_tokens | top_p | 说明 |
|---------|-------------|------------|-------|------|
| 推理分析 | 0.3-0.5 | 3000-4000 | 0.85-0.9 | 需要逻辑性和准确性 |
| 创意写作 | 0.7-0.9 | 4000-6000 | 0.9-0.95 | 需要创造性和流畅性 |
| 信息整合 | 0.4-0.6 | 4000-5000 | 0.85-0.9 | 平衡准确性和连贯性 |
| 任务规划 | 0.5-0.7 | 2000-3000 | 0.8-0.9 | 需要结构化思维 |

### 自定义代理

在 `agents_glm45.yaml` 中添加新代理：

```yaml
- name: "CustomGLM45Agent"
  type: "executor"
  adapter_class: "ExecutorAdapter"
  description: "自定义GLM-4.5代理"
  model:
    provider: "zhipuai"
    model_id: "glm-4.5"
    temperature: 0.7
    max_tokens: 4000
  prompt_source: "your.custom.prompt"
  enabled: true
```

## 🔧 故障排除

### 常见问题

1. **API密钥错误**
   - 检查 `.env` 文件中的 `ZHIPUAI_API_KEY` 是否正确
   - 确认密钥有足够的额度和权限

2. **模型响应慢**
   - 检查网络连接
   - 考虑降低 `max_tokens` 参数
   - 使用更快的模型变体

3. **配置文件错误**
   - 检查YAML文件格式是否正确
   - 确认所有必需的代理都已配置
   - 验证prompt_source路径是否存在

4. **端口占用**
   - 检查5000端口是否被占用
   - 在启动脚本中修改端口配置

### 日志调试

启用详细日志：
```python
# 在sentient_glm45.yaml中设置
logging:
  level: "DEBUG"
  file_mode: "w"
  enable_colors: true
```

## 🚀 性能优化建议

1. **硬件要求**
   - 推荐4GB以上内存
   - 稳定的网络连接

2. **并发处理**
   - 根据API限制调整并发数
   - 使用缓存减少重复调用

3. **参数调优**
   - 根据具体任务调整temperature
   - 合理设置max_tokens避免超时
   - 使用frequency_penalty避免重复

## 📞 技术支持

如遇到问题，请：

1. 检查日志文件中的错误信息
2. 确认所有依赖包已正确安装
3. 验证API密钥和网络连接
4. 参考项目文档和示例配置

---

**享受GLM-4.5驱动的智能研究体验！** 🎉