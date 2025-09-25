@echo off
echo ========================================
echo   ROMA-Chinese 增强递归执行启动器
echo ========================================
echo   智谱AI GLM-4.5 深度递归智能体系统
echo   Enhanced Recursive Execution Mode
echo ========================================
echo.

REM Check if in project root directory
if not exist "pyproject.toml" (
    echo [ERROR] Please run this script in project root directory
    pause
    exit /b 1
)

REM Check UV
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] UV not installed, please install UV first
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not installed, please install Node.js first
    pause
    exit /b 1
)

echo [INFO] Starting enhanced backend service in new window...
start "GLM-4.5 Enhanced Recursive Backend" cmd /k "title GLM-4.5 Enhanced Recursive Backend && echo Starting GLM-4.5 enhanced recursive backend service... && uv run python start_enhanced_backend.py && echo. && echo Enhanced backend service stopped, press any key to close window... && pause"

echo [INFO] Waiting for enhanced backend to start...
timeout /t 5 /nobreak >nul

echo [INFO] Starting frontend service in new window...
start "React Frontend Dev Server" cmd /k "title React Frontend Dev Server && echo Starting React frontend development server... && cd frontend && npm run dev && echo. && echo Frontend service stopped, press any key to close window... && pause"

echo.
echo ========================================
echo   增强递归服务启动成功！
echo ========================================
echo   Frontend: http://localhost:3000
echo   Backend: http://localhost:5000
echo   System Info: http://localhost:5000/api/system-info
echo.
echo   🔄 增强特性:
echo   - 深度递归执行 (最多1000步)
echo   - 智能任务分解
echo   - 多层并行处理
echo   - 复杂问题深度分析
echo.
echo   前后端服务运行在独立窗口中
echo   关闭相应窗口即可停止服务
echo ========================================
echo.

pause