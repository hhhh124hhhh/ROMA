@echo off
chcp 65001 >nul
title Python 环境修复工具

echo.
echo ========================================
echo  Python 环境修复工具
echo ========================================
echo.

echo 🔧 诊断Python环境问题...

:: 检查Python版本
python --version
if errorlevel 1 (
    echo ❌ Python未安装或不在PATH中
    pause
    exit /b 1
)

echo.
echo 🧹 清理损坏的包...

:: 强制卸载可能损坏的包
echo 正在卸载损坏的pydantic包...
pip uninstall -y pydantic pydantic-core 2>nul

:: 清理pip缓存
echo 清理pip缓存...
pip cache purge

:: 升级pip和setuptools
echo 升级pip工具...
python -m pip install --upgrade pip setuptools wheel

:: 重新安装核心依赖
echo.
echo 📦 重新安装核心依赖...

echo 安装pydantic...
pip install --no-cache-dir --force-reinstall pydantic>=2.11.4
if errorlevel 1 (
    echo ❌ pydantic安装失败，尝试指定版本...
    pip install --no-cache-dir pydantic==2.10.0
)

echo 安装其他依赖...
pip install --no-cache-dir omegaconf>=2.3.0
pip install --no-cache-dir loguru>=0.7.3
pip install --no-cache-dir flask>=3.1.1
pip install --no-cache-dir flask-cors>=5.0.1
pip install --no-cache-dir flask-socketio>=5.5.1
pip install --no-cache-dir eventlet>=0.40.0
pip install --no-cache-dir litellm>=1.72.6

echo.
echo ✅ 环境修复完成！

:: 验证安装
echo.
echo 🔍 验证安装...
python -c "import pydantic; print(f'✅ pydantic {pydantic.__version__} 安装成功')" 2>nul
if errorlevel 1 (
    echo ❌ pydantic验证失败
) else (
    echo ✅ pydantic验证成功
)

python -c "import omegaconf; print('✅ omegaconf 安装成功')" 2>nul
if errorlevel 1 (
    echo ❌ omegaconf验证失败
) else (
    echo ✅ omegaconf验证成功
)

python -c "import flask; print('✅ flask 安装成功')" 2>nul
if errorlevel 1 (
    echo ❌ flask验证失败
) else (
    echo ✅ flask验证成功
)

python -c "import litellm; print('✅ litellm 安装成功')" 2>nul
if errorlevel 1 (
    echo ❌ litellm验证失败
) else (
    echo ✅ litellm验证成功
)

echo.
echo 🎉 修复完成！现在可以运行start_glm45.bat了
echo.
pause