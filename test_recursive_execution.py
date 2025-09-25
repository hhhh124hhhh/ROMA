#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROMA-Chinese 深度递归执行测试脚本

测试GLM-4.5系统的深度递归分解和执行能力
"""

import requests
import json
import time
import sys

def test_complex_research(topic, port=5000):
    """测试复杂研究任务的递归执行"""
    url = f"http://localhost:{port}/api/simple/research"
    
    payload = {
        "topic": topic,
        "enable_deep_analysis": True,
        "max_depth": 5
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"🔍 测试复杂研究任务: {topic}")
    print(f"📡 发送请求到: {url}")
    print("⏳ 等待深度递归执行结果...")
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=300)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ 递归执行成功!")
            print(f"📊 响应状态: {response.status_code}")
            print(f"📝 结果长度: {len(str(result))} 字符")
            
            if 'execution_steps' in result:
                print(f"🔄 执行步骤数: {result.get('execution_steps', 0)}")
            
            if 'task_breakdown' in result:
                print(f"🎯 任务分解层数: {len(result.get('task_breakdown', []))}")
            
            return True
        else:
            print(f"\n❌ 请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("\n⏰ 请求超时 - 这可能表示系统正在进行深度递归处理")
        return False
    except requests.exceptions.ConnectionError:
        print("\n🔌 连接错误 - 请确保后端服务正在运行")
        return False
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        return False

def check_service_status(port=5000):
    """检查服务状态"""
    url = f"http://localhost:{port}/api/simple/status"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            status = response.json()
            print("✅ 服务状态检查通过")
            print(f"🔧 配置已加载: {status.get('config_loaded', False)}")
            print(f"🤖 智能体就绪: {status.get('simple_agent_ready', False)}")
            print(f"🏗️ 框架可用: {status.get('framework_available', False)}")
            return True
        else:
            print(f"❌ 服务状态检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到服务: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 ROMA-Chinese 深度递归执行测试")
    print("=" * 50)
    
    # 检查服务状态
    print("\n1. 检查服务状态...")
    if not check_service_status():
        print("请确保运行 start_enhanced_backend.py 启动后端服务")
        sys.exit(1)
    
    # 测试简单任务（应该递归分解）
    print("\n2. 测试复杂任务递归分解...")
    simple_test = test_complex_research("分析人工智能在金融科技领域的应用现状、技术挑战和发展趋势")
    
    # 测试更复杂的任务
    print("\n3. 测试高复杂度任务...")
    complex_test = test_complex_research("深入研究区块链技术在供应链管理中的应用，包括技术架构、实施挑战、成本效益分析和未来发展前景")
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print(f"✅ 复杂任务测试: {'通过' if simple_test else '失败'}")
    print(f"✅ 高复杂度任务测试: {'通过' if complex_test else '失败'}")
    
    if simple_test or complex_test:
        print("\n🎉 深度递归执行功能正常!")
        print("💡 系统现在应该能够进行多层次的任务分解和执行")
    else:
        print("\n⚠️  深度递归执行可能需要调整配置")
        print("💡 请检查 sentient.yaml 和 agents_glm45_simple.yaml 配置")

if __name__ == "__main__":
    main()