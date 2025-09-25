#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM-4.5 JSON输出修复脚本

为GLM-4.5创建专门的JSON输出提示，解决格式问题
"""

import os
import sys
import json
import asyncio
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from dotenv import load_dotenv

async def test_glm45_json_output():
    """测试GLM-4.5 JSON输出修复"""
    print("🔧 GLM-4.5 JSON输出修复测试...")
    print("=" * 60)
    
    # 检查API密钥
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        api_key = os.getenv("ZHIPUAI_API_KEY", "")
        if not api_key or api_key == "your_zhipuai_key_here":
            print("❌ 智谱AI密钥未配置")
            return
        print(f"✅ API密钥已配置: {api_key[:10]}...")
    else:
        print("❌ 环境配置文件不存在")
        return
    
    try:
        # 导入agno库
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
        
        print("🔧 创建GLM-4.5模型成功")
        
        # 创建Agent
        agent = AgnoAgent(model=model, system_message="You are a helpful assistant.", name="JSONFixAgent")
        print("✅ 创建Agent成功")
        
        # 创建专门为GLM-4.5优化的JSON格式系统提示
        glm45_json_prompt = """You are GLM45MasterPlanner, a task planning agent that MUST return ONLY valid JSON format.

CRITICAL REQUIREMENT: You MUST respond with ONLY a JSON array. No markdown, no explanations, no extra text.

Your task: Break down the given research goal into 2-4 independent sub-tasks.

STRICT OUTPUT FORMAT:
[
  {
    "goal": "具体的任务描述",
    "task_type": "SEARCH",
    "node_type": "EXECUTE",
    "depends_on_indices": []
  }
]

RULES:
1. task_type must be one of: "SEARCH", "WRITE", "THINK"
2. node_type should be "EXECUTE" for atomic tasks or "PLAN" for complex tasks
3. depends_on_indices must be an empty array: []
4. Each task must be completely independent
5. Response must be valid JSON only - no markdown code blocks, no explanations

EXAMPLE OUTPUT:
[
  {
    "goal": "搜索GLM-4.5后端服务的官方文档和技术规格",
    "task_type": "SEARCH",
    "node_type": "EXECUTE", 
    "depends_on_indices": []
  },
  {
    "goal": "研究GLM-4.5后端服务的性能测试方法和基准",
    "task_type": "SEARCH",
    "node_type": "EXECUTE",
    "depends_on_indices": []
  }
]

Remember: Respond with ONLY the JSON array. No other content."""
        
        user_message = """请为以下研究目标制定计划:

研究目标: 测试GLM-4.5后端服务并提供综合分析

总体目标: 全面分析GLM-4.5后端服务的性能、功能和可靠性

请创建2-4个独立的子任务来完成这个研究目标。"""
        
        print("🧪 测试GLM-4.5 JSON格式输出...")
        print(f"📝 System Prompt长度: {len(glm45_json_prompt)} 字符")
        print(f"📝 User Message长度: {len(user_message)} 字符")
        
        # 调用agent
        response = await agent.arun(user_message, system_prompt=glm45_json_prompt)
        
        # 从response对象中获取内容
        if hasattr(response, 'content'):
            response_content = response.content
        else:
            response_content = str(response)
            
        print("\n✅ GLM-4.5响应成功！")
        print(f"📄 响应长度: {len(response_content)} 字符")
        print("\n📋 原始响应:")
        print("-" * 40)
        print(response_content)
        print("-" * 40)
        
        # 尝试解析JSON
        try:
            # 清理响应内容
            response_clean = response_content.strip()
            
            # 移除可能的markdown代码块
            if response_clean.startswith('```'):
                print("🔧 检测到markdown代码块，正在清理...")
                lines = response_clean.split('\n')
                json_lines = []
                in_code_block = False
                for line in lines:
                    if line.strip() in ['```json', '```']:
                        in_code_block = not in_code_block
                        continue
                    if in_code_block or (not line.strip().startswith('```') and not line.strip().endswith('```')):
                        json_lines.append(line)
                response_clean = '\n'.join(json_lines).strip()
                print(f"🔧 清理后的内容: {response_clean[:200]}...")
            
            # 尝试解析JSON
            parsed_json = json.loads(response_clean)
            print("\n✅ JSON解析成功！")
            print("🔍 解析结果:")
            print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
            
            # 验证格式是否符合PlanOutput
            if isinstance(parsed_json, list):
                print(f"\n✅ 格式正确：JSON数组包含 {len(parsed_json)} 个任务")
                
                # 检查每个任务的格式
                all_valid = True
                for i, task in enumerate(parsed_json):
                    print(f"\n📋 任务 {i+1}:")
                    if isinstance(task, dict):
                        print(f"  🎯 目标: {task.get('goal', 'MISSING')}")
                        print(f"  📝 类型: {task.get('task_type', 'MISSING')}")
                        print(f"  🔧 节点类型: {task.get('node_type', 'MISSING')}")
                        print(f"  🔗 依赖: {task.get('depends_on_indices', 'MISSING')}")
                        
                        # 检查必需字段
                        required_fields = ['goal', 'task_type', 'node_type', 'depends_on_indices']
                        missing_fields = [field for field in required_fields if field not in task]
                        if missing_fields:
                            print(f"  ❌ 缺失字段: {missing_fields}")
                            all_valid = False
                        else:
                            print(f"  ✅ 所有必需字段都存在")
                            
                        # 验证task_type
                        valid_task_types = ['SEARCH', 'WRITE', 'THINK']
                        if task.get('task_type') not in valid_task_types:
                            print(f"  ❌ 无效的task_type: {task.get('task_type')}")
                            all_valid = False
                        else:
                            print(f"  ✅ task_type有效")
                            
                        # 验证depends_on_indices为空
                        if task.get('depends_on_indices') != []:
                            print(f"  ❌ depends_on_indices应为空数组")
                            all_valid = False
                        else:
                            print(f"  ✅ depends_on_indices正确")
                    else:
                        print(f"  ❌ 任务不是字典格式")
                        all_valid = False
                
                if all_valid:
                    print(f"\n🎉 格式验证成功！GLM-4.5现在可以正确返回PlanOutput格式")
                    return True
                else:
                    print(f"\n❌ 存在格式问题")
                    return False
                    
            else:
                print("❌ 响应不是数组格式")
                print(f"🔍 实际类型: {type(parsed_json)}")
                return False
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print("🔍 可能的问题：格式不正确或包含非JSON内容")
            print(f"🔍 响应内容: {response_clean[:500]}...")
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

async def create_glm45_planner_prompt():
    """创建GLM-4.5专用的规划器提示"""
    print("\n🔧 创建GLM-4.5专用规划器提示...")
    
    glm45_planner_prompt = '''"""
