@echo off
title MediTriag Launcher

echo ==========================================
echo           MediTriag Launcher
echo ==========================================
echo.

:: -------------------------------------------------
:: Check virtual environment
:: -------------------------------------------------
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found.
    echo.
    echo Please create it first:
    echo.
    echo     python -m venv .venv
    echo.
    pause
    exit /b 1
)

echo [OK] Virtual environment found.

:: -------------------------------------------------
:: Activate venv
:: -------------------------------------------------
call .venv\Scripts\activate

:: -------------------------------------------------
:: Check required packages
:: -------------------------------------------------
echo Checking required packages...

python -c "import streamlit, fastapi, uvicorn, langchain, chromadb, google.genai" >nul 2>&1

if errorlevel 1 (
    echo.
    echo [ERROR] Some dependencies are missing.
    echo.
    echo Please run:
    echo.
    echo     pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo [OK] Dependencies verified.
echo.

:: -------------------------------------------------
:: Start Database & Apply Migrations
:: -------------------------------------------------
echo Starting PostgreSQL via Docker Compose...
docker-compose up -d

echo Waiting for database to be ready...
timeout /t 5 >nul

echo Applying database migrations...
call .venv\Scripts\alembic upgrade head

:: -------------------------------------------------
:: Start Backend
:: -------------------------------------------------
echo Starting FastAPI backend...
start "MediTriag Backend" cmd /k "call .venv\Scripts\activate && cd api && uvicorn api:app --reload --port 8000"

:: Give backend time to start
timeout /t 3 >nul

:: -------------------------------------------------
:: Start Streamlit
:: -------------------------------------------------
echo Starting Streamlit UI...
start "MediTriag UI" cmd /k "call .venv\Scripts\activate && streamlit run Ana_Sayfa.py"

echo.
echo ==========================================
echo MediTriag started successfully.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:8501
echo ==========================================
echo.

pause