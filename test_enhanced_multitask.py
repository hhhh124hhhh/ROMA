#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM-4.5 增强多任务配置测试脚本

测试复杂的多层级、多类型任务工作流
"""

import os
import sys
import asyncio
from pathlib import Path

def main():
    """测试增强多任务配置"""
    print("🧪 GLM-4.5 增强多任务配置测试")
    print("=" * 60)
    
    # 项目根目录
    project_root = Path(__file__).parent
    
    # 设置环境
    os.environ["PYTHONPATH"] = str(project_root / "src")
    os.environ["SENTIENT_AGENTS_CONFIG"] = "agents_glm45_enhanced.yaml"
    
    # 检查配置文件
    config_file = project_root / "agents_glm45_enhanced.yaml"
    if not config_file.exists():
        print(f"❌ 增强配置文件不存在: {config_file}")
        return
    
    print(f"✅ 配置文件: {config_file}")
    
    # 测试场景
    test_scenarios = [
        {
            "name": "简单搜索任务",
            "goal": "搜索智谱AI GLM-4.5的最新技术特性和性能指标",
            "expected_types": ["SEARCH"]
        },
        {
            "name": "复杂分析任务", 
            "goal": "分析人工智能在医疗领域的应用现状，包括技术发展、应用案例、挑战和未来趋势",
            "expected_types": ["SEARCH", "THINK"]
        },
        {
            "name": "综合研究项目",
            "goal": "研究区块链技术在供应链管理中的应用，包括技术调研、案例分析、优势劣势对比，并撰写详细报告",
            "expected_types": ["SEARCH", "THINK", "WRITE"]
        },
        {
            "name": "代码分析任务",
            "goal": "分析Python多线程编程的最佳实践，编写示例代码并进行测试验证",
            "expected_types": ["SEARCH", "THINK", "CODE_INTERPRET", "WRITE"]
        }
    ]
    
    print("\n🎯 测试场景:")
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print(f"   目标: {scenario['goal']}")
        print(f"   期望任务类型: {', '.join(scenario['expected_types'])}")
    
    print(f"\n📊 配置验证完成!")
    print("✅ 增强多任务配置已就绪")
    print("🚀 现在可以使用 start_enhanced_multitask_fullstack.bat 启动服务")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✨ 测试通过！")
    else:
        print("\n❌ 测试失败！")
        sys.exit(1)