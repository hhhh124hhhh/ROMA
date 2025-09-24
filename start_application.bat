@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ========================================
echo  🎉 SentientResearchAgent 安装完成验证
echo ========================================
echo.

REM 激活虚拟环境
call .venv\Scripts\activate.bat

echo [INFO] 验证Python后端...
python -c "import sentientresearchagent; print('✅ 后端包导入成功')" 2>nul
if errorlevel 1 (
    echo ❌ 后端包导入失败
    exit /b 1
) else (
    echo ✅ 后端包导入成功
)

echo.
echo [INFO] 验证前端依赖...
if exist "frontend\node_modules" (
    echo ✅ 前端依赖已安装
) else (
    echo ❌ 前端依赖未安装
)

echo.
echo [INFO] 验证配置文件...
if exist ".env" (
    echo ✅ .env 配置文件存在
) else (
    echo ❌ .env 配置文件不存在
)

echo.
echo ========================================
echo  🚀 启动说明
echo ========================================
echo.
echo 1. 启动后端服务：
echo    .venv\Scripts\activate.bat
echo    python -m sentientresearchagent
echo.
echo 2. 启动前端服务（新的命令提示符窗口）：
echo    cd frontend
echo    npm run dev
echo.
echo 3. 访问地址：
echo    前端: http://localhost:3000
echo    后端: http://localhost:5000
echo.
echo ⚠️  重要提示：
echo    请在 .env 文件中配置你的 API 密钥！
echo    编辑 .env 文件添加：
echo    - OPENROUTER_API_KEY=your_key_here
echo    - 或其他所需的 API 密钥
echo.

set /p "start_now=是否现在启动服务？(y/n): "
if /i "%start_now%"=="y" (
    echo.
    echo [INFO] 启动后端服务...
    start "SentientAgent-Backend" cmd /k "cd /d %CD% && .venv\Scripts\activate.bat && python -m sentientresearchagent"
    
    timeout /t 5 /nobreak >nul
    
    echo [INFO] 启动前端服务...
    start "SentientAgent-Frontend" cmd /k "cd /d %CD%\frontend && npm run dev"
    
    timeout /t 8 /nobreak >nul
    
    echo [INFO] 打开浏览器...
    start "" "http://localhost:3000"
    
    echo.
    echo ✅ 服务已启动！
    echo    后端服务运行在端口 5000
    echo    前端服务运行在端口 3000
    echo    浏览器应该会自动打开
)

echo.
pause