#!/usr/bin/env python3
"""
专门调试agno库的arun方法如何处理消息格式
分析为什么会出现"角色信息不正确"错误
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

async def debug_agno_arun():
    """调试agno库的arun方法的消息格式处理"""
    api_key = os.getenv("ZHIPUAI_API_KEY")
    if not api_key:
        print("❌ ZHIPUAI_API_KEY 未配置")
        return
    
    print(f"✅ API密钥已配置: {api_key[:10]}...")
    
    try:
        from agno.models.openai import OpenAIChat
        print("✅ 成功导入agno.models.openai.OpenAIChat")
    except ImportError as e:
        print(f"❌ 无法导入agno: {e}")
        return
    
    # 创建最简单的OpenAIChat实例
    print("\n🧪 创建简单的OpenAIChat实例...")
    try:
        model = OpenAIChat(
            id="glm-4.5",
            base_url="https://open.bigmodel.cn/api/paas/v4/",
            api_key=api_key,
            temperature=0.7,
            max_tokens=200
        )
        print("✅ 成功创建OpenAIChat实例")
        
        # 检查实例的属性
        print(f"模型ID: {model.id}")
        print(f"Base URL: {model.base_url}")
        print(f"System message: {getattr(model, 'system_message', 'None')}")
        
    except Exception as e:
        print(f"❌ 创建OpenAIChat实例失败: {e}")
        return
    
    # 测试1: 最简单的arun调用
    print("\n🧪 测试1: 最简单的arun调用")
    try:
    # 继续测试aresponse方法
    print("\n🧪 测试: 检查aresponse方法")
    try:
        if hasattr(model, 'aresponse'):
            print("✅ 找到aresponse方法")
            
            # 测试aresponse调用
            messages = [
                {"role": "system", "content": "你是一个助手。"},
                {"role": "user", "content": "请简单回复。"}
            ]
            
            response = await model.aresponse(messages=messages)
            print(f"✅ aresponse成功: {response.content[:100]}...")
        else:
            print("❌ 没有aresponse方法")
    except Exception as e:
        print(f"❌ aresponse失败: {e}")
        print(f"✅ 简单arun成功: {response.content[:100]}...")
    except Exception as e:
        print(f"❌ 简单arun失败: {e}")
        print(f"错误类型: {type(e)}")
        
        # 更详细的错误分析
        if hasattr(e, 'response'):
            print(f"HTTP响应: {e.response}")
        if hasattr(e, 'body'):
            print(f"错误体: {e.body}")
    
    # 测试2: 带system_message的OpenAIChat
    print("\n🧪 测试2: 带system_message的OpenAIChat")
    try:
        model_with_system = OpenAIChat(
            id="glm-4.5",
            base_url="https://open.bigmodel.cn/api/paas/v4/",
            api_key=api_key,
            temperature=0.7,
            max_tokens=200
        )
        print("✅ 成功创建带system_message的OpenAIChat实例")
        
        if hasattr(model_with_system, 'aresponse'):
            response = await model_with_system.aresponse(messages=[
                {"role": "user", "content": "请简单回复"}
            ])
            if response and hasattr(response, 'content'):
                print(f"✅ 带system_message的aresponse成功: {response.content[:100]}...")
            else:
                print(f"✅ 带system_message的aresponse成功: {response}")
        else:
            print("❌ 没有aresponse方法")
        print(f"✅ 带system_message的arun成功: {response.content[:100]}...")
    except Exception as e:
        print(f"❌ 带system_message的arun失败: {e}")
    
    # 测试3: 检查OpenAIChat的内部实现
    print("\n🧪 测试3: 检查OpenAIChat的内部方法")
    try:
        # 尝试查看OpenAIChat如何构建消息
        print(f"OpenAIChat可用方法: {[m for m in dir(model) if not m.startswith('_')]}")
        
        # 查看是否有任何内部方法用于消息构建
        internal_methods = [m for m in dir(model) if 'message' in m.lower() or 'prompt' in m.lower()]
        print(f"与消息相关的方法: {internal_methods}")
        
    except Exception as e:
        print(f"❌ 检查内部方法失败: {e}")
    
    # 测试4: 使用Agent包装器
    print("\n🧪 测试4: 使用AgnoAgent包装器")
    try:
        from agno.agent import Agent
        
        # 创建AgnoAgent实例
        agent = Agent(
            model=OpenAIChat(
                id="glm-4.5", 
                base_url="https://open.bigmodel.cn/api/paas/v4/",
                api_key=api_key,
                temperature=0.7,
                max_tokens=200
            ),
            system_message="你是一个规划助手。",
            name="TestAgent"
        )
        print("✅ 成功创建AgnoAgent")
        
        # 测试agent.arun
        response = await agent.arun("制定一个简单计划")
        print(f"✅ AgnoAgent.arun成功: {response.content[:100]}...")
        
    except Exception as e:
        print(f"❌ AgnoAgent测试失败: {e}")
        print(f"错误详情: {str(e)}")
        
        # 尝试捕获更多错误信息
        import traceback
        print(f"错误追踪: {traceback.format_exc()}")

if __name__ == "__main__":
    asyncio.run(debug_agno_arun())