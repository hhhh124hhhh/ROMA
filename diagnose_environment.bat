@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ========================================
echo  SentientResearchAgent 环境诊断工具
echo ========================================
echo.

echo [INFO] 系统信息诊断...
echo 操作系统: %OS%
echo 处理器架构: %PROCESSOR_ARCHITECTURE%
echo 当前目录: %CD%
echo 用户名: %USERNAME%
echo.

echo [INFO] 检查项目文件结构...
if exist "pyproject.toml" (
    echo ✓ pyproject.toml 存在
) else (
    echo ✗ pyproject.toml 不存在
)

if exist ".env.example" (
    echo ✓ .env.example 存在
) else (
    echo ✗ .env.example 不存在
)

if exist ".env" (
    echo ✓ .env 文件存在
) else (
    echo ✗ .env 文件不存在（正常，首次安装时）
)

if exist "frontend\package.json" (
    echo ✓ frontend\package.json 存在
) else (
    echo ✗ frontend\package.json 不存在
)

if exist "src\sentientresearchagent" (
    echo ✓ src\sentientresearchagent 目录存在
) else (
    echo ✗ src\sentientresearchagent 目录不存在
)

echo.
echo [INFO] Python 环境检查...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python 未安装或不在 PATH 中
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do (
        set PYTHON_VERSION=%%i
        echo ✓ Python 版本: %%i
    )
    
    REM 检查 Python 版本是否符合要求
    for /f "tokens=1,2 delims=." %%a in ("!PYTHON_VERSION!") do (
        set MAJOR=%%a
        set MINOR=%%b
    )
    
    if !MAJOR! LSS 3 (
        echo ✗ Python 版本过低，需要 3.11+
    ) else if !MAJOR! EQU 3 if !MINOR! LSS 11 (
        echo ✗ Python 版本过低，需要 3.11+
    ) else (
        echo ✓ Python 版本符合要求
    )
    
    REM 检查 pip
    python -m pip --version >nul 2>&1
    if errorlevel 1 (
        echo ✗ pip 不可用
    ) else (
        echo ✓ pip 可用
    )
)

echo.
echo [INFO] Node.js 环境检查...
node --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Node.js 未安装或不在 PATH 中
) else (
    for /f "tokens=1" %%i in ('node --version 2^>^&1') do (
        set NODE_VERSION=%%i
        echo ✓ Node.js 版本: %%i
    )
    
    npm --version >nul 2>&1
    if errorlevel 1 (
        echo ✗ npm 不可用
    ) else (
        for /f "tokens=1" %%i in ('npm --version 2^>^&1') do (
            set NPM_VERSION=%%i
            echo ✓ npm 版本: %%i
        )
    )
)

echo.
echo [INFO] 网络连接检查...
ping -n 1 pypi.org >nul 2>&1
if errorlevel 1 (
    echo ✗ 无法连接到 pypi.org (Python 包仓库)
) else (
    echo ✓ 可以连接到 pypi.org
)

ping -n 1 registry.npmjs.org >nul 2>&1
if errorlevel 1 (
    echo ✗ 无法连接到 registry.npmjs.org (npm 包仓库)
) else (
    echo ✓ 可以连接到 registry.npmjs.org
)

echo.
echo [INFO] 现有虚拟环境检查...
if exist ".venv" (
    echo ✓ .venv 目录存在
    if exist ".venv\Scripts\activate.bat" (
        echo ✓ 虚拟环境激活脚本存在
        
        REM 尝试激活虚拟环境并检查
        call .venv\Scripts\activate.bat >nul 2>&1
        if errorlevel 1 (
            echo ✗ 虚拟环境激活失败
        ) else (
            echo ✓ 虚拟环境可以激活
            
            REM 检查虚拟环境中的 Python
            python -c "import sys; print('✓ 虚拟环境 Python 路径:', sys.executable)" 2>nul
            if errorlevel 1 (
                echo ✗ 虚拟环境中的 Python 不可用
            )
            
            REM 尝试导入主包
            python -c "import sentientresearchagent" >nul 2>&1
            if errorlevel 1 (
                echo ✗ sentientresearchagent 包未安装或无法导入
            ) else (
                echo ✓ sentientresearchagent 包可以导入
            )
        )
    ) else (
        echo ✗ 虚拟环境激活脚本不存在
    )
) else (
    echo - .venv 目录不存在（正常，首次安装时）
)

echo.
echo [INFO] 前端环境检查...
if exist "frontend\node_modules" (
    echo ✓ frontend\node_modules 存在
) else (
    echo - frontend\node_modules 不存在（正常，首次安装时）
)

if exist "frontend\package-lock.json" (
    echo ✓ frontend\package-lock.json 存在
) else (
    echo - frontend\package-lock.json 不存在
)

echo.
echo [INFO] 权限检查...
echo 测试文件写入权限... > test_write_permission.tmp 2>nul
if exist "test_write_permission.tmp" (
    del test_write_permission.tmp >nul 2>&1
    echo ✓ 当前目录可写
) else (
    echo ✗ 当前目录不可写，可能存在权限问题
)

echo.
echo [INFO] 端口检查...
netstat -an | findstr ":5000" >nul 2>&1
if not errorlevel 1 (
    echo ⚠ 端口 5000 已被占用（可能影响后端服务）
) else (
    echo ✓ 端口 5000 可用
)

netstat -an | findstr ":3000" >nul 2>&1
if not errorlevel 1 (
    echo ⚠ 端口 3000 已被占用（可能影响前端服务）
) else (
    echo ✓ 端口 3000 可用
)

echo.
echo ========================================
echo  诊断完成
echo ========================================
echo.
echo 如果发现问题，请根据上述信息进行修复，或将此诊断结果提供给技术支持。
echo.
pause