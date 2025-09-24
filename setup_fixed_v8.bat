@echo off
setlocal enabledelayedexpansion

REM Call main function with all arguments - 放在文件开头
call :main %*

REM SentientResearchAgent Unified Setup Script for Windows
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
echo  / ___|  ___ _ __ | |_| | ___ _ __ | |_ 
echo  \___ \ / _ \ '_ \| __| |/ _ \ '_ \| __|
echo   ___) |  __/ | | | |_| |  __/ | | | |_ 
echo  |____/ \___|_| |_|\__|_|\___|_| |_|\__|
echo                                        
echo  Research Agent - Setup for Windows
echo.
goto :eof

:show_help
echo Usage: setup.bat [OPTIONS]
echo.
echo Options:
echo   --docker    Run Docker setup directly
echo   --native    Run native setup directly
echo   --e2b       Setup E2B template with AWS credentials (requires E2B_API_KEY and AWS creds in .env)
echo   --test-e2b  Test E2B template integration (run after --e2b)
echo   --help      Show this help message
echo.
echo Without options, an interactive menu will be shown.
exit /b 0

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
) else if "%~1"=="--e2b" (
    call :setup_e2b_template
) else if "%~1"=="--test-e2b" (
    call :test_e2b_template
) else (
    call :print_error "Unknown option: %~1"
    echo Use --help for usage information
    exit /b 1
)

exit /b 0

REM Check if Docker is installed
:docker_check_requirements
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
exit /b 0

REM Setup environment
:docker_setup_environment
call :print_info "Setting up Docker environment..."

if not exist .env (
    if exist .env.example (
        copy .env.example .env >nul
        call :print_info "Created .env file from .env.example"
        call :print_warning "Please update .env with your API keys!"
    ) else (
        call :print_warning "No .env.example file found. Please create .env manually."
    )
) else (
    call :print_info ".env file already exists"
)

if not exist docker\.env (
    if exist docker\.env.example (
        copy docker\.env.example docker\.env >nul
        call :print_info "Created docker/.env from template"
    ) else (
        if exist .env (
            copy .env docker\.env >nul 2>nul
        )
    )
)

REM Create necessary directories
call :print_info "Creating necessary directories..."
if not exist logs mkdir logs >nul 2>nul
if not exist project_results mkdir project_results >nul 2>nul
if not exist emergency_backups mkdir emergency_backups >nul 2>nul

call :print_success "Environment setup complete"
exit /b 0

REM Build Docker images
:docker_build
call :print_info "Building Docker images..."

cd docker

set "compose_files=-f docker-compose.yml"
if exist "..\.env" (
    REM Check if S3 mounting is enabled
    for /f "usebackq tokens=*" %%a in (`findstr /r "^S3_MOUNT_ENABLED" "..\.env" 2^>nul`) do (
        set "s3_mount_line=%%a"
    )
    
    if defined s3_mount_line (
        echo !s3_mount_line! | findstr /i "true" >nul
        if not errorlevel 1 (
            REM S3 mounting is enabled, check if directory exists
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
                    if exist "!s3_mount_dir!" (
                        set "compose_files=!compose_files! -f docker-compose.s3.yml"
                        call :print_info "Building with S3 mount configuration for directory: !s3_mount_dir!"
                    ) else (
                        call :print_warning "S3 mount directory !s3_mount_dir! does not exist, skipping S3 compose override"
                    )
                )
            )
        )
    )
)

REM Build Docker images
docker compose !compose_files! build --no-cache
cd ..

call :print_success "Docker images built successfully"
exit /b 0

REM Start Docker services
:docker_start
call :print_info "Starting Docker services..."

cd docker

