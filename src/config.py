"""Configuration management module."""
import json
import sys
from pathlib import Path


class Config:
    """Configuration manager for the Kick Stream Recorder."""
    
    def __init__(self, config_file: Path):
        """Initialize configuration manager."""
        self.config_file = config_file
        self._config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from config.json file."""
        if not self.config_file.exists():
            return self._create_default_config()
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            self._validate_config(config)
            return config
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON in config.json: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"[ERROR] Failed to load config.json: {e}")
            sys.exit(1)
    
    def _create_default_config(self) -> dict:
        """Create a default configuration file."""
        print("[INFO] config.json file not found. Creating a new one...")
        default_config = {
            "channel": "channel_name_here",
            "recorder_name": "Recorder #1",
            "check_interval": 60,
            "discord": {
                "enabled": False,
                "webhook_url": ""
            }
        }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            print(f"[SUCCESS] Created config.json at: {self.config_file}")
            print("\n" + "=" * 60)
            print("⚠️  PLEASE UPDATE config.json WITH YOUR SETTINGS:")
            print("=" * 60)
            print("\n1. Set 'channel' to the Kick channel you want to monitor")
            print("2. Set 'recorder_name' to identify this recorder instance")
            print("3. (Optional) Enable Discord notifications and add webhook URL")
            print("\nThen run the script again.\n")
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] Failed to create config.json: {e}")
            sys.exit(1)
    
    def _validate_config(self, config: dict) -> None:
        """Validate required configuration fields."""
        if not config.get("channel") or config.get("channel") == "channel_name_here":
            print("\n" + "=" * 60)
            print("[ERROR] Please update 'channel' in config.json!")
            print("=" * 60)
            print("\nOpen config.json and set 'channel' to the Kick channel you want to monitor.")
            print("Example: \"channel\": \"kalnins\"\n")
            sys.exit(1)
        
        if not config.get("recorder_name"):
            print("\n" + "=" * 60)
            print("[ERROR] Please update 'recorder_name' in config.json!")
            print("=" * 60)
            print("\nOpen config.json and set 'recorder_name' to identify this recorder.")
            print("Example: \"recorder_name\": \"My Home PC\"\n")
            sys.exit(1)
    
    @property
    def channel(self) -> str:
        """Get the channel name."""
        return self._config["channel"]
    
    @property
    def recorder_name(self) -> str:
        """Get the recorder name."""
        return self._config["recorder_name"]
    
    @property
    def check_interval(self) -> int:
        """Get the check interval in seconds."""
        return self._config.get("check_interval", 60)
    
    @property
    def discord_enabled(self) -> bool:
        """Check if Discord notifications are enabled."""
        return self._config.get("discord", {}).get("enabled", False)
    
    @property
    def discord_webhook_url(self) -> str:
        """Get the Discord webhook URL."""
        return self._config.get("discord", {}).get("webhook_url", "")

