# Nexto Bot Loader for Rocket League

A Python-based loader that injects the Nexto bot into Rocket League using the RLBot framework.

## Features

- **🌐 Online Play Support**: Attach to custom/private online matches
- **🖥️ Modern GUI Interface**: User-friendly graphical interface with real-time status
- **💻 Command Line Interface**: Traditional CLI for advanced users  
- **Automatic Injection**: Seamlessly injects the Nexto bot into Rocket League
- **Process Monitoring**: Detects when Rocket League is running and monitors bot status
- **Multiple Injection Methods**: Supports both direct API injection and GUI-based injection
- **Configuration Management**: Handles bot configuration and team settings
- **Error Handling**: Comprehensive logging and error recovery
- **Auto-Installation**: Automatically installs missing dependencies
- **Cross-Platform**: Works on Windows (primary), with Linux/Mac support

## Prerequisites

1. **Rocket League**: Must be installed and playable
2. **Python 3.7+**: Required for running the loader and bot
3. **RLBot Framework**: Automatically installed with requirements
4. **BakkesMod** (recommended): For enhanced bot functionality

## Quick Start

### Method 1: GUI Interface (Recommended)

1. Double-click `launch_gui.bat` or run:
   ```bash
   python gui.py
   ```
2. Configure settings in the GUI
3. Click "🚀 Start Bot"
4. Monitor progress in real-time

### Method 2: Interactive Batch File (Windows)

1. Double-click `launch_nexto.bat`
2. Choose interface (GUI/CLI/Setup)
3. Follow the prompts to configure options
4. The loader will automatically handle the rest

### Method 3: Command Line Interface

```bash
# Install dependencies
pip install -r requirements.txt

# Basic usage - will wait for Rocket League to start
python loader.py

# Specify team (0=Blue, 1=Orange)
python loader.py --team 1

# Don't wait for Rocket League (if already running)
python loader.py --no-wait

# Use RLBot GUI instead of direct injection
python loader.py --use-gui
```

## GUI Interface

The GUI provides an intuitive interface with:

### 🎛️ Configuration Panel
- **Bot Path**: Browse and select bot directory
- **Team Selection**: Choose Blue (0) or Orange (1)
- **Options**: Wait for RL, Use RLBot GUI, Auto-install dependencies

### 📊 Status Monitoring  
- **Dependencies**: Real-time dependency status
- **Rocket League**: Game process detection
- **Bot Status**: Current bot state and progress

### 🎮 Control Panel
- **Start/Stop Bot**: Main control buttons
- **Setup & Verify**: Run installation verification
- **Help**: Built-in help and troubleshooting

### 📝 Log Output
- **Real-time Logging**: See all loader activity
- **Save/Clear**: Manage log output
- **Scrollable History**: Review past events

## Usage Options

### GUI Interface
```bash
# Launch GUI
python gui.py

# Or use the universal launcher
python nexto_launcher.py --gui
```

### Command Line Arguments

- `--bot-path PATH`: Specify custom bot directory (default: current directory)
- `--team {0,1}`: Set bot team (0=Blue, 1=Orange, default: 0)
- `--no-wait`: Don't wait for Rocket League to start
- `--use-gui`: Use RLBot GUI for injection instead of direct method
- `--online`: Enable online mode (attach to existing matches)

### Examples

```bash
# Load bot on Orange team, don't wait for RL
python loader.py --team 1 --no-wait

# Use GUI method for troubleshooting
python loader.py --use-gui

# Enable online mode for custom/private matches
python loader.py --online

# Load from custom directory with online mode
python loader.py --bot-path "C:\MyBots\Nexto" --online
```

## 🌐 Online Play Mode

### What is Online Mode?
Online mode allows Nexto to join **custom and private online matches**. This is different from exhibition mode which only works with offline matches.

### ⚠️ Important Limitations:
- **DOES NOT** work with ranked or casual matchmaking
- **ONLY** works with custom/private matches
- Host must enable bots in match settings
- Not all online game modes support bots
- May have connectivity issues depending on server

### How to Use Online Mode:

#### CLI Method:
```bash
python loader.py --online
```

#### GUI Method:
1. Check "🌐 Online Mode" in the configuration panel
2. Click "🚀 Start Bot"
3. Join a custom/private match

#### Steps for Online Play:
1. Start the loader with online mode enabled
2. In Rocket League, create or join a **custom/private match**
3. Ensure the match allows bots (host setting)
4. The bot will automatically attach to the match
5. Play normally - the bot will participate

