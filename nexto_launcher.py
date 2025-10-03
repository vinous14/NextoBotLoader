#!/usr/bin/env python3
"""
Nexto Bot Launcher
Main entry point that can launch either GUI or command line version.
"""

import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Nexto Bot Launcher")
    parser.add_argument("--gui", action="store_true", help="Launch GUI version")
    parser.add_argument("--cli", action="store_true", help="Launch command line version")
    parser.add_argument("--setup", action="store_true", help="Run setup and verification")
    
    # If no arguments, try to detect best mode
    if len(sys.argv) == 1:
        # Default to GUI if available, otherwise CLI
        try:
            import tkinter
            args = argparse.Namespace(gui=True, cli=False, setup=False)
        except ImportError:
            args = argparse.Namespace(gui=False, cli=True, setup=False)
    else:
        args = parser.parse_args()
    
    # Run setup if requested
    if args.setup:
        from setup import main as setup_main
        setup_main()
        return
    
    # Launch GUI version
    if args.gui:
        try:
            import tkinter
            from gui import main as gui_main
            print("🚀 Launching Nexto Bot Loader GUI...")
            gui_main()
        except ImportError:
            print("❌ GUI not available (tkinter not installed)")
            print("💡 Falling back to command line mode...")
            args.cli = True
        except Exception as e:
            print(f"❌ GUI launch failed: {e}")
            print("💡 Falling back to command line mode...")
            args.cli = True
    
    # Launch CLI version
    if args.cli:
        from loader import main as loader_main
        print("🚀 Launching Nexto Bot Loader (Command Line)...")
        loader_main()

if __name__ == "__main__":
    main()