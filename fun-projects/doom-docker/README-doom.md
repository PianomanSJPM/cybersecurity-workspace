# Doom Game Container with Web Interface

Play the original Doom game in your web browser using Docker! This setup uses noVNC to provide a graphical interface accessible through any modern web browser.

## 🎮 Features

- **Original Doom Game**: Play the classic 1993 Doom game
- **Web Interface**: Access through any web browser
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **No Installation**: Everything runs in Docker containers
- **Sound Support**: Full audio support through DOSBox

## 🚀 Quick Start

### Prerequisites
1. **Docker and Docker Compose** installed
2. **Doom Game Files**: You need the original Doom files

### Step 1: Get Doom Files
You need these files:
- `DOOM.EXE` - The main Doom executable
- `DOOM1.WAD` - The game data file

**Legal Sources:**
- **Doom Shareware**: Free from [Doomworld](https://www.doomworld.com/classicdoom/info/shareware.php)
- **Steam**: Purchase the original Doom
- **GOG**: Purchase the original Doom

### Step 2: Prepare Files
```bash
# Create doom directory
mkdir doom

# Copy your Doom files to the doom directory
cp /path/to/your/DOOM.EXE ./doom/
cp /path/to/your/DOOM1.WAD ./doom/
```

### Step 3: Build and Run
```bash
# Build and start the container
docker-compose -f docker-compose.doom.yml up --build

# Or run in background
docker-compose -f docker-compose.doom.yml up -d --build
```

### Step 4: Play Doom
1. Open your web browser
2. Go to: `http://localhost:8080`
3. Click "Connect" in the noVNC interface
4. Doom will start automatically!

## 🎯 How to Play

### Controls
- **Arrow Keys**: Move
- **Ctrl**: Fire
- **Space**: Open doors/activate switches
- **Alt**: Strafe
- **Shift**: Run
- **Esc**: Menu

### Game Commands
- **F1**: Help
- **F2**: Save Game
- **F3**: Load Game
- **F4**: Sound Volume
- **F5**: Screen Size
- **F6**: Quit Game

## 🐳 Docker Concepts Demonstrated

- **Containerization**: Isolated game environment
- **Web Services**: noVNC for remote desktop access
- **Volume Mounting**: Persistent game files
- **Port Mapping**: Web interface access
- **Multi-Service**: VNC + DOSBox + noVNC
- **Cross-Platform**: Works on any OS with Docker

## 🔧 Technical Details

- **Base Image**: Ubuntu 22.04
- **DOSBox**: DOS emulator for running Doom
- **Xvfb**: Virtual framebuffer for headless display
- **x11vnc**: VNC server for remote desktop
- **noVNC**: Web-based VNC client
- **Fluxbox**: Lightweight window manager

## 🛠️ Troubleshooting

### Game Won't Start
1. **Check Files**: Ensure `DOOM.EXE` and `DOOM1.WAD` are in `./doom/`
2. **File Permissions**: Make sure files are readable
3. **Container Logs**: Check with `docker-compose logs doom-game`

### Web Interface Issues
1. **Port 8080**: Make sure port 8080 is not in use
2. **Browser**: Try a different browser
3. **Firewall**: Check if firewall blocks port 8080

### Performance Issues
1. **Browser**: Use Chrome or Firefox for best performance
2. **Network**: Local network connection recommended
3. **Resources**: Ensure Docker has enough RAM/CPU

## 📝 Commands Reference

```bash
# Build and run
docker-compose -f docker-compose.doom.yml up --build

# Run in background
docker-compose -f docker-compose.doom.yml up -d --build

# View logs
docker-compose -f docker-compose.doom.yml logs

# Stop the game
docker-compose -f docker-compose.doom.yml down

# Rebuild if you change files
docker-compose -f docker-compose.doom.yml up --build --force-recreate
```

## 🎓 Learning Objectives

This setup demonstrates:
- **Container Orchestration**: Multi-service Docker setup
- **Remote Desktop**: VNC and noVNC implementation
- **Legacy Software**: Running old games in modern environments
- **Web Services**: Browser-based application access
- **Volume Management**: Persistent data in containers
- **Cross-Platform Deployment**: Universal compatibility

## 🎉 Have Fun!

This is a great way to learn Docker while playing one of the most influential games ever made! The setup shows how containers can bring legacy software to modern platforms.

## ⚖️ Legal Notice

This setup is for educational purposes. You must own a legal copy of Doom to use this container. The shareware version is free and legal to use. 