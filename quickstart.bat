@echo off
setlocal enabledelayedexpansion

REM SentientResearchAgent Quick Start Script for Windows

REM Color codes for output (using PowerShell)
set "RED=Write-Host"
set "GREEN=Write-Host"
set "YELLOW=Write-Host"
set "BLUE=Write-Host"
set "NC="

REM Helper functions
:print_info
powershell -Command "Write-Host '[INFO] %~1' -ForegroundColor Blue"
goto :eof

:print_success
powershell -Command "Write-Host '[SUCCESS] %~1' -ForegroundColor Green"
goto :eof

:print_warning
powershell -Command "Write-Host '[WARNING] %~1' -ForegroundColor Yellow"
goto :eof

:print_error
powershell -Command "Write-Host '[ERROR] %~1' -ForegroundColor Red"
goto :eof

REM Get project root directory
set "PROJECT_ROOT=%~dp0"
REM Remove trailing backslash
if "!PROJECT_ROOT:~-1!"=="\" set "PROJECT_ROOT=!PROJECT_ROOT:~0,-1!"

cd /d "!PROJECT_ROOT!"

REM Kill existing sessions if any (using taskkill instead of screen)
taskkill /f /im python.exe /fi "WINDOWTITLE eq SentientBackend" >nul 2>&1
taskkill /f /im node.exe /fi "WINDOWTITLE eq SentientFrontend" >nul 2>&1

REM Start backend in a new command prompt window
call :print_info "Starting backend in new window..."
start "SentientBackend" /d "!PROJECT_ROOT!" cmd /k "cd /d !PROJECT_ROOT! && echo Activating virtual environment... && call .venv\Scripts\activate.bat && echo Starting backend... && python -m sentientresearchagent"

REM Start frontend in a new command prompt window
call :print_info "Starting frontend in new window..."
if exist "!PROJECT_ROOT!\frontend" (
    start "SentientFrontend" /d "!PROJECT_ROOT!\frontend" cmd /k "cd /d !PROJECT_ROOT!\frontend && echo Installing frontend dependencies... && npm install && echo Starting frontend... && npm run dev"
) else (
    call :print_error "Frontend directory not found"
    exit /b 1
)

REM Wait for ports
call :print_info "Waiting for backend (http://localhost:5000/api/health)..."
set "backend_ready=false"
for /l %%i in (1,1,60) do (
    powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5000/api/health' -Method GET -TimeoutSec 1; if ($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
    if not errorlevel 1 (
        set "backend_ready=true"
        call :print_success "Backend is up."
        goto :backend_check_done
    )
    timeout /t 1 /nobreak >nul
    if %%i equ 60 (
        call :print_warning "Backend still not responding; continuing."
    )
)
:backend_check_done

call :print_info "Waiting for frontend (http://localhost:3000)..."
set "frontend_ready=false"
for /l %%i in (1,1,60) do (
    powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:3000' -Method GET -TimeoutSec 1; if ($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
    if not errorlevel 1 (
        set "frontend_ready=true"
        call :print_success "Frontend is up."
        goto :frontend_check_done
    )
    timeout /t 1 /nobreak >nul
    if %%i equ 60 (
        call :print_warning "Frontend still not responding; continuing."
    )
)
:frontend_check_done

REM Open browser
call :print_info "Opening browser..."
start "" "http://localhost:3000"

echo.
echo ========================================
call :print_success "Quickstart complete!"
echo ========================================
echo.
echo Windows Command Prompt commands:
echo   - Backend is running in a separate window titled "SentientBackend"
echo   - Frontend is running in a separate window titled "SentientFrontend"
echo   - Close those windows to stop the services
echo.