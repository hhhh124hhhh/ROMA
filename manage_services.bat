@echo off
chcp 65001 >nul
echo ========================================
echo  SentientResearchAgent Service Manager
echo ========================================
echo.

echo Choose an option:
echo.
echo   1) Setup Environment (First Time)
echo   2) Start Backend Service
echo   3) Start Frontend Service  
echo   4) Start Both Backend and Frontend
echo   5) Check Service Status
echo   6) View Environment Info
echo   7) Exit
echo.

set /p "choice=Please select (1-7): "

if "%choice%"=="1" (
    echo [INFO] Running environment setup...
    call setup_native_windows.bat
) else if "%choice%"=="2" (
    echo [INFO] Starting backend service...
    start "SentientAgent-Backend" cmd /k start_backend.bat
) else if "%choice%"=="3" (
    echo [INFO] Starting frontend service...
    start "SentientAgent-Frontend" cmd /k start_frontend.bat
) else if "%choice%"=="4" (
    echo [INFO] Starting backend and frontend services...
    start "SentientAgent-Backend" cmd /k start_backend.bat
    timeout /t 3 /nobreak >nul
    start "SentientAgent-Frontend" cmd /k start_frontend.bat
    timeout /t 5 /nobreak >nul
    echo [INFO] Opening browser...
    start "" "http://localhost:3000"
) else if "%choice%"=="5" (
    echo [INFO] Checking service status...
    echo.
    echo Port usage:
    netstat -ano | findstr :5000 && echo Backend service (port 5000) is running || echo Backend service (port 5000) not running
    netstat -ano | findstr :3000 && echo Frontend service (port 3000) is running || echo Frontend service (port 3000) not running
    echo.
    echo Testing service connections:
    powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5000/api/health' -Method GET -TimeoutSec 5; Write-Host 'Backend health check: Success' -ForegroundColor Green } catch { Write-Host 'Backend health check: Failed' -ForegroundColor Red }"
    powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:3000' -Method GET -TimeoutSec 5; Write-Host 'Frontend service: Running' -ForegroundColor Green } catch { Write-Host 'Frontend service: Not running' -ForegroundColor Red }"
) else if "%choice%"=="6" (
    echo [INFO] Environment information:
    echo.
    echo Python version:
    python --version 2>nul || echo Python not installed
    echo.
    echo Node.js version:
    node --version 2>nul || echo Node.js not installed
    echo.
    echo npm version:
    npm --version 2>nul || echo npm not installed
    echo.
    echo Virtual environment status:
    if exist ".venv" (
        echo ^✓ Virtual environment created
    ) else (
        echo ^✗ Virtual environment not created
    )
    echo.
    echo Frontend dependencies status:
    if exist "frontend\node_modules" (
        echo ^✓ Frontend dependencies installed
    ) else (
        echo ^✗ Frontend dependencies not installed
    )
    echo.
    echo .env file status:
    if exist ".env" (
        echo ^✓ .env file exists
    ) else (
        echo ^✗ .env file does not exist
    )
) else if "%choice%"=="7" (
    echo [INFO] Exiting
    exit /b 0
) else (
    echo [ERROR] Invalid selection
)

echo.
pause