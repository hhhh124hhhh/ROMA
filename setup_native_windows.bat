@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ========================================
echo  SentientResearchAgent Windows Native Setup
echo ========================================
echo.

REM Check if we're in the project root directory
if not exist "pyproject.toml" (
    echo [ERROR] 请从项目根目录运行此脚本
    echo 当前目录: %CD%
    pause
    exit /b 1
)

echo [INFO] 检查系统环境...

REM 1. 检查 Python
echo [INFO] 检查 Python 安装...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 未安装或不在 PATH 中
    echo 请安装 Python 3.11+ 或 3.12: https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [INFO] 发现 Python !PYTHON_VERSION!
)

REM 检查 Python 版本是否符合要求 (3.11+)
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)
if !MAJOR! LSS 3 (
    echo [ERROR] Python 版本过低，需要 3.11 或更高版本
    pause
    exit /b 1
)
if !MAJOR! EQU 3 if !MINOR! LSS 11 (
    echo [ERROR] Python 版本过低，需要 3.11 或更高版本
    pause
    exit /b 1
)

REM 2. 检查 Node.js
echo [INFO] 检查 Node.js 安装...
node --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Node.js 未安装，正在尝试安装...
    where winget >nul 2>&1
    if not errorlevel 1 (
        echo [INFO] 通过 winget 安装 Node.js...
        winget install --id OpenJS.NodeJS -e --source winget
        if errorlevel 1 (
            echo [ERROR] winget 安装失败，请手动安装 Node.js
            echo 下载地址: https://nodejs.org/
            pause
            exit /b 1
        )
    ) else (
        echo [ERROR] Node.js 未安装且无法自动安装
        echo 请手动安装: https://nodejs.org/
        pause
        exit /b 1
    )
) else (
    for /f "tokens=1" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
    for /f "tokens=1" %%i in ('npm --version 2^>^&1') do set NPM_VERSION=%%i
    echo [INFO] 发现 Node.js !NODE_VERSION!
    echo [INFO] 发现 npm !NPM_VERSION!
)

echo.
echo [INFO] 开始环境设置...

REM 3. 创建 .env 文件
if not exist ".env" (
    if exist ".env.example" (
        echo [INFO] 从 .env.example 创建 .env 文件...
        copy .env.example .env >nul
        echo [WARNING] 请编辑 .env 文件配置你的 API 密钥！
    ) else (
        echo [WARNING] 未找到 .env.example 文件，请手动创建 .env 文件
    )
) else (
    echo [INFO] .env 文件已存在
)

REM 4. 创建必要目录
echo [INFO] 创建必要目录...
if not exist "logs" mkdir logs
if not exist "project_results" mkdir project_results
if not exist "emergency_backups" mkdir emergency_backups

REM 5. 升级 pip 和安装包管理工具
echo [INFO] 升级 pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [WARNING] pip 升级失败，继续安装过程...
)

echo [INFO] 尝试安装 uv 包管理工具...
python -m pip install uv
if errorlevel 1 (
    echo [WARNING] uv 安装失败，将使用 pip 作为备选方案
    set USE_UV=false
) else (
    echo [INFO] uv 安装成功
    set USE_UV=true
)

REM 6. 创建虚拟环境
echo [INFO] 创建 Python 虚拟环境...
if exist ".venv" (
    echo [INFO] 虚拟环境已存在，跳过创建
) else (
    if "!USE_UV!"=="true" (
        echo [INFO] 使用 uv 创建虚拟环境...
        uv venv
        if errorlevel 1 (
            echo [WARNING] uv 创建虚拟环境失败，尝试使用 python -m venv...
            python -m venv .venv
            if errorlevel 1 (
                echo [ERROR] 虚拟环境创建失败
                pause
                exit /b 1
            )
        )
    ) else (
        echo [INFO] 使用 python -m venv 创建虚拟环境...
        python -m venv .venv
        if errorlevel 1 (
            echo [ERROR] 虚拟环境创建失败
            pause
            exit /b 1
        )
    )
)

REM 7. 激活虚拟环境并安装依赖
echo [INFO] 激活虚拟环境...
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] 虚拟环境激活脚本不存在
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] 无法激活虚拟环境
    pause
    exit /b 1
)

REM 检查是否在虚拟环境中
echo [INFO] 验证虚拟环境...
python -c "import sys; print('虚拟环境路径:', sys.executable)" 2>nul
if errorlevel 1 (
    echo [ERROR] Python 在虚拟环境中无法正常运行
    pause
    exit /b 1
)

