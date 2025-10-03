#!/usr/bin/env python3
"""
Nexto Bot Management Utilities
Additional utilities for managing the Nexto bot injection process.
"""

import os
import sys
import json
import psutil
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class RocketLeagueManager:
    """Utility class for managing Rocket League processes and bot injection"""
    
    @staticmethod
    def find_rocket_league_processes() -> List[Dict[str, Any]]:
        """Find all Rocket League related processes"""
        rl_process_names = [
            "RocketLeague.exe",
            "RLBot.exe",
            "bakkesmod.exe",
            "injector.exe"
        ]
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'create_time']):
            try:
                if proc.info['name'] in rl_process_names:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'exe': proc.info['exe'],
                        'create_time': proc.info['create_time']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return processes
    
    @staticmethod
    def is_rlbot_running() -> bool:
        """Check if RLBot framework is already running"""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'rlbot' in ' '.join(proc.info['cmdline']).lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False
    
    @staticmethod
    def kill_rlbot_processes():
        """Kill any existing RLBot processes"""
        killed = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline']).lower()
                if 'rlbot' in cmdline or 'rlbot_gui' in cmdline:
                    proc.terminate()
                    killed.append(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return killed


class BotConfigManager:
    """Manages bot configuration and setup"""
    
    def __init__(self, bot_path: Path):
        self.bot_path = bot_path
        self.config_file = bot_path / "bot.cfg"
        self.appearance_file = bot_path / "appearance.cfg"
    
    def create_team_config(self, team: int, name: str = "Nexto") -> Dict[str, Any]:
        """Create a team configuration for the bot"""
        return {
            "name": name,
            "team": team,
            "config_file": str(self.config_file.absolute()),
            "python_file": str((self.bot_path / "bot.py").absolute()),
            "logo_file": str((self.bot_path / "nexto_logo.png").absolute()),
            "requirements_file": str((self.bot_path / "requirements.txt").absolute())
        }
    
    def validate_bot_files(self) -> List[str]:
        """Validate that all required bot files exist"""
        required_files = [
            "bot.py",
            "bot.cfg", 
            "requirements.txt",
            "agent.py",
            "nexto_obs.py",
            "__init__.py"
        ]
        
        missing_files = []
        for filename in required_files:
            if not (self.bot_path / filename).exists():
                missing_files.append(filename)
        
        return missing_files
    
    def update_bot_config(self, updates: Dict[str, Any]):
        """Update bot configuration file with new values"""
        if not self.config_file.exists():
            logger.error(f"Config file not found: {self.config_file}")
            return False
        
        try:
            lines = []
            with open(self.config_file, 'r') as f:
                lines = f.readlines()
            
            updated_lines = []
            for line in lines:
                stripped = line.strip()
                if '=' in stripped and not stripped.startswith('#') and not stripped.startswith('//'):
                    key, value = stripped.split('=', 1)
                    key = key.strip()
                    if key in updates:
                        updated_lines.append(f"{key} = {updates[key]}\n")
                    else:
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)
            
            with open(self.config_file, 'w') as f:
                f.writelines(updated_lines)
            
            logger.info(f"Updated bot config with: {updates}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update config: {e}")
            return False


