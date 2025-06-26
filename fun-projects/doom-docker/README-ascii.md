# ASCII Adventure Game Container

A fun, interactive ASCII-based adventure game that runs in Docker! This demonstrates containerization concepts while providing an entertaining experience.

## 🎮 Game Features

- **Interactive Text Adventure**: Explore a mysterious dungeon
- **Simple Commands**: look, move, search, quit
- **Cross-Platform**: Works on any system with Docker
- **Educational**: Demonstrates Docker concepts

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)
```bash
# Build and run the game
docker-compose -f docker-compose.ascii.yml up --build

# To run in detached mode and then attach
docker-compose -f docker-compose.ascii.yml up -d --build
docker attach ascii-adventure-game
```

### Option 2: Using Docker directly
```bash
# Build the image
docker build -f Dockerfile.ascii -t ascii-adventure .

# Run the game
docker run -it --name ascii-adventure-game ascii-adventure
```

## 🎯 How to Play

1. **Look**: Examine your surroundings
2. **Move**: Go to the next room
3. **Search**: Look for items and treasure
4. **Quit**: Exit the game

## 🐳 Docker Concepts Demonstrated

- **Containerization**: Isolated application environment
- **Cross-Platform**: Works on Linux, macOS, Windows
- **Portability**: Easy to share and deploy
- **Isolation**: Game runs in its own environment
- **Reproducibility**: Same experience everywhere

## 🔧 Technical Details

- **Base Image**: Ubuntu 22.04
- **Runtime**: Python 3
- **Architecture**: Terminal-based interactive game
- **Volume Mounting**: Optional save game persistence
- **Environment Variables**: Python unbuffered output

## 🎓 Learning Objectives

This container demonstrates:
- Docker image building
- Container runtime management
- Interactive terminal applications
- Volume mounting for persistence
- Docker Compose orchestration
- Cross-platform compatibility

## 🛠️ Development

To modify the game:
1. Edit the Python code in the Dockerfile
2. Rebuild the image
3. Test your changes

## 📝 Commands Reference

```bash
# Build and run
docker-compose -f docker-compose.ascii.yml up --build

# Stop the game
docker-compose -f docker-compose.ascii.yml down

# View logs
docker-compose -f docker-compose.ascii.yml logs

# Clean up
docker-compose -f docker-compose.ascii.yml down --rmi all
```

## 🎉 Have Fun!

This is a great way to learn Docker while having fun! The game is simple but demonstrates key containerization concepts that are essential for DevSecOps. 