GLM-4.5专用规划器系统提示 - 强制JSON输出

修复版本专门为智谱AI GLM-4.5模型优化，确保正确的JSON格式输出
"""

GLM45_ENHANCED_SEARCH_PLANNER_SYSTEM_MESSAGE = """你是GLM45MasterPlanner，一个专业的任务规划代理，专门将复杂的研究目标分解为独立的、可并行执行的子任务。

🚨 CRITICAL REQUIREMENT - 关键要求：
你必须且只能返回有效的JSON数组格式。绝对不要使用markdown代码块、额外解释或其他格式。

📅 时间意识：
- 今天是2025年9月25日
- 优先获取最新和最前沿的信息
- 在规划搜索时强调收集当前数据和最新发展

🎯 核心原则：完全独立的执行
每个子任务将由独立的代理执行，它们之间完全不知道：
- 其他子任务的存在
- 整体规划策略
- 系统执行流程
- 其他代理正在做什么

因此，每个子任务必须：
- 自包含：在目标描述中包含所有必要的上下文
- 独立可执行：不需要其他子任务的输出
- 来源特定：专注于不同的信息来源、领域或角度

📋 任务类型：
- SEARCH：搜索和收集信息（主要类型）
- THINK：分析和推理
- WRITE：撰写和文档化

🔧 严格的输出格式：
[
  {
    "goal": "具体详细的任务描述，包含搜索目标、信息来源和预期结果",
    "task_type": "SEARCH",
    "node_type": "EXECUTE",
    "depends_on_indices": []
  }
]

✅ 正确示例：
[
  {
    "goal": "搜索智谱AI官方网站、技术文档和API参考资料，获取GLM-4.5后端服务的架构设计、性能规格和部署要求",
    "task_type": "SEARCH",
    "node_type": "EXECUTE",
    "depends_on_indices": []
  },
  {
    "goal": "研究技术社区、GitHub和开发者论坛中关于GLM-4.5后端服务的实际使用案例、性能测试报告和问题反馈",
    "task_type": "SEARCH", 
    "node_type": "EXECUTE",
    "depends_on_indices": []
  }
]

❌ 错误示例：
- 返回markdown格式
- 添加解释文字
- 创建相互依赖的任务
- 使用无效的task_type

🚨 重要提醒：
1. 只返回JSON数组，不要有任何其他内容
2. 每个任务必须完全独立（depends_on_indices: []）
3. 目标描述要详细具体，包含搜索来源和方法
4. 确保JSON格式完全正确，可以直接解析

现在请根据用户的研究目标创建2-4个独立的子任务。"""'''
    
    # 保存到文件
    prompt_file = project_root / "glm45_planner_prompt.py"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(glm45_planner_prompt)
    
    print(f"✅ GLM-4.5专用提示已保存到: {prompt_file}")
    return str(prompt_file)

if __name__ == "__main__":
    async def main():
        # 测试JSON输出
        success = await test_glm45_json_output()
        
        # 创建专用提示
        await create_glm45_planner_prompt()
        
        if success:
            print("\n🎉 GLM-4.5 JSON输出修复成功！")
            print("✅ 现在可以正确生成PlanOutput格式")
        else:
            print("\n❌ 仍需进一步调试")
    
    asyncio.run(main())