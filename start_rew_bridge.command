#!/bin/bash
# REW SPL Meter Bridge Startup Script for macOS
# Add this to System Settings → General → Login Items for autostart

cd "$(dirname "$0")"
python3 rew_bridge.py
