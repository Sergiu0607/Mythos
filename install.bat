@echo off
REM Mythos Installation Script for Windows

echo =========================================
echo   Mythos Programming Language Installer
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed.
    echo Please install Python 3.8 or higher from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [OK] Found Python
python --version

REM Install dependencies
echo.
echo Installing dependencies...
pip install numpy --quiet

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed

REM Install Mythos
echo.
echo Installing Mythos...
pip install -e .

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Mythos
    pause
    exit /b 1
)

echo [OK] Mythos installed successfully!

REM Verify installation
echo.
echo Verifying installation...
mythos --version >nul 2>&1

if %errorlevel% neq 0 (
    echo [WARNING] 'mythos' command not found in PATH
    echo.
    echo You can still run Mythos using:
    echo   python mythos_cli\cli.py
    echo.
    echo To add to PATH, add this directory to your system PATH:
    echo   %APPDATA%\Python\Python3X\Scripts
) else (
    echo [OK] Mythos command is available
    mythos --version
)

echo.
echo =========================================
echo   Installation Complete! 🎉
echo =========================================
echo.
echo Try these commands:
echo   mythos run examples\hello_world.mythos
echo   mythos repl
echo   mythos --help
echo.
echo For more information, see QUICKSTART.md
echo.
pause
