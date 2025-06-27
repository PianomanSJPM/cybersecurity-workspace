# 🧩 Maze Navigator Game

A colorful, graphical maze navigation game built with Python and Pygame. Navigate through progressively challenging mazes to find the exit!

## 🎮 Game Features

- **Colorful Graphics**: Vibrant colors and clean visual design
- **Dynamic Difficulty**: Maze size increases every 3 levels for progressive challenge
- **Random Maze Generation**: Each game creates unique maze layouts
- **Progressive Timer**: Time gets shorter with each maze (30s → 27s → 24s...)
- **High Score System**: Persistent leaderboard with 3-letter initials
- **Move Counter**: Track your progress through the maze
- **Simple Controls**: Easy-to-use arrow key navigation
- **Win Detection**: Clear victory message when you reach the exit
- **Difficulty Indicator**: Visual feedback showing current difficulty level

## 🎯 How to Play

1. **Start**: You begin at the green square (top-left)
2. **Navigate**: Use arrow keys to move through the maze
3. **Goal**: Reach the red square (bottom-right) to win
4. **Timer**: Complete mazes before time runs out
5. **Progression**: Mazes get larger and more challenging every 3 levels
6. **High Score**: Enter your initials if you achieve a high score
7. **Restart**: Press 'R' to start a new game

## 📈 Difficulty Progression

