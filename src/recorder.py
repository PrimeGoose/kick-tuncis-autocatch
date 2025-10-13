"""Stream recording module."""
import subprocess
from datetime import datetime
from pathlib import Path


class StreamRecorder:
    """Handles recording Kick streams using yt-dlp."""
    
    def __init__(self, media_dir: Path, yt_dlp_path: str = "yt-dlp"):
        """Initialize stream recorder."""
        self.media_dir = media_dir
        self.yt_dlp_path = yt_dlp_path
        
        # Ensure media directory exists
        self.media_dir.mkdir(exist_ok=True)
    
    def record_stream(self, channel: str) -> bool:
        """
        Record a live stream using yt-dlp.
        
        Args:
            channel: The Kick channel name to record
            
        Returns:
            bool: True if recording was successful, False otherwise
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = self.media_dir / f"{channel}_{timestamp}.mp4"
        url = f"https://kick.com/{channel}"
        
        print(f"[INFO] Starting yt-dlp recording to {filename} ...")
        print(f"[INFO] Recording from {url}")
        
        # yt-dlp will handle extracting the m3u8 URL automatically
        result = subprocess.run(
            [self.yt_dlp_path, url, "-o", str(filename)],
            capture_output=False
        )
        
        if result.returncode == 0:
            print(f"[INFO] Recording completed successfully: {filename}")
            return True
        else:
            print(f"[ERROR] Recording failed with return code {result.returncode}")
            return False

