@echo off
title Maze Navigator - Speed Challenge

echo.
echo =============================================================================
echo                    MAZE NAVIGATOR - SPEED CHALLENGE
echo =============================================================================
echo.

echo Starting Maze Navigator...

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Python found
    set PYTHON_CMD=python
) else (
    python3 --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✓ Python 3 found
        set PYTHON_CMD=python3
    ) else (
        echo ✗ Python is not installed on this system
        echo Please install Python 3.6 or higher from python.org
        echo.
        pause
        exit /b 1
    )
)

REM Check if pygame is installed
%PYTHON_CMD% -c "import pygame" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Pygame is installed
) else (
    echo Installing pygame...
    %PYTHON_CMD% -m pip install pygame
    if %errorlevel% neq 0 (
        echo ✗ Could not install pygame automatically
        echo Please install pygame manually: pip install pygame
        echo.
        pause
        exit /b 1
    )
)

REM Check if game file exists
if exist "maze_game.py" (
    echo ✓ Game file found
) else (
    echo ✗ Game file not found
    echo.
    pause
    exit /b 1
)

echo.
echo Launching Maze Navigator...
echo Enjoy the game!
echo.

REM Launch the game
%PYTHON_CMD% maze_game.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo Game ended with an error.
    pause
) 