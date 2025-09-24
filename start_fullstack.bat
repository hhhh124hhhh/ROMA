@echo off
echo ========================================
echo   UV Fullstack Launcher - GLM-4.5
echo ========================================
echo   ZhipuAI GLM-4.5 Research Agent System
echo   Quick Start Frontend and Backend
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

echo [INFO] Starting backend service in new window...
start "GLM-4.5 Backend Service" cmd /k "title GLM-4.5 Backend Service && echo Starting GLM-4.5 backend service... && uv run python start_backend.py && echo. && echo Backend service stopped, press any key to close window... && pause"

echo [INFO] Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo [INFO] Starting frontend service in new window...
start "React Frontend Dev Server" cmd /k "title React Frontend Dev Server && echo Starting React frontend development server... && cd frontend && npm run dev && echo. && echo Frontend service stopped, press any key to close window... && pause"

echo.
echo ========================================
echo   Services Started Successfully!
echo ========================================
echo   Frontend: http://localhost:3000
echo   Backend: http://localhost:5000
echo   System Info: http://localhost:5000/api/system-info
echo.
echo   Frontend and backend services run in separate windows
echo   Close respective windows to stop services
echo ========================================
echo.

pause