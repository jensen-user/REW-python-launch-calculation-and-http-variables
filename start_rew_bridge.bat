@echo off
REM REW SPL Meter Bridge Startup Script for Windows
REM Run this once as Administrator to set up firewall rule, then it can run normally

REM Check if firewall rule exists, if not create it (requires admin)
netsh advfirewall firewall show rule name="REW SPL Bridge" >nul 2>&1
if %errorlevel% neq 0 (
    echo Adding firewall rule for REW SPL Bridge...
    netsh advfirewall firewall add rule name="REW SPL Bridge" dir=in action=allow protocol=tcp localport=8080 program="%~dp0rew_bridge.py" description="Allow Bitfocus Companion to connect to REW SPL Bridge"
    if %errorlevel% neq 0 (
        echo WARNING: Could not add firewall rule. Run this script as Administrator once.
    ) else (
        echo Firewall rule added successfully.
    )
)

cd /d "%~dp0"
pythonw rew_bridge.py
