#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试GLM-4.5输出格式脚本

测试GLM-4.5返回的实际格式并分析PlanOutput解析错误
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

async def test_glm45_planning_output():
    """测试GLM-4.5规划输出格式"""
    print("🔍 调试GLM-4.5规划输出格式...")
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
            "system": "system",  # 保持system为system，不是developer
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
            temperature=0.7,
            max_tokens=2000,
            role_map=zhipuai_role_map
        )
        
        print("🔧 创建GLM-4.5模型成功")
        
        # 创建Agent
        agent = AgnoAgent(model=model, system_message="You are a helpful assistant.", name="DebugAgent")
        print("✅ 创建Agent成功")
        
        # 测试规划任务的system prompt（模拟系统实际使用的prompt）
        system_prompt = """You are GLM45MasterPlanner, a sophisticated planning agent that breaks down complex tasks into actionable sub-tasks.

Your role:
- Analyze the given task goal and context
- Create a structured plan with clear sub-tasks
- Ensure each sub-task is specific and actionable
- Consider dependencies between sub-tasks

Output Format Requirements:
You MUST return a JSON object in exactly this format:
{
    "sub_tasks": [
        {
            "goal": "Specific description of what needs to be done",
            "task_type": "SEARCH|WRITE|THINK",
            "node_type": "PLAN",
            "depends_on_indices": []
        }
    ]
}

Important Rules:
- The root key MUST be "sub_tasks" (not "sub_goals")
- Each sub-task MUST have: goal, task_type, node_type, depends_on_indices
- task_type must be one of: SEARCH, WRITE, THINK
- node_type should be "PLAN" for complex tasks or "EXECUTE" for atomic tasks
- depends_on_indices is a list of 0-based indices of other sub-tasks this task depends on
- Return ONLY the JSON object, no additional text or formatting

Example:
{
    "sub_tasks": [
        {
            "goal": "Research current GLM-4.5 backend service status",
            "task_type": "SEARCH",
            "node_type": "EXECUTE",
            "depends_on_indices": []
        },
        {
            "goal": "Analyze service performance metrics",
            "task_type": "THINK", 
            "node_type": "EXECUTE",
            "depends_on_indices": [0]
        }
    ]
}"""
        
        user_message = """Current Task Goal: Research 测试GLM-4.5后端服务 and provide a comprehensive summary

Context:
Overall Objective: Research 测试GLM-4.5后端服务 and provide a comprehensive summary
Current Task: Research 测试GLM-4.5后端服务 and provide a comprehensive summary

Please create a structured plan to accomplish this research task."""
        
        print("🧪 测试GLM-4.5规划任务...")
        print(f"📝 System Prompt长度: {len(system_prompt)} 字符")
        print(f"📝 User Message长度: {len(user_message)} 字符")
        
        # 调用agent
        response = await agent.arun(user_message, system_prompt=system_prompt)
        
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
            if response_content.strip().startswith('```'):
                # 移除markdown代码块
                lines = response_content.strip().split('\n')
                json_lines = []
                in_code_block = False
                for line in lines:
                    if line.strip() == '```json' or line.strip() == '```':
                        in_code_block = not in_code_block
                        continue
                    if in_code_block:
                        json_lines.append(line)
                response_clean = '\n'.join(json_lines)
            else:
                response_clean = response_content.strip()
            
            parsed_json = json.loads(response_clean)
            print("\n✅ JSON解析成功！")
            print("🔍 解析结果:")
            print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
            
            # 检查格式是否符合PlanOutput
            if "sub_tasks" in parsed_json:
                sub_tasks = parsed_json["sub_tasks"]
                print(f"\n✅ 找到sub_tasks字段，包含 {len(sub_tasks)} 个任务")
                
                for i, task in enumerate(sub_tasks):
                    print(f"\n📋 任务 {i+1}:")
                    print(f"  🎯 目标: {task.get('goal', 'MISSING')}")
                    print(f"  📝 类型: {task.get('task_type', 'MISSING')}")
                    print(f"  🔧 节点类型: {task.get('node_type', 'MISSING')}")
                    print(f"  🔗 依赖: {task.get('depends_on_indices', 'MISSING')}")
                    
                    # 检查必需字段
                    required_fields = ['goal', 'task_type', 'node_type', 'depends_on_indices']
                    missing_fields = [field for field in required_fields if field not in task]
                    if missing_fields:
                        print(f"  ❌ 缺失字段: {missing_fields}")
                    else:
                        print(f"  ✅ 所有必需字段都存在")
                        
            else:
                print("❌ 未找到sub_tasks字段")
                print(f"🔍 实际字段: {list(parsed_json.keys())}")
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print("🔍 可能的问题：格式不正确或包含非JSON内容")
            
        except Exception as e:
            print(f"❌ 解析过程出错: {e}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        print("完整错误追踪:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_glm45_planning_output())