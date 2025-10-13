# Changelog

## [Unreleased] - 2024-10-13

### Added
- **Discord Notifications**: Send webhook alerts when streams go live
  - Rich embed messages with stream info and recorder name
  - Configurable via `discord.enabled` and `discord.webhook_url` in config
  - @everyone mentions for instant alerts
- **JSON Configuration System**: Config-driven instead of hardcoded values
  - Auto-creates `config.json` with defaults on first run
  - Validates required fields with helpful error messages
  - Supports: channel, recorder_name, check_interval, discord settings
- **Mac/Linux Launcher**: `run_recorder.sh` bash script
  - Auto-creates venv, installs dependencies, runs recorder
  - Matches functionality of existing Windows `run_recorder.bat`
- **Architecture Documentation**: `ARCHITECTURE.md` explaining modular design

### Changed
- **Major Refactor**: Restructured monolithic code into modular architecture
  - Created `src/` directory with focused modules:
    - `src/config.py` - Configuration loading and validation
    - `src/discord_notifier.py` - Discord webhook handling
    - `src/live_check.py` - Stream live detection
    - `src/recorder.py` - Stream recording logic
  - Reduced `main.py` from 240 to 70 lines (orchestration only)
  - Improved separation of concerns and testability
- **Configuration**: Moved from hardcoded values to `config.json`
  - Channel name, recorder name, check interval now configurable
  - No more editing Python code for basic settings

### Dependencies
- Added `requests` library for Discord webhook HTTP calls

### Documentation
- Updated README.md with new architecture, configuration guide, and Discord setup
- Created ARCHITECTURE.md with detailed module responsibilities
- Updated troubleshooting section for config-related issues

### Technical Improvements
- Class-based design for all components
- Better error handling and validation
- Privacy-friendly recorder identification (no system info leaked)
- Each module is independently testable
- Easier to extend with new features

### Backward Compatibility
- 100% feature parity maintained
- No breaking changes to existing functionality
- Existing users need to create `config.json` (auto-generated on first run)