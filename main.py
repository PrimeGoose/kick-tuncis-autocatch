import asyncio
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright
import subprocess
import time

CHANNEL = "kalnins"   # Kick channel
CHECK_INTERVAL = 60         # seconds between checks
YT_DLP_PATH = "yt-dlp"      # assumes yt-dlp installed in venv

# recordings directory
MEDIA_DIR = Path(__file__).parent / "media"
MEDIA_DIR.mkdir(exist_ok=True)

async def is_stream_live(channel: str) -> bool:
    """Check if a Kick stream is currently live by examining the page content."""
    url = f"https://kick.com/{channel}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            
            # Set a user agent to appear more like a real browser
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            
            # Use domcontentloaded instead of networkidle (Kick has constant network activity)
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # Wait for dynamic content to load
            await asyncio.sleep(8)
            
            # Multiple checks to determine if stream is live
            is_live = await page.evaluate("""() => {
                // Method 1: Check page title
                if (document.title.toLowerCase().includes('watch live')) {
                    const hasVideo = document.querySelector('video') !== null;
                    if (hasVideo) return true;
                }
                
                // Method 2: Look for specific LIVE indicators in HTML
                const html = document.documentElement.outerHTML;
                const liveIndicators = [
                    '"is_live":true',
                    '"livestream":{',
                    'LIVE</span>',
                    'LIVE</div>',
                    'stream is live'
                ];
                
                for (const indicator of liveIndicators) {
                    if (html.includes(indicator)) return true;
                }
                
                // Method 3: Check for video element with source
                const video = document.querySelector('video');
                if (video && (video.src || video.currentSrc)) {
                    return true;
                }
                
                // Method 4: Look for offline message
                if (html.toLowerCase().includes('offline') || 
                    html.toLowerCase().includes('not streaming')) {
                    return false;
                }
                
                return false;
            }""")
            
            return is_live
        except Exception as e:
            print(f"[ERROR] Failed to check stream status: {e}")
            return False
        finally:
            await browser.close()

def record_stream(channel: str):
    """Record a live stream using yt-dlp."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = MEDIA_DIR / f"{channel}_{timestamp}.mp4"
    url = f"https://kick.com/{channel}"
    
    print(f"[INFO] Starting yt-dlp recording to {filename} ...")
    print(f"[INFO] Recording from {url}")
    
    # yt-dlp will handle extracting the m3u8 URL automatically
    result = subprocess.run(
        [YT_DLP_PATH, url, "-o", str(filename)],
        capture_output=False
    )
    
    if result.returncode == 0:
        print(f"[INFO] Recording completed successfully: {filename}")
    else:
        print(f"[ERROR] Recording failed with return code {result.returncode}")

async def main():
    print(f"[INFO] Kick Stream Recorder started")
    print(f"[INFO] Monitoring channel: {CHANNEL}")
    print(f"[INFO] Check interval: {CHECK_INTERVAL} seconds")
    print(f"[INFO] Recordings will be saved to: {MEDIA_DIR}")
    print("-" * 50)
    
    while True:
        try:
            print(f"[INFO] Checking if {CHANNEL} is live...")
            is_live = await is_stream_live(CHANNEL)
            
            if is_live:
                print(f"[INFO] ✓ {CHANNEL} is LIVE! Starting recording...")
                record_stream(CHANNEL)
                # After recording ends, wait before next check
                print(f"[INFO] Recording ended. Waiting 60 seconds before next check...")
                time.sleep(60)
            else:
                print(f"[INFO] ✗ {CHANNEL} is not live. Checking again in {CHECK_INTERVAL} seconds...")
                await asyncio.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n[INFO] Shutting down...")
            break
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            print(f"[INFO] Retrying in {CHECK_INTERVAL} seconds...")
            await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())

