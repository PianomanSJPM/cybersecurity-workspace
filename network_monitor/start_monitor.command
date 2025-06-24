#!/bin/bash

# Enable error handling
set -e

# Print debug information
echo "Starting network monitor..."
echo "Current directory: $(pwd)"

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Script directory: $DIR"

# Change to the script directory
cd "$DIR"
echo "Changed to directory: $(pwd)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/.requirements_installed" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
    touch venv/.requirements_installed
fi

# Run the network monitor with sudo
echo "Starting network monitor with sudo..."
sudo python3 network_monitor.py

# Deactivate virtual environment on exit
deactivate 