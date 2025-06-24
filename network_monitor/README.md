# Network Activity Monitor

A Python-based network monitoring tool that captures and displays network activity on your home network. This tool provides a clean user interface to monitor:
- Device connections
- Network traffic
- Connection duration
- Protocol information
- Data transfer sizes

## Prerequisites

- macOS (tested on MacBook Air)
- Python 3.x
- Homebrew
- Suricata
- Required Python packages (installed automatically in virtual environment):
  - scapy
  - pyshark
  - pandas
  - tkinter (usually comes with Python)

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Create and activate the virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Activate the virtual environment if not already activated:
   ```bash
   source venv/bin/activate
   ```

2. Run the network monitor:
   ```bash
   python network_monitor.py
   ```

3. Use the interface:
   - Click "Start Monitoring" to begin capturing network traffic
   - Click "Stop Monitoring" to stop capturing
   - Click "Save Data" to export the captured data to a CSV file

## Features

- Real-time network traffic monitoring
- Clean, user-friendly interface
- Detailed packet information including:
  - Timestamp
  - Source IP
  - Destination IP
  - Protocol
  - Packet length
  - Connection duration
- Data export to CSV format
- Thread-safe packet processing
- Scrollable interface for large amounts of data

## Security Note

This tool requires root/administrator privileges to capture network packets. Run with appropriate permissions:

```bash
sudo python network_monitor.py
```

## Data Storage

Captured data is stored in memory during the session and can be exported to CSV files. The CSV files are named with the format: `network_data_YYYYMMDD_HHMMSS.csv`

## Troubleshooting

If you encounter permission issues:
1. Ensure you're running the script with sudo
2. Check that your user has the necessary permissions to capture network traffic
3. Verify that Suricata is properly installed and configured

For any other issues, check the console output for error messages. 