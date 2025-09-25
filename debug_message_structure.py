#!/usr/bin/env python3
"""
直接调试agno Agent如何构建消息结构
找出"角色信息不正确"错误的确切原因
"""

import os
import sys
import asyncio
import json
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

class InterceptorOpenAIChat:
    """拦截OpenAIChat的aresponse方法来分析消息"""
    def __init__(self, original_model):
        self.original_model = original_model
        # 复制所有属性
        for attr in dir(original_model):
            if not attr.startswith('_'):
                try:
                    setattr(self, attr, getattr(original_model, attr))
                except:
                    pass  # 忽略无法设置的属性
    
    async def aresponse(self, messages=None, **kwargs):
        print("\n" + "="*80)
        print("🔍 INTERCEPTED ARESPONSE CALL")
        print("="*80)
        
        print(f"📨 Message count: {len(messages) if messages else 0}")
        print(f"📨 Message types: {[type(msg).__name__ for msg in messages] if messages else []}")
        
        if messages:
            for i, msg in enumerate(messages):
                print(f"\n--- Message {i+1} ---")
                print(f"Type: {type(msg)}")
                
                # 处理不同类型的消息对象
                if hasattr(msg, 'role'):
                    role = msg.role
                elif isinstance(msg, dict):
                    role = msg.get('role', 'unknown')
                else:
                    role = 'unknown'
                
                if hasattr(msg, 'content'):
                    content = getattr(msg, 'content', '')
                elif isinstance(msg, dict):
                    content = msg.get('content', '')
                else:
                    content = str(msg)
                
                print(f"Role: '{role}'")
                print(f"Content length: {len(str(content))}")
                print(f"Content preview: {str(content)[:200]}...")
                
                # 检查消息的完整属性
                if hasattr(msg, '__dict__'):
                    print(f"Message attributes: {list(msg.__dict__.keys())}")
                elif isinstance(msg, dict):
                    print(f"Dict keys: {list(msg.keys())}")
                
                # 特别检查系统消息
                if role == 'system':
                    print(f"🚨 SYSTEM MESSAGE DETECTED:")
                    print(f"Full content: {str(content)}")
        
        print("\n" + "="*80)
        print("📤 CALLING ORIGINAL ARESPONSE")
        print("="*80)
        
        # 调用原始方法
        try:
            return await self.original_model.aresponse(messages=messages, **kwargs)
        except Exception as e:
            print(f"❌ ARESPONSE ERROR: {e}")
            print(f"❌ ERROR TYPE: {type(e)}")
            if hasattr(e, 'response'):
                print(f"❌ HTTP RESPONSE: {getattr(e, 'response', '')}")
            if hasattr(e, 'body'):
                print(f"❌ ERROR BODY: {getattr(e, 'body', '')}")
            raise

async def debug_message_structure():
    """调试消息结构问题"""
    api_key = os.getenv("ZHIPUAI_API_KEY")
    if not api_key:
        print("❌ ZHIPUAI_API_KEY 未配置")
        return
    
    print(f"✅ API密钥已配置: {api_key[:10]}...")
    
    try:
        from agno.agent import Agent
        from agno.models.openai import OpenAIChat
        
        # 创建原始模型
        model = OpenAIChat(
            id="glm-4.5",
            base_url="https://open.bigmodel.cn/api/paas/v4/",
            api_key=api_key,
            temperature=0.7,
            max_tokens=200
        )
        
        # 让我们直接使用原始模型，但创建一个简单的调试版本
        print("🔧 创建简单的OpenAIChat模型用于调试")
        
        # 创建Agent，使用简单的系统消息
        agent = Agent(
            model=model,
            system_message="你是一个助手。",
            name="DebugAgent",
            create_default_system_message=False  # 不创建默认系统消息，使用我们提供的简单消息
        )
        
        print("✅ 成功创建Agent")
        
        # 测试简单调用
        print("\n🧪 测试Agent.arun调用")
        try:
            response = await agent.arun("你好")
            print(f"✅ Agent.arun成功")
            if hasattr(response, 'content'):
                print(f"响应内容: {response.content[:200]}...")
            else:
                print(f"响应: {response}")
                
        except Exception as e:
            print(f"❌ Agent.arun失败: {e}")
            print(f"错误类型: {type(e)}")
            if hasattr(e, '__dict__'):
                print(f"错误属性: {list(e.__dict__.keys())}")
            
            # 尝试获取更多错误信息
            import traceback
            print(f"完整错误追踪: {traceback.format_exc()}")
    
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        import traceback
        print(f"完整错误追踪: {traceback.format_exc()}")

if __name__ == "__main__":
    asyncio.run(debug_message_structure())