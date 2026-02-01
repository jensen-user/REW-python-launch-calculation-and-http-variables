@echo off
REM REW SPL Meter Bridge Startup Script for Windows
REM Copy this to shell:startup folder for autostart

cd /d "%~dp0"
pythonw rew_bridge.py
