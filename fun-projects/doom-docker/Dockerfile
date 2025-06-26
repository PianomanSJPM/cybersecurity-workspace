# Doom Docker Container
# Runs the original Doom game using DOSBox

FROM ubuntu:22.04

# Set build arguments
ARG BUILD_DATE=unknown
ARG VCS_REF=unknown
ARG VERSION=1.0.0

# Set labels
LABEL maintainer="Stephen Miller <stephen.miller@example.com>"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.revision="${VCS_REF}"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.title="Doom Game Container"
LABEL org.opencontainers.image.description="Original Doom game running in Docker with DOSBox"

# Install dependencies
RUN apt-get update && apt-get install -y \
    dosbox \
    wget \
    unzip \
    xvfb \
    x11vnc \
    fluxbox \
    novnc \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Create game directory
WORKDIR /games

# Download Doom shareware version (legal to distribute)
RUN wget -O doom.zip "https://archive.org/download/DoomShareware/doom.zip" && \
    unzip doom.zip && \
    rm doom.zip && \
    mkdir -p /root/.dosbox

# Create DOSBox configuration
RUN echo "[dosbox]" > /root/.dosbox/dosbox-0.74-3.conf && \
    echo "fullscreen=false" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "fulldouble=false" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "fullresolution=original" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "windowresolution=1024x768" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "output=opengl" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "autolock=true" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "sensitivity=100" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "waitonerror=true" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "usescancodes=true" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "[cpu]" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "core=auto" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "cputype=auto" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "cycles=auto" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "cycles-realmode=auto" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "cycles-up=10" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "cycles-down=20" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "cycle-max=0" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "[mixer]" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "nosound=false" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "rate=22050" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "blocksize=1024" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "prebuffer=25" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "[midi]" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "mpu401=intelligent" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "intelligent=true" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "device=default" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "config=" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "[sblaster]" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "sbtype=sb16" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "sbbase=220" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "irq=7" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "dma=1" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "hdma=5" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "sbmixer=true" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "oplmode=auto" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "oplrate=22050" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "[gus]" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "gus=false" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "gusrate=22050" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "gusbase=240" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "gusirq=5" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "gusdma=3" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "ultradir=C:\\ULTRASND" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "[speaker]" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "pcspeaker=true" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "pcrate=22050" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "tandy=auto" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "tandyrate=22050" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "disney=true" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "[joystick]" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "joysticktype=auto" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "timed=true" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "autofire=false" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "swap34=false" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "buttonwrap=false" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "[serial]" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "serial1=dummy" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "serial2=dummy" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "serial3=disabled" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "serial4=disabled" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "[dos]" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "xms=true" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "ems=true" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "umb=true" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "keyboardlayout=auto" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "[ipx]" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "ipx=true" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "[autoexec]" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "mount c /games" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "c:" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "cd doom" >> /root/.dosbox/dosbox-0.74-3.conf && \
    echo "doom.exe" >> /root/.dosbox/dosbox-0.74-3.conf

# Create startup script
RUN echo '#!/bin/bash' > /start-doom.sh && \
    echo 'echo "🎮 Starting Doom..."' >> /start-doom.sh && \
    echo 'echo "🌐 Access Doom at: http://localhost:8080"' >> /start-doom.sh && \
    echo 'echo "🎯 Controls: Arrow keys to move, Ctrl to shoot, Space to open doors"' >> /start-doom.sh && \
    echo 'echo "🚪 Exit: Alt+F4 or close browser tab"' >> /start-doom.sh && \
    echo '' >> /start-doom.sh && \
    echo '# Start virtual display' >> /start-doom.sh && \
    echo 'Xvfb :99 -screen 0 1024x768x24 &' >> /start-doom.sh && \
    echo 'export DISPLAY=:99' >> /start-doom.sh && \
    echo '' >> /start-doom.sh && \
    echo '# Start window manager' >> /start-doom.sh && \
    echo 'fluxbox &' >> /start-doom.sh && \
    echo '' >> /start-doom.sh && \
    echo '# Start VNC server' >> /start-doom.sh && \
    echo 'x11vnc -display :99 -nopw -listen localhost -xkb -ncache 10 -ncache_cr -forever &' >> /start-doom.sh && \
    echo '' >> /start-doom.sh && \
    echo '# Start noVNC' >> /start-doom.sh && \
    echo '/usr/share/novnc/utils/launch.sh --vnc localhost:5900 --listen 8080 &' >> /start-doom.sh && \
    echo '' >> /start-doom.sh && \
    echo '# Start DOSBox with Doom' >> /start-doom.sh && \
    echo 'dosbox -conf /root/.dosbox/dosbox-0.74-3.conf' >> /start-doom.sh && \
    chmod +x /start-doom.sh

# Expose port for noVNC
EXPOSE 8080

# Set the default command
CMD ["/start-doom.sh"] 