#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROMA智能体灵活启动脚本

支持动态选择不同的智能体配置文件，提供灵活的启动选项
支持命令行参数和交互式选择模式
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# 可用的智能体配置映射
AVAILABLE_PROFILES = {
    "1": {
        "name": "ai_product_pain_point_collector",
        "display": "AI产品痛点收集智能体",
        "description": "专业的AI产品痛点收集、分析和解决方案生成系统",
        "agents_config": "agents_pain_point_collector.yaml",
        "features": [
            "多步骤痛点收集工作流",
            "6个专业化智能体团队",
            "多渠道数据源支持",
            "竞品对比分析"
        ]
    },
    "2": {
        "name": "glm45_enhanced_multitask",
        "display": "GLM-4.5增强多任务智能体",
        "description": "复杂的多层级、多类型任务工作流处理系统",
        "agents_config": "agents_glm45_enhanced.yaml",
        "features": [
            "多层级任务分解",
            "并行执行支持",
            "依赖关系管理",
            "结果聚合整合"
        ]
    },
    "3": {
        "name": "glm45_professional",
        "display": "GLM-4.5专业智能体",
        "description": "专为智谱AI GLM-4.5模型优化的专业代理配置",
        "agents_config": "agents_glm45.yaml",
        "features": [
            "中文理解优化",
            "逻辑推理能力",
            "创意写作支持",
            "问答系统"
        ]
    },
    "4": {
        "name": "deep_research_agent",
        "display": "深度研究智能体",
        "description": "综合性研究任务处理，支持多步骤分析",
        "agents_config": "agents_deep_research.yaml",
        "features": [
            "学术研究支持",
            "市场分析能力",
            "技术调研",
            "事实核查验证"
        ]
    },
    "5": {
        "name": "crypto_analytics_agent",
        "display": "加密货币分析智能体",
        "description": "专门用于加密货币和DeFi分析的智能体",
        "agents_config": "agents_crypto_analytics.yaml",
        "features": [
            "代币分析",
            "DeFi研究",
            "市场情报",
            "链上数据分析"
        ]
    }
}

def show_available_profiles():
    """显示可用的智能体配置"""
    print("🤖 可用的智能体配置:")
    print("=" * 70)
    
    for key, profile in AVAILABLE_PROFILES.items():
        print(f"\n{key}. {profile['display']}")
        print(f"   📝 描述: {profile['description']}")
        print(f"   🔧 配置: {profile['name']}")
        print(f"   ⚡ 特性:")
        for feature in profile['features']:
            print(f"      • {feature}")

def get_user_choice() -> Optional[str]:
    """获取用户选择"""
    while True:
        try:
            choice = input(f"\n请选择智能体配置 (1-{len(AVAILABLE_PROFILES)}, q退出): ").strip()
            
            if choice.lower() == 'q':
                return None
                
            if choice in AVAILABLE_PROFILES:
                return choice
            else:
                print(f"❌ 无效选择，请输入1-{len(AVAILABLE_PROFILES)}或q")
                
        except KeyboardInterrupt:
            print("\n👋 用户取消")
            return None
        except EOFError:
            print("\n👋 退出")
            return None

def check_environment() -> bool:
    """检查运行环境"""
    project_root = Path(__file__).parent
    
    # 检查环境配置
    env_path = project_root / ".env"
    if not env_path.exists():
        print(f"❌ 环境配置不存在: {env_path}")
        return False
    
    # 加载环境变量
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
        print(f"✅ 环境配置: {env_path}")
    except ImportError:
        print("❌ 缺少python-dotenv包，请安装: pip install python-dotenv")
        return False
    
    # 检查智谱AI密钥
    zhipuai_key = os.getenv("ZHIPUAI_API_KEY", "")
    if not zhipuai_key or zhipuai_key == "your_zhipuai_key_here":
        print("❌ 智谱AI密钥未配置")
        print("请在.env文件中设置: ZHIPUAI_API_KEY=你的密钥")
        return False
    
    print(f"✅ 智谱AI密钥: {zhipuai_key[:10]}...")
    
    # 检查E2B配置（可选）
    e2b_key = os.getenv("E2B_API_KEY", "")
    e2b_template = os.getenv("E2B_TEMPLATE_ID", "")
    if e2b_key and e2b_template:
        print(f"✅ E2B沙箱: {e2b_key[:10]}.../{e2b_template}")
    else:
        print("⚠️  E2B沙箱未完全配置，代码执行功能受限")
    
    return True

