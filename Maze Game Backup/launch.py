#!/usr/bin/env python3
import os
import sys

# Change to the directory where this script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Import and run the game
from maze_game import MazeGame

if __name__ == "__main__":
    game = MazeGame()
    game.run() 