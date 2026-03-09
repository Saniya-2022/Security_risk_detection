@echo off
echo ========================================
echo   UNSW-NB15 System Setup
echo ========================================
echo.
echo This will:
echo 1. Install all dependencies
echo 2. Train ML models (may take 10-15 minutes)
echo 3. Prepare the system for launch
echo.
pause

cd /d "%~dp0"
call venv\Scripts\activate.bat

python setup_unsw_system.py

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next: Run 2_START_UNSW_BACKEND.bat
echo.
pause
