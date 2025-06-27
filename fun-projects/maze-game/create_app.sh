#!/bin/bash

# Create macOS App Bundle for Maze Game
# This script creates a standalone .app that users can double-click to run

APP_NAME="Maze Navigator"
APP_BUNDLE="${APP_NAME}.app"
CONTENTS_DIR="${APP_BUNDLE}/Contents"
MACOS_DIR="${CONTENTS_DIR}/MacOS"
RESOURCES_DIR="${CONTENTS_DIR}/Resources"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Creating macOS App Bundle for Maze Navigator...${NC}"

# Create directory structure
mkdir -p "${MACOS_DIR}"
mkdir -p "${RESOURCES_DIR}"

# Create the main executable script
cat > "${MACOS_DIR}/MazeNavigator" << 'EOF'
#!/bin/bash

# Get the directory where the app is located
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../Resources" && pwd)"
cd "$APP_DIR"

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    osascript -e 'display alert "Error" message "Python is not installed on this system. Please install Python 3.6 or higher."'
    exit 1
fi

# Check if pygame is installed
if ! $PYTHON_CMD -c "import pygame" 2>/dev/null; then
    osascript -e 'display alert "Missing Dependency" message "Pygame is not installed. The game will attempt to install it now."'
    
    if command -v pip3 &> /dev/null; then
        pip3 install pygame
    elif command -v pip &> /dev/null; then
        pip install pygame
    else
        osascript -e 'display alert "Error" message "Could not install pygame automatically. Please install it manually: pip install pygame"'
        exit 1
    fi
fi

# Launch the game
$PYTHON_CMD maze_game.py
EOF

# Make the executable script executable
chmod +x "${MACOS_DIR}/MazeNavigator"

# Copy game files to resources
cp maze_game.py "${RESOURCES_DIR}/"
cp high_scores.json "${RESOURCES_DIR}/" 2>/dev/null || true
cp requirements.txt "${RESOURCES_DIR}/" 2>/dev/null || true

# Create Info.plist
cat > "${CONTENTS_DIR}/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>MazeNavigator</string>
    <key>CFBundleIdentifier</key>
    <string>com.stephenmiller.mazenavigator</string>
    <key>CFBundleName</key>
    <string>Maze Navigator</string>
    <key>CFBundleDisplayName</key>
    <string>Maze Navigator - Speed Challenge</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.10</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.games</string>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeName</key>
            <string>Maze Game</string>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>maze</string>
            </array>
            <key>CFBundleTypeRole</key>
            <string>Viewer</string>
        </dict>
    </array>
</dict>
</plist>
EOF

echo -e "${GREEN}✓ App bundle created: ${APP_BUNDLE}${NC}"
echo -e "${BLUE}You can now double-click ${APP_BUNDLE} to run the game!${NC}"
echo ""
echo -e "${BLUE}To install the app:${NC}"
echo "1. Drag ${APP_BUNDLE} to your Applications folder"
echo "2. Double-click to run from Applications"
echo "3. Or keep it in this folder and double-click to run" 