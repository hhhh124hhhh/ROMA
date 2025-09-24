@echo off
echo ========================================
echo  启动 SentientResearchAgent 后端服务
echo ========================================
echo.

REM 检查是否在项目根目录
if not exist "pyproject.toml" (
    echo [ERROR] 请在项目根目录运行此脚本
    pause
    exit /b 1
)

REM 检查虚拟环境是否存在
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] 虚拟环境不存在，请先运行 setup_native_windows.bat
    pause
    exit /b 1
)

echo [INFO] 激活虚拟环境...
call .venv\Scripts\activate.bat

echo [INFO] 检查环境变量...
if exist ".env" (
    echo [INFO] .env 文件存在
) else (
    echo [WARNING] .env 文件不存在，某些功能可能无法正常工作
)

echo [INFO] 启动后端服务...
echo [INFO] 后端将在 http://localhost:5000 运行
echo [INFO] 按 Ctrl+C 停止服务
echo.

python -m sentientresearchagent

pause