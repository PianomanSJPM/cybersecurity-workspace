#!/bin/bash

# =============================================================================
# MAZE NAVIGATOR GAME - LAUNCH SCRIPT
# =============================================================================
# Developer: Stephen Miller
# Version: 1.0
# Description: Comprehensive launch script for Maze Navigator Speed Challenge
# =============================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Game information
GAME_NAME="Maze Navigator - Speed Challenge"
GAME_FILE="maze_game.py"
GAME_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to print colored output
print_header() {
    echo -e "${PURPLE}"
    echo "============================================================================="
    echo "                    MAZE NAVIGATOR - SPEED CHALLENGE"
    echo "============================================================================="
    echo -e "${NC}"
}

print_info() {
    echo -e "${CYAN}$1${NC}"
}

print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_warning() {
    echo -e "${YELLOW}$1${NC}"
}

print_error() {
    echo -e "${RED}$1${NC}"
}

# Function to check if Python is available
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        return 0
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        return 0
    else
        return 1
    fi
}

# Function to check if pygame is installed
check_pygame() {
    if $PYTHON_CMD -c "import pygame" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Function to install pygame
install_pygame() {
    print_warning "Installing pygame..."
    if command -v pip3 &> /dev/null; then
        pip3 install pygame
    elif command -v pip &> /dev/null; then
        pip install pygame
    else
        print_error "Please install pygame manually: pip install pygame"
        return 1
    fi
}

# Function to show game information
show_game_info() {
    print_header
    echo -e "${BLUE}Game Information:${NC}"
    echo "  • Name: $GAME_NAME"
    echo "  • Developer: Stephen Miller"
    echo "  • Version: 1.0"
    echo "  • File: $GAME_FILE"
    echo "  • Directory: $GAME_DIR"
    echo ""
    echo -e "${BLUE}Game Features:${NC}"
    echo "  • Dynamic maze generation with multiple algorithms"
    echo "  • Progressive difficulty system"
    echo "  • Timer-based challenge with 10-maze reset cycles"
    echo "  • High score system with arcade-style input"
    echo "  • Fullscreen support and dynamic scaling"
    echo "  • Comprehensive menu system"
    echo ""
    echo -e "${BLUE}Controls:${NC}"
    echo "  • Arrow Keys: Move player"
    echo "  • SPACEBAR: Continue to next maze"
    echo "  • M: Open menu"
    echo "  • ENTER: Select menu option"
    echo "  • BACKSPACE: Return to previous screen"
    echo "  • Q: Quit game"
    echo ""
}

# Function to check system requirements
check_requirements() {
    print_info "Checking system requirements..."
    
    if check_python; then
        print_success "✓ Python found: $($PYTHON_CMD --version)"
    else
        print_error "✗ Python not found"
        return 1
    fi
    
    if check_pygame; then
        print_success "✓ Pygame is installed"
    else
        print_warning "✗ Pygame is not installed"
        return 1
    fi
    
    if [ -f "$GAME_FILE" ]; then
        print_success "✓ Game file found"
    else
        print_error "✗ Game file not found"
        return 1
    fi
    
    return 0
}

# Function to launch game normally
launch_game() {
    print_info "Launching $GAME_NAME..."
    cd "$GAME_DIR"
    $PYTHON_CMD "$GAME_FILE"
}

# Function to launch game with debug output
launch_debug() {
    print_info "Launching with debug output..."
    cd "$GAME_DIR"
    $PYTHON_CMD "$GAME_FILE" 2>&1 | tee game_debug.log
}

# Function to show launch options
show_menu() {
    echo -e "${BLUE}Launch Options:${NC}"
    echo "  1) Launch game"
    echo "  2) Launch with debug output"
    echo "  3) Show game information"
    echo "  4) Check requirements"
    echo "  5) Install dependencies"
    echo "  6) Exit"
    echo ""
}

# Main menu function
main_menu() {
    while true; do
        show_menu
        read -p "Select option (1-6): " choice
        
        case $choice in
            1)
                if check_requirements > /dev/null 2>&1; then
                    launch_game
                else
                    print_error "Requirements not met. Check requirements first."
                fi
                break
                ;;
            2)
                if check_requirements > /dev/null 2>&1; then
                    launch_debug
                else
                    print_error "Requirements not met. Check requirements first."
                fi
                break
                ;;
            3)
                show_game_info
                ;;
            4)
                check_requirements
                ;;
            5)
                install_pygame
                ;;
            6)
                print_info "Goodbye!"
                exit 0
                ;;
            *)
                print_error "Invalid option. Please select 1-6."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
        clear
    done
}

# Function to handle command line arguments
handle_arguments() {
    case "$1" in
        --info|-i)
            show_game_info
            exit 0
            ;;
        --check|-c)
            check_requirements
            exit $?
            ;;
        --install|-I)
            install_pygame
            exit $?
            ;;
        --debug|-d)
            if check_requirements > /dev/null 2>&1; then
                launch_debug
            else
                print_error "Requirements not met."
                exit 1
            fi
            exit 0
            ;;
        --help|-h)
            echo "Usage: $0 [OPTION]"
            echo ""
            echo "Options:"
            echo "  --info, -i        Show game information"
            echo "  --check, -c       Check system requirements"
            echo "  --install, -I     Install dependencies"
            echo "  --debug, -d       Launch with debug output"
            echo "  --help, -h        Show this help message"
            echo ""
            echo "If no option is provided, the interactive menu will be shown."
            exit 0
            ;;
        "")
            # No arguments, show interactive menu
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information."
            exit 1
            ;;
    esac
}

# Main execution
main() {
    # Handle command line arguments
    handle_arguments "$1"
    
    # Show interactive menu if no arguments provided
    main_menu
}

# Run main function with all arguments
main "$@" 