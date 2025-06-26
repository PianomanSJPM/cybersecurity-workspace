# 🎮 Doom Docker Container

A fun Docker project that runs the original Doom game in a container using DOSBox and noVNC for web access.

## 🚀 **What This Does**

This Docker container:
- Downloads the original Doom shareware version (legal to distribute)
- Runs it using DOSBox emulator
- Provides web access via noVNC
- Works on any operating system with Docker

## 🛠️ **How It Works**

1. **DOSBox**: Emulates a DOS environment to run the original Doom executable
2. **Xvfb**: Virtual display server for headless operation
3. **noVNC**: Web-based VNC client for browser access
4. **Fluxbox**: Lightweight window manager

## 🎯 **Quick Start**

### **Build the Image**
```bash
docker build -t doom-game .
```

### **Run the Container**
```bash
docker run -p 8080:8080 doom-game
```

### **Play Doom**
1. Open your web browser
2. Go to: `http://localhost:8080`
3. Click "Connect" in the noVNC interface
4. Enjoy Doom!

## 🎮 **Controls**

- **Arrow Keys**: Move
- **Ctrl**: Shoot
- **Space**: Open doors/activate switches
- **Alt+F4**: Exit game
- **ESC**: Menu

## 📁 **Project Structure**

```
doom-docker/
├── Dockerfile          # Container definition
├── README.md          # This file
└── .dockerignore      # Files to exclude from build
```

## 🔧 **Technical Details**

### **Base Image**
- Ubuntu 22.04 LTS

### **Key Components**
- **DOSBox**: DOS emulator
- **Xvfb**: Virtual framebuffer
- **noVNC**: Web VNC client
- **Fluxbox**: Window manager

### **Ports**
- **8080**: noVNC web interface

### **Game Files**
- Doom shareware version (Episode 1: Knee-Deep in the Dead)
- Automatically downloaded during build
- Legal to distribute (shareware)

## 🎯 **Learning Objectives**

This project demonstrates:
- **Multi-stage Docker builds**
- **Legacy software containerization**
- **Web-based remote desktop**
- **Game preservation through containers**
- **Cross-platform compatibility**

## 🚀 **Advanced Usage**

### **Custom Port**
```bash
docker run -p 9000:8080 doom-game
# Access at http://localhost:9000
```

### **Background Mode**
```bash
docker run -d -p 8080:8080 --name doom-container doom-game
```

### **Stop Container**
```bash
docker stop doom-container
```

## 🎮 **Why This is Cool**

1. **Cross-Platform**: Works on Windows, Mac, Linux
2. **No Installation**: Just Docker required
3. **Web Access**: Play from any browser
4. **Preservation**: Keeps classic games accessible
5. **Learning**: Great way to learn Docker concepts

## 🔗 **Related Projects**

- **Wolfenstein 3D**: Similar setup for Wolfenstein
- **Quake**: 3D game containerization
- **Retro Gaming**: Classic game preservation

## 📚 **Resources**

- [DOSBox Documentation](https://www.dosbox.com/wiki/)
- [noVNC Documentation](https://github.com/novnc/noVNC)
- [Doom Wiki](https://doomwiki.org/)

---

*This project demonstrates how Docker can be used for fun and educational purposes while preserving classic games for future generations.* 