@echo off
echo ========================================
echo   Geo3D Backend Server
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8+
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

echo [2/3] Checking dependencies...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo WARNING: FastAPI not installed!
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
)
echo Dependencies OK
echo.

echo [3/3] Starting server...
echo.
echo Server will start at: http://127.0.0.1:8000
echo Frontend available at: http://127.0.0.1:8000/fe/pages/index.html
echo API docs at: http://127.0.0.1:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python -m uvicorn main:app --reload --port 8000

pause
