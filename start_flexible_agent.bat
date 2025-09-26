@echo off
chcp 65001 >nul
echo ========================================
echo   ROMA智能体灵活启动器
echo ========================================
echo   支持多种智能体配置的动态选择和启动
echo ========================================
echo.

REM Check if in project root directory
if not exist "pyproject.toml" (
    echo [ERROR] 请在项目根目录运行此脚本
    pause
    exit /b 1
)

REM Check UV
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] UV未安装，请先安装UV
    pause
    exit /b 1
)

REM Check environment file
if not exist ".env" (
    echo [ERROR] 环境配置文件.env不存在
    echo 请创建.env文件并配置ZHIPUAI_API_KEY
    pause
    exit /b 1
)

echo 可用的智能体配置:
echo ========================================
echo.
echo 1. AI产品痛点收集智能体
echo    专业的AI产品痛点收集、分析和解决方案生成系统
echo    特性: 多步骤工作流、6个专业团队、多渠道数据源
echo.
echo 2. GLM-4.5增强多任务智能体  
echo    复杂的多层级、多类型任务工作流处理系统
echo    特性: 多层级分解、并行执行、依赖管理
echo.
echo 3. GLM-4.5专业智能体
echo    专为智谱AI GLM-4.5模型优化的专业代理配置
echo    特性: 中文优化、逻辑推理、创意写作
echo.
echo 4. 深度研究智能体
echo    综合性研究任务处理，支持多步骤分析
echo    特性: 学术研究、市场分析、技术调研
echo.
echo 5. 加密货币分析智能体
echo    专门用于加密货币和DeFi分析的智能体
echo    特性: 代币分析、DeFi研究、链上数据
echo.
echo F. 使用Python灵活启动脚本（推荐）
echo    使用Python脚本进行更灵活的配置和启动
echo    特性: 交互式选择、命令行参数、详细检查
echo.

:choice
set /p choice="请选择智能体配置 (1-5, F, Q退出): "

if /i "%choice%"=="Q" (
    echo 退出
    pause
    exit /b 0
)

if "%choice%"=="f" goto python_script
if "%choice%"=="F" goto python_script

if "%choice%"=="1" (
    set PROFILE=ai_product_pain_point_collector
    set AGENTS_CONFIG=agents_pain_point_collector.yaml
    set DISPLAY_NAME=AI产品痛点收集智能体
    set DESCRIPTION=专业的AI产品痛点收集、分析和解决方案生成系统
    goto start_service
)

if "%choice%"=="2" (
    set PROFILE=glm45_enhanced_multitask
    set AGENTS_CONFIG=agents_glm45_enhanced.yaml
    set DISPLAY_NAME=GLM-4.5增强多任务智能体
    set DESCRIPTION=复杂的多层级、多类型任务工作流处理系统
    goto start_service
)

if "%choice%"=="3" (
    set PROFILE=glm45_professional
    set AGENTS_CONFIG=agents_glm45.yaml
    set DISPLAY_NAME=GLM-4.5专业智能体
    set DESCRIPTION=专为智谱AI GLM-4.5模型优化的专业代理配置
    goto start_service
)

if "%choice%"=="4" (
    set PROFILE=deep_research_agent
    set AGENTS_CONFIG=agents_deep_research.yaml
    set DISPLAY_NAME=深度研究智能体
    set DESCRIPTION=综合性研究任务处理，支持多步骤分析
    goto start_service
)

if "%choice%"=="5" (
    set PROFILE=crypto_analytics_agent
    set AGENTS_CONFIG=agents_crypto_analytics.yaml
    set DISPLAY_NAME=加密货币分析智能体
    set DESCRIPTION=专门用于加密货币和DeFi分析的智能体
    goto start_service
)

echo 无效选择，请重新输入
echo.
goto choice

:start_service
echo.
echo 启动 %DISPLAY_NAME%
echo ========================================
echo 配置: %PROFILE%
echo 服务: http://localhost:5000
echo 描述: %DESCRIPTION%
echo.

REM Check config file exists for pain point collector
if "%choice%"=="1" (
    if not exist "src\sentientresearchagent\hierarchical_agent_framework\agent_configs\profiles copy\ai_product_pain_point_collector.yaml" (
        echo 配置文件不存在: ai_product_pain_point_collector.yaml
        echo 请确保配置文件存在于正确路径
        pause
        exit /b 1
    )
)

echo [INFO] 设置环境变量...
set SENTIENT_PROFILE=%PROFILE%
set SENTIENT_AGENTS_CONFIG=%AGENTS_CONFIG%
set DISPLAY_NAME=%DISPLAY_NAME%

echo [INFO] 启动后端服务...
echo 按 Ctrl+C 停止服务
echo.

REM 使用独立的Python后端脚本（参考enhanced multitask模式）
uv run python start_flexible_backend.py

pause

:python_script
echo.
echo 启动Python灵活启动脚本...
echo ========================================
uv run python start_flexible_agent.py
pause
exit /b 0