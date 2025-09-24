@echo off
echo ========================================
echo  启动 SentientResearchAgent 前端服务
echo ========================================
echo.

REM 检查是否在项目根目录
if not exist "frontend" (
    echo [ERROR] 前端目录不存在，请检查项目结构
    pause
    exit /b 1
)

REM 检查前端依赖是否已安装
if not exist "frontend\node_modules" (
    echo [ERROR] 前端依赖未安装，请先运行 setup_native_windows.bat
    pause
    exit /b 1
)

echo [INFO] 进入前端目录...
cd frontend

echo [INFO] 启动前端开发服务器...
echo [INFO] 前端将在 http://localhost:3000 运行
echo [INFO] 按 Ctrl+C 停止服务
echo.

npm run dev

pause