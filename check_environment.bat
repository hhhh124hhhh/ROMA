@echo off
echo ========================================
echo  SentientResearchAgent 环境检查
echo ========================================
echo.

set "errors=0"

echo [INFO] 检查项目结构...
if exist "pyproject.toml" (
    echo ✓ pyproject.toml 存在
) else (
    echo ✗ pyproject.toml 不存在 - 请确保在项目根目录运行
    set /a errors+=1
)

if exist "frontend" (
    echo ✓ frontend 目录存在
) else (
    echo ✗ frontend 目录不存在
    set /a errors+=1
)

echo.
echo [INFO] 检查系统依赖...

python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python 未安装或不在 PATH 中
    set /a errors+=1
) else (
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do echo ✓ Python %%v
)

node --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Node.js 未安装或不在 PATH 中
    set /a errors+=1
) else (
    for /f "tokens=1" %%v in ('node --version 2^>^&1') do echo ✓ Node.js %%v
)

npm --version >nul 2>&1
if errorlevel 1 (
    echo ✗ npm 未安装或不在 PATH 中
    set /a errors+=1
) else (
    for /f "tokens=1" %%v in ('npm --version 2^>^&1') do echo ✓ npm %%v
)

echo.
echo [INFO] 检查项目环境...

if exist ".venv" (
    echo ✓ Python 虚拟环境已创建
) else (
    echo ✗ Python 虚拟环境未创建
    set /a errors+=1
)

if exist "frontend\node_modules" (
    echo ✓ 前端依赖已安装
) else (
    echo ✗ 前端依赖未安装
    set /a errors+=1
)

if exist ".env" (
    echo ✓ .env 配置文件存在
) else (
    echo ✗ .env 配置文件不存在
    set /a errors+=1
)

echo.
echo [INFO] 检查必要目录...
if exist "logs" (
    echo ✓ logs 目录存在
) else (
    echo ✗ logs 目录不存在
    set /a errors+=1
)

if exist "project_results" (
    echo ✓ project_results 目录存在
) else (
    echo ✗ project_results 目录不存在
    set /a errors+=1
)

echo.
echo ========================================
if %errors%==0 (
    echo [SUCCESS] 环境检查通过！所有依赖都已就绪。
    echo.
    echo 你可以运行以下命令启动服务：
    echo   - 管理服务: manage_services.bat
    echo   - 仅后端: start_backend.bat
    echo   - 仅前端: start_frontend.bat
) else (
    echo [ERROR] 发现 %errors% 个问题需要解决
    echo.
    echo 建议运行: setup_native_windows.bat 来设置环境
)
echo ========================================

pause