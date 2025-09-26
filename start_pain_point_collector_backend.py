#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI产品痛点收集智能体启动脚本

专门用于启动AI产品痛点收集与分析的多步骤智能体系统
基于GLM-4.5模型，采用ROMA框架的原子化执行模式
"""

import os
import sys
from pathlib import Path

def main():
    """AI产品痛点收集智能体启动函数"""
    print("🎯 AI产品痛点收集智能体启动器")
    print("=" * 70)
    print("🔍 专业的AI产品痛点收集、分析和解决方案生成系统")
    
    # 项目根目录
    project_root = Path(__file__).parent
    
    # 检查智谱AI密钥
    env_path = project_root / ".env"
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(env_path)
        print(f"✅ 环境配置: {env_path}")
        
        zhipuai_key = os.getenv("ZHIPUAI_API_KEY", "")
        if zhipuai_key and zhipuai_key != "your_zhipuai_key_here":
            print(f"✅ 智谱AI密钥: {zhipuai_key[:10]}...")
        else:
            print("❌ 智谱AI密钥未配置")
            print("请在.env文件中设置: ZHIPUAI_API_KEY=你的密钥")
            return
            
        # 检查E2B配置
        e2b_key = os.getenv("E2B_API_KEY", "")
        e2b_template = os.getenv("E2B_TEMPLATE_ID", "")
        if e2b_key and e2b_template:
            print(f"✅ E2B沙箱: {e2b_key[:10]}.../{e2b_template}")
        else:
            print("⚠️  E2B沙箱未完全配置，数据分析功能受限")
    else:
        print(f"❌ 环境配置不存在: {env_path}")
        return
    
    # 检查配置文件是否存在
    config_path = project_root / "src/sentientresearchagent/hierarchical_agent_framework/agent_configs/profiles copy/ai_product_pain_point_collector.yaml"
    if not config_path.exists():
        print(f"❌ 配置文件不存在: {config_path}")
        print("请确保 ai_product_pain_point_collector.yaml 配置文件存在")
        return
    
    # 设置痛点收集智能体配置
    os.environ["PYTHONPATH"] = str(project_root / "src")
    # 使用正确的agents配置文件路径
    os.environ["SENTIENT_AGENTS_CONFIG"] = str(project_root / "src/sentientresearchagent/hierarchical_agent_framework/agent_configs/profiles copy/agents_pain_point_collector.yaml")
    os.environ["SENTIENT_PROFILE"] = "ai_product_pain_point_collector"
    
    print("\n🎯 痛点收集智能体配置信息:")
    print("🤖 模型: 智谱AI GLM-4.5")
    print("📋 配置: ai_product_pain_point_collector.yaml")
    print("🌐 服务: http://localhost:5000")
    print("⚡ 特点: 多步骤痛点收集与分析工作流")
    print()
    print("👥 专业智能体团队:")
    print("   🔍 痛点发现专家    - 多渠道信息收集和痛点识别")
    print("   📊 痛点分析专家    - 深度分析、分类和评估")
    print("   🏆 竞品研究专家    - 竞品痛点分析和对比研究")
    print("   📈 优先级专家      - 基于影响和资源的优先级排序")
    print("   💡 解决方案专家    - 可行改进方案和实施计划")
    print("   📝 报告专家        - 专业报告生成和可视化")
    print()
    print("🔄 多步骤工作流程:")
    print("   1️⃣  痛点发现阶段   - 多渠道信息收集、用户反馈聚合")
    print("   2️⃣  痛点分类阶段   - 类型分类、严重程度评估")
    print("   3️⃣  深度分析阶段   - 根因分析、业务影响评估")
    print("   4️⃣  优先级排序阶段 - 重要性评分、资源需求分析")
    print("   5️⃣  解决方案阶段   - 改进方案设计、可行性评估")
    print()
    print("📊 数据源覆盖:")
    print("   📱 用户反馈: 应用商店、客服工单、反馈平台")
    print("   💬 社交媒体: 微博、知乎、技术论坛")
    print("   🏢 竞品分析: 竞品评价、行业报告、专家评测")
    print("   📈 内部数据: 用户行为、使用统计、A/B测试")
    print()
    print("📋 输出格式:")
    print("   📊 痛点概览表   - 结构化痛点信息汇总")
    print("   📝 分析报告     - 详细的痛点分析报告")
    print("   🎯 优先级矩阵   - 可视化优先级排序")
    print("   📅 行动计划     - 可执行的改进实施清单")
    print()
    print("💡 使用示例:")
    print('   "请系统性收集和分析我们AI写作助手产品的用户痛点"')
    print('   "分析AI聊天机器人的用户体验问题并提供改进建议"')
    print('   "对比我们产品与主要竞品的痛点差异"')
    print()
    print("🚀 启动痛点收集智能体服务...")
    print("按 Ctrl+C 停止服务\n")
    
    try:
        # 启动服务器
        from sentientresearchagent.server.main import main as server_main
        server_main()
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保在正确的UV环境中运行")
        
    except KeyboardInterrupt:
        print("\n👋 痛点收集智能体服务已停止")
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()