@echo off
echo ========================================
echo  Environment Check
echo ========================================
echo.

set "errors=0"

echo Checking project structure...
if exist "pyproject.toml" (
    echo + pyproject.toml found
) else (
    echo - pyproject.toml missing
    set /a errors+=1
)

if exist "frontend" (
    echo + frontend directory found
) else (
    echo - frontend directory missing
    set /a errors+=1
)

echo.
echo Checking system dependencies...

python --version >nul 2>&1
if errorlevel 1 (
    echo - Python not found
    set /a errors+=1
) else (
    echo + Python found
)

node --version >nul 2>&1
if errorlevel 1 (
    echo - Node.js not found
    set /a errors+=1
) else (
    echo + Node.js found
)

echo.
echo Checking project setup...

if exist ".venv" (
    echo + Virtual environment created
) else (
    echo - Virtual environment missing
    set /a errors+=1
)

if exist "frontend\node_modules" (
    echo + Frontend dependencies installed
) else (
    echo - Frontend dependencies missing
    set /a errors+=1
)

if exist ".env" (
    echo + .env file exists
) else (
    echo - .env file missing
    set /a errors+=1
)

echo.
echo ========================================
if %errors%==0 (
    echo [SUCCESS] All checks passed!
    echo.
    echo Ready to start services:
    echo   Run: quick_start.bat
) else (
    echo [ERROR] Found %errors% issues
    echo.
    echo Please run: setup_native_windows.bat
)
echo ========================================

pause