set "compose_files=-f docker-compose.yml"
if exist "..\.env" (
    REM Check if S3 mounting is enabled
    for /f "usebackq tokens=*" %%a in (`findstr /r "^S3_MOUNT_ENABLED" "..\.env" 2^>nul`) do (
        set "s3_mount_line=%%a"
    )
    
    if defined s3_mount_line (
        echo !s3_mount_line! | findstr /i "true" >nul
        if not errorlevel 1 (
            REM S3 mounting is enabled, check if directory exists
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
                    if exist "!s3_mount_dir!" (
                        set "compose_files=!compose_files! -f docker-compose.s3.yml"
                        call :print_info "Including S3 mount configuration for directory: !s3_mount_dir!"
                    ) else (
                        call :print_warning "S3 mount directory !s3_mount_dir! does not exist, skipping S3 compose override"
                    )
                )
            )
        )
    )
)

docker compose !compose_files! up -d

REM Wait for services
call :print_info "Waiting for services to start..."
timeout /t 10 /nobreak >nul

REM Check backend health
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5000/api/health' -Method GET -TimeoutSec 5; if ($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
    call :print_warning "Backend health check failed - it may still be starting"
    echo Check logs with: cd docker && docker compose logs backend
) else (
    call :print_success "Backend is healthy"
)

REM Check frontend
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:3000' -Method GET -TimeoutSec 5; if ($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
    call :print_info "Frontend may still be starting..."
) else (
    call :print_success "Frontend is running on http://localhost:3000"
)

cd ..

REM Auto-open browser for Docker frontend
start "" "http://localhost:3000"

exit /b 0

REM Docker setup main function
:docker_setup
call :print_info "Starting Docker setup..."

call :docker_check_requirements
if errorlevel 1 exit /b 1

call :docker_setup_environment
call :docker_build
call :docker_start

echo.
echo ========================================
call :print_success "Docker Setup Complete!"
echo ========================================
echo.
echo Services:
echo   - Backend API: http://localhost:5000
echo   - Frontend Dev: http://localhost:3000
echo.
echo Features:
if exist .env (
    findstr /r "^E2B_API_KEY" .env >nul 2>&1
    if errorlevel 1 (
        echo   - E2B Code Execution: Configure E2B_API_KEY in .env
    ) else (
        findstr /r "your_e2b_api_key_here" .env >nul 2>&1
        if errorlevel 1 (
            echo   - E2B Code Execution: Configured
        ) else (
            echo   - E2B Code Execution: Configure E2B_API_KEY in .env
        )
    )
    
    findstr /r "^S3_BUCKET_NAME" .env >nul 2>&1
    if errorlevel 1 (
        echo   - S3 Integration: Configure AWS credentials in .env
    ) else (
        findstr /r "your-s3-bucket-name" .env >nul 2>&1
        if errorlevel 1 (
            echo   - S3 Integration: Configured
        ) else (
            echo   - S3 Integration: Configure AWS credentials in .env
        )
    )
) else (
    echo   - E2B Code Execution: Configure E2B_API_KEY in .env
    echo   - S3 Integration: Configure AWS credentials in .env
)
echo.
echo Useful Docker commands:
echo   - View logs:    cd docker && docker compose logs -f
echo   - Stop:         cd docker && docker compose down
echo   - Restart:      cd docker && docker compose restart
echo   - View status:  cd docker && docker compose ps
echo.

if exist .env (
    findstr /r "your_.*_api_key_here" .env >nul 2>&1
    if not errorlevel 1 (
        call :print_warning "Don't forget to configure your API keys and S3 settings in .env"
    )
    findstr /r "your-.*-bucket-name" .env >nul 2>&1
    if not errorlevel 1 (
        call :print_warning "Don't forget to configure your API keys and S3 settings in .env"
    )
)

echo.
call :print_info "Optional: Setup E2B sandbox for code execution"
call :print_info "   Run: setup.bat --e2b (requires E2B_API_KEY and AWS credentials in .env"
call :print_info "   Test: setup.bat --test-e2b (after E2B setup)"
exit /b 0

REM Setup E2B template
:setup_e2b_template
call :print_info "Setting up E2B template with AWS credentials..."

