echo ========================================
echo   GLM-4.5 增强多任务全栈启动器
echo ========================================
echo   智谱AI GLM-4.5 增强多任务智能体系统
echo   Enhanced Multitask Execution Mode
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

echo [INFO] Starting enhanced multitask backend service in new window...
start "GLM-4.5 Enhanced Multitask Backend" cmd /k "title GLM-4.5 Enhanced Multitask Backend && echo Starting GLM-4.5 enhanced multitask backend service... && uv run python start_enhanced_multitask_backend.py && echo. && echo Enhanced backend service stopped, press any key to close window... && pause"

echo [INFO] Waiting for enhanced backend to start...
timeout /t 5 /nobreak >nul

echo [INFO] Starting frontend service in new window...
start "React Frontend Dev Server" cmd /k "title React Frontend Dev Server && echo Starting React frontend development server... && cd frontend && npm run dev && echo. && echo Frontend service stopped, press any key to close window... && pause"

echo.
echo ========================================
echo   增强多任务服务启动成功！
echo ========================================
echo   Frontend: http://localhost:3000
echo   Backend: http://localhost:5000
echo   System Info: http://localhost:5000/api/system-info
echo.
echo   支持的任务类型:
echo   - SEARCH: 信息搜索和收集
echo   - THINK: 逻辑推理和分析
echo   - WRITE: 内容创作和报告生成
echo   - CODE_INTERPRET: 代码执行和解释
echo.
echo   智能功能:
echo   - 智能任务分解 (根据复杂度自动分解)
echo   - 并行执行支持 (独立任务同时处理)
echo   - 依赖关系管理 (智能处理任务间依赖)
echo   - 结果聚合整合 (自动整合多任务结果)
echo.
echo   前后端服务运行在独立窗口中
echo   关闭相应窗口即可停止服务
echo ========================================
echo.

pause