# Kick Recorder

<span style="color:red; font-weight:bold;">⚠️ Minimum Python version required: 3.8 or higher</span>

Automatically record Kick live streams using Playwright + yt-dlp.

## 📂 Project Structure

```
kick-tuncis-autocatch-main/
├── main.py                  # Main orchestration loop
├── config.json              # Configuration file
├── requirements.txt         # Python dependencies
├── run_recorder.bat         # Windows launcher
├── run_recorder.sh          # Mac/Linux launcher
├── src/                     # Modular components
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration management
│   ├── discord_notifier.py  # Discord webhook notifications
│   ├── live_check.py        # Stream live detection
│   └── recorder.py          # Stream recording logic
├── media/                   # Recordings saved here (auto-created)
└── README.md
```

### Architecture

The codebase follows a modular architecture with clear separation of concerns:

- **`main.py`**: Orchestrates the main monitoring loop
- **`src/config.py`**: Loads and validates configuration
- **`src/live_check.py`**: Detects if streams are live using Playwright
- **`src/recorder.py`**: Records streams using yt-dlp
- **`src/discord_notifier.py`**: Sends Discord webhook notifications

## 🔧 Setup

### 🪟 Windows (PowerShell)

> ⚠️ Do **not** type commands inside the Python shell (`>>>`). These must be run in **PowerShell** or **CMD**, not inside Python.

You can either run everything **manually** or simply double-click the **`run_recorder.bat`** file.

#### Option 1 – Run automatically (recommended)

Just run:

```powershell
run_recorder.bat
```

This batch file automatically creates a virtual environment, installs dependencies, ensures Playwright is available, and starts recording.

#### Option 2 – Manual setup

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

### 🪟 Windows – Save to Downloads Folder Instead of /media

By default, the script saves recordings inside the project folder under `/media`.
To save them directly to your **Windows Downloads** folder instead, modify this part of `main.py`:

```python
# Replace this:
MEDIA_DIR = Path(__file__).parent / "media"
MEDIA_DIR.mkdir(exist_ok=True)

# With this:
from pathlib import Path
MEDIA_DIR = Path.home() / "Downloads" / "KickRecordings"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
```

This will save all recordings into:

```
C:\Users\<YourName>\Downloads\KickRecordings\
```

If you prefer to save directly into the Downloads folder without the subfolder, use:

```python
MEDIA_DIR = Path.home() / "Downloads"
MEDIA_DIR.mkdir(exist_ok=True)
```

---

### 🍎 macOS / 🐧 Linux

#### Option 1 – Run automatically (recommended)

Just run:

```bash
./run_recorder.sh
```

This script automatically creates a virtual environment, installs dependencies, ensures Playwright is available, and starts recording.

#### Option 2 – Manual setup

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

### First Time Setup

1. **Run the script for the first time** - it will automatically create a `config.json` file:
   ```bash
   python main.py   # or python3 main.py on macOS/Linux
   ```

2. **Edit the `config.json`** file that was created with your settings:
   ```json
   {
     "channel": "your_channel_name",
     "recorder_name": "Recorder #1",
     "check_interval": 60,
     "discord": {
       "enabled": false,
       "webhook_url": ""
     }
   }
   ```

3. **Run the script again** and it will start monitoring!

### Run the recorder

```bash
python main.py   # or python3 main.py on macOS/Linux
```

Or use the launcher scripts:
- **Windows**: Double-click `run_recorder.bat`
- **Mac/Linux**: Run `./run_recorder.sh`

The script will:

* Monitor the configured channel every 60 seconds
* Automatically detect when the stream goes live
* Send Discord notification (if enabled)
* Start recording using yt-dlp
* Save recordings to the `media/` folder with timestamps

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
* ✅ Discord notifications when stream goes live
* ✅ Easy JSON configuration file
* ✅ Multiple recorder instance support
* ✅ Continuous monitoring
* ✅ Error handling and auto-retry
* ✅ Clean console output
* ✅ Cross-platform (Windows, Mac, Linux)

## ⚙️ Configuration

All settings are managed through `config.json`:

```json
{
  "channel": "kalnins",
  "recorder_name": "Recorder #1",
  "check_interval": 60,
  "discord": {
    "enabled": true,
    "webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
  }
}
```

### Required Fields

- **`channel`**: The Kick channel name to monitor (e.g., "trainwreckstv")
- **`recorder_name`**: A custom name to identify this recorder instance (e.g., "Home PC", "Server #1")

### Optional Fields

- **`check_interval`**: Seconds between live checks (default: 60)
- **`discord.enabled`**: Enable/disable Discord notifications (default: false)
- **`discord.webhook_url`**: Your Discord webhook URL (only needed if enabled is true)

### Discord Notifications

To enable Discord notifications when a stream goes live:

1. Create a webhook in your Discord server:
   - Go to Server Settings → Integrations → Webhooks
   - Click "New Webhook"
   - Copy the webhook URL

2. Update `config.json`:
   ```json
   "discord": {
     "enabled": true,
     "webhook_url": "YOUR_WEBHOOK_URL_HERE"
   }
   ```

When a stream goes live, you'll receive a Discord notification with:
- @everyone mention
- Stream title and link
- Recorder name
- Timestamp

## 🐛 Troubleshooting

### "Please update 'channel' in config.json"

The script detected the default placeholder value. Open `config.json` and change:
```json
"channel": "channel_name_here"
```
to your actual Kick channel name:
```json
"channel": "trainwreckstv"
```

### "Please update 'recorder_name' in config.json"

Make sure your `config.json` includes the `recorder_name` field to identify this recorder instance:
```json
"recorder_name": "My Home PC"
```

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