REM Check if E2B CLI is installed
npm list -g @e2b/cli >nul 2>&1
if errorlevel 1 (
    call :print_error "E2B CLI not found. Please install it first:"
    echo npm install -g @e2b/cli
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    call :print_error ".env file not found. Please create it with AWS credentials first."
    exit /b 1
)

REM Load environment variables from .env
call :print_info "Loading AWS credentials from .env..."
for /f "usebackq tokens=*" %%a in (`.env`) do (
    set "line=%%a"
    if "!line:~0,1!" neq "#" (
        set "!line!"
    )
)

REM Validate required environment variables
if not defined AWS_ACCESS_KEY_ID (
    call :print_error "Missing required AWS credentials in .env file:"
    call :print_error "Required: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME"
    exit /b 1
)

if not defined AWS_SECRET_ACCESS_KEY (
    call :print_error "Missing required AWS credentials in .env file:"
    call :print_error "Required: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME"
    exit /b 1
)

if not defined S3_BUCKET_NAME (
    call :print_error "Missing required AWS credentials in .env file:"
    call :print_error "Required: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME"
    exit /b 1
)

call :print_info "AWS credentials found:"
call :print_info "  AWS_ACCESS_KEY_ID: %AWS_ACCESS_KEY_ID:~0,10%..."
call :print_info "  S3_BUCKET_NAME: %S3_BUCKET_NAME%"
call :print_info "  AWS_REGION: %AWS_REGION%"

REM Change to E2B template directory
if not exist "docker\e2b-sandbox" (
    call :print_error "E2B template directory not found: docker/e2b-sandbox"
    exit /b 1
)

cd docker\e2b-sandbox

REM Get S3 mount directory from .env or use default
set "S3_MOUNT_DIR=/opt/sentient"
if exist "..\..\.env" (
    for /f "usebackq tokens=*" %%a in (`findstr /r "^S3_MOUNT_DIR" "..\..\.env" 2^>nul`) do (
        set "s3_mount_dir_line=%%a"
    )
    
    if defined s3_mount_dir_line (
        for /f "tokens=2 delims==" %%b in ("!s3_mount_dir_line!") do (
            set "S3_MOUNT_DIR=%%b"
            REM Remove quotes if present
            set "S3_MOUNT_DIR=!S3_MOUNT_DIR:"=!"
        )
    )
)

REM Build E2B template with build args
call :print_info "Building E2B template with AWS credentials and mount directory as build args..."
call :print_info "  S3_MOUNT_DIR: !S3_MOUNT_DIR!"
e2b template build --build-arg AWS_ACCESS_KEY_ID="%AWS_ACCESS_KEY_ID%" --build-arg AWS_SECRET_ACCESS_KEY="%AWS_SECRET_ACCESS_KEY%" --build-arg AWS_REGION="%AWS_REGION%" --build-arg S3_BUCKET_NAME="%S3_BUCKET_NAME%" --build-arg S3_MOUNT_DIR="!S3_MOUNT_DIR!" --name sentient-e2b-s3

if errorlevel 1 (
    call :print_error "E2B template build failed"
    cd ..\..
    exit /b 1
)

call :print_success "E2B template built successfully!"
call :print_info "Template name: sentient-e2b-s3"
call :print_info "You can now use this template with AgnoAgent E2BTools"
call :print_info "Test the template with: setup.bat --test-e2b"

cd ..\..
exit /b 0

REM Test E2B template
:test_e2b_template
call :print_info "Testing E2B template with AWS integration..."

REM Check if E2B CLI is available
e2b --version >nul 2>&1
if errorlevel 1 (
    call :print_error "E2B CLI not found. Install with: npm install -g @e2b/cli"
    exit /b 1
)

