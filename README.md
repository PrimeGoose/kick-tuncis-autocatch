# Kick Recorder

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

### 1. Clone/Navigate to the project

```bash
cd kick-tuncis-autocatch-main
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip3 install -r requirements.txt
playwright install chromium
```

## 🚀 Usage

### Run the recorder

```bash
python3 main.py
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

1. **Live Detection**: Uses Playwright to check the Kick page for live indicators
2. **Recording**: Passes the Kick URL directly to yt-dlp, which extracts and records the stream
3. **Monitoring**: Continuously checks every 60 seconds when offline
4. **Auto-restart**: After a recording ends, waits 60 seconds then resumes monitoring

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
pip3 install yt-dlp
```

### "Chromium not found"

Run the Playwright installer:

```bash
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
