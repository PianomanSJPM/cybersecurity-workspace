# 🐳 Maze Game Docker Setup - Quick Reference

## 🚀 Quick Start Commands

### For Linux:
```bash
# Build and run
./build_and_run.sh
docker-compose up
```

### For macOS:
```bash
# Use the macOS-specific script
./run_on_macos.sh
```

### For Windows (WSL2):
```bash
# Build and run
./build_and_run.sh
docker-compose up
```

## 📁 Docker Files Created

- **`Dockerfile`** - Container definition with Python and pygame
- **`docker-compose.yml`** - Easy deployment with X11 forwarding
- **`.dockerignore`** - Optimizes build by excluding unnecessary files
- **`build_and_run.sh`** - Automated build and run script
- **`run_on_macos.sh`** - macOS-specific setup with XQuartz
- **`README-Docker.md`** - Comprehensive Docker documentation

## 🎮 Features

✅ **Cross-Platform**: Works on Linux, macOS, Windows  
✅ **Persistent High Scores**: Saved to `high_scores.json`  
✅ **Isolated Environment**: All dependencies included  
✅ **Easy Deployment**: Single command to run  
✅ **GUI Support**: Full graphical interface  

## 🔧 Troubleshooting

### X11 Issues:
```bash
xhost +local:docker  # Linux
xhost + 127.0.0.1    # macOS
```

### Build Issues:
```bash
docker system prune  # Clean up Docker cache
docker build --no-cache -t maze-navigator-game .  # Rebuild
```

## 🎯 Game Controls

- **Arrow Keys**: Move player
- **R**: Restart game  
- **H**: View high scores
- **Q**: Quit game
- **SPACE**: Next maze (when won)

## 📊 Image Size

The Docker image is approximately **~500MB** and includes:
- Python 3.11
- Pygame with all SDL2 dependencies
- Game files and scripts

## 🏆 High Scores

High scores are automatically saved to `high_scores.json` in your current directory and persist between game sessions.

---

**Ready to play?** Run `./build_and_run.sh` and follow the instructions! 🎮 