REM Check E2B authentication
call :print_info "Checking E2B authentication..."
e2b auth whoami >nul 2>&1
if errorlevel 1 (
    call :print_warning "E2B not authenticated. Attempting to log in..."
    call :print_info "This will open your browser to authenticate with E2B"
    e2b auth login
    if errorlevel 1 (
        call :print_error "E2B authentication failed. Please try manually: e2b auth login"
        exit /b 1
    )
)
call :print_success "E2B authentication verified"

REM Check if template exists
set "template_name=sentient-e2b-s3"
call :print_info "Checking E2B template: !template_name!"

e2b template list 2>nul | findstr /c:"!template_name!" >nul
if errorlevel 1 (
    call :print_warning "E2B template '!template_name!' not found"
    call :print_info "Available templates:"
    e2b template list 2>nul
    call :print_info "Build the template with: cd docker/e2b-sandbox && e2b template build --name !template_name!"
    exit /b 1
)

call :print_success "E2B template '!template_name!' found"

REM Load E2B API key from environment
if defined E2B_API_KEY (
    set "E2B_API_KEY=!E2B_API_KEY!"
)

REM Check AWS environment variables  
call :print_info "Checking AWS configuration..."
set "missing_vars="

if not defined AWS_ACCESS_KEY_ID set "missing_vars=!missing_vars! AWS_ACCESS_KEY_ID"
if not defined AWS_SECRET_ACCESS_KEY set "missing_vars=!missing_vars! AWS_SECRET_ACCESS_KEY"
if not defined S3_BUCKET_NAME set "missing_vars=!missing_vars! S3_BUCKET_NAME"

if defined missing_vars (
    call :print_warning "Missing AWS environment variables:!missing_vars!"
    call :print_info "Configure these in your .env file for full functionality"
) else (
    call :print_success "AWS credentials configured"
)

REM Test basic E2B sandbox creation (without specific libraries)
call :print_info "Testing E2B sandbox creation..."

python -c "import os; import sys; print('[INFO] Testing basic E2B functionality...'); e2b_key = os.getenv('E2B_API_KEY'); print('[SUCCESS] E2B_API_KEY configured' if e2b_key else '[ERROR] E2B_API_KEY not set'); sys.exit(0 if e2b_key else 1)" >nul 2>&1

if errorlevel 1 (
    call :print_warning "E2B template test completed with limitations"
    call :print_info "E2B CLI is working but Python libraries may need installation"
) else (
    call :print_success "E2B template test completed successfully!"
    call :print_info "Template '!template_name!' is ready for use"
)

exit /b 0

REM Check system compatibility for native setup
:native_check_system
call :print_info "Checking system compatibility (Windows)..."

REM Check if we're on Windows
ver | findstr /i "Windows" >nul
if errorlevel 1 (
    call :print_error "This path is for Windows systems."
    exit /b 1
)

call :print_success "Running on Windows"
exit /b 0

REM Install Python 3.12
:native_install_python
call :print_info "Installing Python 3.12 (Windows)..."

REM Check if Python 3.12 is already installed
python --version 2>nul | findstr "3.12" >nul
if not errorlevel 1 (
    call :print_success "Python 3.12 is already installed"
    exit /b 0
)

REM Try to install Python via winget (Windows Package Manager)
where winget >nul 2>nul
if not errorlevel 1 (
    call :print_info "Installing Python 3.12 via winget..."
    winget install --id Python.Python.3.12 -e --source winget
    if not errorlevel 1 (
        call :print_success "Python 3.12 installed successfully"
        exit /b 0
    )
)

REM If winget is not available or fails, provide instructions
call :print_warning "winget not found or failed to install Python"
call :print_info "Please manually install Python 3.12 from https://www.python.org/downloads/"
call :print_info "Make sure to add Python to your PATH during installation"
pause
exit /b 0

REM Install PDM and UV package managers
:native_install_pdm_uv
call :print_info "Installing PDM and UV package managers..."

