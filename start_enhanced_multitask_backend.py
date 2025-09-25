#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM-4.5 增强多任务执行启动脚本

启用复杂的多层级、多类型任务工作流，展示ROMA-Chinese的完整智能处理能力
"""

import os
import sys
from pathlib import Path

def main():
    """增强多任务启动函数，启用复杂工作流"""
    print("🚀 GLM-4.5 增强多任务执行启动器")
    print("=" * 70)
    print("🔧 启用复杂的多层级、多类型任务工作流")
    
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
            print("⚠️  E2B沙箱未完全配置，代码执行功能受限")
    else:
        print(f"❌ 环境配置不存在: {env_path}")
        return
    
    # 设置增强多任务配置
    os.environ["PYTHONPATH"] = str(project_root / "src")
    os.environ["SENTIENT_AGENTS_CONFIG"] = "agents_glm45_enhanced.yaml"
    os.environ["SENTIENT_PROFILE"] = "glm45_enhanced_multitask"
    
    print("\n✨ 增强多任务配置信息:")
    print("🤖 模型: 智谱AI GLM-4.5")
    print("📋 配置: agents_glm45_enhanced.yaml (完整多任务版)")
    print("🌐 服务: http://localhost:5000")
    print("⚡ 特点: 复杂多层级、多类型任务工作流")
    print()
    print("📊 支持的任务类型:")
    print("   🔍 SEARCH     - 信息搜索和收集")
    print("   🧠 THINK      - 逻辑推理和分析")
    print("   ✍️  WRITE      - 内容创作和报告生成")
    print("   📈 ANALYZE    - 数据分析和见解提取")
    print("   💻 CODE_INTERPRET - 代码执行和解释")
    print()
    print("🔧 智能功能:")
    print("   🎯 智能任务分解 - 根据复杂度自动分解")
    print("   ⚡ 并行执行支持 - 独立任务同时处理")
    print("   🔗 依赖关系管理 - 智能处理任务间依赖")
    print("   🔄 结果聚合整合 - 自动整合多任务结果")
    print("   🎛️  迭代优化机制 - 支持任务重新规划")
    print()
    print("🚀 启动增强多任务服务...")
    print("按 Ctrl+C 停止服务\n")
    
    try:
        # 启动服务器
        from sentientresearchagent.server.main import main as server_main
        server_main()
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保在正确的UV环境中运行")
        
    except KeyboardInterrupt:
        print("\n👋 增强多任务服务已停止")
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()