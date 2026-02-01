# REW SPL Meter Bridge

A Python bridge that launches REW (Room EQ Wizard) headlessly, reads SPL values from REW's API, and exposes them via HTTP for Bitfocus Companion integration.

## Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│      REW        │◄───────►│  Python Bridge  │◄───────►│    Companion    │
│  (localhost)    │  :4735  │   (FastAPI)     │  :8080  │   (remote PC)   │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

## Features

- Launches REW automatically with API mode enabled
- Subscribes to real-time SPL meter updates
- Computes 2-minute rolling Leq (not natively available in REW)
- Exposes values via simple HTTP API for Bitfocus Companion
- Control commands: start, stop, restart, shutdown

## Available Values

| Value | Source |
|-------|--------|
| SPL A Slow | Direct from REW API |
| 2-min Leq | Computed from buffered SPL readings |
| 15-min Leq | Direct from REW API (rolling Leq) |

## Requirements

- Python 3.8+
- REW (Room EQ Wizard) installed
  - **macOS**: REW.app in `/Applications`
  - **Windows**: REW in `C:\Program Files\REW`

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Start the Bridge

```bash
python rew_bridge.py
```

The bridge will:
1. Launch REW with `-api -nogui` flags
2. Wait for REW's API to become available
3. Configure the SPL meter (A-weighting, Slow filter, 15-min rolling Leq)
4. Subscribe to SPL meter updates
5. Start the HTTP server on port 8080

### API Endpoints

#### GET /api/spl

Returns current SPL values:

```json
{
  "spl_a_slow": 75.2,
  "leq_2min": 74.8,
  "leq_15min": 73.1,
  "elapsed_time": 125.5,
  "valid_2min": true,
  "rew_running": true,
  "measurement_active": true,
  "buffer_samples": 1200,
  "buffer_seconds": 120.0
}
```

#### POST /api/control

Control the SPL meter:

```bash
# Start measurement
curl -X POST http://localhost:8080/api/control \
  -H "Content-Type: application/json" \
  -d '{"action":"start"}'

# Stop measurement
curl -X POST http://localhost:8080/api/control \
  -H "Content-Type: application/json" \
  -d '{"action":"stop"}'

# Restart REW
curl -X POST http://localhost:8080/api/control \
  -H "Content-Type: application/json" \
  -d '{"action":"restart"}'

# Shutdown REW
curl -X POST http://localhost:8080/api/control \
  -H "Content-Type: application/json" \
  -d '{"action":"shutdown"}'
```

#### GET /health

Health check endpoint:

```json
{
  "status": "healthy",
  "rew_running": true,
  "last_update": 1234567890.123,
  "seconds_since_update": 0.5
}
```

## Autostart on Boot

### macOS

1. Make the script executable: `chmod +x start_rew_bridge.command`
2. Go to System Settings → General → Login Items
3. Add `start_rew_bridge.command`

### Windows

1. **First time only**: Right-click `start_rew_bridge.bat` → "Run as administrator" (this creates the firewall rule)
2. Press `Win+R`, type `shell:startup`, press Enter
3. Copy `start_rew_bridge.bat` to that folder

## Bitfocus Companion Integration

Use the Generic HTTP module in Companion to poll `/api/spl` and display values.

Example variable parsing:
- `$.spl_a_slow` - Current SPL
- `$.leq_2min` - 2-minute Leq
- `$.leq_15min` - 15-minute Leq

## Firewall Notes

- **Windows**: The startup script automatically adds a firewall rule when run as Administrator the first time. If you need to add it manually:
  ```
  netsh advfirewall firewall add rule name="REW SPL Bridge" dir=in action=allow protocol=tcp localport=8080
  ```
- **macOS**: Allow incoming connections when prompted

## License

MIT
