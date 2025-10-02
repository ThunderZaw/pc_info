@echo off
title System Information Collector
color 0B

echo.
echo ====================================================================
echo                    SYSTEM INFORMATION COLLECTOR
echo ====================================================================
echo.
echo This tool will generate comprehensive hardware and software reports
echo for your computer. This may take a few moments...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Check and install required packages
echo Checking required packages...
echo.

python -c "import psutil" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing psutil...
    pip install psutil
)

python -c "import wmi" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing WMI...
    pip install WMI
)

echo.
echo Starting system scan...
echo.

REM Run the Python script
python system_info_collector.py

REM Check if reports were generated successfully
if %errorlevel% equ 0 (
    echo.
    echo Reports generated successfully!
    echo Opening reports folder...
    start "" "%~dp0Reports"
)

pause
