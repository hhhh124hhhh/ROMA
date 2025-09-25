# ROMA-Chinese 结果保存位置详解

## 📁 结果保存的主要位置

根据代码分析和实际文件检查，ROMA-Chinese系统的结果保存在以下位置：

### 1. 主要结果存储目录

#### **experiments/results/** 📊
这是最重要的结果保存目录，包含完整的项目执行结果：

```
f:\person\3-数字化集锦\ROMA\experiments\results\
├── 35a9bef7-3b14-43d2-9261-462cff82cbc5_results.json  (224KB)
├── 8e2ab444-c7e8-45ac-b393-71554870a687_results.json  (258KB)
├── c89ba440-c616-4c8c-be03-35654b8859fc_results.json  (1.6KB)
└── traces/  (包含详细的执行轨迹)
```

**文件格式**: 每个结果文件命名为 `{项目ID}_results.json`

**内容包含**:
- 完整的项目信息和元数据
- 所有节点的执行结果
- 任务分解结构
- 最终的研究报告和分析
- 保存时间戳和版本信息

### 2. 项目运行时目录

#### **runtime/projects/** 🏗️
包含每个项目的运行时状态和工作目录：

```
f:\person\3-数字化集锦\ROMA\runtime\projects\
├── 35a9bef7-3b14-43d2-9261-462cff82cbc5/
│   ├── graph_state.json      (224KB - 执行图状态)
│   ├── results/
│   │   ├── artifacts/        (工件存储)
│   │   ├── plots/           (图表和可视化)
│   │   └── reports/         (报告文件)
│   └── toolkits/           (工具包数据)
└── projects.json           (项目列表和元数据)
```

### 3. 紧急备份目录

#### **experiments/emergency_backups/** 🚨
系统自动创建的紧急备份：

```
f:\person\3-数字化集锦\ROMA\experiments\emergency_backups\
├── 35a9bef7-3b14-43d2-9261-462cff82cbc5_20250925_153915_emergency.json
├── 8e2ab444-c7e8-45ac-b393-71554870a687_20250925_155515_emergency.json
└── ... (其他紧急备份文件)
```

### 4. 执行轨迹存储

#### **experiments/results/traces/** 🔍
详细的执行过程记录：

```
f:\person\3-数字化集锦\ROMA\experiments\results\traces\
└── sentient_v2/
    ├── trace_root.json                    (919KB - 根轨迹)
    ├── trace_root.1.json                  (187KB)
    ├── trace_root.2.json                  (197KB)
    ├── trace_root.1.1.1.1.1.json         (66KB)
    ├── trace_root.1.1.1.1.2.json         (49KB)
    └── ... (120+ 个详细轨迹文件)
```

## 📂 具体的结果文件内容

### 主结果文件示例
以 `35a9bef7-3b14-43d2-9261-462cff82cbc5_results.json` 为例：

```json
{
  "basic_state": {
    "overall_project_goal": "Impact of AI on software development",
    "all_nodes": {
      "root": {
        "output_summary": "完整的研究综合报告...",
        "full_result": "详细的分析结果...",
        "status": "DONE"
      }
    }
  },
  "saved_at": "2025-09-25T16:01:09.684105",
  "metadata": {
    "total_nodes": 3,
    "completion_status": "completed"
  }
}
```

## 🔍 如何查看结果

### 1. 通过文件系统直接访问
```bash
# 查看所有结果文件
dir "f:\person\3-数字化集锦\ROMA\experiments\results\*.json"

# 查看特定项目结果
type "f:\person\3-数字化集锦\ROMA\experiments\results\项目ID_results.json"
```

### 2. 通过前端界面
- 启动前端: `http://localhost:3000`
- 在项目列表中选择已完成的项目
- 点击"下载结果"或"查看详情"

### 3. 通过API访问
```bash
# 获取项目结果
curl http://localhost:5000/api/projects/项目ID

# 下载结果文件
curl http://localhost:5000/api/projects/项目ID/results
```

## 📊 结果文件大小和内容

根据实际检查：

| 项目 | 结果文件大小 | 状态 | 内容类型 |
|------|-------------|------|----------|
| 35a9bef7... | 224KB | 完成 | AI软件开发影响研究 |
| 8e2ab444... | 258KB | 完成 | 开源大模型配置研究 |
| c89ba440... | 1.6KB | 简单 | 基础任务 |

## 🔧 配置和自定义

### 结果保存路径配置
在 [`src/sentientresearchagent/config/paths.py`](file://f:\person\3-数字化集锦\ROMA\src\sentientresearchagent\config\paths.py) 中定义：

```python
self.experiment_results_dir = self.experiments_dir / "results"
self.experiment_emergency_dir = self.experiments_dir / "emergency_backups"
```

### 自动保存机制
- **项目完成时**: 自动保存到 `experiments/results/`
- **执行过程中**: 状态保存到 `runtime/projects/`
- **异常情况**: 紧急备份到 `emergency_backups/`

## 📝 最佳实践

### 1. 结果备份建议
```bash
# 定期备份重要结果
xcopy "f:\person\3-数字化集锦\ROMA\experiments\results" "备份目录\" /s /e /y
```

### 2. 清理旧结果
```bash
# 查看文件大小
dir "f:\person\3-数字化集锦\ROMA\experiments\results" /s

# 清理30天前的轨迹文件（可选）
forfiles /p "f:\person\3-数字化集锦\ROMA\experiments\results\traces" /m *.json /d -30 /c "cmd /c del @path"
```

### 3. 导出和分享
- 使用前端的导出功能导出为 Markdown 或 HTML
- 直接复制 JSON 文件进行程序化处理
- 使用 API 批量下载多个项目结果

## 🎯 总结

**最终结果保存位置**: 
- **主要位置**: `f:\person\3-数字化集锦\ROMA\experiments\results\{项目ID}_results.json`
- **运行时状态**: `f:\person\3-数字化集锦\ROMA\runtime\projects\{项目ID}/`
- **紧急备份**: `f:\person\3-数字化集锦\ROMA\experiments\emergency_backups\`

您的ROMA-Chinese系统已经成功保存了多个项目的完整结果，包括深度递归执行产生的详细分析报告！🎉