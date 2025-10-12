@echo off
REM ============================================================
REM Kick Recorder launcher for Windows
REM ============================================================

REM Activate virtual environment (create if missing)
if not exist "venv\" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate

REM Install dependencies if missing
echo [INFO] Installing dependencies...
pip install -r requirements.txt

REM Ensure Playwright is globally available
pip install playwright

REM Install Chromium browser if not already present
echo [INFO] Installing Playwright Chromium (this may take a while)...
playwright install chromium

REM Start the recorder
echo [INFO] Starting Kick Recorder...
python main.py

pause
