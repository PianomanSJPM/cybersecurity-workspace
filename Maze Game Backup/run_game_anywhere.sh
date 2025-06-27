#!/bin/bash

# Get the absolute path to this script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if we're in the right place
if [ ! -f "maze_game.py" ]; then
    echo "ERROR: maze_game.py not found in $(pwd)"
    echo "This script should be in the same directory as maze_game.py"
    exit 1
fi

# Check if pygame is installed
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "Installing pygame..."
    pip3 install pygame
fi

# Run the game
echo "Starting Maze Navigator from: $(pwd)"
python3 maze_game.py 