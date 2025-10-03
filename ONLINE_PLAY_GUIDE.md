# 🌐 Nexto Bot Online Play Guide

This guide explains how to use Nexto bot in online matches with other players.

## ⚡ Quick Start

### Method 1: GUI (Easiest)
1. Run `python gui.py` or double-click `launch_gui.bat`
2. Check "🌐 Online Mode" checkbox
3. Click "🚀 Start Bot"
4. Create/join a custom match in Rocket League

### Method 2: Command Line
```bash
python loader.py --online
```

## 📋 Requirements for Online Play

### ✅ What You Need:
- Nexto bot properly installed and working in exhibition mode
- Rocket League running
- Access to create custom matches OR invitation to private match
- Host that allows bots in match settings

### ❌ What WON'T Work:
- Ranked matches (Competitive)
- Casual playlists
- Tournament matches
- Matches where host has disabled bots

## 🎮 Step-by-Step Online Play

### Step 1: Start the Bot Loader
```bash
# Choose one of these methods:
python loader.py --online              # Command line
python gui.py                          # GUI (check online mode)
.\launch_nexto.bat                     # Batch file (choose online)
```

### Step 2: Set Up the Match in Rocket League

#### If You're Hosting:
1. Go to **Play → Custom Games → Create**
2. Choose your preferred game mode
3. **IMPORTANT:** In match settings, enable "Allow Bots"
4. Set other settings as desired
5. Start the match or invite friends

#### If You're Joining:
1. Get invited to a private match
2. Ensure the host has enabled bots
3. Join the match normally

### Step 3: Bot Attachment
- The bot will automatically detect and attach to the match
- You should see the bot join your team (Blue/Orange based on configuration)
- The bot will start playing immediately

### Step 4: Play!
- Play normally with the bot as your teammate/opponent
- The bot will behave just like in exhibition mode
- You can chat, score goals, and interact normally

## ⚙️ Configuration Options

### Team Selection
```bash
python loader.py --online --team 0     # Blue team
python loader.py --online --team 1     # Orange team
```

### Advanced Options
```bash
# Online mode with GUI fallback
python loader.py --online --use-gui

# Online mode without waiting for RL
python loader.py --online --no-wait
```

## 🔧 Troubleshooting Online Mode

### Problem: "Bot injection failed"
**Solutions:**
- Ensure you're in a custom/private match, not ranked/casual
- Check that the host has enabled bots in match settings
- Try exhibition mode first to verify bot works
- Restart Rocket League and try again

### Problem: "Bot not appearing in match"
**Solutions:**
- Make sure the match allows bots (host setting)
- Check that you're on the correct team
- Try leaving and rejoining the match
- Restart the bot loader

### Problem: "Cannot attach to match"
**Solutions:**
- Only custom/private matches support bot attachment
- Ensure Rocket League is fully loaded before starting bot
- Try using `--use-gui` option for better compatibility

### Problem: "Bot disconnects frequently"
**Solutions:**
- Check your internet connection
- Use wired connection instead of WiFi
- Try different game modes
- Some online modes may be unstable for bots

## 🎯 Best Practices for Online Play

### For Hosts:
1. **Always enable bots** in match settings before starting
2. **Inform players** that a bot will be joining
3. **Choose stable game modes** (1v1, 2v2, 3v3 standard)
4. **Use voice chat** to coordinate with bot behavior

### For Players:
1. **Test in exhibition mode first** to ensure bot works
2. **Communicate with host** about bot settings
3. **Be patient** - online mode can be less stable than exhibition
4. **Have fun!** - bots can make matches more interesting

## 📊 Supported Online Features

| Feature | Exhibition Mode | Online Mode |
|---------|----------------|-------------|
| **Basic Gameplay** | ✅ Full | ✅ Full |
| **Team Play** | ✅ Full | ✅ Full |
| **Custom Mutators** | ✅ Full | ⚠️ Limited |
| **Ranked Matches** | ❌ N/A | ❌ Not Supported |
| **Tournament Mode** | ❌ N/A | ❌ Not Supported |
| **Custom Maps** | ✅ Full | ⚠️ Depends on Map |
| **Replays** | ✅ Full | ✅ Full |

## 🎲 Game Modes That Work Well

### ✅ Recommended:
- **Soccer** (standard 1v1, 2v2, 3v3)
- **Hockey** (with proper arena)
- **Basketball** (Hoops)
- **Dropshot** (limited support)

### ⚠️ May Work:
- **Rumble** (depends on mutators)
- **Snow Day** (depends on physics)
- **Custom game modes** (varies by implementation)

### ❌ Not Recommended:
- **Ranked playlists** (not supported)
- **Casual playlists** (not supported)
- **Heavily modded servers** (compatibility issues)

## 🔗 Quick Reference Commands

```bash
# Start online mode (GUI)
python gui.py

# Start online mode (CLI)
python loader.py --online

# Online mode, Orange team
python loader.py --online --team 1

# Online mode with GUI fallback
python loader.py --online --use-gui

# Setup and verify installation
python setup.py
```

## 💡 Pro Tips

1. **Test First**: Always verify the bot works in exhibition mode before trying online
2. **Communicate**: Let other players know a bot will be joining
3. **Be Patient**: Online mode can take longer to connect than exhibition
4. **Backup Plan**: Keep the GUI option ready in case direct injection fails
5. **Network Stability**: Use wired internet for best bot performance

---

**🎉 Ready to dominate online matches with your Nexto bot! Good luck and have fun!**