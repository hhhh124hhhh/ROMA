#!/usr/bin/env python3
"""
调试agno Agent的消息格式
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

class DebugOpenAIChat:
    """包装OpenAIChat来拦截消息"""
    def __init__(self, original_model):
        self.original_model = original_model
        # 复制所有属性
        for attr in dir(original_model):
            if not attr.startswith('_'):
                setattr(self, attr, getattr(original_model, attr))
    
    async def aresponse(self, messages=None, **kwargs):
        print("\n🔍 拦截到的消息调用:")
        print(f"消息数量: {len(messages) if messages else 0}")
        
        if messages:
            for i, msg in enumerate(messages):
                print(f"消息 {i+1}: role='{getattr(msg, 'role', 'unknown')}', content_length={len(getattr(msg, 'content', ''))}")
                content = getattr(msg, 'content', '')
                print(f"消息 {i+1} 内容: {content[:100]}...")
                
                # 检查消息的实际结构
                if hasattr(msg, '__dict__'):
                    print(f"消息 {i+1} 属性: {list(msg.__dict__.keys())}")
                else:
                    print(f"消息 {i+1} 类型: {type(msg)}")
        
        # 调用原始方法
        return await self.original_model.aresponse(messages=messages, **kwargs)

async def debug_message_format():
    """调试消息格式问题"""
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
        
        # 包装模型以拦截消息
        debug_model = DebugOpenAIChat(model)
        
        # 创建Agent
        agent = Agent(
            model=debug_model,
            system_message="你是一个助手。",
            name="DebugAgent"
        )
        
        print("✅ 成功创建调试Agent")
        
        # 测试简单调用
        print("\n🧪 测试简单调用")
        try:
            response = await agent.arun("你好")
            print("✅ 调用成功")
        except Exception as e:
            print(f"❌ 调用失败: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(debug_message_format())
    if success:
        print("\n🎉 调试完成！")
    else:
        print("\n💥 调试失败！")