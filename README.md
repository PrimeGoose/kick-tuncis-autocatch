# Kick Recorder

<span style="color:red; font-weight:bold;">⚠️ Minimum Python version required: 3.8 or higher</span>

Automatically record Kick live streams using Playwright + yt-dlp.

## 📂 Project Structure

```
kick-tuncis-autocatch-main/
├── main.py          # recorder script
├── requirements.txt # dependencies
├── .gitignore       # git exclusions
├── /media           # recordings saved here (auto-created)
└── README.md
```

## 🔧 Setup

### 🪟 Windows (PowerShell)

> ⚠️ Do **not** type commands inside the Python shell (`>>>`). These must be run in **PowerShell** or **CMD**, not inside Python.

```powershell
# 1. Navigate to the project folder
cd "D:\Downloads\kick-tuncis-autocatch-main"

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
venv\Scripts\activate

# 4. Install dependencies (yt-dlp)
pip install -r requirements.txt

# 5. Manually install Playwright globally so Windows can find it
pip install playwright

# 6. Download Chromium browser for Playwright
playwright install chromium

# 7. Run the recorder
python main.py
```

If you see `ModuleNotFoundError: No module named 'playwright'`, it means Playwright was not installed globally. Run `pip install playwright` outside the venv, then retry.

---

### 🍎 macOS / 🐧 Linux

```bash
# 1. Navigate to the project folder
cd kick-tuncis-autocatch-main

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies (Playwright + yt-dlp)
pip3 install -r requirements.txt

# 4. Download Chromium browser for Playwright
playwright install chromium

# 5. Run the recorder
python3 main.py
```

---

## 🚀 Usage

### Run the recorder

```bash
python main.py   # or python3 main.py on macOS/Linux
```

The script will:

* Monitor the configured channel every 60 seconds
* Automatically detect when the stream goes live
* Start recording using yt-dlp
* Save recordings to the `media/` folder with timestamps

### Change the channel

Edit `main.py` and change the `CHANNEL` variable:

```python
CHANNEL = "your_channel_name"  # Change this
```

### Run in background (optional)

```bash
# Using tmux
tmux new -s kick-recorder
python3 main.py
# Press Ctrl+B then D to detach

# Using screen
screen -S kick-recorder
python3 main.py
# Press Ctrl+A then D to detach

# Using nohup
nohup python3 main.py > recorder.log 2>&1 &
```

## 📝 How It Works

1. **Live Detection**: Uses Playwright to check the Kick page for live indicators.
2. **Recording**: Passes the Kick URL directly to yt-dlp, which extracts and records the stream.
3. **Monitoring**: Continuously checks every 60 seconds when offline.
4. **Auto-restart**: After a recording ends, waits 60 seconds then resumes monitoring.

## 🎯 Features

* ✅ Automatic live stream detection
* ✅ Timestamped recordings (`channel_YYYY-MM-DD_HH-MM-SS.mp4`)
* ✅ Continuous monitoring
* ✅ Error handling and auto-retry
* ✅ Clean console output

## ⚙️ Configuration

Edit these variables in `main.py`:

```python
CHANNEL = "kalnins"    # Channel to monitor
CHECK_INTERVAL = 60           # Seconds between checks
YT_DLP_PATH = "yt-dlp"       # Path to yt-dlp executable
```

## 🐛 Troubleshooting

### "yt-dlp not found"

Make sure yt-dlp is installed in your venv:

```bash
pip install yt-dlp  # or pip3 install yt-dlp
```

### "playwright: command not found" or "ModuleNotFoundError: No module named 'playwright'"

Make sure Playwright is installed globally:

```bash
pip install playwright
playwright install chromium
```

### Stream not detected

* Check the channel name is correct (case-sensitive)
* Verify the stream is actually live on [https://kick.com/channelname](https://kick.com/channelname)
* Some streams may take a few minutes to appear as "live"
* The detection waits 8 seconds for the page to load - if still failing, increase the wait time in `main.py`

## ✅ Next Steps

* Add notification hooks (Discord/Telegram) when a stream goes live
* Support multiple channels simultaneously
* Add configuration file support (YAML/JSON)
* Implement stream quality selection
