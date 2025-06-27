# 🐳 Maze Navigator Game - Docker Setup

This guide explains how to run the Maze Navigator Game using Docker, making it easy to play on any system with Docker installed.

## 📋 Prerequisites

- **Docker** installed on your system
- **Docker Compose** (usually comes with Docker Desktop)
- **X11** (for GUI display on Linux/macOS)

## 🚀 Quick Start

### Method 1: Using the Build Script (Easiest)

```bash
# Run the build script
./build_and_run.sh
```

This will build the Docker image and show you the commands to run the game.

### Method 2: Manual Build and Run

```bash
# Build the Docker image
docker build -t maze-navigator-game .

# Allow X11 connections (Linux/macOS)
xhost +local:docker

# Run with docker-compose (Recommended)
docker-compose up

# Or run with docker directly
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $(pwd)/high_scores.json:/app/high_scores.json \
  --network host \
  maze-navigator-game
```

## 🎮 Game Controls

| Key | Action |
|-----|--------|
| ↑ | Move Up |
| ↓ | Move Down |
| ← | Move Left |
| → | Move Right |
| SPACE | Continue to next maze (when won) |
| H | View high scores during gameplay |
| R | Restart Game |
| Q | Quit Game |

## 🏆 Features

- **Persistent High Scores**: High scores are saved to `high_scores.json` in your current directory
- **Cross-Platform**: Works on Linux, macOS, and Windows (with WSL2)
- **Isolated Environment**: Game runs in its own container with all dependencies included
- **Easy Deployment**: Single command to build and run

## 🔧 Troubleshooting

### X11 Display Issues (Linux/macOS)

If you get display errors, try:

```bash
# Allow X11 connections
xhost +local:docker

# Or for more permissive access (less secure)
xhost +
```

### macOS Specific

On macOS, you might need to install XQuartz:

```bash
# Install XQuartz
brew install --cask xquartz

# Start XQuartz
open -a XQuartz

# Allow connections
xhost + 127.0.0.1
```

### Windows (WSL2)

For Windows users with WSL2:

1. Install an X11 server like VcXsrv
2. Configure WSL2 to use the X11 server
3. Run the Docker commands as shown above

## 🐳 Docker Commands Reference

### Build Image
```bash
docker build -t maze-navigator-game .
```

### Run with Docker Compose
```bash
docker-compose up
```

### Run with Docker
```bash
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $(pwd)/high_scores.json:/app/high_scores.json \
  --network host \
  maze-navigator-game
```

### Stop Container
```bash
# If using docker-compose
docker-compose down

# If using docker run
# Just press Ctrl+C in the terminal
```

### Remove Image
```bash
docker rmi maze-navigator-game
```

## 📁 File Structure

```
maze-game/
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore          # Files to exclude from build
├── build_and_run.sh       # Build and run script
├── maze_game.py           # Main game file
├── requirements.txt       # Python dependencies
├── high_scores.json      # Persistent high scores (created after first run)
└── README-Docker.md      # This file
```

## 🔒 Security Notes

- The Docker container runs with `privileged: true` to allow X11 connections
- High scores are persisted through a volume mount
- The container is isolated from your system except for display and file access

## 🎯 Next Steps

Once you have the game running:

1. **Play the game** using arrow keys to navigate
2. **Try to beat your high score** on increasingly difficult mazes
3. **Share your high scores** with friends
4. **Customize the game** by modifying the source code

Enjoy playing Maze Navigator! 🎮 