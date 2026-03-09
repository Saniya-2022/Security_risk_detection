@echo off
echo ========================================
echo Starting Mini SIEM Backend Server
echo ========================================
echo.
echo Make sure virtual environment is activated!
echo.
uvicorn backend.api.main_enhanced:app --reload --host 0.0.0.0 --port 8000
