Room EQ Wizard (REW) offers an SPL meter with API access limited to localhost, providing real-time SPL A-weighted readings like "slow" (1s time constant), 1-minute Leq, and 10-minute Leq, but lacks direct support for 2-minute or 15-minute averages. Your setup bridges this by running REW headless (no GUI) on one computer via a Python script that launches it, polls these API values twice per second, computes custom averages (e.g., rolling SPL A 2min and 15min from logged data or API Leq), and exposes them as HTTP endpoints for Bitfocus Companion on another computer. The script also accepts HTTP commands from Companion to start/stop measurements, restart REW, or shut it down entirely.
​

Core Components
REW SPL Meter: Use its built-in logging to a local folder (typically CSV/TSV files updated periodically, often every few seconds during active metering) for historical data to calculate custom Leq periods like 2min/15min via simple RMS averaging in Python. Real-time API (e.g., via REW's HTTP server on port 4823) delivers SPL A slow, 1min Leq, and 10min Leq directly—no GUI needed if launched with command-line flags like REW -m for SPL metering mode.
​

Python Bridge Script: A lightweight Flask/FastAPI server running alongside REW. It spawns REW as a subprocess, queries the localhost API or tails log files every 500ms, maintains rolling averages (e.g., using a deque for fixed-window RMS calc: SPL_Leq = 10*log10(mean(10^(SPL_i/10)))), and serves JSON like {"spl_a_slow": 75.2, "spl_a_2min": 74.8, "spl_a_15min": 73.1} at /api/spl. Logs confirm update frequency (user observation: likely 1-10s intervals, parseable for precision).

Bitfocus Companion Integration: On the remote computer, Companion pulls variables via HTTP GET to the Python server's IP:port (e.g., http://rew-host:8080/api/spl), mapping them to buttons/feedback. Send POST to /api/control with JSON payloads like {"action": "start_measuring"} for commands.

Control Commands
HTTP POST to /api/control handles these, with the script proxying to REW:

Start REW & Measure: Launch REW process if not running, enable SPL meter via API (e.g., POST to REW's /spl/start), begin logging.

Restart REW: Kill/relaunch subprocess, reset averages/logs.

Close REW: Graceful shutdown via API or SIGTERM, stop HTTP updates.

Calculation Confirmation
REW's API exposes exactly SPL A Slow, SPL A 1min (Leq), and SPL A 10min (Leq)—no native 2min/15min, so Python must compute them. Use REW logs (e.g., parse timestamped SPL rows into pandas deque, compute Leq as above) or buffer API "slow" readings (deque of 240 for 2min at 2Hz, 1800 for 15min). Logs are reliable for long averages since they're persistent; API suits real-time slow reading.
​

Implementation Sketch
Install REW (Java-based), enable API in prefs (-Djava.awt.headless=true for no GUI).

Python deps: flask, requests, pandas, subprocess, collections.deque.

Script loop: while True: poll_rew_api_or_logs(), calc_averages(), expose_json(), sleep(0.5).

Run as service (e.g., systemd) on REW host; secure with auth token if networked.

This creates a robust, low-latency SPL monitoring/control system for live audio setups, like concert mixing in your Århus location.