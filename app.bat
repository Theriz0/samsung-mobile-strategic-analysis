@echo off
title Samsung Strategic Analysis Pipeline
echo ==============================================

echo [1/2] Installing Dependencies...
python -m pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b
)

echo [2/2] Launching Dashboard...
python -m streamlit run app.py

echo ==============================================
pause