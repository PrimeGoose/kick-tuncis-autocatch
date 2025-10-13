"""Discord notification module."""
import requests
from datetime import datetime


class DiscordNotifier:
    """Handles Discord webhook notifications."""
    
    def __init__(self, webhook_url: str, recorder_name: str, enabled: bool = True):
        """Initialize Discord notifier."""
        self.webhook_url = webhook_url
        self.recorder_name = recorder_name
        self.enabled = enabled
    
    def send_live_notification(self, channel: str, message: str = None) -> None:
        """Send a notification when a stream goes live."""
        if not self.enabled:
            print("[INFO] Discord notifications are disabled in config")
            return
        
        if not self.webhook_url:
            print("[WARNING] Discord enabled but webhook URL is missing in config")
            return
        
        if message is None:
            message = f"@everyone {channel} has gone live!"
        
        try:
            data = {
                "content": message,
                "embeds": [{
                    "title": f"🔴 {channel} is LIVE!",
                    "description": f"Stream has started on Kick\n\n**Recording on:** 📹 `{self.recorder_name}`",
                    "url": f"https://kick.com/{channel}",
                    "color": 0x00ff00,  # Green color
                    "timestamp": datetime.utcnow().isoformat(),
                    "footer": {
                        "text": "Kick Stream Recorder"
                    }
                }]
            }
            
            response = requests.post(self.webhook_url, json=data)
            
            if response.status_code == 204:
                print("[INFO] Discord notification sent successfully!")
            else:
                print(f"[WARNING] Discord notification failed with status code: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] Failed to send Discord notification: {e}")

