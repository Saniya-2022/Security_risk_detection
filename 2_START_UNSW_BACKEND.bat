@echo off
echo ========================================
echo   Starting UNSW-NB15 Backend
echo ========================================
echo.
echo Starting real-time intrusion detection...
echo.
cd /d "%~dp0"
call venv\Scripts\activate.bat
uvicorn backend.api.main_unsw:app --reload --host 0.0.0.0 --port 8000
