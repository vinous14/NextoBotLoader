#!/usr/bin/env python3
"""
Nexto Bot Setup Script
Quick setup and verification script for the Nexto bot loader.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    print("=" * 60)
    print("🚀 NEXTO BOT SETUP & VERIFICATION")
    print("=" * 60)
    print()

def check_python():
    """Check Python version"""
    print("📋 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ required")
        return False
    
    print("✅ Python version OK")
    return True

def check_files():
    """Check required files"""
    print("\n📁 Checking required files...")
    
    required_files = [
        "bot.py", "bot.cfg", "requirements.txt", 
        "agent.py", "nexto_obs.py", "__init__.py", "loader.py"
    ]
    
    missing = []
    for file in required_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
            missing.append(file)
    
    if missing:
        print(f"\n❌ Missing files: {', '.join(missing)}")
        return False
    
    print("✅ All required files found")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False

def verify_imports():
    """Verify key imports work"""
    print("\n🔍 Verifying imports...")
    
    imports = [
        ("rlbot", "RLBot framework"),
        ("torch", "PyTorch"),
        ("numpy", "NumPy"),
        ("rlgym_compat", "RLGym compatibility"),
        ("psutil", "Process utilities")
    ]
    
    for module, name in imports:
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError as e:
            print(f"   ❌ {name}: {e}")
            return False
    
    print("✅ All imports successful")
    return True

def test_loader():
    """Test the loader functionality"""
    print("\n🧪 Testing loader functionality...")
    
    try:
        from loader import NextoBotLoader
        
        loader = NextoBotLoader()
        print("   ✅ Loader class imported")
        
        if loader.check_dependencies(auto_install=False):
            print("   ✅ Dependency check passed")
        else:
            print("   ❌ Dependency check failed")
            return False
        
        if loader.bot_config:
            print(f"   ✅ Configuration loaded: {loader.bot_config.get('name', 'Unknown')}")
        else:
            print("   ❌ Configuration loading failed")
            return False
        
        print("✅ Loader functionality verified")
        return True
        
    except Exception as e:
        print(f"❌ Loader test failed: {e}")
        return False

def show_usage():
    """Show usage instructions"""
    print("\n📚 USAGE INSTRUCTIONS:")
    print("-" * 30)
    print()
    print("🎮 Basic Usage:")
    print("   python loader.py")
    print()
    print("⚙️  Advanced Options:")
    print("   python loader.py --team 1          # Orange team")
    print("   python loader.py --no-wait         # Don't wait for RL")
    print("   python loader.py --use-gui         # Use RLBot GUI")
    print()
    print("🖱️  Windows Users:")
    print("   Double-click: launch_nexto.bat")
    print()
    print("🚀 Next Steps:")
    print("   1. Start Rocket League")
    print("   2. Run the loader")
    print("   3. Bot will automatically inject!")
    print()

def main():
    print_header()
    
    checks = [
        ("Python Version", check_python),
        ("Required Files", check_files),
        ("Dependencies", install_dependencies),
        ("Import Verification", verify_imports),
        ("Loader Test", test_loader)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        if not check_func():
            all_passed = False
            break
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("🎉 SETUP COMPLETE! Nexto bot is ready to use.")
        show_usage()
    else:
        print("❌ SETUP FAILED! Please fix the issues above.")
        print("\n💡 Common solutions:")
        print("   • Ensure Python 3.7+ is installed")
        print("   • Run: pip install -r requirements.txt")
        print("   • Check that all bot files are present")
    
    print("=" * 60)

if __name__ == "__main__":
    main()