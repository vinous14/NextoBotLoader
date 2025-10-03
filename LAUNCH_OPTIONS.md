# 🚀 Nexto Bot Launcher Options

This document provides a quick reference for all the ways to launch the Nexto bot.

## 🖥️ GUI Interface (Recommended for Beginners)

### Option 1: Quick GUI Launch
```
Double-click: launch_gui.bat
```

### Option 2: Python GUI
```bash
python gui.py
```

### Option 3: Universal Launcher (GUI)
```bash
python nexto_launcher.py --gui
```

**Features:**
- ✨ User-friendly interface
- 📊 Real-time status monitoring  
- 🎛️ Easy configuration
- 📝 Built-in logging
- ❓ Help and troubleshooting

## 💻 Command Line Interface (Advanced Users)

### Option 1: Interactive Batch
```
Double-click: launch_nexto.bat
Choose option 2 (Command Line Interface)
```

### Option 2: Direct Python
```bash
python loader.py
```

### Option 3: Universal Launcher (CLI)
```bash
python nexto_launcher.py --cli
```

**Advanced Arguments:**
```bash
# Orange team, no wait for RL
python loader.py --team 1 --no-wait

# Use RLBot GUI for injection
python loader.py --use-gui

# Custom bot directory
python loader.py --bot-path "C:\path\to\bot"
```

## 🔧 Setup and Verification

### Option 1: Batch File Setup
```
Double-click: launch_nexto.bat
Choose option 3 (Setup & Verify)
```

### Option 2: Direct Setup
```bash
python setup.py
```

### Option 3: Universal Launcher Setup
```bash
python nexto_launcher.py --setup
```

## 📋 Quick Reference Table

| Method | File | Interface | Best For |
|--------|------|-----------|----------|
| **GUI Launcher** | `launch_gui.bat` | GUI | New users |
| **Interactive Batch** | `launch_nexto.bat` | Both | All users |
| **Python GUI** | `gui.py` | GUI | GUI lovers |
| **Python CLI** | `loader.py` | CLI | Advanced users |
| **Universal** | `nexto_launcher.py` | Both | Flexibility |
| **Setup** | `setup.py` | CLI | Troubleshooting |

## 🎯 Recommended Workflow

### For New Users:
1. Double-click `launch_gui.bat`
2. Configure settings in GUI
3. Click "🚀 Start Bot"

### For Advanced Users:
1. Run `python setup.py` (first time)
2. Run `python loader.py --team 1` (or preferred args)

### For Troubleshooting:
1. Run `python setup.py` to verify installation
2. Try GUI mode for visual feedback
3. Check log output for errors

## 💡 Tips

- **First time?** Use the GUI interface for easiest setup
- **Command line user?** Use `loader.py` with arguments  
- **Problems?** Run `setup.py` first to diagnose issues
- **Multiple bots?** Use `--bot-path` to specify different directories
- **Team games?** Use `--team 1` for Orange team

## 🆘 If Nothing Works

1. Open Command Prompt/PowerShell in the bot directory
2. Run: `python setup.py`
3. Follow the diagnostic output
4. Install missing dependencies as needed
5. Try again with GUI: `python gui.py`

---

**Choose your preferred method and start dominating Rocket League! 🏆**