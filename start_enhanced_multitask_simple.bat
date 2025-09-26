echo ========================================
echo   GLM-4.5 Enhanced Multi-Task Full-Stack Launcher
echo ========================================
echo   ZhipuAI GLM-4.5 Enhanced Multi-Task Agent System
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
echo   Enhanced Multi-Task Services Started Successfully!
echo ========================================
echo   Frontend: http://localhost:3000
echo   Backend: http://localhost:5000
echo   System Info: http://localhost:5000/api/system-info
echo.
echo   Supported Task Types:
echo   - SEARCH: Information Search and Collection
echo   - THINK: Logical Reasoning and Analysis
echo   - WRITE: Content Creation and Report Generation
echo   - CODE_INTERPRET: Code Execution and Interpretation
echo.
echo   Intelligent Features:
echo   - Smart Task Decomposition (Auto-split by complexity)
echo   - Parallel Execution Support (Process independent tasks simultaneously)
echo   - Dependency Management (Smart handling of task dependencies)
echo   - Result Aggregation (Auto-integrate multi-task results)
echo.
echo   Frontend and Backend services run in separate windows
echo   Close respective windows to stop services
echo ========================================
echo.

pause