REM 安装 Python 依赖
echo [INFO] 安装 Python 依赖包...
if "!USE_UV!"=="true" (
    echo [INFO] 使用 uv 同步依赖...
    uv sync
    if errorlevel 1 (
        echo [WARNING] uv sync 失败，尝试使用 pip 安装...
        echo [INFO] 从 pyproject.toml 安装依赖...
        pip install -e .
        if errorlevel 1 (
            echo [ERROR] 依赖安装失败
            pause
            exit /b 1
        )
    )
) else (
    echo [INFO] 使用 pip 安装依赖...
    pip install -e .
    if errorlevel 1 (
        echo [ERROR] 依赖安装失败
        pause
        exit /b 1
    )
)

REM 8. 安装前端依赖
echo [INFO] 安装前端依赖...
if not exist "frontend\package.json" (
    echo [ERROR] 找不到前端项目文件 frontend\package.json
    pause
    exit /b 1
)

cd frontend
echo [INFO] 清理 npm 缓存...
npm cache clean --force 2>nul

echo [INFO] 运行 npm install...
npm install
if errorlevel 1 (
    echo [ERROR] 前端依赖安装失败，尝试删除 node_modules 重新安装...
    if exist "node_modules" rmdir /s /q node_modules
    if exist "package-lock.json" del package-lock.json
    npm install
    if errorlevel 1 (
        echo [ERROR] 前端依赖安装失败
        cd ..
        pause
        exit /b 1
    )
)
cd ..

REM 9. 验证安装
echo [INFO] 验证安装结果...
echo [INFO] 检查 Python 包安装...
python -c "import sentientresearchagent; print('✓ SentientResearchAgent 包可用')" 2>nul
if errorlevel 1 (
    echo [WARNING] SentientResearchAgent 包导入失败，可能需要手动修复
) else (
    echo [SUCCESS] Python 包安装验证成功
)

echo.
echo ========================================
echo [SUCCESS] 环境设置完成！
echo ========================================
echo.
echo 现在你可以启动服务：
echo.
echo 1. 启动后端服务（在新的命令提示符窗口中）：
echo    cd %CD%
echo    .venv\Scripts\activate.bat
echo    python -m sentientresearchagent
echo.
echo 2. 启动前端服务（在另一个新的命令提示符窗口中）：
echo    cd %CD%\frontend
echo    npm run dev
echo.
echo 服务地址：
echo   - 前端: http://localhost:3000
echo   - 后端 API: http://localhost:5000
echo.
echo [WARNING] 请记得在 .env 文件中配置你的 API 密钥！
echo [INFO] 可以编辑 .env 文件或运行: copy .env.example .env
echo.

REM 询问是否自动启动服务
set /p "start_services=是否现在启动服务？(y/n): "
if /i "%start_services%"=="y" (
    echo [INFO] 启动服务...
    
    REM 检查 .env 文件
    if not exist ".env" (
        echo [WARNING] .env 文件不存在，服务可能无法正常工作
        set /p "create_env=是否现在创建 .env 文件？(y/n): "
        if /i "!create_env!"=="y" (
            if exist ".env.example" (
                copy .env.example .env >nul
                echo [INFO] .env 文件已创建，请编辑配置你的 API 密钥
            ) else (
                echo [ERROR] .env.example 文件不存在
            )
        )
    )
    
    REM 启动后端服务（在新窗口中）
    echo [INFO] 启动后端服务...
    start "SentientAgent-Backend" cmd /k "cd /d %CD% && .venv\Scripts\activate.bat && echo [INFO] 后端服务启动中... && python -m sentientresearchagent"
    
    REM 等待几秒让后端启动
    echo [INFO] 等待后端服务启动...
    timeout /t 8 /nobreak >nul
    
    REM 启动前端服务（在新窗口中）
    echo [INFO] 启动前端服务...
    start "SentientAgent-Frontend" cmd /k "cd /d %CD%\frontend && echo [INFO] 前端服务启动中... && npm run dev"
    
    REM 等待几秒让前端启动
    echo [INFO] 等待前端服务启动...
    timeout /t 12 /nobreak >nul
    
    REM 打开浏览器
    echo [INFO] 正在打开浏览器...
    start "" "http://localhost:3000"
    
    echo [SUCCESS] 服务已启动！
    echo [INFO] 如果浏览器没有自动打开，请手动访问: http://localhost:3000
) else (
    echo [INFO] 手动启动服务时请参考上面的说明
    echo [INFO] 别忘了先配置 .env 文件中的 API 密钥！
)

echo.
pause