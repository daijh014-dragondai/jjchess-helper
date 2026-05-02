@echo off
chcp 65001 >nul
title JJ象棋助手 - 推送代码到GitHub
color 0A

echo ========================================
echo   JJ象棋AI悬浮助手 - 推送代码到GitHub
echo ========================================
echo.
echo 【第1步】创建GitHub令牌
echo.
echo  1. 按任意键自动打开浏览器...
pause >nul
start https://github.com/settings/tokens
echo.
echo  2. 点 "Generate new token (classic)"
echo  3. 设置:
echo     - Note: jjchess-push
echo     - Expiration: No expiration
echo     - 勾选: repo, workflow
echo  4. 点 "Generate token"
echo  5. 复制生成的token (ghp_开头的)
echo.
echo ========================================
set /p TOKEN=粘贴Token后按回车: 

if "%TOKEN%"=="" (
    echo Token不能为空！
    pause
    exit /b
)

echo.
echo 【第2步】正在推送代码到GitHub...
echo.

cd /d "%~dp0"

:: 临时使用token推送（不保存到配置）
git push https://daijh014-dragondai:%TOKEN%@github.com/daijh014-dragondai/jjchess-helper.git main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   ✅ 推送成功！APK正在自动构建...
    echo.
    echo   查看进度（需要等30分钟）：
    echo   https://github.com/daijh014-dragondai/jjchess-helper/actions
    echo.
    echo   构建完成后，APK从这里下载：
    echo   https://github.com/daijh014-dragondai/jjchess-helper/actions
    echo   - 点击最新的绿色工作流
    echo   - 找到 JJChessHelper-APK 下载
    echo ========================================
) else (
    echo.
    echo ❌ 推送失败
    echo.
    echo 可能原因：
    echo 1. Token权限不够（需要勾选 repo 和 workflow）
    echo 2. Token已过期
    echo 3. 仓库名不一致
    echo.
    echo 请重试或在浏览器中访问：
    echo https://github.com/daijh014-dragondai/jjchess-helper
)

echo.
pause
