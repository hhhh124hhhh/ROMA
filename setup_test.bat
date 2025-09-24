@echo off
setlocal enabledelayedexpansion

REM SentientResearchAgent Unified Setup Script for Windows (Simplified Test Version)
REM Supports both Docker and Native installation on Windows

REM Helper functions (using echo instead of PowerShell for compatibility)
:print_info
echo [INFO] %~1
goto :eof

:print_success
echo [SUCCESS] %~1
goto :eof

:print_warning
echo [WARNING] %~1
goto :eof

:print_error
echo [ERROR] %~1
goto :eof

REM ASCII Banner
:show_banner
echo.
echo   ____            _   _            _   
echo  / ___|  ___ _ __ ^| ^|_^| ^| ___ _ __ ^| ^|_ 
echo  \___ \ / _ \ '_ \^| __^| ^|/ _ \ '_ \^| __^|
echo   ___^) ^|  __/ ^| ^| ^| ^|_^| ^|  __/ ^| ^| ^| ^|_ 
echo  ^|____/ \___^|_^| ^|_^|\__^|_^|\___^|_^| ^|_^|\__^|
echo                                        
echo  Research Agent - Setup for Windows
echo.
goto :eof

:show_help
echo Usage: setup_test.bat [OPTIONS]
echo.
echo Options:
echo   --docker    Run Docker setup directly
echo   --native    Run native setup directly
echo   --help      Show this help message
echo.
echo Without options, an interactive menu will be shown.
exit /b 0

REM Show menu
:show_menu
echo.
echo Choose your setup method:
echo.
echo   1) Docker Setup (Recommended)
echo      - Isolated environment
echo      - No system dependencies
echo      - One-command setup
echo      - Best for production
echo.
echo   2) Native Setup (Windows)
echo      - Direct installation
echo      - Full development access
echo      - Manual dependency management
echo      - Best for development
echo.
echo Both options provide the same functionality!
echo.
set /p "choice=Enter your choice (1 or 2): "

if "%choice%"=="1" (
    call :docker_setup
) else if "%choice%"=="2" (
    call :native_setup
) else (
    call :print_error "Invalid choice. Please run the script again and select 1 or 2."
    exit /b 1
)
exit /b 0

REM Main execution
:main
call :show_banner

REM Handle command line arguments
if "%~1"=="" (
    call :show_menu
) else if "%~1"=="--help" (
    call :show_help
    exit /b 0
) else if "%~1"=="--docker" (
    call :docker_setup
) else if "%~1"=="--native" (
    call :native_setup
) else (
    call :print_error "Unknown option: %~1"
    echo Use --help for usage information
    exit /b 1
)

exit /b 0

REM Native setup main function
:native_setup
call :print_info "Starting native Windows setup..."

call :print_info "Checking system compatibility (Windows)..."
ver | findstr /i "Windows" >nul
if errorlevel 1 (
    call :print_error "This path is for Windows systems."
    exit /b 1
)
call :print_success "Running on Windows"

call :print_info "Installing Python 3.12 (Windows)..."
python --version 2>nul | findstr "3.12" >nul
if not errorlevel 1 (
    call :print_success "Python 3.12 is already installed"
) else (
    call :print_warning "Python 3.12 not found. Please install it manually from https://www.python.org/downloads/"
)

call :print_info "Installing PDM and UV package managers..."
where pdm >nul 2>nul
if not errorlevel 1 (
    call :print_success "PDM is already installed"
) else (
    call :print_info "Please install PDM manually with: pip install pdm"
)

where uv >nul 2>nul
if not errorlevel 1 (
    call :print_success "UV is already installed"
) else (
    call :print_info "Please install UV manually with: pip install uv"
)

call :print_info "Installing Node.js..."
where node >nul 2>nul
if not errorlevel 1 (
    call :print_success "Node.js is already installed"
    node --version
) else (
    call :print_warning "Node.js not found. Please install it manually from https://nodejs.org/"
)

call :print_success "Native Setup Complete!"
echo.
echo To run the servers:
echo.
echo 1. Start the backend server:
echo    Start a new Command Prompt window
echo    Navigate to the project directory
echo    Run: .venv\Scripts\activate.bat
echo    Run: python -m sentientresearchagent
echo.
echo 2. Start the frontend server:
echo    Start a new Command Prompt window
echo    Navigate to the frontend directory
echo    Run: npm run dev
echo.
echo Server URLs:
echo   - Backend API: http://localhost:5000
echo   - Frontend: http://localhost:3000
echo.
call :print_warning "Don't forget to update .env file with your API keys"
exit /b 0

REM Call main function with all arguments
call :main %*