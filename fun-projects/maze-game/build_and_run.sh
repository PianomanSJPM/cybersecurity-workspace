#!/bin/bash

# Maze Game Docker Build and Run Script
# This script builds the Docker image and provides instructions for running the game

set -e

echo "🎮 Building Maze Navigator Game Docker Image..."
echo "================================================"

# Build the Docker image
docker build -t maze-navigator-game .

echo ""
echo "✅ Docker image built successfully!"
echo ""
echo "🚀 To run the game, use one of these methods:"
echo ""
echo "Method 1: Using docker-compose (Recommended)"
echo "  docker-compose up"
echo ""
echo "Method 2: Using docker run"
echo "  docker run -it --rm \\"
echo "    -e DISPLAY=\$DISPLAY \\"
echo "    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \\"
echo "    -v \$(pwd)/high_scores.json:/app/high_scores.json \\"
echo "    --network host \\"
echo "    maze-navigator-game"
echo ""
echo "⚠️  Note: You may need to allow X11 connections first:"
echo "  xhost +local:docker"
echo ""
echo "🎯 Game Controls:"
echo "  Arrow Keys: Move player"
echo "  R: Restart game"
echo "  H: View high scores"
echo "  Q: Quit game"
echo "  SPACE: Continue to next maze (when won)"
echo ""
echo "🏆 High scores will be saved to high_scores.json in the current directory" 