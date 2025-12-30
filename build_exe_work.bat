@echo off
:: 设置编码为 UTF-8
chcp 65001 >nul

:: 强制切换到脚本所在的实际目录，确保能找到 SourceCodeBinder.py
cd /d "%~dp0"

echo ============================================
echo   SourceCodeBinder 自动化打包程序 (GUI模式)
echo ============================================

:: 检查主文件是否存在
if not exist "SourceCodeBinder.py" (
    echo [错误] 找不到主程序文件 SourceCodeBinder.py！
    echo 请确认当前目录下存在该文件。
    pause
    exit
)

:: 执行 PyInstaller
python -m PyInstaller --noconfirm --onefile --windowed ^
--name="SourceCodeBinder" ^
--collect-all "customtkinter" ^
--icon="C:\Users\EJI1WX\OneDrive - Bosch Group\PythonProject\SourceCodeBinder\resources\SourceCodeBinder.ico" ^
--add-data "function;function" ^
--add-data "gui;gui" ^
--add-data "C:\Users\EJI1WX\OneDrive - Bosch Group\PythonProject\SourceCodeBinder\resources\SourceCodeBinder.ico;." ^
--hidden-import="customtkinter" ^
--hidden-import="markdown2" ^
--hidden-import="pdfkit" ^
--distpath="C:/Users/EJI1WX/OneDrive - Bosch Group/Program" ^
--workpath="C:/Temp_Build" ^
--clean SourceCodeBinder.py

echo.
echo --------------------------------------------
echo 打包执行完毕！EXE 文件名：SourceCodeBinder.exe
echo 输出目录: C:/Users/EJI1WX/OneDrive - Bosch Group/Program
echo --------------------------------------------
pause