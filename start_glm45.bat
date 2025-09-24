@echo off
chcp 65001 >nul
title GLM-4.5 SentientResearchAgent 启动器 (UV环境)

echo.
echo ========================================
echo  GLM-4.5 SentientResearchAgent 启动器
echo  使用UV包管理器
echo ========================================
echo.

:: 检查UV
uv --version >nul 2>&1
if errorlevel 1 (
    echo ❌ UV包管理器未安装或不在PATH中
    echo 请先安装UV: https://github.com/astral-sh/uv
    pause
    exit /b 1
)

echo ✅ UV包管理器可用

:: 检查.env文件
if not exist ".env" (
    echo ⚠️  .env文件不存在，从.env.example创建...
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo ✅ 已创建.env文件，请编辑并配置您的API密钥
    ) else (
        echo ❌ .env.example文件不存在
    )
    echo.
    echo 请编辑.env文件并配置以下密钥：
    echo   ZHIPUAI_API_KEY=你的智谱AI密钥
    echo.
    pause
    exit /b 1
)

:: 检查智谱AI API密钥
findstr /C:"ZHIPUAI_API_KEY=" .env | findstr /V /C:"your_zhipuai_key_here" >nul
if errorlevel 1 (
    echo ❌ 智谱AI API密钥未配置
    echo 请在.env文件中设置: ZHIPUAI_API_KEY=你的智谱AI密钥
    echo.
    pause
    exit /b 1
)

echo ✅ 环境检查通过
echo.

:: 同步依赖
echo 🔧 同步项目依赖...
uv sync
if errorlevel 1 (
    echo ❌ 依赖同步失败
    pause
    exit /b 1
)

echo ✅ 依赖同步完成
echo.

:: 启动GLM-4.5服务
echo 🚀 启动GLM-4.5 SentientResearchAgent...
echo.
echo 🤖 模型: 智谱AI GLM-4.5
echo 🌐 Web界面: http://localhost:5000
echo 📡 WebSocket: ws://localhost:5000
echo 🎯 配置档案: GLM45Professional
echo.
echo 按 Ctrl+C 停止服务
echo.

:: 使用UV运行Python脚本
uv run python start_glm45_simple.py

echo.
echo 👋 服务已停止
pause