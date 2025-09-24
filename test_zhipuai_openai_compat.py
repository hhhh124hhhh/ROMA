#!/usr/bin/env python3
"""
智谱AI OpenAI兼容API测试脚本
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
    print(f"✅ 已加载环境配置文件: {env_path.absolute()}")
else:
    print(f"⚠️  环境配置文件不存在: {env_path.absolute()}")

async def test_zhipuai_openai_compat():
    """测试智谱AI OpenAI兼容API"""
    api_key = os.getenv("ZHIPUAI_API_KEY")
    if not api_key or api_key == "your_zhipuai_key_here":
        print("❌ ZHIPUAI_API_KEY 未配置")
        return False
    
    print(f"✅ API密钥已配置: {api_key[:10]}...")
    
    try:
        from openai import AsyncOpenAI
        
        # 创建OpenAI客户端，使用智谱AI的兼容端点
        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://open.bigmodel.cn/api/paas/v4/"
        )
        
        print("🧪 测试1: 基础消息")
        try:
            response = await client.chat.completions.create(
                model="glm-4.5",
                messages=[
                    {"role": "user", "content": "你好"}
                ],
                temperature=0.7,
                max_tokens=100
            )
            print(f"✅ 基础测试成功: {response.choices[0].message.content}")
        except Exception as e:
            print(f"❌ 基础测试失败: {e}")
            return False
        
        print("\n🧪 测试2: 带系统消息")
        try:
            response = await client.chat.completions.create(
                model="glm-4.5",
                messages=[
                    {"role": "system", "content": "你是一个有用的AI助手。"},
                    {"role": "user", "content": "用一句话简单介绍人工智能"}
                ],
                temperature=0.7,
                max_tokens=200
            )
            print(f"✅ 系统消息测试成功: {response.choices[0].message.content}")
        except Exception as e:
            print(f"❌ 系统消息测试失败: {e}")
            return False
        
        print("\n🧪 测试3: 长系统消息（模拟agent prompt）")
        long_system_prompt = """You are an expert parallel search decomposition agent specialized in breaking down complex research goals into independent, self-contained search tasks that can execute simultaneously. Your primary role is to create **2 to 4 completely independent search subtasks** that together gather comprehensive information from different sources, domains, or perspectives without any dependencies between them.

**TEMPORAL AWARENESS:**
- Today's date: September 24, 2025
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

        try:
            response = await client.chat.completions.create(
                model="glm-4.5",
                messages=[
                    {"role": "system", "content": long_system_prompt},
                    {"role": "user", "content": "用一句话简单介绍人工智能"}
                ],
                temperature=0.7,
                max_tokens=200
            )
            print(f"✅ 长系统消息测试成功: {response.choices[0].message.content}")
        except Exception as e:
            print(f"❌ 长系统消息测试失败: {e}")
            return False
        
        print("\n🧪 测试4: 使用agno.models.openai.OpenAIChat")
        try:
            from agno.models.openai import OpenAIChat
            
            # 创建OpenAIChat实例
            model = OpenAIChat(
                id="glm-4.5",
                base_url="https://open.bigmodel.cn/api/paas/v4/",
                api_key=api_key,
                temperature=0.7,
                max_tokens=200
            )
            
            response = await model.arun("用一句话简单介绍人工智能")
            print(f"✅ AgnoOpenAIChat测试成功: {response.content}")
        except Exception as e:
            print(f"❌ AgnoOpenAIChat测试失败: {e}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ 缺少依赖库: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_zhipuai_openai_compat())
    if success:
        print("\n🎉 所有测试通过！智谱AI OpenAI兼容API工作正常")
    else:
        print("\n💥 测试失败！需要检查配置或API兼容性")