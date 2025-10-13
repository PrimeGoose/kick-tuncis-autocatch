#!/bin/bash
# ============================================================
# Kick Recorder launcher for Mac/Linux
# ============================================================
# To make this script executable, run:
# chmod +x run_recorder.sh
# Then run with: ./run_recorder.sh

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if missing
echo "[INFO] Installing dependencies..."
pip install -r requirements.txt

# Ensure Playwright is globally available
pip install playwright

# Install Chromium browser if not already present
echo "[INFO] Installing Playwright Chromium (this may take a while)..."
playwright install chromium

# Start the recorder
echo "[INFO] Starting Kick Recorder..."
python main.py

# Wait for user input before closing (equivalent to 'pause' in Windows)
read -p "Press Enter to continue..."

