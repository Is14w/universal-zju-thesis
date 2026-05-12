@echo off
chcp 65001 >nul
cd /d "%~dp0.."

echo ========================================
echo   Typst -> Word 转换
echo ========================================

echo [1/2] 编译 Typst -> HTML...
typst compile works/jlu-bachelor-thesis.typ works/thesis.html --format html --features html --root .
if %errorlevel% neq 0 (
    echo [错误] 编译失败
    pause
    exit /b 1
)
echo [完成] HTML 已生成

echo [2/2] Pandoc HTML -> Word...
pandoc works/thesis.html -o works/thesis.docx
if %errorlevel% neq 0 (
    echo [错误] 转换失败
    pause
    exit /b 1
)
echo [完成] Word 已生成

echo ========================================
echo   生成完毕: works\thesis.docx
echo ========================================
pause
