#!/usr/bin/env python3
"""
测试简化的系统消息是否能解决智谱AI的"角色信息不正确"问题
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

async def test_simplified_system_message():
    """测试简化的系统消息"""
    api_key = os.getenv("ZHIPUAI_API_KEY")
    if not api_key:
        print("❌ ZHIPUAI_API_KEY 未配置")
        return
    
    print(f"✅ API密钥已配置: {api_key[:10]}...")
    
    try:
        from openai import AsyncOpenAI
        
        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://open.bigmodel.cn/api/paas/v4/"
        )
        
        # 测试1: 非常简短的系统消息
        print("\n🧪 测试1: 简短系统消息")
        simple_prompt = "你是一个专业的规划助手。"
        try:
            response = await client.chat.completions.create(
                model="glm-4.5",
                messages=[
                    {"role": "system", "content": simple_prompt},
                    {"role": "user", "content": "请为智谱AI技术研究制定一个简单计划"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            print(f"✅ 成功 (长度: {len(simple_prompt)}): {response.choices[0].message.content[:100]}...")
        except Exception as e:
            print(f"❌ 失败 (长度: {len(simple_prompt)}): {e}")
        
        # 测试2: 中等长度的系统消息
        print("\n🧪 测试2: 中等长度系统消息")
        medium_prompt = """你是一个专业的任务规划代理，专门将复杂目标分解为独立的子任务。你的作用是创建2到4个完全独立的子任务，这些子任务可以同时执行，共同收集来自不同来源或角度的综合信息。

重要原则：
- 每个子任务必须是自包含的
- 子任务之间不能有依赖关系  
- 专注于不同的信息来源或角度

请以JSON数组格式回复，每个任务包含goal、task_type和depends_on_indices字段。"""
        
        try:
            response = await client.chat.completions.create(
                model="glm-4.5",
                messages=[
                    {"role": "system", "content": medium_prompt},
                    {"role": "user", "content": "请为智谱AI技术研究制定一个计划"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            print(f"✅ 成功 (长度: {len(medium_prompt)}): {response.choices[0].message.content[:100]}...")
        except Exception as e:
            print(f"❌ 失败 (长度: {len(medium_prompt)}): {e}")
        
        # 测试3: 较长的系统消息（模拟原始长度的一部分）
        print("\n🧪 测试3: 较长系统消息")
        long_prompt = """你是一个专业的并行搜索分解代理，专门将复杂的研究目标分解为独立的、自包含的搜索任务，这些任务可以同时执行。你的主要作用是创建2到4个完全独立的搜索子任务，这些子任务共同从不同的来源、领域或角度收集综合信息，彼此之间没有任何依赖关系。

时间意识：
- 今天的日期：2025年9月25日
- 你的搜索能力提供对实时信息和当前数据的访问
- 在规划搜索时，强调收集最新和最前沿的可用信息
- 考虑时间约束并在相关时指定时间范围（例如，"最新趋势"、"当前数据"、"最新发展"）
- 优先考虑实时信息收集而不是可能过时的上下文

关键原则：独立搜索执行
每个搜索子任务将由独立的代理执行，该代理不了解：
- 你计划中的其他搜索任务
- 整体搜索策略
- 系统执行流程
- 其他搜索代理正在发现什么

因此，每个搜索子任务必须是：
- 自包含的：包括所有必要的上下文和搜索参数
- 独立可执行的：不需要其他搜索任务的输出
- 特定来源的：专注于不同的信息来源、领域或角度

请以JSON数组格式回复，每个任务对象包含：
- goal (字符串)：完整的搜索规范
- task_type (字符串)：'SEARCH'、'THINK'或'WRITE'
- depends_on_indices (列表)：对于所有任务必须为空[]"""
        
        try:
            response = await client.chat.completions.create(
                model="glm-4.5",
                messages=[
                    {"role": "system", "content": long_prompt},
                    {"role": "user", "content": "请为智谱AI GLM-4.5技术研究制定一个详细的搜索计划"}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            print(f"✅ 成功 (长度: {len(long_prompt)}): {response.choices[0].message.content[:100]}...")
        except Exception as e:
            print(f"❌ 失败 (长度: {len(long_prompt)}): {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_simplified_system_message())
    if success:
        print("\n🎉 测试完成！")
    else:
        print("\n💥 测试失败！")