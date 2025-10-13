"""
Kick Stream Recorder - Main orchestration
Monitors a Kick channel and automatically records when live.
"""
import asyncio
import time
from pathlib import Path

from src.config import Config
from src.discord_notifier import DiscordNotifier
from src.live_check import LiveChecker
from src.recorder import StreamRecorder


async def main():
    """Main application loop."""
    # Initialize configuration
    config_file = Path(__file__).parent / "config.json"
    config = Config(config_file)
    
    # Initialize components
    media_dir = Path(__file__).parent / "media"
    recorder = StreamRecorder(media_dir)
    live_checker = LiveChecker()
    discord_notifier = DiscordNotifier(
        webhook_url=config.discord_webhook_url,
        recorder_name=config.recorder_name,
        enabled=config.discord_enabled
    )
    
    # Display startup information
    print(f"[INFO] Kick Stream Recorder started")
    print(f"[INFO] Recorder Name: {config.recorder_name}")
    print(f"[INFO] Monitoring channel: {config.channel}")
    print(f"[INFO] Check interval: {config.check_interval} seconds")
    print(f"[INFO] Discord notifications: {'Enabled' if config.discord_enabled else 'Disabled'}")
    print(f"[INFO] Recordings will be saved to: {media_dir}")
    print("-" * 50)
    
    # Main monitoring loop
    while True:
        try:
            print(f"[INFO] Checking if {config.channel} is live...")
            is_live = await live_checker.is_stream_live(config.channel)
            
            if is_live:
                print(f"[INFO] ✓ {config.channel} is LIVE! Starting recording...")
                discord_notifier.send_live_notification(
                    config.channel,
                    f"@everyone {config.channel} has gone live!"
                )
                recorder.record_stream(config.channel)
                
                # After recording ends, wait before next check
                print(f"[INFO] Recording ended. Waiting 60 seconds before next check...")
                time.sleep(60)
            else:
                print(f"[INFO] ✗ {config.channel} is not live. Checking again in {config.check_interval} seconds...")
                await asyncio.sleep(config.check_interval)
                
        except KeyboardInterrupt:
            print("\n[INFO] Shutting down...")
            break
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            print(f"[INFO] Retrying in {config.check_interval} seconds...")
            await asyncio.sleep(config.check_interval)


if __name__ == "__main__":
    asyncio.run(main())
