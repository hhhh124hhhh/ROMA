#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM-4.5 UV环境专用启动脚本

专门为uv包管理器环境设计的GLM-4.5启动脚本
"""

import os
import sys
from pathlib import Path

def main():
    """UV环境专用启动函数"""
    print("🚀 GLM-4.5 SentientResearchAgent (UV环境)")
    print("=" * 50)
    
    # 项目根目录
    project_root = Path(__file__).parent
    
    # 检查UV环境
    print("🔍 检查UV环境...")
    
    # 检查.env文件
    env_path = project_root / ".env"
    if env_path.exists():
        print(f"✅ 环境配置: {env_path}")
        
        # 读取智谱AI密钥
        with open(env_path, 'r', encoding='utf-8') as f:
            env_content = f.read()
            
        if "ZHIPUAI_API_KEY=" in env_content and "your_zhipuai_key_here" not in env_content:
            print("✅ 智谱AI密钥已配置")
        else:
            print("❌ 智谱AI密钥未配置")
            print("请在.env文件中设置: ZHIPUAI_API_KEY=你的密钥")
    else:
        print(f"⚠️  环境配置不存在: {env_path}")
    
    # 检查配置文件
    agents_config = project_root / "agents_glm45.yaml"
    if agents_config.exists():
        print("✅ GLM-4.5代理配置文件存在")
    else:
        print("❌ GLM-4.5代理配置文件不存在")
    
    # 设置环境变量
    os.environ["PYTHONPATH"] = str(project_root / "src")
    
    print("\n🚀 启动服务...")
    print("🤖 模型: 智谱AI GLM-4.5")
    print("🌐 界面: http://localhost:5000")
    print("📡 WebSocket: ws://localhost:5000")
    print("🎯 配置: GLM45Professional")
    print("\n按 Ctrl+C 停止服务\n")
    
    try:
        # 使用uv run执行主服务器
        import subprocess
        import sys
        
        # 构建命令
        cmd = [
            "uv", "run", "python", "-m", 
            "sentientresearchagent.server.main",
            "--config", "sentient_glm45.yaml"
        ]
        
        # 设置工作目录
        os.chdir(project_root)
        
        # 执行命令
        result = subprocess.run(cmd, cwd=project_root)
        
    except FileNotFoundError:
        print("❌ UV命令未找到")
        print("请确保已安装UV: https://github.com/astral-sh/uv")
        
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("尝试手动运行:")
        print("uv run python -m sentientresearchagent.server.main")

if __name__ == "__main__":
    main()