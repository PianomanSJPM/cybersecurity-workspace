#!/bin/bash

# Maze Navigator - Double-Click Launcher
# Users can simply double-click this file to play the game

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}"
echo "============================================================================="
echo "                    MAZE NAVIGATOR - SPEED CHALLENGE"
echo "============================================================================="
echo -e "${NC}"

echo -e "${BLUE}Starting Maze Navigator...${NC}"

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo -e "${GREEN}✓ Python 3 found${NC}"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo -e "${GREEN}✓ Python found${NC}"
else
    echo -e "${RED}✗ Python is not installed on this system${NC}"
    echo -e "${YELLOW}Please install Python 3.6 or higher from python.org${NC}"
    echo ""
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

# Check if pygame is installed
if $PYTHON_CMD -c "import pygame" 2>/dev/null; then
    echo -e "${GREEN}✓ Pygame is installed${NC}"
else
    echo -e "${YELLOW}Installing pygame...${NC}"
    if command -v pip3 &> /dev/null; then
        pip3 install pygame
    elif command -v pip &> /dev/null; then
        pip install pygame
    else
        echo -e "${RED}✗ Could not install pygame automatically${NC}"
        echo -e "${YELLOW}Please install pygame manually: pip install pygame${NC}"
        echo ""
        echo "Press any key to exit..."
        read -n 1
        exit 1
    fi
fi

# Check if game file exists
if [ -f "maze_game.py" ]; then
    echo -e "${GREEN}✓ Game file found${NC}"
else
    echo -e "${RED}✗ Game file not found${NC}"
    echo ""
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

echo ""
echo -e "${GREEN}Launching Maze Navigator...${NC}"
echo -e "${BLUE}Enjoy the game!${NC}"
echo ""

# Launch the game
$PYTHON_CMD maze_game.py

# Keep terminal open if there's an error
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}Game ended with an error.${NC}"
    echo "Press any key to exit..."
    read -n 1
fi 