| Maze Range | Size | Difficulty | Time Limit |
|------------|------|------------|------------|
| 1-3        | 15×10 | Beginner   | 30s        |
| 4-6        | 16×11 | Easy       | 27s        |
| 7-9        | 17×12 | Medium     | 24s        |
| 10-12      | 18×13 | Hard       | 21s        |
| 13-15      | 19×14 | Expert     | 18s        |
| 16+        | 20×15 | Master     | 15s        |

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download the project**
2. **Navigate to the maze-game directory**:
   ```bash
   cd fun-projects/maze-game
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Game

### **Easy Launch Methods (Recommended):**

#### **Method 1: Shell Script**
```bash
./run_game.sh
```

#### **Method 2: Python Launcher**
```bash
python3 launch.py
```

#### **Method 3: Direct (if in correct directory)**
```bash
python3 maze_game.py
```

### **Troubleshooting:**
If you get "file not found" errors, make sure you're in the correct directory:
```bash
cd /Users/stephenmiller/Desktop/Cybersecurity/fun-projects/maze-game
python3 maze_game.py
```

## 🎨 Game Elements

- **🟦 Blue Square**: Your player character
- **🟩 Green Square**: Starting position
- **🟥 Red Square**: Exit/Goal
- **🟪 Purple Squares**: Walls (impassable)
- **⬜ White Squares**: Paths (walkable)

## 🎮 Controls

| Key | Action |
|-----|--------|
| ↑ | Move Up |
| ↓ | Move Down |
| ← | Move Left |
| → | Move Right |
| SPACE | Continue to next maze (when won) |
| M | Toggle game menu |
| H | View high scores during gameplay |
| R | Restart Game |
| Q | Quit Game |

## 🍔 Menu System

Press **M** to access the game menu, which displays:
- **Arrow Keys** - Move player
- **SPACE** - Continue to next maze (when won)
- **R** - Restart game
- **H** - View high scores
- **M** - Toggle menu
- **Q** - Quit game

The menu provides easy access to controls without cluttering the game interface.

## 🏅 High Score System

- **Persistent Storage**: Scores saved to `high_scores.json`
- **Top 10 Leaderboard**: Only the best scores are kept
- **3-Letter Initials**: Classic arcade-style input
- **Rank Display**: See your position on the leaderboard
- **Automatic Detection**: High scores are detected automatically

## 🏗️ Technical Details

### Architecture
- **Object-Oriented Design**: Clean class structure with `MazeGame` class
- **Event-Driven**: Pygame event handling for responsive controls
- **Modular Code**: Separate methods for different game functions
- **Data Persistence**: JSON-based high score storage
- **Dynamic Difficulty**: Progressive maze sizing and algorithm selection

### Key Components
- **Maze Generation**: Three algorithms (Recursive, Kruskal, Prim)
- **Dynamic Sizing**: Maze size increases with progression
- **Collision Detection**: Prevents moving through walls
- **State Management**: Tracks game progress and win conditions
- **UI Rendering**: Dynamic display of game elements and instructions
- **Timer System**: Progressive difficulty with countdown
- **High Score Manager**: Persistent leaderboard functionality

### Performance
- **60 FPS**: Smooth gameplay with consistent frame rate
- **Efficient Rendering**: Optimized drawing routines
- **Memory Management**: Clean resource handling
- **Scalable Design**: Handles different maze sizes efficiently

## 🚀 Portfolio Value

This project demonstrates:

### Technical Skills
- **Python Programming**: Core language features and best practices
- **Game Development**: Pygame framework usage
- **Algorithm Design**: Multiple maze generation algorithms
- **Object-Oriented Programming**: Clean class design and inheritance
- **Data Persistence**: File I/O and JSON handling
- **User Input Processing**: Real-time keyboard input handling
- **Dynamic Systems**: Progressive difficulty implementation

### Software Engineering
- **Code Organization**: Modular, maintainable code structure
- **Documentation**: Comprehensive README and code comments
- **User Experience**: Intuitive controls and clear visual feedback
- **Testing**: Game logic validation and edge case handling
- **Deployment**: Multiple launch methods for different environments
- **Scalability**: Progressive difficulty systems

### Creative Problem Solving
- **Maze Generation**: Algorithm design for creating solvable mazes
- **Game Mechanics**: Balanced difficulty and engaging gameplay
- **Visual Design**: Color theory and user interface design
- **Competitive Features**: High score system and progressive difficulty
- **Difficulty Balancing**: Mathematical progression systems

## 🔧 Customization Ideas

### Easy Enhancements
- **Multiple Levels**: Different maze sizes and difficulties
- **Sound Effects**: Audio feedback for movements and wins
- **Power-ups**: Special abilities or shortcuts
- **Different Themes**: Visual themes and color schemes
- **Algorithm Mixing**: Combine different generation methods

### Advanced Features
- **Maze Editor**: Create custom mazes
- **Save/Load**: Persist game progress
- **Multiplayer**: Competitive or cooperative modes
- **3D Graphics**: Upgrade to 3D maze navigation
- **Online Leaderboards**: Global high score competition
- **Custom Difficulty**: Player-selectable difficulty settings

## 📝 Code Structure

```
maze_game.py
├── Constants & Configuration
├── CellType Enum
├── HighScoreManager Class
│   ├── load_scores() - Load from JSON file
│   ├── save_scores() - Save to JSON file
│   ├── add_score() - Add new score
│   ├── is_high_score() - Check qualification
│   └── get_rank() - Calculate rank
├── MazeGame Class
│   ├── __init__() - Game initialization
│   ├── calculate_maze_size() - Dynamic size calculation
│   ├── generate_maze() - Maze creation algorithm
│   ├── draw_maze() - Visual rendering
│   ├── draw_ui() - Interface elements
│   ├── draw_initials_screen() - High score input
│   ├── draw_high_scores_screen() - Leaderboard
│   ├── move_player() - Movement logic
│   ├── update_timer() - Timer management
│   ├── next_maze() - Progress to next maze
│   ├── reset_game() - Game state reset
│   └── run() - Main game loop
└── Main execution
```

## 🎯 Learning Outcomes

This project provides hands-on experience with:
- **Game Development Fundamentals**
- **Python Programming Best Practices**
- **Algorithm Design and Implementation**
- **User Interface Design**
- **Software Architecture**
- **Data Persistence and File I/O**
- **User Input Processing**
- **Documentation and Presentation**
- **Dynamic Difficulty Systems**
- **Progressive Game Design**

Perfect for showcasing programming skills in a portfolio while demonstrating creativity and technical competence! 