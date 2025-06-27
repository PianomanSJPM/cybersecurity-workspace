#!/usr/bin/env python3
"""
Maze Navigator Icon Generator
Creates a maze-themed icon for the macOS app
"""

import pygame
import os
import math

# Initialize Pygame
pygame.init()

# Icon sizes for macOS
ICON_SIZES = [16, 32, 64, 128, 256, 512, 1024]

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
DARK_GOLD = (218, 165, 32)

def create_compass_background(surface, size):
    """Create a compass design behind the M"""
    center_x, center_y = size // 2, size // 2
    radius = size // 3
    
    # Draw outer circle
    pygame.draw.circle(surface, GOLD, (center_x, center_y), radius, max(2, size // 64))
    
    # Draw inner circle
    inner_radius = radius // 2
    pygame.draw.circle(surface, GOLD, (center_x, center_y), inner_radius, max(1, size // 128))
    
    # Draw compass points (N, S, E, W)
    point_length = radius // 3
    point_width = max(2, size // 64)
    
    # North point
    pygame.draw.polygon(surface, GOLD, [
        (center_x, center_y - radius),
        (center_x - point_width, center_y - radius + point_length),
        (center_x + point_width, center_y - radius + point_length)
    ])
    
    # South point
    pygame.draw.polygon(surface, GOLD, [
        (center_x, center_y + radius),
        (center_x - point_width, center_y + radius - point_length),
        (center_x + point_width, center_y + radius - point_length)
    ])
    
    # East point
    pygame.draw.polygon(surface, GOLD, [
        (center_x + radius, center_y),
        (center_x + radius - point_length, center_y - point_width),
        (center_x + radius - point_length, center_y + point_width)
    ])
    
    # West point
    pygame.draw.polygon(surface, GOLD, [
        (center_x - radius, center_y),
        (center_x - radius + point_length, center_y - point_width),
        (center_x - radius + point_length, center_y + point_width)
    ])
    
    # Draw diagonal lines for NE, NW, SE, SW
    line_length = radius // 2
    line_width = max(1, size // 128)
    
    # NE line
    start_x = center_x + line_length * 0.7
    start_y = center_y - line_length * 0.7
    end_x = center_x + line_length * 0.3
    end_y = center_y - line_length * 0.3
    pygame.draw.line(surface, DARK_GOLD, (start_x, start_y), (end_x, end_y), line_width)
    
    # NW line
    start_x = center_x - line_length * 0.7
    start_y = center_y - line_length * 0.7
    end_x = center_x - line_length * 0.3
    end_y = center_y - line_length * 0.3
    pygame.draw.line(surface, DARK_GOLD, (start_x, start_y), (end_x, end_y), line_width)
    
    # SE line
    start_x = center_x + line_length * 0.7
    start_y = center_y + line_length * 0.7
    end_x = center_x + line_length * 0.3
    end_y = center_y + line_length * 0.3
    pygame.draw.line(surface, DARK_GOLD, (start_x, start_y), (end_x, end_y), line_width)
    
    # SW line
    start_x = center_x - line_length * 0.7
    start_y = center_y + line_length * 0.7
    end_x = center_x - line_length * 0.3
    end_y = center_y + line_length * 0.3
    pygame.draw.line(surface, DARK_GOLD, (start_x, start_y), (end_x, end_y), line_width)

def create_maze_icon(size):
    """Create a maze icon at the specified size"""
    # Create surface with black background
    surface = pygame.Surface((size, size))
    surface.fill(BLACK)
    
    # Create compass background
    create_compass_background(surface, size)
    
    # Create and render the "M"
    # Use a font size that scales with the icon size
    font_size = size // 2
    try:
        # Try to use a system font that looks good
        font = pygame.font.Font(None, font_size)
    except:
        # Fallback to default font
        font = pygame.font.Font(None, font_size)
    
    # Render the "M"
    text_surface = font.render("M", True, WHITE)
    text_rect = text_surface.get_rect(center=(size // 2, size // 2))
    
    # Draw the "M" on top of the compass
    surface.blit(text_surface, text_rect)
    
    return surface

def create_icns_file():
    """Create a .icns file for macOS"""
    # Create icons directory
    icons_dir = "icons"
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
    
    # Generate icons at different sizes
    icon_surfaces = {}
    for size in ICON_SIZES:
        icon_surfaces[size] = create_maze_icon(size)
        # Save individual PNG files for debugging
        pygame.image.save(icon_surfaces[size], f"{icons_dir}/icon_{size}.png")
    
    # Create a simple icon set (we'll use the 512x512 as the main icon)
    main_icon = icon_surfaces[512]
    
    # Save the main icon as PNG (we'll use this for the app)
    pygame.image.save(main_icon, "maze_icon.png")
    
    print("✓ Icon created: maze_icon.png")
    print("✓ Individual icons saved in icons/ directory")
    
    return "maze_icon.png"

if __name__ == "__main__":
    icon_file = create_icns_file()
    print(f"✓ Main icon saved as: {icon_file}")
    print("✓ You can now use this icon for your app!") 