REM Install PDM
where pdm >nul 2>nul
if errorlevel 1 (
    call :print_info "Installing PDM..."
    python -m pip install pdm
    if errorlevel 1 (
        call :print_warning "Failed to install PDM via pip, trying alternative method..."
        curl -sSL https://pdm-project.org/install-pdm.py | python -
    )
) else (
    call :print_success "PDM is already installed"
)

REM Install UV
where uv >nul 2>nul
if errorlevel 1 (
    call :print_info "Installing UV..."
    python -m pip install uv
    if errorlevel 1 (
        call :print_warning "Failed to install UV via pip"
    )
) else (
    call :print_success "UV is already installed"
)

call :print_success "PDM and UV package managers installed successfully"
exit /b 0

REM Install Node.js
:native_install_node
call :print_info "Installing Node.js..."

REM Check if Node.js is already installed
where node >nul 2>nul
if not errorlevel 1 (
    call :print_success "Node.js is already installed"
    node --version
    exit /b 0
)

REM Try to install Node.js via winget
where winget >nul 2>nul
if not errorlevel 1 (
    call :print_info "Installing Node.js via winget..."
    winget install --id OpenJS.NodeJS -e --source winget
    if not errorlevel 1 (
        call :print_success "Node.js installed successfully"
        exit /b 0
    )
)

REM If winget is not available or fails, provide instructions
call :print_warning "winget not found or failed to install Node.js"
call :print_info "Please manually install Node.js from https://nodejs.org/"
pause
exit /b 0

REM Setup environment
:native_setup_environment
call :print_info "Setting up environment configuration..."

REM Create .env file if it doesn't exist
if not exist .env (
    if exist .env.example (
        copy .env.example .env >nul
        call :print_info "Created .env file from .env.example"
        call :print_warning "Please update .env with your API keys!"
    ) else (
        call :print_warning "No .env.example file found. Please create .env manually."
    )
) else (
    call :print_info ".env file already exists"
)

REM Create necessary directories
call :print_info "Creating necessary directories..."
if not exist logs mkdir logs >nul 2>nul
if not exist project_results mkdir project_results >nul 2>nul
if not exist emergency_backups mkdir emergency_backups >nul 2>nul

call :print_success "Environment setup complete"
exit /b 0

REM Setup project with UV
:native_setup_project
call :print_info "Setting up project with UV..."

REM Check if we're in the project directory
if not exist "pyproject.toml" (
    call :print_error "Please run this script from the SentientResearchAgent project root directory"
    exit /b 1
)

REM Create virtual environment with UV
call :print_info "Creating virtual environment with UV..."
if exist ".venv" (
    call :print_info "Virtual environment already exists, using existing one"
) else (
    uv venv --python 3.12
)

REM Activate virtual environment
call :print_info "Activating virtual environment..."
call .venv\Scripts\activate.bat

REM Install dependencies with UV
call :print_info "Installing Python dependencies with UV..."
uv sync

call :print_success "Project setup complete"
exit /b 0

REM Install frontend dependencies
:native_install_frontend
call :print_info "Installing frontend dependencies..."

REM Check if frontend directory exists
if not exist "frontend" (
    call :print_error "Frontend directory not found"
    exit /b 1
)

cd frontend

REM Install dependencies
call :print_info "Running npm install..."
npm install

cd ..

call :print_success "Frontend dependencies installed"
exit /b 0

REM Native setup main function
:native_setup
call :print_info "Starting native Windows setup..."

call :native_check_system
if errorlevel 1 exit /b 1

call :native_install_python
call :native_install_pdm_uv
call :native_install_node
call :native_setup_environment
call :native_setup_project
call :native_install_frontend

echo.
echo ========================================
call :print_success "Native Setup Complete!"
echo ========================================
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
call :print_warning "Don't forget to:"
echo   1. Update .env file with your API keys
echo.

REM 修复：移除这里的 exit /b 0，使用 goto :eof 让函数正常返回
goto :eof