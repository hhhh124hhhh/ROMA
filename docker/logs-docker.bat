@echo off
setlocal enabledelayedexpansion

REM SentientResearchAgent Docker Logs Script for Windows

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

REM Get script directory
set "SCRIPT_DIR=%~dp0"
REM Remove trailing backslash
if "!SCRIPT_DIR:~-1!"=="\" set "SCRIPT_DIR=!SCRIPT_DIR:~0,-1!"

cd /d "!SCRIPT_DIR!"

REM Check if Docker is installed
call :print_info "Checking Docker requirements..."

docker --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Docker is not installed"
    echo Please install Docker Desktop: https://docs.docker.com/docker-for-windows/install/
    exit /b 1
)

docker compose version >nul 2>&1
if errorlevel 1 (
    call :print_error "Docker Compose is not installed"
    echo Please install Docker Desktop which includes Docker Compose
    exit /b 1
)

call :print_success "Docker and Docker Compose found"

REM Determine compose files to use
set "compose_files=-f docker-compose.yml"

REM Check if .env file exists in parent directory
if exist "..\.env" (
    call :print_info "Checking for S3 mounting configuration..."
    
    REM Check if S3 mounting is enabled
    for /f "usebackq tokens=*" %%a in (`findstr /r "^S3_MOUNT_ENABLED" "..\.env" 2^>nul`) do (
        set "s3_mount_line=%%a"
    )
    
    if defined s3_mount_line (
        echo !s3_mount_line! | findstr /i "true" >nul
        if not errorlevel 1 (
            call :print_info "S3 mounting is enabled"
            
            REM Get S3 mount directory
            for /f "usebackq tokens=*" %%a in (`findstr /r "^S3_MOUNT_DIR" "..\.env" 2^>nul`) do (
                set "s3_mount_dir_line=%%a"
            )
            
            if defined s3_mount_dir_line (
                for /f "tokens=2 delims==" %%b in ("!s3_mount_dir_line!") do (
                    set "s3_mount_dir=%%b"
                    REM Remove quotes if present
                    set "s3_mount_dir=!s3_mount_dir:"=!"
                )
                
                if defined s3_mount_dir (
                    call :print_info "S3 mount directory: !s3_mount_dir!"
                    
                    REM Check if directory exists
                    if exist "!s3_mount_dir!" (
                        set "compose_files=!compose_files! -f docker-compose.s3.yml"
                        call :print_info "Including S3 mount configuration"
                    ) else (
                        call :print_warning "S3 mount directory !s3_mount_dir! does not exist"
                        call :print_warning "Using base compose configuration only"
                    )
                ) else (
                    call :print_warning "S3_MOUNT_DIR not properly configured in .env"
                )
            ) else (
                call :print_warning "S3_MOUNT_DIR not found in .env"
            )
        ) else (
            call :print_info "S3 mounting is disabled"
        )
    ) else (
        call :print_info "S3 mounting not configured in .env"
    )
) else (
    call :print_warning "No .env file found in parent directory"
)

REM Show Docker logs
call :print_info "Showing Docker logs with command:"
call :print_info "docker compose !compose_files! logs -f"
echo.
echo Press Ctrl+C to stop viewing logs
echo.
docker compose !compose_files! logs -f

if errorlevel 1 (
    call :print_error "Failed to show Docker logs"
    exit /b 1
)

exit /b 0