@echo off
echo ========================================
echo Starting Mini SIEM DYNAMIC System
echo ========================================
echo.
echo This will start the LIVE event-driven SIEM
echo Events will be generated automatically every 3-7 seconds
echo.
echo Make sure virtual environment is activated!
echo.
pause
echo.
echo Starting backend with continuous event generation...
uvicorn backend.api.main_dynamic:app --reload --host 0.0.0.0 --port 8000
