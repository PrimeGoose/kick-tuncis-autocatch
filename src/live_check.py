"""Live stream detection module."""
import asyncio
from playwright.async_api import async_playwright


class LiveChecker:
    """Handles checking if a Kick stream is live."""
    
    def __init__(self):
        """Initialize live checker."""
        pass
    
    async def is_stream_live(self, channel: str) -> bool:
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

