#!/usr/bin/env python3
"""
深入调试agno库与智谱AI的兼容性问题
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

async def debug_agno_compatibility():
    """深入调试agno与智谱AI的兼容性"""
    api_key = os.getenv("ZHIPUAI_API_KEY")
    if not api_key:
        print("❌ ZHIPUAI_API_KEY 未配置")
        return
    
    print(f"✅ API密钥已配置: {api_key[:10]}...")
    
    # 首先，直接测试OpenAI客户端
    try:
        from openai import AsyncOpenAI
        
        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://open.bigmodel.cn/api/paas/v4/"
        )
        
        print("\n🧪 测试1: 直接OpenAI客户端调用")
        simple_system = "你是一个规划助手。"
        
        response = await client.chat.completions.create(
            model="glm-4.5",
            messages=[
                {"role": "system", "content": simple_system},
                {"role": "user", "content": "制定一个简单计划"}
            ],
            temperature=0.7,
            max_tokens=200
        )
        print(f"✅ 直接调用成功: {response.choices[0].message.content[:50]}...")
        
    except Exception as e:
        print(f"❌ 直接调用失败: {e}")
        return False
    
    # 然后测试agno库
    try:
        print("\n🧪 测试2: 检查agno库的实际行为")
        
        # 尝试导入agno
        try:
            from agno.models.openai import OpenAIChat
            print("✅ 成功导入agno.models.openai.OpenAIChat")
        except ImportError as e:
            print(f"❌ 无法导入agno: {e}")
            return False
        
        # 创建OpenAIChat实例
        model = OpenAIChat(
            id="glm-4.5",
            base_url="https://open.bigmodel.cn/api/paas/v4/",
            api_key=api_key,
            temperature=0.7,
            max_tokens=200
        )
        print("✅ 成功创建OpenAIChat实例")
        
        # 检查可用方法
        available_methods = [method for method in dir(model) if not method.startswith('_')]
        print(f"✅ 可用方法: {available_methods}")
        
        # 检查是否有aresponse方法
        if hasattr(model, 'aresponse'):
            print("✅ 找到aresponse方法")
            
            # 尝试调用aresponse
            print("\n🧪 测试3: 调用aresponse方法")
            try:
                messages = [
                    {"role": "system", "content": "你是一个助手。"},
                    {"role": "user", "content": "你好"}
                ]
                print(f"发送消息: {messages}")
                
                response = await model.aresponse(messages=messages)
                print(f"✅ aresponse成功: {response}")
                
                # 检查response的属性
                if hasattr(response, 'content'):
                    print(f"✅ 响应内容: {response.content}")
                else:
                    print(f"✅ 响应对象: {response}")
                    print(f"响应类型: {type(response)}")
                    print(f"响应属性: {dir(response)}")
                
            except Exception as e:
                print(f"❌ aresponse调用失败: {e}")
                print(f"错误类型: {type(e)}")
                
                # 打印详细错误信息
                import traceback
                traceback.print_exc()
        else:
            print("❌ 没有找到aresponse方法")
        
        # 检查是否有其他异步方法
        async_methods = [method for method in dir(model) if method.startswith('a') and callable(getattr(model, method))]
        print(f"✅ 异步方法: {async_methods}")
        
        return True
        
    except Exception as e:
        print(f"❌ agno测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(debug_agno_compatibility())
    if success:
        print("\n🎉 调试完成！")
    else:
        print("\n💥 调试失败！")