def check_config_files(profile_info: Dict) -> bool:
    """检查配置文件是否存在"""
    project_root = Path(__file__).parent
    
    # 检查profile配置文件
    profile_path = project_root / f"src/sentientresearchagent/hierarchical_agent_framework/agent_configs/profiles copy/{profile_info['name']}.yaml"
    if not profile_path.exists():
        print(f"❌ Profile配置文件不存在: {profile_path}")
        return False
    
    # 检查agents配置文件
    agents_path = project_root / f"src/sentientresearchagent/hierarchical_agent_framework/agent_configs/profiles copy/{profile_info['agents_config']}"
    if not agents_path.exists():
        print(f"⚠️  Agents配置文件不存在: {agents_path}")
        print("   将使用默认智能体配置")
    
    print(f"✅ 配置文件: {profile_path.name}")
    return True

def start_agent_service(profile_info: Dict):
    """启动智能体服务"""
    project_root = Path(__file__).parent
    
    # 设置环境变量
    os.environ["PYTHONPATH"] = str(project_root / "src")
    os.environ["SENTIENT_PROFILE"] = profile_info["name"]
    
    # 如果agents配置文件存在，则设置
    agents_config_path = project_root / f"src/sentientresearchagent/hierarchical_agent_framework/agent_configs/profiles copy/{profile_info['agents_config']}"
    if agents_config_path.exists():
        os.environ["SENTIENT_AGENTS_CONFIG"] = profile_info["agents_config"]
    
    print(f"\n🚀 启动 {profile_info['display']}")
    print("=" * 70)
    print(f"📋 配置: {profile_info['name']}")
    print(f"🌐 服务: http://localhost:5000")
    print(f"📝 描述: {profile_info['description']}")
    print("\n⚡ 特性:")
    for feature in profile_info['features']:
        print(f"   • {feature}")
    
    print(f"\n🚀 启动服务...")
    print("按 Ctrl+C 停止服务\n")
    
    try:
        # 启动服务器
        from sentientresearchagent.server.main import main as server_main
        server_main()
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保在正确的UV环境中运行")
        
    except KeyboardInterrupt:
        print(f"\n👋 {profile_info['display']} 服务已停止")
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="ROMA智能体灵活启动脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python start_flexible_agent.py                    # 交互式选择模式
  python start_flexible_agent.py --profile 1       # 直接启动痛点收集智能体
  python start_flexible_agent.py --list            # 列出所有可用配置
  python start_flexible_agent.py --profile pain    # 使用配置名称启动
        """
    )
    
    parser.add_argument(
        "--profile", "-p",
        help="指定要启动的智能体配置 (序号或名称)"
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="列出所有可用的智能体配置"
    )
    
    args = parser.parse_args()
    
    print("🤖 ROMA智能体灵活启动器")
    print("=" * 70)
    
    # 如果只是列出配置
    if args.list:
        show_available_profiles()
        return
    
    # 检查环境
    if not check_environment():
        return
    
    profile_choice = None
    profile_info = None
    
    # 如果指定了配置
    if args.profile:
        # 尝试按序号匹配
        if args.profile in AVAILABLE_PROFILES:
            profile_choice = args.profile
            profile_info = AVAILABLE_PROFILES[args.profile]
        else:
            # 尝试按名称匹配
            for key, info in AVAILABLE_PROFILES.items():
                if args.profile.lower() in info['name'].lower() or args.profile.lower() in info['display'].lower():
                    profile_choice = key
                    profile_info = info
                    break
            
            if not profile_info:
                print(f"❌ 未找到配置: {args.profile}")
                show_available_profiles()
                return
    else:
        # 交互式选择
        show_available_profiles()
        profile_choice = get_user_choice()
        
        if not profile_choice:
            print("👋 退出")
            return
            
        profile_info = AVAILABLE_PROFILES[profile_choice]
    
    # 检查配置文件
    if not check_config_files(profile_info):
        return
    
    # 启动服务
    start_agent_service(profile_info)

if __name__ == "__main__":
    main()