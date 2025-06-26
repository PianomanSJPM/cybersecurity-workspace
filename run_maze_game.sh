#!/bin/bash

# Universal Maze Game Launcher
# This script works from ANY directory

# Get the absolute path to the Cybersecurity directory
CYBERSECURITY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GAME_DIR="$CYBERSECURITY_DIR/fun-projects/maze-game"

echo "🔍 Looking for maze game in: $GAME_DIR"

# Check if game directory exists
if [ ! -d "$GAME_DIR" ]; then
    echo "❌ ERROR: Game directory not found at $GAME_DIR"
    echo "Please make sure the maze game is installed in fun-projects/maze-game/"
    exit 1
fi

# Check if game file exists
if [ ! -f "$GAME_DIR/maze_game.py" ]; then
    echo "❌ ERROR: maze_game.py not found in $GAME_DIR"
    exit 1
fi

# Change to game directory
cd "$GAME_DIR"
echo "✅ Found maze game in: $(pwd)"

# Check if pygame is installed
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "📦 Installing pygame..."
    pip3 install pygame
fi

# Run the game
echo "🎮 Starting Maze Navigator..."
python3 maze_game.py 