# 🧩 Maze Navigator - Speed Challenge

A sophisticated, feature-rich maze navigation game built with Python and Pygame. Navigate through progressively challenging mazes with balanced difficulty, customizable controls, and professional presentation!

## 🎮 Game Features

### **Core Gameplay**
- **Dynamic Maze Generation**: Three algorithms (Recursive, Kruskal, Prim) for varied gameplay
- **Progressive Difficulty**: Maze size increases every 5 levels (15×10 → 50×40 max)
- **Balanced Timer System**: 1-second reduction per maze, 20-second minimum, resets every 10 mazes
- **Multiple Control Schemes**: Arrow keys AND WASD support for accessibility
- **Movement Speed Adjustment**: Customizable player movement speed (0.05-0.15s per move)
- **Continuous Movement**: Smooth, responsive controls with key tracking

### **Professional Features**
- **High Score System**: Persistent leaderboard with arcade-style scrolling input
- **Menu System**: Context-aware menu with fullscreen toggle, settings, and navigation
- **Transition Screens**: Professional countdown between mazes
- **Dynamic UI**: Responsive interface that adapts to screen size
- **Fullscreen Support**: Seamless fullscreen/windowed mode toggle
- **Cross-Platform**: Works on macOS, Windows, and Linux

### **User Experience**
- **Multiple Launch Options**: Shell scripts, Python launchers, and platform-specific files
- **macOS App Bundle**: Professional .app file with custom icon
- **Docker Support**: Containerized deployment with X11 forwarding
- **Comprehensive Documentation**: Multiple README files for different use cases
- **Error Handling**: Robust fallback systems and user-friendly error messages

## 🎯 How to Play

1. **Start**: Launch the game using any of the provided methods
2. **Navigate**: Use arrow keys OR WASD to move through the maze
3. **Goal**: Reach the red square (exit) before time runs out
4. **Progression**: Mazes get larger and more challenging every 5 levels
5. **Timer Management**: Complete mazes efficiently - timer reduces by 1s per maze
6. **High Score**: Enter your initials if you achieve a top 10 score
7. **Customization**: Adjust movement speed and settings via the menu

## 📈 Difficulty Progression

| Maze Range | Size | Difficulty | Time Limit | Timer Reset |
|------------|------|------------|------------|-------------|
| 1-5        | 15×10 | Beginner   | 30s → 26s  | Every 10 mazes |
| 6-10       | 16×11 | Easy       | 25s → 21s  | Every 10 mazes |
| 11-15      | 17×12 | Medium     | 30s → 26s  | Every 10 mazes |
| 16-20      | 18×13 | Hard       | 25s → 21s  | Every 10 mazes |
| 21-25      | 19×14 | Expert     | 30s → 26s  | Every 10 mazes |
| 26-30      | 20×15 | Master     | 25s → 21s  | Every 10 mazes |
| ...        | ...   | ...        | ...        | ...         |
| 176+       | 50×40 | Ultimate   | 20s minimum| Every 10 mazes |

**Timer System**: Starts at 30s, reduces by 1s per maze, minimum 20s, resets every 10 mazes for player relief.

## 🚀 Installation & Setup

### **Method 1: Direct Python (Recommended)**
```bash
# Clone or download the project
cd fun-projects/maze-game

# Install dependencies
pip install -r requirements.txt

# Run the game
python3 maze_game.py
```

### **Method 2: Easy Launch Scripts**
```bash
# macOS/Linux
./run_game.sh
# or
./launch_maze_game.sh

# Windows
Play Maze Game.bat
```

### **Method 3: macOS App Bundle**
```bash
# Double-click the app bundle
open "Maze Navigator.app"
```

### **Method 4: Docker Container**
```bash
# Build and run with Docker
docker build -t maze-navigator .
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix maze-navigator
```

## 🎮 Controls

### **Movement**
| Key | Action |
|-----|--------|
| ↑ / W | Move Up |
| ↓ / S | Move Down |
| ← / A | Move Left |
| → / D | Move Right |

### **Game Controls**
| Key | Action |
|-----|--------|
| SPACE | Continue to next maze (when won) |
| M | Open/close game menu |
| ENTER | Select menu option |
| BACKSPACE | Return to previous screen |
| Q | Quit game |

### **Menu Navigation**
| Key | Action |
|-----|--------|
| ↑/↓ | Navigate menu options |
| ENTER | Select option |
| BACKSPACE | Return to previous screen |

## 🍔 Menu System

Press **M** to access the comprehensive game menu:

- **Full Screen**: Toggle between fullscreen and windowed mode
- **Toggle Transition Screen**: Enable/disable maze transition countdown
- **High Scores**: View the top 10 leaderboard
- **Controls**: Display control instructions
- **Adjust Movement Speed**: Customize player movement speed (0.05-0.15s per move)
- **Return to Title Screen**: Reset the game
- **Back to Game**: Return to current maze (when in game)
- **Quit Game**: Exit the application

## 🏅 High Score System

- **Persistent Storage**: Scores saved to `high_scores.json`
- **Top 10 Leaderboard**: Only the best scores are kept
- **Arcade-Style Input**: Scrolling character selection for initials
- **Rank Display**: See your position on the leaderboard
- **Automatic Detection**: High scores are detected automatically
- **36 Character Options**: A-Z and 0-9 for initials