class InjectionMethods:
    """Different methods for injecting the bot into Rocket League"""
    
    @staticmethod
    def direct_rlbot_injection(bot_path: Path, team: int = 0) -> bool:
        """Direct injection using RLBot Python API"""
        try:
            from rlbot.setup_manager import SetupManager
            from rlbot.parsing.agent_config_parser import AgentConfigParser
            
            config_manager = BotConfigManager(bot_path)
            
            missing = config_manager.validate_bot_files()
            if missing:
                logger.error(f"Missing required files: {missing}")
                return False
            
            agent_config = config_manager.create_team_config(team)
            
            setup_manager = SetupManager()
            setup_manager.startup_bot_agents([agent_config])
            
            logger.info("Direct RLBot injection completed")
            return True
            
        except Exception as e:
            logger.error(f"Direct injection failed: {e}")
            return False
    
    @staticmethod
    def gui_injection(bot_path: Path) -> bool:
        """Injection via RLBot GUI"""
        try:
            import subprocess
            
            config_path = bot_path / "nexto_gui_config.json"
            config = {
                "team_configurations": [{"team_color_id": 0}],
                "bot_configurations": [{
                    "name": "Nexto",
                    "team": 0,
                    "python_file": str((bot_path / "bot.py").absolute()),
                    "config_file": str((bot_path / "bot.cfg").absolute())
                }]
            }
            
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            cmd = [sys.executable, "-m", "rlbot_gui", "--config", str(config_path)]
            subprocess.Popen(cmd, cwd=str(bot_path))
            
            logger.info("RLBot GUI launched with Nexto configuration")
            return True
            
        except Exception as e:
            logger.error(f"GUI injection failed: {e}")
            return False
    
    @staticmethod
    def auto_injection(bot_path: Path, team: int = 0, prefer_gui: bool = False) -> bool:
        """Automatically choose the best injection method"""
        logger.info("Attempting automatic bot injection...")
        
        if not prefer_gui:
            if InjectionMethods.direct_rlbot_injection(bot_path, team):
                return True
            logger.warning("Direct injection failed, trying GUI method...")
        
        return InjectionMethods.gui_injection(bot_path)


def setup_environment(bot_path: Path) -> bool:
    """Setup the environment for bot injection"""
    logger.info("Setting up environment for Nexto bot...")
    
    if str(bot_path) not in sys.path:
        sys.path.insert(0, str(bot_path))
    
    os.environ['RLBOT_BOTPACK_PATH'] = str(bot_path)
    
    config_manager = BotConfigManager(bot_path)
    missing_files = config_manager.validate_bot_files()
    
    if missing_files:
        logger.error(f"Bot setup incomplete. Missing files: {missing_files}")
        return False
    
    logger.info("Environment setup completed successfully")
    return True


def create_desktop_shortcut(bot_path: Path):
    """Create a desktop shortcut for easy bot launching"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "Launch Nexto Bot.lnk")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{bot_path / "loader.py"}"'
        shortcut.WorkingDirectory = str(bot_path)
        shortcut.IconLocation = str(bot_path / "nexto_logo.png") if (bot_path / "nexto_logo.png").exists() else ""
        shortcut.save()
        
        logger.info(f"Desktop shortcut created: {shortcut_path}")
        return True
        
    except ImportError:
        logger.warning("Cannot create desktop shortcut - winshell/pywin32 not available")
        return False
    except Exception as e:
        logger.error(f"Failed to create desktop shortcut: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Nexto Bot Management Utilities")
    parser.add_argument("--bot-path", type=str, default=".", help="Path to bot directory")
    parser.add_argument("--check-processes", action="store_true", help="Check for RL processes")
    parser.add_argument("--setup-env", action="store_true", help="Setup environment")
    parser.add_argument("--create-shortcut", action="store_true", help="Create desktop shortcut")
    parser.add_argument("--kill-rlbot", action="store_true", help="Kill existing RLBot processes")
    
    args = parser.parse_args()
    
    bot_path = Path(args.bot_path).absolute()
    
    if args.check_processes:
        processes = RocketLeagueManager.find_rocket_league_processes()
        print(f"Found {len(processes)} RL-related processes:")
        for proc in processes:
            print(f"  - {proc['name']} (PID: {proc['pid']})")
    
    if args.kill_rlbot:
        killed = RocketLeagueManager.kill_rlbot_processes()
        print(f"Killed {len(killed)} RLBot processes")
    
    if args.setup_env:
        success = setup_environment(bot_path)
        print(f"Environment setup: {'Success' if success else 'Failed'}")
    
    if args.create_shortcut:
        success = create_desktop_shortcut(bot_path)
        print(f"Desktop shortcut: {'Created' if success else 'Failed'}")