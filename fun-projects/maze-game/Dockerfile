# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for pygame
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy game files
COPY maze_game.py .
COPY launch.py .
COPY run_game.sh .
COPY run_game_anywhere.sh .

# Make shell scripts executable
RUN chmod +x run_game.sh run_game_anywhere.sh

# Set environment variable for pygame display
ENV DISPLAY=:0
ENV SDL_VIDEODRIVER=x11

# Expose port for X11 forwarding (if needed)
EXPOSE 6000

# Set the default command to run the game
CMD ["python3", "maze_game.py"] 