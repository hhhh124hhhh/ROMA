#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM-4.5 增强递归执行启动脚本

启用深度递归执行，展示ROMA-Chinese的多层智能处理能力
"""

import os
import sys
from pathlib import Path

def main():
    """增强启动函数，启用深度递归执行"""
    print("🚀 GLM-4.5 增强递归执行启动器")
    print("=" * 60)
    print("🔧 启用深度递归执行，展示多层智能处理")
    
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
    else:
        print(f"❌ 环境配置不存在: {env_path}")
        return
    
    # 设置增强配置
    os.environ["PYTHONPATH"] = str(project_root / "src")
    os.environ["SENTIENT_AGENTS_CONFIG"] = "agents_glm45_enhanced.yaml"
    os.environ["SENTIENT_PROFILE"] = "glm45_professional"
    
    print("\n✨ 增强配置信息:")
    print("🤖 模型: 智谱AI GLM-4.5")
    print("📋 配置: agents_glm45_enhanced.yaml (完整多任务版，启用E2B沙箱)")
    print("🌐 服务: http://localhost:5000")
    print("⚡ 特点: 深度递归执行，多层智能分解")
    print("🔄 递归层数: 支持最多1000执行步骤")
    print("🧠 智能分解: 启用任务原子化和多层规划")
    print("\n🚀 启动增强服务...")
    print("按 Ctrl+C 停止服务\n")
    
    try:
        # 启动服务器
        from sentientresearchagent.server.main import main as server_main
        server_main()
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保在正确的UV环境中运行")
        
    except KeyboardInterrupt:
        print("\n👋 增强服务已停止")
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()