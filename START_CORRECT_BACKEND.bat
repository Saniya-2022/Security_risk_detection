@echo off
echo ========================================
echo   Starting DYNAMIC Mini SIEM Backend
echo ========================================
echo.
echo Stopping any running Python processes...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting the CORRECT backend (main_dynamic.py)...
echo.
cd /d "%~dp0"
call venv\Scripts\activate.bat
uvicorn backend.api.main_dynamic:app --reload --host 0.0.0.0 --port 8000
