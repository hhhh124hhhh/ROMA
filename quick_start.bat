@echo off
echo ========================================
echo  SentientResearchAgent Quick Start
echo ========================================
echo.

REM Check if in project directory
if not exist "pyproject.toml" (
    echo [ERROR] Please run from project root directory
    pause
    exit /b 1
)

echo [INFO] Checking environment...

REM Check if virtual environment exists
if not exist ".venv" (
    echo [ERROR] Virtual environment not found
    echo Please run: setup_native_windows.bat first
    pause
    exit /b 1
)

REM Check if frontend dependencies exist
if not exist "frontend\node_modules" (
    echo [ERROR] Frontend dependencies not found
    echo Please run: setup_native_windows.bat first
    pause
    exit /b 1
)

echo [INFO] Environment OK!
echo [INFO] Starting services...

REM Start backend in new window
echo [INFO] Starting backend service...
start "Backend" cmd /k "cd /d %CD% && .venv\Scripts\activate.bat && python -m sentientresearchagent"

REM Wait a bit for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend in new window  
echo [INFO] Starting frontend service...
start "Frontend" cmd /k "cd /d %CD%\frontend && npm run dev"

REM Wait for frontend to start
timeout /t 10 /nobreak >nul

REM Open browser
echo [INFO] Opening browser...
start "" "http://localhost:3000"

echo.
echo [SUCCESS] Services started!
echo.
echo Services:
echo   - Backend: http://localhost:5000
echo   - Frontend: http://localhost:3000
echo.
echo Press any key to exit this window...
pause