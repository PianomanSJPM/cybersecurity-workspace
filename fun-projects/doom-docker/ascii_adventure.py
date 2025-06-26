#!/usr/bin/env python3
"""
ASCII Adventure Game
A simple text-based adventure game that runs in Docker
"""

import random
import time
import os

def clear_screen():
    """Clear the terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")

def print_ascii_art():
    """Print the game's ASCII art header."""
    art = """
    ╔══════════════════════════════════════╗
    ║         🎮 ASCII ADVENTURE 🎮         ║
    ║                                      ║
    ║  You are in a mysterious dungeon!    ║
    ║  Find the treasure and escape!       ║
    ║                                      ║
    ║  Commands:                           ║
    ║  - look: Look around                 ║
    ║  - move: Move to next room           ║
    ║  - search: Search for items          ║
    ║  - quit: Exit game                   ║
    ╚══════════════════════════════════════╝
    """
    print(art)

def main():
    """Main game loop."""
    clear_screen()
    print_ascii_art()
    print("\n🎮 Welcome to ASCII Adventure!")
    print("🎯 Type commands to explore the dungeon.")
    print("🚪 Type 'quit' to exit.\n")
    
    room = 1
    treasure_found = False
    moves = 0
    
    while True:
        command = input("🎮 What would you like to do? ").lower().strip()
        moves += 1
        
        if command == "quit":
            print("👋 Thanks for playing!")
            break
        elif command == "look":
            if room == 1:
                print("👀 You see a dark stone room with ancient walls.")
                print("🚪 There is a door to the north.")
            elif room == 2:
                print("👀 You are in a treasure chamber!")
                print("💎 There is a golden chest in the corner.")
        elif command == "move":
            if room == 1:
                room = 2
                print("🚶 You move to the next room.")
            else:
                print("🚪 You are already in the treasure room!")
        elif command == "search":
            if room == 2 and not treasure_found:
                treasure_found = True
                print("💎 You found the treasure! You win!")
                print(f"🎯 Moves taken: {moves}")
                break
            else:
                print("🔍 You search but find nothing.")
        else:
            print("❓ Unknown command. Try: look, move, search, or quit")

if __name__ == "__main__":
    main() 