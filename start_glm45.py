#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM-4.5 专用启动脚本

快速启动配置了智谱AI GLM-4.5模型的SentientResearchAgent服务
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

def check_environment():
    """检查环境配置"""
    print("🔍 检查GLM-4.5运行环境...")
    
    # 加载环境变量
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ 已加载环境配置: {env_path}")
    else:
        print(f"⚠️  环境配置文件不存在: {env_path}")
    
    # 检查智谱AI API密钥
    zhipuai_key = os.getenv("ZHIPUAI_API_KEY", "")
    if zhipuai_key and zhipuai_key != "your_zhipuai_key_here":
        print(f"✅ 智谱AI API密钥已配置: {zhipuai_key[:10]}...")
    else:
        print("❌ 智谱AI API密钥未配置!")
        print("请在.env文件中设置 ZHIPUAI_API_KEY=你的智谱AI密钥")
        return False
    
    # 检查配置文件
    agents_config = project_root / "agents_glm45.yaml"
    profile_config = project_root / "profiles" / "glm45_profile.yaml"
    
    if agents_config.exists():
        print(f"✅ GLM-4.5代理配置文件: {agents_config}")
    else:
        print(f"❌ 代理配置文件不存在: {agents_config}")
        return False
    
    if profile_config.exists():
        print(f"✅ GLM-4.5配置档案: {profile_config}")
    else:
        print(f"❌ 配置档案不存在: {profile_config}")
        return False
    
    return True

def create_sentient_config():
    """创建针对GLM-4.5优化的配置"""
    config_content = '''# GLM-4.5 专用配置
# SentientResearchAgent GLM-4.5优化配置

# 默认使用GLM-4.5配置档案
default_profile: "GLM45Professional"

# 激活的配置档案
active_profile_name: "GLM45Professional"

# 代理配置文件路径
agents_config_path: "agents_glm45.yaml"

# 配置档案目录
profiles_dir: "profiles"

# 日志配置
logging:
  level: "INFO"
  file_mode: "w"
  enable_colors: true

# Web服务器配置
web_server:
  host: "0.0.0.0"
  port: 5000
  debug: false
  secret_key: "glm45-sentient-secret-key"
  cors_origins:
    - "http://localhost:3000"
    - "http://127.0.0.1:3000"

# 执行配置
execution:
  enable_hitl: true
  max_iterations: 10
  timeout_seconds: 300

# 缓存配置
cache:
  enabled: true
  directory: ".agent_cache"
  ttl_seconds: 3600

# 实验配置
experiments:
  base_dir: "experiments"
  retention_days: 30
'''
    
    config_path = project_root / "sentient_glm45.yaml"
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"✅ 已创建GLM-4.5专用配置: {config_path}")
    return config_path

def start_server():
    """启动GLM-4.5优化的服务器"""
    try:
        from sentientresearchagent.server.main import create_server
        from sentientresearchagent.config import SentientConfig
        
        # 使用GLM-4.5专用配置
        config_path = project_root / "sentient_glm45.yaml"
        if config_path.exists():
            config = SentientConfig.from_yaml(str(config_path))
            print(f"✅ 使用配置文件: {config_path}")
        else:
            print("⚠️  使用默认配置启动")
            config = None
        
        print("\n🚀 启动GLM-4.5 SentientResearchAgent服务...")
        print("=" * 60)
        print("🤖 模型: 智谱AI GLM-4.5")
        print("🌐 Web界面: http://localhost:5000")
        print("📡 WebSocket: ws://localhost:5000")
        print("🎯 配置档案: GLM45Professional")
        print("=" * 60)
        print("\n🔧 API端点:")
        print("   POST /api/simple/execute - 执行任务")
        print("   POST /api/simple/research - 研究任务")
        print("   POST /api/simple/analysis - 分析任务")
        print("   GET  /api/system-info - 系统信息")
        print("\n📚 使用示例:")
        print("   curl -X POST http://localhost:5000/api/simple/research \\")
        print("        -H 'Content-Type: application/json' \\")
        print("        -d '{\"topic\": \"人工智能发展趋势分析\"}'")
        print("\n按 Ctrl+C 停止服务\n")
        
        # 创建并运行服务器
        server = create_server(config)
        server.run(host='0.0.0.0', port=5000, debug=False)
        
    except KeyboardInterrupt:
        print("\n\n👋 GLM-4.5服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    print("🚀 GLM-4.5 SentientResearchAgent 启动器")
    print("=" * 50)
    
    # 检查环境
    if not check_environment():
        print("\n❌ 环境检查失败，请修复配置后重试")
        return
    
    # 创建专用配置
    create_sentient_config()
    
    print("\n✅ 环境检查完成，准备启动服务...")
    input("按回车键继续启动服务...")
    
    # 启动服务器
    start_server()

if __name__ == "__main__":
    main()