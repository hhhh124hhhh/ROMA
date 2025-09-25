# ROMA-Chinese 深度递归执行指南

## 问题诊断与解决

### 原始问题
您遇到的"只启动一层就结束"问题是由于以下配置导致的：

1. **任务原子化被禁用**: `skip_atomization: true`
2. **强制根节点规划**: `force_root_node_planning: true`
3. **执行步骤限制过低**: `max_execution_steps: 500`

### 解决方案

我们已经修改了以下配置文件：

#### 1. sentient.yaml 配置优化
```yaml
# 执行框架优化
execution:
  max_execution_steps: 1000  # 增加到1000步，支持更深层递归
  max_concurrent_nodes: 15   # 增加并发节点数
  max_parallel_nodes: 12     # 增加并行处理能力
  
  # 启用深度递归执行
  skip_atomization: false    # ✅ 启用任务原子化
  force_root_node_planning: false  # ✅ 允许智能决策
```

#### 2. agents_glm45_simple.yaml 模型优化
- **规划器**: 温度降低到0.3，令牌增加到5000，提供更精确的规划
- **原子化器**: 温度降低到0.2，提供更精准的任务分解

### 启动方式

#### 方式1: 增强递归执行（推荐）
```bash
# 使用增强版后端
uv run python start_enhanced_backend.py

# 或使用增强版全栈启动
start_enhanced_fullstack.bat
```

#### 方式2: 标准启动
```bash
# 标准后端启动
uv run python start_backend.py

# 标准全栈启动
start_fullstack.bat
```

### 配置对比

| 特性 | 原始配置 | 增强配置 | 效果 |
|------|----------|----------|------|
| 任务原子化 | 禁用 | ✅ 启用 | 支持深度分解 |
| 执行步骤 | 500 | 1000 | 支持更长推理链 |
| 并发节点 | 10 | 15 | 更高并行处理 |
| 规划精度 | 0.6温度 | 0.3温度 | 更精确规划 |

### 验证深度递归执行

运行测试脚本验证改进效果：
```bash
uv run python test_recursive_execution.py
```

### 关键改进指标

启动日志中关键指标应显示：
```
🐛 NodeProcessorConfig: skip_atomization = False, max_planning_layer = 5
```

这表明系统已启用深度递归执行。

## 使用建议

### 适合深度递归的任务类型
1. **复杂研究任务**: 需要多维度分析的主题
2. **技术调研**: 需要深入了解技术架构、应用、挑战等
3. **对比分析**: 需要多角度比较的复杂问题
4. **系统设计**: 需要分层设计的复杂系统

### API 使用示例
```bash
# 复杂研究任务
curl -X POST http://localhost:5000/api/simple/research \
  -H "Content-Type: application/json" \
  -d '{"topic": "区块链技术在供应链管理中的应用研究，包括技术架构、实施挑战、成本效益分析和发展前景"}'

# 技术分析任务
curl -X POST http://localhost:5000/api/simple/analysis \
  -H "Content-Type: application/json" \
  -d '{"topic": "人工智能在金融科技领域的应用现状、技术挑战和未来趋势"}'
```

### 监控执行过程

查看实时日志了解递归执行情况：
```bash
# Windows PowerShell
Get-Content runtime\logs\sentient.log -Tail 50 -Wait

# 查看特定执行步骤
Get-Content runtime\logs\sentient.log | Select-String "execution.*step|步骤" | Select-Object -Last 20
```

## 故障排除

### 如果仍然只执行一层
1. 确认配置文件修改已生效
2. 重启后端服务
3. 检查日志中的 `skip_atomization = False`
4. 尝试更复杂的任务来触发递归

### 性能优化建议
- 对于简单任务，使用标准启动方式
- 对于复杂任务，使用增强递归执行方式
- 根据任务复杂度调整 `max_execution_steps`
- 监控系统资源使用情况

## 结论

通过这些配置优化，ROMA-Chinese 现在应该能够：
- ✅ 进行深度任务分解
- ✅ 支持多层递归执行
- ✅ 处理复杂的研究和分析任务
- ✅ 提供更详细和全面的结果

您的"只启动一层就结束"问题应该已经得到解决！