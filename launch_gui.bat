@echo off
:: Quick launcher for Nexto Bot GUI
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    start "Nexto Bot GUI" ".venv\Scripts\python.exe" gui.py
) else (
    start "Nexto Bot GUI" python gui.py
)