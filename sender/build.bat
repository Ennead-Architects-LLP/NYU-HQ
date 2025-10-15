@echo off
REM Build script for send_report.exe with embedded configuration

echo ============================================================
echo Building send_report.exe with embedded configuration
echo ============================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if config.json exists
if not exist "config.json" (
    echo [ERROR] config.json not found
    echo Please create config.json with your GitHub token first
    pause
    exit /b 1
)

echo.
echo [1/4] Installing PyInstaller...
pip install pyinstaller --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller
    pause
    exit /b 1
)

echo [2/4] Creating build version with embedded config...
python create_build_version.py
if errorlevel 1 (
    echo [ERROR] Failed to create build version
    pause
    exit /b 1
)

echo [3/4] Compiling to executable...
python -m PyInstaller --onefile --name send_report --console --clean send_report_build.py
if errorlevel 1 (
    echo [ERROR] Failed to compile
    pause
    exit /b 1
)

echo [4/4] Cleaning up...
del send_report_build.py >nul 2>&1
rmdir /s /q build >nul 2>&1
del send_report.spec >nul 2>&1

echo [5/5] Deploying to ExeProducts...
set TARGET_DIR=C:\Users\%USERNAME%\github\EnneadTab-OS\Apps\lib\ExeProducts
set TARGET_FILE=%TARGET_DIR%\NYU_HQ.exe

if not exist "%TARGET_DIR%" (
    echo [ERROR] Target directory not found: %TARGET_DIR%
    echo Please check the path and try again.
    pause
    exit /b 1
)

copy /Y dist\send_report.exe "%TARGET_FILE%" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to copy executable to target directory
    pause
    exit /b 1
)

echo.
echo ============================================================
echo SUCCESS! Executable created and deployed
echo ============================================================
echo.
echo Local copy: dist\send_report.exe
echo Deployed to: %TARGET_FILE%
echo.
echo The .exe is ready for distribution!
echo.
pause

