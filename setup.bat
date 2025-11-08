@echo off
chcp 65001 >nul
echo ================================================
echo    Google Scholar + PubMed 检索工具安装脚本
echo ================================================
echo.

REM 检查conda是否安装
where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Conda未安装，请先安装Anaconda或Miniconda
    echo    下载地址：https://www.anaconda.com/download
    pause
    exit /b 1
)

echo ✓ 检测到Conda已安装
echo.

REM 检查环境是否已存在
conda env list | findstr "scholar_pubmed" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  环境scholar_pubmed已存在
    echo 是否删除并重新创建？[Y/N]
    set /p response=
    if /i "%response%"=="Y" (
        echo 🗑️  删除旧环境...
        call conda env remove -n scholar_pubmed -y
    ) else (
        echo ✓ 使用现有环境
        call conda activate scholar_pubmed
        echo 📥 更新依赖包...
        pip install --upgrade requests feedparser
        echo.
        echo ✅ 环境准备完成！
        echo.
        echo 使用方法：
        echo   conda activate scholar_pubmed
        echo   python combined_scraper.py
        pause
        exit /b 0
    )
)

echo 📦 创建conda环境 scholar_pubmed...
call conda create -n scholar_pubmed python=3.10 -y

echo.
echo 📥 安装Python依赖包...
call conda activate scholar_pubmed
pip install requests feedparser

echo.
echo ✅ 环境创建成功！
echo.
echo ================================================
echo    下一步操作：
echo ================================================
echo.
echo 1. 激活环境：
echo    conda activate scholar_pubmed
echo.
echo 2. 运行检索脚本：
echo    python combined_scraper.py
echo.
echo 3. 或合并已有CSV文件：
echo    python merge_results.py pubmed.csv scholar.csv
echo.
echo ================================================
echo.

REM 询问是否立即运行
echo 是否立即运行检索脚本？[Y/N]
set /p run_now=
if /i "%run_now%"=="Y" (
    echo.
    echo 🚀 开始检索...
    python combined_scraper.py
)

pause