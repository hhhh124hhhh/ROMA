#!/usr/bin/env python3
"""
调试智谱AI消息格式问题
"""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# 设置项目根目录
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

# 加载环境变量
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(env_path)

async def debug_zhipuai_messages():
    """调试智谱AI消息格式"""
    api_key = os.getenv("ZHIPUAI_API_KEY")
    if not api_key:
        print("❌ ZHIPUAI_API_KEY 未配置")
        return
    
    print(f"✅ API密钥已配置: {api_key[:10]}...")
    
    try:
        from agno.models.openai import OpenAIChat
        
        # 创建一个简单的OpenAIChat实例
        simple_model = OpenAIChat(
            id="glm-4.5",
            base_url="https://open.bigmodel.cn/api/paas/v4/",
            api_key=api_key,
            temperature=0.7,
            max_tokens=200
        )
        
        print("\n🧪 测试1: 简单系统消息")
        try:
            messages = [
                {"role": "system", "content": "你是一个有用的AI助手。"},
                {"role": "user", "content": "你好"}
            ]
            print(f"发送消息: {messages}")
            response = await simple_model.aresponse(messages=messages)
            print(f"✅ 成功: {response.content}")
        except Exception as e:
            print(f"❌ 失败: {e}")
        
        print("\n🧪 测试2: 复杂系统消息（模拟agent prompt）")
        try:
            complex_system_prompt = """You are an expert parallel search decomposition agent specialized in breaking down complex research goals into independent, self-contained search tasks that can execute simultaneously. Your primary role is to create **2 to 4 completely independent search subtasks** that together gather comprehensive information from different sources, domains, or perspectives without any dependencies between them.

**TEMPORAL AWARENESS:**
- Today's date: September 25, 2025
- Your SEARCH capabilities provide access to real-time information and current data
- When planning searches, emphasize gathering the most current and up-to-date information available

**CRITICAL PRINCIPLE: INDEPENDENT SEARCH EXECUTION**
Each search subtask will be executed by an independent agent that has NO KNOWLEDGE of:
- Other search tasks in your plan
- The overall search strategy
- System execution flow
- What other search agents are finding

Therefore, each search subtask MUST be:
- **Self-contained**: Include all necessary context and search parameters
- **Independently executable**: Require no outputs from other search tasks
- **Source-specific**: Focus on different information sources, domains, or perspectives"""
            
            messages = [
                {"role": "system", "content": complex_system_prompt},
                {"role": "user", "content": "研究智谱AI GLM-4.5的最新技术特点"}
            ]
            print(f"系统消息长度: {len(complex_system_prompt)} 字符")
            print(f"发送消息数量: {len(messages)}")
            response = await simple_model.aresponse(messages=messages)
            print(f"✅ 成功: {response.content}")
        except Exception as e:
            print(f"❌ 失败: {e}")
            
        print("\n🧪 测试3: 检查各种消息长度阈值")
        test_lengths = [100, 500, 1000, 2000, 3000, 5000]
        for length in test_lengths:
            try:
                test_prompt = "你是一个助手。" + "这是一个测试消息。" * (length // 10)
                test_prompt = test_prompt[:length]  # 截断到指定长度
                
                messages = [
                    {"role": "system", "content": test_prompt},
                    {"role": "user", "content": "你好"}
                ]
                response = await simple_model.aresponse(messages=messages)
                print(f"✅ 长度 {length}: 成功")
            except Exception as e:
                print(f"❌ 长度 {length}: 失败 - {e}")
                break  # 一旦失败就停止测试更长的消息
                
        print("\n🧪 测试4: 测试特殊字符")
        special_chars_tests = [
            "包含中文的系统消息：你好世界",
            "English with Chinese: Hello 世界",
            "Special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?",
            "Unicode: 🤖 🔍 📊 ✅ ❌",
            "Mixed: You are an AI assistant. 你是一个AI助手。🤖"
        ]
        
        for i, test_content in enumerate(special_chars_tests):
            try:
                messages = [
                    {"role": "system", "content": test_content},
                    {"role": "user", "content": "测试"}
                ]
                response = await simple_model.aresponse(messages=messages)
                print(f"✅ 特殊字符测试 {i+1}: 成功")
            except Exception as e:
                print(f"❌ 特殊字符测试 {i+1}: 失败 - {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(debug_zhipuai_messages())
    if success:
        print("\n🎉 调试完成！")
    else:
        print("\n💥 调试失败！")