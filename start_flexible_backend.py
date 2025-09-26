#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROMA智能体灵活启动后端脚本

支持通过环境变量动态配置不同的智能体
参考 start_enhanced_multitask_backend.py 的实现模式
"""

import os
import sys
from pathlib import Path

def main():
    """灵活智能体启动函数"""
    # 从环境变量读取配置
    profile = os.environ.get("SENTIENT_PROFILE", "")
    agents_config = os.environ.get("SENTIENT_AGENTS_CONFIG", "")
    display_name = os.environ.get("DISPLAY_NAME", "智能体")
    
    print(f"🚀 启动 {display_name}")
    print("=" * 50)
    print(f"📋 配置: {profile}")
    print(f"🌐 服务: http://localhost:5000")
    print(f"📝 描述: {os.environ.get('DESCRIPTION', '')}")
    print()
    
    # 项目根目录
    project_root = Path(__file__).parent
    
    # 设置Python路径
    if "PYTHONPATH" not in os.environ:
        os.environ["PYTHONPATH"] = str(project_root / "src")
    
    # 对于痛点收集智能体，需要特殊处理agents配置路径
    if profile == "ai_product_pain_point_collector":
        agents_config_path = project_root / "src/sentientresearchagent/hierarchical_agent_framework/agent_configs/profiles copy/agents_pain_point_collector.yaml"
        if agents_config_path.exists():
            os.environ["SENTIENT_AGENTS_CONFIG"] = str(agents_config_path)
            print(f"✅ 使用痛点收集agents配置: {agents_config_path}")
        else:
            print(f"❌ 痛点收集agents配置不存在: {agents_config_path}")
            return
    
    print(f"[INFO] 设置环境变量...")
    print(f"[INFO] 启动后端服务...")
    print("按 Ctrl+C 停止服务")
    print()
    
    try:
        # 启动服务器
        from sentientresearchagent.server.main import main as server_main
        server_main()
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保在正确的UV环境中运行")
        
    except KeyboardInterrupt:
        print(f"\n👋 {display_name}服务已停止")
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()