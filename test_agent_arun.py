#!/usr/bin/env python3
"""
测试agno Agent的arun方法并诊断消息格式问题
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

async def test_agent_arun():
    """测试Agent的arun方法"""
    api_key = os.getenv("ZHIPUAI_API_KEY")
    if not api_key:
        print("❌ ZHIPUAI_API_KEY 未配置")
        return
    
    print(f"✅ API密钥已配置: {api_key[:10]}...")
    
    try:
        from agno.agent import Agent
        from agno.models.openai import OpenAIChat
        
        # 创建OpenAIChat模型
        model = OpenAIChat(
            id="glm-4.5",
            base_url="https://open.bigmodel.cn/api/paas/v4/",
            api_key=api_key,
            temperature=0.7,
            max_tokens=200
        )
        
        # 创建Agent
        agent = Agent(
            model=model,
            system_message="你是一个助手。",
            name="TestAgent"
        )
        
        print("✅ 成功创建Agent实例")
        print(f"Agent 有 arun 方法: {hasattr(agent, 'arun')}")
        print(f"Agent.model 有 arun 方法: {hasattr(agent.model, 'arun')}")
        print(f"Agent.model 有 aresponse 方法: {hasattr(agent.model, 'aresponse')}")
        
        # 测试Agent.arun
        print("\n🧪 测试Agent.arun")
        try:
            response = await agent.arun("你好，请简单介绍一下自己")
            print(f"✅ Agent.arun成功")
            print(f"响应类型: {type(response)}")
            if hasattr(response, 'content'):
                print(f"响应内容: {response.content[:200]}...")
            else:
                print(f"响应: {response}")
        except Exception as e:
            print(f"❌ Agent.arun失败: {e}")
            print(f"错误类型: {type(e)}")
            
            # 分析错误内容
            error_str = str(e)
            if "角色信息不正确" in error_str:
                print("🔍 发现'角色信息不正确'错误")
            if "1214" in error_str:
                print("🔍 发现错误代码1214")
            
            import traceback
            print(f"错误追踪: {traceback.format_exc()}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agent_arun())
    if success:
        print("\n🎉 测试完成！")
    else:
        print("\n💥 测试失败！")