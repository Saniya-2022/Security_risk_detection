@echo off
echo ========================================
echo   Mini SIEM - ENTERPRISE EDITION
echo ========================================
echo.
echo Stopping any running Python processes...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting Enterprise SIEM Backend...
echo.
echo Features Enabled:
echo  - Event Correlation Engine
echo  - Threat Intelligence Enrichment
echo  - Anomaly Detection
echo  - MITRE ATT^&CK Mapping
echo  - Advanced Risk Scoring
echo  - Incident Management
echo  - Auto IP Blocking
echo  - Email Alerts
echo.
cd /d "%~dp0"
call venv\Scripts\activate.bat
uvicorn backend.api.main_enterprise:app --reload --host 0.0.0.0 --port 8000
