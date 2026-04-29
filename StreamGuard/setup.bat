@echo off
REM StreamGuard Setup Script for Windows
REM This script sets up the project for development on Windows

echo ============================================
echo StreamGuard Setup - Windows
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    exit /b 1
)

echo [OK] Python found
python --version

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    exit /b 1
)

echo [OK] pip found

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo.
    echo Creating virtual environment...
    python -m venv .venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo WARNING: requirements.txt not found in StreamGuard directory
    echo Please ensure you're running this script from the StreamGuard directory
)

REM Create .env if it doesn't exist
if not exist "backend\.env" (
    echo.
    echo Creating .env file from template...
    copy backend\.env.example backend\.env
    echo [OK] Created backend\.env
)

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo To start the development server:
echo   1. Run: .venv\Scripts\activate.bat
echo   2. Run: cd backend
echo   3. Run: python app.py
echo.
echo The API will be available at: http://localhost:5000
echo.
echo To run tests:
echo   cd backend
echo   python test_app.py
echo.
