#!/usr/bin/env python3
"""
测试GLM-4.5修复后的JSON包装格式

验证GLM-4.5现在是否能返回正确的{sub_tasks: [...]}格式
"""

import os
import asyncio
import json
from dotenv import load_dotenv

async def test_glm45_fixed_format():
    """测试GLM-4.5修复后的JSON包装格式"""
    
    print("🧪 测试GLM-4.5修复后的JSON包装格式...")
    
    # 加载环境变量
    load_dotenv()
    api_key = os.getenv("ZHIPUAI_API_KEY")
    
    if not api_key:
        print("❌ 未找到ZHIPUAI_API_KEY环境变量")
        return False
    
    try:
        from agno.models.openai.chat import OpenAIChat
        from agno.agent import Agent as AgnoAgent
        
        # 创建角色映射修复
        zhipuai_role_map = {
            "system": "system",
            "user": "user", 
            "assistant": "assistant",
            "tool": "tool",
            "model": "assistant",
        }
        
        # 创建GLM-4.5模型
        model = OpenAIChat(
            id="glm-4.5",
            base_url="https://open.bigmodel.cn/api/paas/v4/",
            api_key=api_key,
            temperature=0.6,
            max_tokens=2000,
            role_map=zhipuai_role_map
        )
        
        print("✅ 创建GLM-4.5模型成功")
        
        # 创建Agent
        agent = AgnoAgent(model=model, system_message="You are a helpful assistant.", name="FormatFixTestAgent")
        print("✅ 创建Agent成功")
        
        # 使用修复后的GLM45专用提示
        fixed_system_prompt = """🚨 CRITICAL: 你必须且只能返回有效的JSON对象格式（包含sub_tasks字段），绝对不要使用markdown、解释或其他格式！

你是GLM45MasterPlanner，专业的任务规划代理，将复杂研究目标分解为独立的、可并行执行的子任务。

📅 时间意识：
- 今天：2025年9月25日
- 强调收集最新和实时信息
- 优先获取当前数据和最新发展

🎯 核心原则：完全独立执行
每个子任务由独立代理执行，它们之间完全不知道：
- 其他子任务的存在
- 整体规划策略
- 系统执行流程
- 其他代理正在做什么

每个子任务必须：
- 自包含：在目标描述中包含所有必要上下文
- 独立可执行：不需要其他子任务输出
- 来源特定：专注不同信息来源、领域或角度

📋 任务类型：
- SEARCH：搜索和收集信息（主要）
- THINK：分析和推理
- WRITE：撰写和文档化

🔧 严格输出格式（ONLY JSON对象）：
{
  "sub_tasks": [
    {
      "goal": "详细的任务描述，包含搜索目标、来源和方法",
      "task_type": "SEARCH",
      "node_type": "EXECUTE", 
      "depends_on_indices": []
    }
  ]
}

✅ 正确示例：
{
  "sub_tasks": [
    {
      "goal": "搜索智谱AI官方网站、技术文档和API参考，获取GLM-4.5架构设计、性能规格和部署要求",
      "task_type": "SEARCH",
      "node_type": "EXECUTE",
      "depends_on_indices": []
    },
    {
      "goal": "研究技术社区、GitHub和开发者论坛中GLM-4.5的实际使用案例、性能测试和问题反馈", 
      "task_type": "SEARCH",
      "node_type": "EXECUTE",
      "depends_on_indices": []
    }
  ]
}

🚨 绝对禁止：
- Markdown格式（# ## ###）
- 代码块（```）
- 解释性文字
- 相互依赖的任务
- 无效的task_type

⚡ 重要：只返回带sub_tasks字段的JSON对象，无其他内容！"""
        
        # 更新Agent的系统消息
        agent.system_message = fixed_system_prompt
        
        # 测试任务
        test_query = "请为'GLM-4.5 JSON修复测试'制定一个详细的研究计划"
        
        print(f"\n🔍 测试查询: {test_query}")
        print("🚀 发送请求...")
        
        # 发送请求
        response = await agent.arun(test_query)
        
        # 提取实际的内容字符串
        if hasattr(response, 'content'):
            response_content = response.content
        else:
            response_content = str(response)
        
        print(f"📨 GLM-4.5响应:")
        print(f"原始响应: {response_content}")
        
        # 验证JSON格式
        try:
            # 清理响应（移除可能的markdown标记）
            response_clean = response_content.strip()
            if response_clean.startswith("```json"):
                response_clean = response_clean[7:]
            if response_clean.startswith("```"):
                response_clean = response_clean[3:]
            if response_clean.endswith("```"):
                response_clean = response_clean[:-3]
            response_clean = response_clean.strip()
            
            print(f"清理后响应: {response_clean}")
            
            # 解析JSON
            parsed_json = json.loads(response_clean)
            
            # 验证结构
            if isinstance(parsed_json, dict) and "sub_tasks" in parsed_json:
                sub_tasks = parsed_json["sub_tasks"]
                
                if isinstance(sub_tasks, list) and len(sub_tasks) > 0:
                    print(f"✅ 格式正确！包含 {len(sub_tasks)} 个子任务")
                    
                    # 验证每个子任务的结构
                    all_valid = True
                    for i, task in enumerate(sub_tasks):
                        if not isinstance(task, dict):
                            print(f"❌ 任务 {i} 不是字典格式")
                            all_valid = False
                            continue
                            
                        required_fields = ["goal", "task_type", "depends_on_indices"]
                        for field in required_fields:
                            if field not in task:
                                print(f"❌ 任务 {i} 缺少字段: {field}")
                                all_valid = False
                        
                        # 验证task_type有效性
                        if "task_type" in task and task["task_type"] not in ["SEARCH", "THINK", "WRITE"]:
                            print(f"❌ 任务 {i} task_type无效: {task['task_type']}")
                            all_valid = False
                        
                        # 验证depends_on_indices是列表
                        if "depends_on_indices" in task and not isinstance(task["depends_on_indices"], list):
                            print(f"❌ 任务 {i} depends_on_indices不是列表")
                            all_valid = False
                    
                    if all_valid:
                        print(f"\n🎉 完美！GLM-4.5现在可以正确返回PlanOutput包装格式")
                        print("✅ 包含sub_tasks字段的JSON对象")
                        print("✅ 所有子任务格式正确")
                        print("✅ 字段验证通过")
                        return True
                    else:
                        print(f"\n❌ 子任务格式存在问题")
                        return False
                        
                else:
                    print("❌ sub_tasks不是有效数组或为空")
                    return False
                    
            else:
                print("❌ 响应不包含sub_tasks字段或不是对象格式")
                print(f"🔍 实际结构: {type(parsed_json)}")
                if isinstance(parsed_json, dict):
                    print(f"🔍 可用字段: {list(parsed_json.keys())}")
                return False
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print("🔍 可能的问题：格式不正确或包含非JSON内容")
            print(f"🔍 响应内容: {response_content[:500]}...")
            return False
            
        except Exception as e:
            print(f"❌ 解析过程出错: {e}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        print("完整错误追踪:")
        traceback.print_exc()
        return False

async def main():
    """主函数"""
    print("=" * 80)
    print("🧪 GLM-4.5 JSON包装格式修复测试")
    print("=" * 80)
    
    success = await test_glm45_fixed_format()
    
    print("\n" + "=" * 80)
    if success:
        print("🎉 测试成功！GLM-4.5现在可以返回正确的包装格式")
        print("✅ 数据格式问题已解决")
        print("✅ 后端服务应该可以正常运行")
    else:
        print("❌ 测试失败，需要进一步调试")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())