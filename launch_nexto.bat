@echo off
:: Nexto Bot Loader - Windows Batch Script
:: This script provides an easy way to launch # Build command arguments
set args=--team %team%
if /i "%wait_rl%"=="n" set args=%args% --no-wait
if /i "%use_gui%"=="y" set args=%args% --use-gui
if /i "%online_mode%"=="y" set args=%args% --online

echo.
echo Starting Nexto bot loader...
echo Team: %team% (0=Blue, 1=Orange)
echo Wait for RL: %wait_rl%
echo Use GUI: %use_gui%
echo Online Mode: %online_mode%
echo.ot into Rocket League

echo ================================================
echo          NEXTO BOT LOADER FOR ROCKET LEAGUE
echo ================================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

:: Check if we're in the right directory
if not exist "bot.py" (
    echo ERROR: bot.py not found in current directory
    echo Please run this script from the Nexto bot directory
    pause
    exit /b 1
)

:: Ask user for interface preference
echo Select interface:
echo 1. GUI (Graphical Interface) - Recommended
echo 2. Command Line Interface
echo 3. Setup & Verify Installation
echo.
set /p interface="Enter choice (1-3) [1]: "
if "%interface%"=="" set interface=1

if "%interface%"=="3" (
    echo.
    echo Running setup and verification...
    if exist ".venv\Scripts\python.exe" (
        .venv\Scripts\python.exe setup.py
    ) else (
        python setup.py
    )
    pause
    exit /b 0
)

if "%interface%"=="1" (
    echo.
    echo Launching GUI...
    if exist ".venv\Scripts\python.exe" (
        .venv\Scripts\python.exe nexto_launcher.py --gui
    ) else (
        python nexto_launcher.py --gui
    )
    pause
    exit /b 0
)

:: Command line interface (original behavior)
echo.
echo Launching command line interface...

:: Check if requirements are installed
echo Checking dependencies...
python -c "import rlbot" >nul 2>&1
if errorlevel 1 (
    echo Installing requirements...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install requirements
        pause
        exit /b 1
    )
)

echo Dependencies OK!
echo.

:: Ask user for preferences
set /p team="Enter team (0 for Blue, 1 for Orange) [0]: "
if "%team%"=="" set team=0

set /p wait_rl="Wait for Rocket League to start? (y/n) [y]: "
if "%wait_rl%"=="" set wait_rl=y

set /p use_gui="Use RLBot GUI? (y/n) [n]: "
if "%use_gui%"=="" set use_gui=n

set /p online_mode="Enable online mode? (y/n) [n]: "
if "%online_mode%"=="" set online_mode=n

if /i "%online_mode%"=="y" (
    echo.
    echo WARNING: Online mode only works with custom/private matches!
    echo - Does NOT work with ranked/casual matchmaking
    echo - Host must allow bots in match settings
    echo.
    pause
)

:: Build command arguments
set args=--team %team%
if /i "%wait_rl%"=="n" set args=%args% --no-wait
if /i "%use_gui%"=="y" set args=%args% --use-gui

echo.
echo Starting Nexto bot loader...
echo Team: %team% (0=Blue, 1=Orange)
echo Wait for RL: %wait_rl%
echo Use GUI: %use_gui%
echo.

:: Launch the loader (use virtual environment if available)
if exist ".venv\Scripts\python.exe" (
    echo Using virtual environment...
    .venv\Scripts\python.exe loader.py %args%
) else (
    echo Using system Python...
    python loader.py %args%
)

echo.
echo Bot loader finished.
pause