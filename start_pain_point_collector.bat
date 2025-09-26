@echo off
chcp 65001 >nul
echo ========================================
echo   AI产品痛点收集智能体启动器
echo ========================================
echo   专业的AI产品痛点收集和分析系统
echo   基于GLM-4.5模型，采用ROMA框架
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

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js未安装，请先安装Node.js
    pause
    exit /b 1
)

REM Check configuration file
if not exist "src\sentientresearchagent\hierarchical_agent_framework\agent_configs\profiles copy\ai_product_pain_point_collector.yaml" (
    echo [ERROR] 配置文件不存在
    echo 请确保配置文件存在于正确路径
    pause
    exit /b 1
)

echo [INFO] 启动痛点收集智能体后端服务...
start "痛点收集后端" cmd /k "title 痛点收集后端 && uv run python start_pain_point_collector_backend.py && pause"

echo [INFO] 等待后端服务启动...
timeout /t 5 /nobreak >nul

echo [INFO] 启动前端服务...
start "前端服务" cmd /k "title 前端服务 && cd frontend && npm run dev && pause"

echo.
echo ========================================
echo   服务启动成功！
echo ========================================
echo   前端界面: http://localhost:3000
echo   后端API: http://localhost:5000
echo   系统信息: http://localhost:5000/api/system-info
echo.
echo   专业智能体团队已就绪:
echo   1. 痛点发现专家
echo   2. 痛点分析专家
echo   3. 竞品研究专家
echo   4. 优先级专家
echo   5. 解决方案专家
echo   6. 报告专家
echo.
echo   工作流程:
echo   1. 痛点发现
echo   2. 痛点分类
echo   3. 深度分析
echo   4. 优先级排序
echo   5. 解决方案
echo.
echo   数据源:
echo   1. 用户反馈
echo   2. 社交媒体
echo   3. 竞品分析
echo   4. 内部数据
echo.
echo   使用示例:
echo   "分析AI写作助手产品的主要用户痛点"
echo   "分析AI聊天机器人的用户体验问题"
echo   "对比我们产品与主要竞品的痛点差异"
echo.
echo   前端和后端服务在独立窗口运行
echo   关闭对应窗口可停止服务
echo ========================================
echo.

pause