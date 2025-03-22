@echo off
chcp 65001 > nul
title 骰子概率计算器打包工具

echo 骰子概率计算器打包工具
echo =============================
echo.

REM 检查Python是否安装
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：找不到Python。请安装Python 3.7或更高版本。
    echo 您可以从 https://www.python.org/downloads/ 下载Python。
    pause
    exit /b 1
)

REM 检查所需的Python库
echo 正在检查并安装所需的Python库...
python -m pip install --upgrade pip > nul
python -m pip install pyinstaller pillow > nul

echo.
echo 开始打包骰子概率计算器...
echo.

REM 运行打包脚本
python build.py

if %errorlevel% neq 0 (
    echo.
    echo 打包过程中出现错误。
    pause
    exit /b 1
)

echo.
echo 创建安装向导...
echo.

REM 运行安装程序生成脚本
python create_installer.py

echo.
echo.
echo 打包完成！您可以在dist文件夹中找到可执行文件。
echo.
echo 按任意键打开dist文件夹...
pause > nul

explorer dist
exit /b 0 