#!/bin/bash

# Maze Game macOS Runner Script
# This script sets up XQuartz and runs the maze game on macOS

set -e

echo "🍎 Maze Navigator Game - macOS Setup"
echo "===================================="

# Check if XQuartz is installed
if ! command -v xquartz &> /dev/null; then
    echo "❌ XQuartz not found. Installing..."
    if command -v brew &> /dev/null; then
        brew install --cask xquartz
    else
        echo "❌ Homebrew not found. Please install XQuartz manually:"
        echo "   Visit: https://www.xquartz.org/"
        exit 1
    fi
fi

echo "✅ XQuartz found"

# Start XQuartz if not running
if ! pgrep -x "Xquartz" > /dev/null; then
    echo "🚀 Starting XQuartz..."
    open -a XQuartz
    sleep 3
fi

# Allow X11 connections
echo "🔓 Allowing X11 connections..."
xhost + 127.0.0.1

# Build Docker image if not exists
if ! docker image inspect maze-navigator-game > /dev/null 2>&1; then
    echo "🐳 Building Docker image..."
    docker build -t maze-navigator-game .
fi

echo ""
echo "🎮 Starting Maze Navigator Game..."
echo "=================================="

# Run the game
docker run -it --rm \
  -e DISPLAY=host.docker.internal:0 \
  -v $(pwd)/high_scores.json:/app/high_scores.json \
  maze-navigator-game

echo ""
echo "🎯 Game finished!"
echo "🏆 Check high_scores.json for your scores" 