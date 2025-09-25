#!/usr/bin/env python3
"""
简单直接测试GLM-4.5角色映射修复
避免复杂的导入问题
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

async def test_glm45_direct():
    """直接测试GLM-4.5模型"""
    api_key = os.getenv("ZHIPUAI_API_KEY")
    if not api_key:
        print("❌ ZHIPUAI_API_KEY 未配置")
        return False
    
    print(f"✅ API密钥已配置: {api_key[:10]}...")
    
    try:
        from agno.models.openai import OpenAIChat
        from agno.agent import Agent as AgnoAgent
        
        # 创建GLM-4.5模型，应用正确的角色映射
        print("🔧 创建GLM-4.5模型（带角色映射修复）...")
        
        # 定义正确的角色映射（ZhipuAI支持的格式）
        zhipuai_role_map = {
            "system": "system",  # 保持system为system，不是developer
            "user": "user",
            "assistant": "assistant", 
            "tool": "tool",
            "model": "assistant",
        }
        
        model = OpenAIChat(
            id="glm-4.5",
            base_url="https://open.bigmodel.cn/api/paas/v4/",
            api_key=api_key,
            temperature=0.7,
            max_tokens=200,
            role_map=zhipuai_role_map  # 应用修复的角色映射
        )
        
        print("✅ GLM-4.5模型创建成功")
        print(f"   🗺️ Role Map: {model.role_map}")
        
        # 创建Agent
        agent = AgnoAgent(
            model=model,
            system_message="你是一个助手。",
            name="GLM45TestAgent"
        )
        
        print("✅ 成功创建AgnoAgent")
        
        # 测试调用
        print("\n🧪 测试Agent.arun调用...")
        response = await agent.arun("请简单说一句话，证明你是GLM-4.5模型。")
        
        print("🎉 GLM-4.5角色映射修复成功！")
        print(f"✅ 响应: {response.content}")
        return True
        
    except Exception as e:
        error_str = str(e)
        if "角色信息不正确" in error_str or "1214" in error_str:
            print("❌ 仍然出现'角色信息不正确'错误")
            print(f"   错误: {e}")
            return False
        else:
            print(f"❌ 其他错误: {e}")
            print(f"   错误类型: {type(e)}")
            return False

async def main():
    """主测试函数"""
    print("🚀 开始测试GLM-4.5角色映射修复...")
    print("="*60)
    
    success = await test_glm45_direct()
    
    print("="*60)
    if success:
        print("🎉 测试成功！GLM-4.5角色映射问题已解决！")
        print("✅ 智谱AI GLM-4.5现在可以正常使用了")
    else:
        print("❌ 测试失败！角色映射问题尚未解决")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())