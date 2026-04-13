@echo off
echo ========================================
echo 安装 matplotlib 和 seaborn
echo ========================================
echo.

REM 使用系统 pip 安装到虚拟环境
echo 正在安装 matplotlib...
py -m pip install matplotlib --target E:\Project\论文\.venv\Lib\site-packages

echo.
echo 正在安装 seaborn...
py -m pip install seaborn --target E:\Project\论文\.venv\Lib\site-packages

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 现在可以运行：
echo   E:\Project\论文\.venv\Scripts\python.exe E:\Project\论文\workspace\generate_figures_simple.py
echo.
pause
