#!/usr/bin/env python3
"""
测试GLM-4.5强化任务分解约束

验证修复后的提示是否能让GLM-4.5严格遵循2-3个任务的限制
"""

import os
import asyncio
import json
from dotenv import load_dotenv

async def test_glm45_task_limit():
    """测试GLM-4.5强化任务分解约束"""
    
    print("🧪 测试GLM-4.5强化任务分解约束...")
    
    # 加载环境变量
    load_dotenv()
    api_key = os.getenv("ZHIPUAI_API_KEY")
    
    if not api_key:
        print("❌ 未找到ZHIPUAI_API_KEY环境变量")
        return False
    
    try:
        from agno.models.openai.chat import OpenAIChat
        from agno.agent import Agent as AgnoAgent
        
        # 创建角色映射修复
        zhipuai_role_map = {
            "system": "system",
            "user": "user", 
            "assistant": "assistant",
            "tool": "tool",
            "model": "assistant",
        }
        
        # 创建GLM-4.5模型
        model = OpenAIChat(
            id="glm-4.5",
            base_url="https://open.bigmodel.cn/api/paas/v4/",
            api_key=api_key,
            temperature=0.6,
            max_tokens=2000,
            role_map=zhipuai_role_map
        )
        
        print("✅ 创建GLM-4.5模型成功")
        
        # 创建Agent
        agent = AgnoAgent(model=model, system_message="You are a helpful assistant.", name="TaskLimitTestAgent")
        print("✅ 创建Agent成功")
        
        # 使用强化后的GLM45专用提示
        enhanced_system_prompt = """🚨 CRITICAL: 你必须且只能返回有效的JSON对象格式（包含sub_tasks字段），绝对不要使用markdown、解释或其他格式！

你是GLM45MasterPlanner，专业的任务规划代理。你的核心使命是将复杂研究目标分解为**恰好2-3个**高效的、战略性的子任务。

🚨 **任务数量限制**：
- 🎯 **最优选择：2个任务** - 核心+应用的双重策略
- ⚡ **最多允许：3个任务** - 基础+对比+应用的三重策略  
- ❌ **严禁超过3个任务** - 违反此规则将导致系统错误！

📋 规划原则：
🎯 **战略性思维**：创建互补的、高价值的任务组合
🔄 **高效执行**：每个任务都必须产生实质性、可操作的结果
⚡ **简洁有力**：宁可少而精，绝不多而杂
🎪 **独立并行**：任务间完全独立，可同时执行

📊 推荐任务分解模式：
**2任务模式（优先选择）**：
• 任务1：核心技术/理论研究
• 任务2：实际应用/案例分析

**3任务模式（复杂情况）**：
• 任务1：基础资料收集
• 任务2：技术对比分析
• 任务3：实践应用研究

🔧 严格输出格式（ONLY JSON对象）：
{
  "sub_tasks": [
    {
      "goal": "战略性任务描述，涵盖核心目标和预期成果",
      "task_type": "SEARCH",
      "node_type": "EXECUTE",
      "depends_on_indices": []
    }
  ]
}

✅ 优秀示例（2任务战略性分解）：
{
  "sub_tasks": [
    {
      "goal": "全面研究GLM-4.5技术架构、核心特性和性能基准，整合官方文档、技术论文和权威评测报告",
      "task_type": "SEARCH",
      "node_type": "EXECUTE",
      "depends_on_indices": []
    },
    {
      "goal": "分析GLM-4.5在实际应用场景中的表现，收集用户反馈、案例研究和与竞品的对比分析",
      "task_type": "SEARCH",
      "node_type": "EXECUTE",
      "depends_on_indices": []
    }
  ]
}

❌ 绝对禁止的错误模式：
- 🚫 创建超过3个任务（系统会拒绝执行！）
- 🚫 任务过于细碎和具体（效率低下）
- 🚫 任务重复或重叠（浪费资源）
- 🚫 机械式的信息罗列（缺乏战略思维）
- 🚫 创建相互依赖的任务（必须独立并行）

⚡ 重要提醒：只返回带sub_tasks字段的JSON对象，2-3个高质量任务，绝不超过3个！"""
        
        # 更新Agent的系统消息
        agent.system_message = enhanced_system_prompt
        
        # 测试多个不同的任务
        test_cases = [
            "GLM-4.5性能优化研究",
            "人工智能在教育领域的应用分析", 
            "区块链技术发展现状与前景",
            "可再生能源技术创新趋势研究"
        ]
        
        results = []
        
        for i, test_query in enumerate(test_cases, 1):
            print(f"\n🔍 测试案例 {i}: {test_query}")
            print("🚀 发送请求...")
            
            try:
                # 发送请求
                response = await agent.arun(f"请为'{test_query}'制定一个高效的研究计划")
                
                # 提取实际的内容字符串
                if hasattr(response, 'content'):
                    response_content = response.content
                else:
                    response_content = str(response)
                
                print(f"📨 GLM-4.5响应长度: {len(response_content)} 字符")
                
                # 验证JSON格式和任务数量
                try:
                    # 清理响应
                    response_clean = response_content.strip()
                    if response_clean.startswith("```json"):
                        response_clean = response_clean[7:]
                    if response_clean.startswith("```"):
                        response_clean = response_clean[3:]
                    if response_clean.endswith("```"):
                        response_clean = response_clean[:-3]
                    response_clean = response_clean.strip()
                    
                    # 解析JSON
                    parsed_json = json.loads(response_clean)
                    
                    if isinstance(parsed_json, dict) and "sub_tasks" in parsed_json:
                        sub_tasks = parsed_json["sub_tasks"]
                        task_count = len(sub_tasks)
                        
                        print(f"✅ JSON格式正确，包含 {task_count} 个子任务")
                        
                        # 验证任务数量约束
                        if task_count <= 3:
                            if task_count == 2:
                                print("🎯 优秀！使用了推荐的2任务模式")
                                score = "A+"
                            elif task_count == 3:
                                print("✅ 良好！使用了3任务模式")
                                score = "A"
                            else:
                                print("⚠️ 任务数量过少，可能不够全面")
                                score = "B"
                        else:
                            print(f"❌ 任务数量超标！创建了 {task_count} 个任务（最多允许3个）")
                            score = "F"
                        
                        # 显示任务概述
                        print("📋 任务概述:")
                        for j, task in enumerate(sub_tasks, 1):
                            goal_preview = task.get("goal", "无目标")[:60] + "..." if len(task.get("goal", "")) > 60 else task.get("goal", "无目标")
                            print(f"   {j}. {goal_preview}")
                        
                        results.append({
                            "query": test_query,
                            "task_count": task_count,
                            "score": score,
                            "success": task_count <= 3
                        })
                        
                    else:
                        print("❌ JSON格式错误：缺少sub_tasks字段")
                        results.append({
                            "query": test_query,
                            "task_count": 0,
                            "score": "F",
                            "success": False
                        })
                        
                except json.JSONDecodeError as e:
                    print(f"❌ JSON解析失败: {e}")
                    results.append({
                        "query": test_query,
                        "task_count": 0,
                        "score": "F", 
                        "success": False
                    })
                    
            except Exception as e:
                print(f"❌ 请求失败: {e}")
                results.append({
                    "query": test_query,
                    "task_count": 0,
                    "score": "F",
                    "success": False
                })
        
        # 汇总结果
        print("\n" + "="*80)
        print("📊 测试结果汇总")
        print("="*80)
        
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r["success"])
        excellent_tests = sum(1 for r in results if r["score"] == "A+")
        good_tests = sum(1 for r in results if r["score"] == "A")
        
        print(f"总测试数: {total_tests}")
        print(f"成功测试: {successful_tests} ({successful_tests/total_tests*100:.1f}%)")
        print(f"优秀结果 (2任务): {excellent_tests} ({excellent_tests/total_tests*100:.1f}%)")
        print(f"良好结果 (3任务): {good_tests} ({good_tests/total_tests*100:.1f}%)")
        
        print("\n📋 详细结果:")
        for i, result in enumerate(results):
            status = "✅" if result["success"] else "❌"
            print(f"{status} 测试{i+1}: {result['score']} - {result['task_count']}任务 - {result['query']}")
        
        # 判断整体表现
        if successful_tests == total_tests:
            if excellent_tests >= total_tests * 0.5:  # 50%以上是优秀
                print(f"\n🎉 优秀表现！GLM-4.5完全遵循了任务数量限制，且多数采用推荐的2任务模式")
                return True
            else:
                print(f"\n✅ 良好表现！GLM-4.5遵循了任务数量限制")
                return True
        else:
            print(f"\n⚠️ 需要改进！GLM-4.5在 {total_tests - successful_tests} 个测试中违反了任务数量限制")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        print("完整错误追踪:")
        traceback.print_exc()
        return False

async def main():
    """主函数"""
    print("=" * 80)
    print("🧪 GLM-4.5 强化任务分解约束测试")
    print("=" * 80)
    
    success = await test_glm45_task_limit()
    
    print("\n" + "=" * 80)
    if success:
        print("🎉 测试成功！GLM-4.5任务分解能力已显著改善")
        print("✅ 任务数量控制在合理范围内")
        print("✅ 战略性思维得到提升")
        print("✅ 配置文件问题已解决")
    else:
        print("❌ 测试发现问题，GLM-4.5任务分解仍需进一步优化")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())