### Troubleshooting Online Mode:
- Ensure you're in a custom/private match, not ranked/casual
- Check that the host has enabled bots
- Try exhibition mode first to verify the bot works
- Some game modes may not support bots

## How It Works

1. **Dependency Check**: Verifies all required files and packages are present
2. **Process Detection**: Optionally waits for Rocket League to start
3. **Configuration**: Loads bot configuration from `bot.cfg`
4. **Injection**: Injects the bot using RLBot framework
5. **Monitoring**: Continuously monitors bot and game status

## Injection Methods

### Direct Injection (Default)
- Uses RLBot Python API directly
- Faster and more reliable
- Recommended for most users

### GUI Injection (Fallback)
- Launches RLBot GUI with bot pre-configured
- Useful for troubleshooting
- Allows manual control over bot settings

## File Structure

```
nexto/
├── gui.py              # Modern GUI interface
├── loader.py           # Main bot loader script
├── nexto_launcher.py   # Universal launcher (GUI/CLI)
├── bot_utils.py        # Utility functions and classes
├── setup.py            # Setup and verification script
├── launch_nexto.bat    # Windows batch file (interactive)
├── launch_gui.bat      # Quick GUI launcher
├── bot.py              # Main bot implementation
├── bot.cfg             # Bot configuration file
├── agent.py            # Bot AI agent
├── nexto_obs.py        # Observation builder
├── requirements.txt    # Python dependencies
├── appearance.cfg      # Bot appearance settings
├── nexto_logo.png      # Bot logo
└── README_LOADER.md    # This file
```

## Configuration

### Bot Settings

Edit `bot.cfg` to customize bot behavior:

```ini
[Locations]
looks_config = ./appearance.cfg
python_file = ./bot.py
requirements_file = ./requirements.txt
logo_file = ./nexto_logo.png

[Details]
name = Nexto
maximum_tick_rate_preference = 120
developer = Rolv, Soren, and several contributors
```

### Loader Settings

The loader automatically reads configuration from `bot.cfg` but can be overridden with command line arguments.

## Troubleshooting

### Common Issues

1. **"RLBot not found"**
   - Run: `pip install -r requirements.txt`
   - Ensure Python 3.7+ is installed

2. **"Rocket League not detected"**
   - Make sure Rocket League is running
   - Use `--no-wait` if RL is already started
   - Check Windows firewall/antivirus settings

3. **"Bot injection failed"**
   - Try using `--use-gui` option
   - Restart Rocket League and try again
   - Check RLBot framework compatibility

4. **"Permission denied"**
   - Run as Administrator on Windows
   - Check that Rocket League isn't running as Admin if the loader isn't

### Debug Mode

For detailed logging, check the `nexto_loader.log` file that's automatically created.

### Manual Injection Steps

If automatic injection fails:

1. Start Rocket League
2. Run: `python loader.py --use-gui`
3. In the RLBot GUI, click "Add Bot" 
4. Select the Nexto configuration
5. Click "Start Match"

## Advanced Usage

### Using Bot Utilities

```bash
# Check for Rocket League processes
python bot_utils.py --check-processes

# Setup environment
python bot_utils.py --setup-env

# Kill existing RLBot processes
python bot_utils.py --kill-rlbot

# Create desktop shortcut (Windows)
python bot_utils.py --create-shortcut
```

### Programmatic Usage

```python
from loader import NextoBotLoader

# Create loader instance
loader = NextoBotLoader(bot_path="./")

# Check dependencies
if loader.check_dependencies():
    # Run the bot
    loader.run(wait_for_rl=True, use_gui=False)
```

## System Requirements

- **OS**: Windows 10/11 (primary), Linux, macOS
- **Python**: 3.7 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB for bot and dependencies
- **Network**: Internet connection for initial setup

## Performance Tips

1. **Close unnecessary programs** before running the bot
2. **Set Rocket League to 120fps** with vsync off for optimal bot performance
3. **Use fullscreen mode** in Rocket League for better performance
4. **Disable replay recording** if experiencing lag

## Support

- **Bot Issues**: Check the [Nexto GitHub repository](https://github.com/Rolv-Arild/Necto)
- **RLBot Framework**: Visit [RLBot documentation](https://rlbot.org/)
- **Loader Issues**: Check `nexto_loader.log` for detailed error information

## Contributing

Feel free to submit improvements to the loader:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This loader follows the same license as the Nexto bot project.

---

**Note**: This loader is designed specifically for the Nexto bot. For other bots, you may need to modify the configuration and injection methods accordingly.