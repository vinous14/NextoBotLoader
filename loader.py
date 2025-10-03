#!/usr/bin/env python3
"""
Nexto Bot Loader for Rocket League
A Python loader that injects the Nexto bot into Rocket League using the RLBot framework.
"""

import os
import sys
import time
import json
import psutil
import logging
import subprocess
import threading
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nexto_loader.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class NextoBotLoader:
    """Main loader class for injecting Nexto bot into Rocket League"""
    
    def __init__(self, bot_path: str = None):
        self.bot_path = Path(bot_path) if bot_path else Path(__file__).parent
        self.config_file = self.bot_path / "bot.cfg"
        self.requirements_file = self.bot_path / "requirements.txt"
        self.python_file = self.bot_path / "bot.py"
        self.logo_file = self.bot_path / "nexto_logo.png"
        self.appearance_file = self.bot_path / "appearance.cfg"
        
        self.rlbot_process = None
        self.bot_process = None
        self.is_running = False
        
        self.bot_config = self._load_bot_config()
        
        self.online_mode = False
        self.match_attach_mode = True
        
        logger.info(f"Nexto Bot Loader initialized at: {self.bot_path}")
    
    def _load_bot_config(self) -> Dict[str, Any]:
        """Load bot configuration from bot.cfg"""
        config = {
            'name': 'Nexto',
            'team': 0,
            'maximum_tick_rate_preference': 120,
            'python_file': './bot.py',
            'requirements_file': './requirements.txt',
            'looks_config': './appearance.cfg',
            'logo_file': './nexto_logo.png'
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    lines = f.readlines()
                    
                current_section = None
                for line in lines:
                    line = line.strip()
                    if line.startswith('[') and line.endswith(']'):
                        current_section = line[1:-1].lower()
                        continue
                    
                    if '=' in line and not line.startswith('#') and not line.startswith('//'):
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        if value.lower() in ['true', 'false']:
                            value = value.lower() == 'true'
                        elif value.isdigit():
                            value = int(value)
                        
                        config[key] = value
                        
                logger.info(f"Loaded bot configuration: {config['name']}")
            except Exception as e:
                logger.warning(f"Error loading bot config: {e}. Using defaults.")
        
        return config
    
    def check_dependencies(self, auto_install: bool = True) -> bool:
        """Check if all required dependencies are installed"""
        logger.info("Checking dependencies...")
        
        required_files = [
            self.python_file,
            self.requirements_file,
            self.config_file
        ]
        
        for file_path in required_files:
            if not file_path.exists():
                logger.error(f"Required file missing: {file_path}")
                return False
        
        try:
            import rlbot
            logger.info(f"RLBot version {rlbot.__version__} found")
        except ImportError:
            if auto_install:
                logger.info("RLBot not found. Attempting to install dependencies...")
                if self.install_dependencies():
                    try:
                        import rlbot
                        logger.info(f"RLBot version {rlbot.__version__} installed successfully")
                    except ImportError:
                        logger.error("Failed to import RLBot after installation")
                        return False
                else:
                    return False
            else:
                logger.error("RLBot not found. Please install requirements: pip install -r requirements.txt")
                return False
        
        try:
            import torch
            import numpy as np
            import rlgym_compat
            logger.info("All core dependencies found")
        except ImportError as e:
            if auto_install:
                logger.warning(f"Missing dependency: {e}. Attempting installation...")
                if self.install_dependencies():
                    try:
                        import torch
                        import numpy as np
                        import rlgym_compat
                        logger.info("Dependencies installed successfully")
                    except ImportError as e:
                        logger.error(f"Failed to import after installation: {e}")
                        return False
                else:
                    return False
            else:
                logger.error(f"Missing dependency: {e}")
                return False
        
        return True
    
    def install_dependencies(self) -> bool:
        """Install required dependencies from requirements.txt"""
        try:
            logger.info("Installing dependencies from requirements.txt...")
            
            import subprocess
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(self.requirements_file)
            ], capture_output=True, text=True, cwd=str(self.bot_path))
            
            if result.returncode == 0:
                logger.info("Dependencies installed successfully")
                return True
            else:
                logger.error(f"Failed to install dependencies: {result.stderr}")
                
                logger.info("Attempting to install core packages individually...")
                core_packages = ["rlbot", "torch", "numpy", "rlgym-compat", "msgpack", "psutil"]
                
                for package in core_packages:
                    try:
                        result = subprocess.run([
                            sys.executable, "-m", "pip", "install", package
                        ], capture_output=True, text=True)
                        
                        if result.returncode == 0:
                            logger.info(f"Successfully installed {package}")
                        else:
                            logger.warning(f"Failed to install {package}: {result.stderr}")
                    except Exception as e:
                        logger.warning(f"Error installing {package}: {e}")
                
                return True
                
        except Exception as e:
            logger.error(f"Error during dependency installation: {e}")
            return False
    
    def is_rocket_league_running(self) -> bool:
        """Check if Rocket League is currently running"""
        rl_processes = [
            "RocketLeague.exe",
            "RLBot.exe", 
            "bakkesmod.exe"
        ]
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] in rl_processes:
                    logger.info(f"Found Rocket League process: {proc.info['name']} (PID: {proc.info['pid']})")
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return False
    
    def wait_for_rocket_league(self, timeout: int = 300) -> bool:
        """Wait for Rocket League to start"""
        logger.info("Waiting for Rocket League to start...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.is_rocket_league_running():
                logger.info("Rocket League detected!")
                return True
            
            time.sleep(2)
            print(".", end="", flush=True)
        
        logger.error("Timeout waiting for Rocket League to start")
        return False
    
    def create_rlbot_config(self, online_mode: bool = False) -> str:
        """Create temporary RLBot configuration file for the bot"""
        if online_mode:
            rlbot_config = {
                "bot_configurations": [
                    {
                        "name": self.bot_config.get('name', 'Nexto'),
                        "team": self.bot_config.get('team', 0),
                        "python_file": str(self.python_file.absolute()),
                        "config_file": str(self.config_file.absolute()),
                        "logo_file": str(self.logo_file.absolute()) if self.logo_file.exists() else "",
                        "requirements_file": str(self.requirements_file.absolute()),
                        "maximum_tick_rate_preference": self.bot_config.get('maximum_tick_rate_preference', 120)
                    }
                ],
                "launcher_configuration": {
                    "launcher_car_id": 0,
                    "launcher_team": self.bot_config.get('team', 0),
                    "launcher_primary_color": 0,
                    "launcher_secondary_color": 0,
                    "auto_save_replay": False,
                    "enable_rendering": False,
                    "enable_state_setting": False,
                    "auto_start_bots": True,
                    "look_for_custom_maps": False,
                    "match_attach_timeout": 30.0,
                    "enable_match_attachment": True
                }
            }
        else:
            rlbot_config = {
                "team_configurations": [
                    {
                        "team_color_id": 0,
                        "custom_color_id": 0,
                        "car_id": 0,
                        "decal_id": 0,
                        "wheels_id": 0,
                        "boost_id": 0,
                        "antenna_id": 0,
                        "hat_id": 0,
                        "paint_finish_id": 0,
                        "custom_finish_id": 0,
                        "engine_audio_id": 0,
                        "trails_id": 0,
                        "goal_explosion_id": 0
                    }
                ],
                "bot_configurations": [
                    {
                        "name": self.bot_config.get('name', 'Nexto'),
                        "team": self.bot_config.get('team', 0),
                        "python_file": str(self.python_file.absolute()),
                        "config_file": str(self.config_file.absolute()),
                        "logo_file": str(self.logo_file.absolute()) if self.logo_file.exists() else "",
                        "requirements_file": str(self.requirements_file.absolute()),
                        "maximum_tick_rate_preference": self.bot_config.get('maximum_tick_rate_preference', 120)
                    }
                ],
                "match_configuration": {
                    "game_mode": "Soccer",
                    "game_map": "DFHStadium",
                    "skip_replays": False,
                    "instant_start": False,
                    "existing_match_behavior": "Continue_And_Spawn",
                    "mutators": {
                        "match_length": "5 Minutes",
                        "max_score": "Unlimited",
                        "overtime": "Unlimited",
                        "series_length": "Unlimited",
                        "game_speed": "Default",
                        "ball_max_speed": "Default",
                        "ball_type": "Default",
                        "ball_weight": "Default",
                        "ball_size": "Default",
                        "ball_bounciness": "Default",
                        "boost_amount": "Default",
                        "rumble": "None",
                        "boost_strength": "1x",
                        "gravity": "Default",
                        "demolish": "Default",
                        "respawn_time": "3 Seconds"
                    }
                },
                "launcher_configuration": {
                    "launcher_car_id": 0,
                    "launcher_team": self.bot_config.get('team', 0),
                    "launcher_primary_color": 0,
                    "launcher_secondary_color": 0,
                    "auto_save_replay": False,
                    "enable_rendering": False,
                    "enable_state_setting": True,
                    "auto_start_bots": True,
                    "look_for_custom_maps": False
                }
            }
        
        config_path = self.bot_path / "nexto_rlbot_config.json"
        with open(config_path, 'w') as f:
            json.dump(rlbot_config, f, indent=2)
        
        logger.info(f"Created RLBot config: {config_path}")
        return str(config_path)
    
    def inject_bot(self, online_mode: bool = False) -> bool:
        """Inject the bot into Rocket League"""
        if online_mode:
            logger.info("Starting online bot injection process...")
            return self.inject_bot_online()
        else:
            logger.info("Starting exhibition bot injection process...")
            return self.inject_bot_exhibition()
    
    def inject_bot_online(self) -> bool:
        """Inject bot for online play by attaching to existing match"""
        try:
            logger.info("Setting up Python 3.13 compatibility layer for RLBot...")
            
            import sys
            if sys.version_info >= (3, 13) and 'imp' not in sys.modules:
                logger.info("Creating imp module compatibility layer for Python 3.13...")
                
                class ImpModule:
                    """Compatibility layer for the deprecated imp module"""
                    
                    @staticmethod
                    def find_module(name, path=None):
                        import importlib.util
                        spec = importlib.util.find_spec(name)
                        return spec
                    
                    @staticmethod
                    def load_module(name):
                        import importlib
                        return importlib.import_module(name)
                    
                    @staticmethod
                    def new_module(name):
                        import types
                        return types.ModuleType(name)
                    
                    PY_SOURCE = 1
                    PY_COMPILED = 2
                    C_EXTENSION = 3
                    PKG_DIRECTORY = 5
                    C_BUILTIN = 6
                    PY_FROZEN = 7
                
                sys.modules['imp'] = ImpModule()
                logger.info("imp module compatibility layer installed successfully")
            
            try:
                logger.info("Importing RLBot modules...")
                from rlbot.setup_manager import SetupManager
                logger.info("RLBot SetupManager imported successfully")
                
                if hasattr(SetupManager, 'startup_bot_agents'):
                    method_name = 'startup_bot_agents'
                elif hasattr(SetupManager, 'start_bot_agents'):
                    method_name = 'start_bot_agents'
                elif hasattr(SetupManager, 'load_config'):
                    method_name = 'load_config'
                else:
                    logger.error("No compatible startup method found in SetupManager")
                    return False
                    
                logger.info(f"Using SetupManager method: {method_name}")
                
            except ImportError as e:
                logger.error(f"Failed to import RLBot: {e}")
                logger.info("RLBot may not be compatible with Python 3.13. Consider using Python 3.11 or 3.12")
                return False
            
            logger.info("Attempting to attach bot to online match...")
            
            config_path = self.create_rlbot_config(online_mode=True)
            
            setup_manager = SetupManager()
            
            agent_config = {
                'name': self.bot_config.get('name', 'Nexto'),
                'team': self.bot_config.get('team', 0),
                'config_path': str(self.config_file.absolute()),
                'python_file': str(self.python_file.absolute())
            }
            
            logger.info("Waiting for online match to attach to...")
            
            if method_name == 'startup_bot_agents':
                setup_manager.startup_bot_agents([agent_config])
            elif method_name == 'start_bot_agents':
                setup_manager.start_bot_agents([agent_config])
            elif method_name == 'load_config':
                setup_manager.load_config(config_path)
            
            self.is_running = True
            logger.info("Bot successfully configured for online match attachment!")
            logger.info("Join a custom/private match in Rocket League to see the bot")
            logger.info("Note: Only works with matches that allow bots")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to inject bot for online play: {e}")
            logger.info("Troubleshooting tips:")
            logger.info("1. Make sure you're in a custom/private match that allows bots")
            logger.info("2. Consider using Python 3.11 or 3.12 for better RLBot compatibility")
            logger.info("3. Try using --use-gui option for alternative injection method")
            return False
    
    def inject_bot_exhibition(self) -> bool:
        """Inject bot for exhibition/offline play"""
        try:
            config_path = self.create_rlbot_config(online_mode=False)
            
            from rlbot.setup_manager import SetupManager
            from rlbot.utils.logging_utils import get_logger
            
            setup_manager = SetupManager()
            setup_manager.startup_bot_agents([{
                'name': self.bot_config.get('name', 'Nexto'),
                'team': self.bot_config.get('team', 0),
                'config_path': str(self.config_file.absolute()),
                'python_file': str(self.python_file.absolute())
            }])
            
            self.is_running = True
            logger.info("Bot successfully injected for exhibition play!")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to inject bot for exhibition play: {e}")
            return False
    
    def inject_via_rlbot_gui(self, online_mode: bool = False) -> bool:
        """Alternative injection method using RLBot GUI"""
        try:
            logger.info(f"Attempting injection via RLBot GUI ({'online' if online_mode else 'exhibition'} mode)...")
            
            config_path = self.create_rlbot_config(online_mode=online_mode)
            rlbot_command = [
                sys.executable, "-m", "rlbot_gui", 
                "--config", config_path
            ]
            
            if online_mode:
                rlbot_command.extend(["--attach-mode", "true"])
            
            self.rlbot_process = subprocess.Popen(
                rlbot_command,
                cwd=str(self.bot_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            if online_mode:
                logger.info("RLBot GUI launched in online mode. Bot will attach to existing matches.")
                logger.info("⚠️  Make sure you're in a custom/private match that allows bots!")
            else:
                logger.info("RLBot GUI launched in exhibition mode. Bot should be available in the interface.")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to launch RLBot GUI: {e}")
            return False
    
    def monitor_bot(self):
        """Monitor the bot process and restart if needed"""
        while self.is_running:
            try:
                if not self.is_rocket_league_running():
                    logger.warning("Rocket League process not found. Bot may have been disconnected.")
                
                time.sleep(10)
                
            except KeyboardInterrupt:
                logger.info("Bot monitoring interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error in bot monitoring: {e}")
                time.sleep(5)
    
    def stop(self):
        """Stop the bot and clean up"""
        logger.info("Stopping Nexto bot loader...")
        self.is_running = False
        
        if self.rlbot_process:
            try:
                self.rlbot_process.terminate()
                self.rlbot_process.wait(timeout=10)
            except:
                self.rlbot_process.kill()
        
        if self.bot_process:
            try:
                self.bot_process.terminate()
                self.bot_process.wait(timeout=10)
            except:
                self.bot_process.kill()
        
        logger.info("Bot loader stopped")
    
    def run(self, wait_for_rl: bool = True, use_gui: bool = False, online_mode: bool = False):
        """Main entry point to run the bot loader"""
        logger.info("=" * 50)
        logger.info(f"NEXTO BOT LOADER STARTING ({'ONLINE' if online_mode else 'EXHIBITION'} MODE)")
        logger.info("=" * 50)
        
        if online_mode:
            logger.info("Online Mode: Bot will attach to existing online matches")
            logger.info("Note: Only works with custom/private matches that allow bots")
        else:
            logger.info("Exhibition Mode: Bot will work in offline/exhibition matches")
        
        self.online_mode = online_mode
        
        if not self.check_dependencies():
            logger.error("Dependency check failed. Please install requirements.")
            return False
        
        if wait_for_rl and not self.is_rocket_league_running():
            if not self.wait_for_rocket_league():
                logger.error("Failed to detect Rocket League. Please start the game first.")
                return False
        
        logger.info("Waiting for Rocket League to fully load...")
        time.sleep(5)
        
        success = False
        if use_gui:
            success = self.inject_via_rlbot_gui(online_mode=online_mode)
        else:
            success = self.inject_bot(online_mode=online_mode)
        
        if not success:
            logger.error("Bot injection failed!")
            return False
        
        monitor_thread = threading.Thread(target=self.monitor_bot, daemon=True)
        monitor_thread.start()
        
        if online_mode:
            logger.info("Bot loader running in ONLINE mode. Join a custom/private match to see the bot!")
        else:
            logger.info("Bot loader running in EXHIBITION mode. Start an exhibition match to see the bot!")
        
        logger.info("Press Ctrl+C to stop.")
        
        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutdown requested by user")
        finally:
            self.stop()
        
        return True


def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(description="Nexto Bot Loader for Rocket League")
    parser.add_argument("--bot-path", type=str, help="Path to bot directory", default=None)
    parser.add_argument("--no-wait", action="store_true", help="Don't wait for Rocket League to start")
    parser.add_argument("--use-gui", action="store_true", help="Use RLBot GUI for injection")
    parser.add_argument("--team", type=int, choices=[0, 1], help="Team (0=Blue, 1=Orange)", default=0)
    parser.add_argument("--online", action="store_true", help="Enable online play mode (attach to existing matches)")
    
    args = parser.parse_args()
    
    loader = NextoBotLoader(bot_path=args.bot_path)
    
    if hasattr(args, 'team'):
        loader.bot_config['team'] = args.team
    
    try:
        success = loader.run(
            wait_for_rl=not args.no_wait, 
            use_gui=args.use_gui,
            online_mode=args.online
        )
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()