## 🎨 Game Elements

- **🟦 Blue Square**: Your player character
- **🟩 Green Square**: Starting position
- **🟥 Red Square**: Exit/Goal
- **🟪 Purple Squares**: Walls (impassable)
- **⬜ White Squares**: Paths (walkable)
- **🎨 Dynamic Colors**: Difficulty indicators and timer colors

## 🛠️ Technical Architecture

### **Core Components**
- **MazeGame Class**: Main game logic and state management
- **HighScoreManager**: Persistent leaderboard functionality
- **Multiple Algorithms**: Recursive, Kruskal, and Prim maze generation
- **Dynamic Scaling**: Responsive UI that adapts to any screen size
- **Event-Driven Architecture**: Pygame event handling for smooth controls

### **Advanced Features**
- **Continuous Movement**: Key tracking for responsive controls
- **Timer System**: Sophisticated countdown with progression and resets
- **State Management**: Complex game state handling across multiple screens
- **Error Recovery**: Fallback algorithms and robust error handling
- **Performance Optimization**: 60 FPS gameplay with efficient rendering

### **Deployment Options**
- **Native Python**: Direct execution with dependency management
- **macOS App Bundle**: Professional .app with custom icon
- **Docker Container**: Containerized deployment with X11 support
- **Cross-Platform Scripts**: Platform-specific launch files
- **Virtual Environment**: Isolated dependency management

## 📊 Performance & Testing

### **Comprehensive Testing**
- **Timer Mechanics**: Verified progression and reset cycles
- **Difficulty Analysis**: Mathematical analysis of maze complexity
- **Route Analysis**: Longest possible path calculations
- **Performance Testing**: Frame rate and responsiveness validation
- **Cross-Platform Testing**: macOS, Windows, and Linux compatibility

### **Quality Assurance**
- **Debug Logging**: Comprehensive real-time monitoring
- **Error Handling**: Graceful fallbacks and user-friendly messages
- **State Validation**: Game state consistency checks
- **User Experience Testing**: Intuitive controls and feedback

## 🚀 Portfolio Value

This project demonstrates advanced software development skills:

### **Technical Excellence**
- **Python Mastery**: Advanced language features and best practices
- **Game Development**: Professional Pygame implementation
- **Algorithm Design**: Multiple maze generation algorithms
- **Software Architecture**: Clean, maintainable code structure
- **Performance Optimization**: Efficient rendering and state management

### **Professional Development**
- **Version Control**: Complete git workflow with meaningful commits
- **Documentation**: Comprehensive README files and code comments
- **Testing**: Systematic testing and validation methodology
- **Deployment**: Multiple deployment strategies and containerization
- **User Experience**: Accessibility and user-centered design

### **Creative Problem Solving**
- **Game Balance**: Mathematical difficulty progression systems
- **User Interface**: Intuitive controls and visual feedback
- **Cross-Platform**: Compatibility across different operating systems
- **Performance Analysis**: Data-driven optimization decisions

## 🔧 Customization & Extensibility

### **Easy Enhancements**
- **Sound System**: Audio feedback and background music
- **Additional Themes**: Visual themes and color schemes
- **Power-ups**: Special abilities or shortcuts
- **Achievement System**: Unlockable achievements and milestones

### **Advanced Features**
- **Level Editor**: Create and share custom mazes
- **Multiplayer Support**: Competitive or cooperative modes
- **Cloud Integration**: Online leaderboards and save sync
- **Mobile Adaptation**: Touch controls for mobile devices

## 📁 Project Structure

```
maze-game/
├── maze_game.py                 # Main game file (1,117 lines)
├── requirements.txt             # Python dependencies
├── README.md                    # This comprehensive guide
├── DOCKER-SETUP.md             # Docker deployment guide
├── README-Docker.md            # Detailed Docker instructions
├── HOW TO PLAY - READ THIS FIRST.txt  # User instructions
├── Development_Journal_Stephen_Miller.txt  # Development history
├── test_*.py                   # Comprehensive test suite
├── Maze Navigator.app/         # macOS app bundle
├── Dockerfile                  # Docker containerization
├── docker-compose.yml          # Docker orchestration
├── *.sh                        # Launch scripts
├── *.bat                       # Windows launch files
├── *.command                   # macOS launch files
└── icons/                      # App icon resources
```

## 🎯 Learning Outcomes

This project showcases:
- **Complete Software Lifecycle**: From concept to deployment
- **Professional Development Practices**: Git, testing, documentation
- **User Experience Design**: Accessibility and intuitive interfaces
- **Performance Optimization**: Data-driven decision making
- **Cross-Platform Development**: Compatibility and deployment
- **Game Design Principles**: Balance, progression, and engagement

Perfect for demonstrating advanced programming skills, creative problem-solving, and professional software development practices in any portfolio!

## 🏆 Recent Achievements

- **Balanced Timer System**: Mathematical analysis and optimization
- **Movement Speed Customization**: User preference accommodation
- **WASD Controls**: Enhanced accessibility
- **Professional Presentation**: Custom app icon and branding
- **Comprehensive Testing**: Systematic validation and analysis
- **Production Ready**: Multiple deployment options and error handling

**Ready for professional deployment and portfolio showcase!** 🚀 