#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM-4.5 模型集成测试脚本

测试智谱AI GLM-4.5模型的直接API调用集成
包括流式和非流式响应测试
"""

import os
import json
import asyncio
import requests
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# 设置项目根目录
project_root = Path(__file__).parent
os.chdir(project_root)

# 加载环境变量
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ 已加载环境配置文件: {env_path.absolute()}")
else:
    print(f"⚠️  环境配置文件不存在: {env_path.absolute()}")

def check_zhipuai_key() -> str:
    """检查智谱AI API密钥"""
    api_key = os.getenv("ZHIPUAI_API_KEY", "")
    if api_key and api_key != "your_zhipuai_key_here":
        print(f"✅ 智谱AI API密钥已配置: {api_key[:10]}...")
        return api_key
    else:
        print("❌ 智谱AI API密钱未配置或使用默认值")
        return ""

def test_direct_api_call(api_key: str, stream: bool = False) -> bool:
    """测试直接API调用"""
    print(f"\n🧪 测试GLM-4.5直接API调用 (stream={stream})...")
    
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "glm-4.5",
        "messages": [
            {
                "role": "system",
                "content": "你是一个有用的AI助手。"
            },
            {
                "role": "user",
                "content": "你好，请介绍一下自己。"
            }
        ],
        "temperature": 0.6,
        "stream": stream
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        if stream:
            # 处理流式响应
            print("📡 流式响应:")
            for line in response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')
                    if line_text.startswith("data: "):
                        data_part = line_text[6:]
                        if data_part.strip() != "[DONE]":
                            try:
                                json_data = json.loads(data_part)
                                if "choices" in json_data and json_data["choices"]:
                                    delta = json_data["choices"][0].get("delta", {})
                                    if "content" in delta:
                                        print(delta["content"], end="", flush=True)
                            except json.JSONDecodeError:
                                continue
            print("\n")
        else:
            # 处理非流式响应
            result = response.json()
            print("📄 非流式响应:")
            if "choices" in result and result["choices"]:
                content = result["choices"][0]["message"]["content"]
                print(f"回复: {content}")
            else:
                print(f"原始响应: {result}")
        
        print(f"✅ 直接API调用成功 (stream={stream})")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 直接API调用失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 处理响应失败: {e}")
        return False

def test_litellm_integration(api_key: str) -> bool:
    """测试LiteLLM集成"""
    print(f"\n🔧 测试LiteLLM集成GLM-4.5...")
    
    try:
        # 设置环境变量
        os.environ["ZHIPUAI_API_KEY"] = api_key
        
        # 导入LiteLLM
        import litellm
        
        # 配置LiteLLM for 智谱AI
        litellm.api_base = "https://open.bigmodel.cn/api/paas/v4/"
        
        # 测试completion调用
        response = litellm.completion(
            model="zhipuai/glm-4.5",
            messages=[
                {
                    "role": "system", 
                    "content": "你是一个有用的AI助手。"
                },
                {
                    "role": "user", 
                    "content": "请用一句话介绍一下你的能力。"
                }
            ],
            temperature=0.6,
            api_key=api_key
        )
        
        try:
            if response and hasattr(response, 'choices') and response.choices:
                content = getattr(response.choices[0], 'message', None)
                if content and hasattr(content, 'content'):
                    print(f"🤖 LiteLLM响应: {content.content}")
                    print("✅ LiteLLM集成成功")
                    return True
            print("❌ LiteLLM响应为空或格式不正确")
            return False
        except AttributeError as e:
            print(f"❌ LiteLLM响应属性错误: {e}")
            return False
            
    except ImportError:
        print("❌ LiteLLM未安装，跳过集成测试")
        return False
    except Exception as e:
        print(f"❌ LiteLLM集成失败: {e}")
        return False

def test_model_config_validation() -> bool:
    """测试模型配置验证"""
    print(f"\n⚙️  测试模型配置验证...")
    
    try:
        # 导入模型配置类
        import sys
        sys.path.append(str(project_root / "src"))
        from sentientresearchagent.hierarchical_agent_framework.agent_configs.models import ModelConfig
        
        # 测试配置1: 智谱AI通过LiteLLM
        config1_dict = {
            "provider": "litellm",
            "model_id": "zhipuai/glm-4.5",
            "temperature": 0.6,
            "max_tokens": 2000
        }
        
        config1 = ModelConfig(**config1_dict)
        print(f"✅ 配置验证成功: {config1.provider}/{config1.model_id}")
        
        # 测试配置2: 直接智谱AI provider
        config2_dict = {
            "provider": "zhipuai",
            "model_id": "glm-4.5",
            "temperature": 0.7
        }
        
        config2 = ModelConfig(**config2_dict)
        print(f"✅ 配置验证成功: {config2.provider}/{config2.model_id}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 无法导入模型配置类: {e}")
        return False
    except Exception as e:
        print(f"❌ 模型配置验证失败: {e}")
        return False

def test_agent_factory_integration() -> bool:
    """测试AgentFactory集成"""
    print(f"\n🏭 测试AgentFactory集成...")
    
    try:
        # 导入必要的类
        import sys
        sys.path.append(str(project_root / "src"))
        from sentientresearchagent.hierarchical_agent_framework.agent_configs.agent_factory import AgentFactory
        from sentientresearchagent.hierarchical_agent_framework.agent_configs.models import ModelConfig
        
        # 创建模型配置
        model_config = ModelConfig(
            provider="zhipuai",
            model_id="glm-4.5",
            temperature=0.6
        )
        
        # 创建AgentFactory实例 (需要config_loader, 这里模拟一个)
        class MockConfigLoader:
            def resolve_prompt(self, prompt_source):
                return "You are a helpful AI assistant."
        
        factory = AgentFactory(MockConfigLoader())
        
        # 测试模型创建
        try:
            model_instance = factory.create_model_instance(model_config)
            print(f"✅ AgentFactory模型创建成功: {type(model_instance).__name__}")
            return True
        except Exception as e:
            print(f"❌ AgentFactory模型创建失败: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ 无法导入AgentFactory类: {e}")
        return False
    except Exception as e:
        print(f"❌ AgentFactory集成测试失败: {e}")
        return False

def create_sample_agent_config() -> bool:
    """创建示例智谱AI代理配置"""
    print(f"\n📝 创建示例GLM-4.5代理配置...")
    
    sample_config = {
        "agents": [
            {
                "name": "glm45-planner",
                "type": "planner",
                "adapter_class": "PlannerAdapter",
                "description": "使用GLM-4.5的规划代理",
                "enabled": True,
                "model": {
                    "provider": "zhipuai",
                    "model_id": "glm-4.5",
                    "temperature": 0.6,
                    "max_tokens": 2000
                },
                "prompt_source": "prompts.planner_prompts.SYSTEM_MESSAGE",
                "response_model": "PlanOutput",
                "tools": [],
                "toolkits": []
            },
            {
                "name": "glm45-executor",
                "type": "executor", 
                "adapter_class": "ExecutorAdapter",
                "description": "使用GLM-4.5的执行代理",
                "enabled": True,
                "model": {
                    "provider": "litellm",
                    "model_id": "zhipuai/glm-4.5",
                    "temperature": 0.7,
                    "max_tokens": 1500
                },
                "prompt_source": "prompts.executor_prompts.SYSTEM_MESSAGE",
                "tools": ["web_search"],
                "toolkits": []
            }
        ],
        "metadata": {
            "created_for": "GLM-4.5集成测试",
            "api_version": "v4",
            "model_version": "glm-4.5"
        }
    }
    
    try:
        config_path = project_root / "examples" / "glm45-agents-config.yaml"
        config_path.parent.mkdir(exist_ok=True)
        
        import yaml
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(sample_config, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        print(f"✅ 示例配置已创建: {config_path}")
        return True
        
    except Exception as e:
        print(f"❌ 创建示例配置失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🚀 GLM-4.5模型集成测试开始...")
    
    # 检查API密钥
    api_key = check_zhipuai_key()
    
    test_results = []
    
    # 测试1: 模型配置验证
    result1 = test_model_config_validation()
    test_results.append(("模型配置验证", result1))
    
    # 测试2: 创建示例配置
    result2 = create_sample_agent_config()
    test_results.append(("示例配置创建", result2))
    
    # 如果有API密钥，进行API调用测试
    if api_key:
        # 测试3: 直接API调用 (非流式)
        result3 = test_direct_api_call(api_key, stream=False)
        test_results.append(("直接API调用(非流式)", result3))
        
        # 测试4: 直接API调用 (流式)
        result4 = test_direct_api_call(api_key, stream=True)
        test_results.append(("直接API调用(流式)", result4))
        
        # 测试5: LiteLLM集成
        result5 = test_litellm_integration(api_key)
        test_results.append(("LiteLLM集成", result5))
    else:
        print("\n⚠️  跳过API调用测试 (需要有效的ZHIPUAI_API_KEY)")
    
    # 测试6: AgentFactory集成
    result6 = test_agent_factory_integration()
    test_results.append(("AgentFactory集成", result6))
    
    # 汇总结果
    print(f"\n📊 测试结果汇总:")
    print("-" * 50)
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print("-" * 50)
    print(f"通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 所有测试通过！GLM-4.5集成成功！")
    else:
        print("⚠️  部分测试失败，请检查配置和依赖。")

if __name__ == "__main__":
    asyncio.run(main())