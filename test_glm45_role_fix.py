#!/usr/bin/env python3
"""
直接测试GLM-4.5模型与修复的角色映射
验证"角色信息不正确"错误是否已被解决
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

async def test_glm45_role_mapping_fix():
    """测试GLM-4.5角色映射修复"""
    api_key = os.getenv("ZHIPUAI_API_KEY")
    if not api_key:
        print("❌ ZHIPUAI_API_KEY 未配置")
        return False
    
    print(f"✅ API密钥已配置: {api_key[:10]}...")
    
    try:
        # 导入我们修复后的agent factory
        from sentientresearchagent.hierarchical_agent_framework.agent_configs.agent_factory import AgentFactory
        from sentientresearchagent.hierarchical_agent_framework.agent_configs.config_loader import AgentConfigLoader
        from agno.agent import Agent as AgnoAgent
        
        # 创建配置加载器（空的，因为我们不需要加载配置文件）
        config_loader = None
        
        # 创建agent factory
        factory = AgentFactory(config_loader)
        
        # 构建GLM-4.5模型配置（使用我们修复的格式）
        model_config = {
            'provider': 'openai',
            'model_id': 'glm-4.5',
            'api_base': 'https://open.bigmodel.cn/api/paas/v4/',
            'api_key': api_key,
            'temperature': 0.7,
            'max_tokens': 200
        }
        
        print("🔧 创建GLM-4.5模型实例（使用修复的角色映射）...")
        
        # 创建模型实例 - 这会应用我们的角色映射修复
        model = factory.create_model_instance(model_config)
        
        print("✅ GLM-4.5模型实例创建成功")
        print(f"   📋 模型类型: {type(model).__name__}")
        print(f"   🔧 Base URL: {getattr(model, 'base_url', 'N/A')}")
        print(f"   🗺️ Role Map: {getattr(model, 'role_map', 'N/A')}")
        
        # 创建AgnoAgent来测试
        agent = AgnoAgent(
            model=model,
            system_message="你是一个助手。",
            name="GLM45TestAgent"
        )
        
        print("✅ 成功创建AgnoAgent")
        
        # 测试Agent.arun调用
        print("\n🧪 测试Agent.arun调用...")
        try:
            response = await agent.arun("请简单介绍一下你自己，说明你使用的是什么模型。")
            print("🎉 GLM-4.5角色映射修复成功！")
            print(f"✅ 响应: {response.content}")
            return True
            
        except Exception as e:
            error_str = str(e)
            if "角色信息不正确" in error_str or "1214" in error_str:
                print("❌ 角色映射修复失败 - 仍然出现'角色信息不正确'错误")
                print(f"   错误: {e}")
                return False
            else:
                print(f"❌ 其他错误: {e}")
                return False
                
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        print(f"完整错误追踪: {traceback.format_exc()}")
        return False

async def main():
    """主测试函数"""
    print("🚀 开始测试GLM-4.5角色映射修复...")
    print("="*60)
    
    success = await test_glm45_role_mapping_fix()
    
    print("="*60)
    if success:
        print("🎉 测试成功！GLM-4.5角色映射问题已解决！")
        print("✅ 智谱AI GLM-4.5现在可以正常使用了")
    else:
        print("❌ 测试失败！角色映射问题尚未解决")
        print("🔧 需要进一步调试和修复")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())