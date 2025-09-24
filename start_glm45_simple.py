#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM-4.5 简化启动脚本 (UV环境优化)

直接启动智谱AI GLM-4.5服务，专为UV包管理器环境优化
"""

import os
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

def main():
    """简化的主函数，适用于UV环境"""
    print("🚀 GLM-4.5 启动器 (UV环境)")
    print("=" * 40)
    
    # 基本环境检查
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("❌ python-dotenv未安装")
        print("请运行: uv add python-dotenv")
        return
    
    # 加载环境变量
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ 环境配置: {env_path}")
    else:
        print(f"⚠️  环境配置不存在: {env_path}")
    
    # 检查智谱AI密钥
    zhipuai_key = os.getenv("ZHIPUAI_API_KEY", "")
    if zhipuai_key and zhipuai_key != "your_zhipuai_key_here":
        print(f"✅ 智谱AI密钥: {zhipuai_key[:10]}...")
    else:
        print("❌ 智谱AI密钥未配置")
        print("请在.env文件中设置: ZHIPUAI_API_KEY=你的密钥")
        input("按回车继续（可能无法使用智谱AI功能）...")
    
    # 设置GLM-4.5相关的环境变量
    os.environ.setdefault("SENTIENT_AGENTS_CONFIG", "agents_glm45.yaml")
    os.environ.setdefault("SENTIENT_PROFILE", "GLM45Professional")
    
    print("\n🚀 启动SentientResearchAgent...")
    print("🤖 模型: GLM-4.5")
    print("📱 界面: http://localhost:5000")
    print("🔄 正在启动...")
    
    try:
        # 尝试启动主服务器
        from sentientresearchagent.server.main import main as server_main
        server_main()
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("可能的解决方案:")
        print("1. 运行: uv sync")
        print("2. 检查依赖是否完整安装")
        print("3. 确认在正确的UV环境中运行")
        
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("请检查:")
        print("1. UV环境是否正确激活")
        print("2. 所有依赖是否正确安装")
        print("3. 配置文件是否存在")

if __name__ == "__main__":
    main()