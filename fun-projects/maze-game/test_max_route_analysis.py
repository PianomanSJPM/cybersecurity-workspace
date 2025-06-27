#!/usr/bin/env python3
"""
Maze Navigator - Maximum Route Analysis
======================================

This script analyzes the longest possible route through a maximum-sized maze
and compares it with cursor speed to determine if completion is possible.
"""

import math
from collections import deque

def calculate_maze_size(maze_count):
    """Calculate maze size for a given maze count"""
    size_increase = (maze_count - 1) // 5
    current_width = min(15 + size_increase, 50)
    current_height = min(10 + size_increase, 40)
    return current_width, current_height

def calculate_timer(maze_number):
    """Calculate timer for a given maze number"""
    base_time = 30
    time_reduction = 2
    
    if maze_number % 10 == 1:
        return base_time
    else:
        mazes_since_reset = (maze_number - 1) % 10
        return max(5, base_time - (mazes_since_reset * time_reduction))

def estimate_maximum_path_length(width, height):
    """
    Estimate the maximum possible path length in a maze.
    This is a theoretical worst-case scenario.
    """
    # In the worst case, a maze could force the player to visit nearly every cell
    # before reaching the end. This is extremely unlikely but theoretically possible.
    
    total_cells = width * height
    wall_cells = estimate_wall_cells(width, height)
    accessible_cells = total_cells - wall_cells
    
    # In the absolute worst case, player might need to visit 80-90% of accessible cells
    worst_case_factor = 0.85
    max_path_length = int(accessible_cells * worst_case_factor)
    
    return max_path_length

def estimate_wall_cells(width, height):
    """Estimate how many cells are walls in a typical maze"""
    # In a typical maze, about 30-40% of cells are walls
    # This varies by algorithm but is a reasonable estimate
    wall_percentage = 0.35
    return int(width * height * wall_percentage)

def calculate_movement_time(path_length, move_delay=0.08):
    """Calculate time needed to traverse the path"""
    return path_length * move_delay

def analyze_maximum_route():
    """Analyze the maximum possible route through maximum-sized mazes"""
    print("MAZE NAVIGATOR - MAXIMUM ROUTE ANALYSIS")
    print("=" * 60)
    print()
    
    print("ANALYSIS PARAMETERS:")
    print("-" * 25)
    print("Player movement delay: 0.08 seconds per move")
    print("Maximum maze size: 50×40 cells")
    print("Worst-case path estimate: 85% of accessible cells")
    print("Wall percentage estimate: 35% of total cells")
    print()
    
    # Find when we reach maximum size
    max_size_maze = None
    for maze_num in range(1, 200):
        width, height = calculate_maze_size(maze_num)
        if width == 50 and height == 40:
            max_size_maze = maze_num
            break
    
    print(f"MAXIMUM SIZE ANALYSIS:")
    print("-" * 25)
    print(f"Maximum size (50×40) reached at: Maze {max_size_maze}")
    print()
    
    # Analyze maximum-sized mazes
    print("MAXIMUM-SIZED MAZE ANALYSIS:")
    print("-" * 35)
    print("Maze | Timer | Total Cells | Accessible | Max Path | Max Time | Status")
    print("-" * 75)
    
    impossible_count = 0
    critical_count = 0
    
    for maze_num in range(max_size_maze, max_size_maze + 20):  # Analyze next 20 mazes
        timer = calculate_timer(maze_num)
        width, height = 50, 40  # Maximum size
        
        total_cells = width * height
        wall_cells = estimate_wall_cells(width, height)
        accessible_cells = total_cells - wall_cells
        max_path_length = estimate_maximum_path_length(width, height)
        max_time = calculate_movement_time(max_path_length)
        
        # Determine status
        if max_time <= timer * 0.8:
            status = "Possible"
        elif max_time <= timer:
            status = "Challenging"
            critical_count += 1
        else:
            status = "IMPOSSIBLE"
            impossible_count += 1
        
        print(f"{maze_num:4d} | {timer:5.0f}s | {total_cells:10d} | {accessible_cells:10d} | {max_path_length:8d} | {max_time:8.1f}s | {status}")
    
    print()
    
    # Detailed worst-case analysis
    print("WORST-CASE SCENARIO ANALYSIS:")
    print("-" * 35)
    
    # Calculate for maximum maze
    width, height = 50, 40
    total_cells = width * height
    wall_cells = estimate_wall_cells(width, height)
    accessible_cells = total_cells - wall_cells
    max_path_length = estimate_maximum_path_length(width, height)
    
    print(f"Maximum maze dimensions: {width}×{height} = {total_cells} total cells")
    print(f"Estimated wall cells: {wall_cells} ({wall_cells/total_cells*100:.1f}%)")
    print(f"Accessible cells: {accessible_cells}")
    print(f"Worst-case path length: {max_path_length} moves")
    print(f"Time needed at 0.08s/move: {max_path_length * 0.08:.1f} seconds")
    print()
    
    # Compare with different timer values
    print("TIMER COMPARISON:")
    print("-" * 20)
    
    timer_values = [5, 10, 15, 20, 25, 30]
    for timer in timer_values:
        max_time = max_path_length * 0.08
        if max_time <= timer:
            status = "✓ Possible"
        else:
            deficit = max_time - timer
            status = f"✗ Impossible (need {deficit:.1f}s more)"
        print(f"Timer {timer:2d}s: {status}")
    
    print()
    
    # Performance implications
    print("PERFORMANCE IMPLICATIONS:")
    print("-" * 25)
    
    print(f"Maximum maze has {total_cells} cells")
    print(f"Worst-case path visits {max_path_length} cells")
    print(f"At 60 FPS, rendering takes {max_path_length/60:.1f} seconds just for display")
    print(f"Player movement time: {max_path_length * 0.08:.1f} seconds")
    print(f"Total theoretical time: {max_path_length/60 + max_path_length * 0.08:.1f} seconds")
    print()
    
    # Recommendations
    print("RECOMMENDATIONS:")
    print("-" * 15)
    
    if impossible_count > 0:
        print("🚨 CRITICAL ISSUES:")
        print("1. Maximum-sized mazes become impossible to complete")
        print("2. Timer is insufficient for worst-case scenarios")
        print("3. Consider implementing minimum timer of 20+ seconds")
        print("4. Add difficulty settings for different skill levels")
    
    print("5. Consider capping maze size at 40×30 for better balance")
    print("6. Implement power-ups or time bonuses for large mazes")
    print("7. Add practice mode with no time limit")
    print("8. Test with actual players to validate worst-case scenarios")
    
    print()
    
    # Alternative analysis with more realistic path estimates
    print("REALISTIC PATH ANALYSIS:")
    print("-" * 25)
    
    realistic_factors = [1.5, 2.0, 2.5, 3.0]
    manhattan_distance = (width - 2) + (height - 2)  # Start to end distance
    
    print("Path Factor | Est. Length | Time Needed | Status")
    print("-" * 50)
    
    for factor in realistic_factors:
        realistic_path = int(manhattan_distance * factor)
        realistic_time = realistic_path * 0.08
        
        if realistic_time <= 20:  # Using 20s as reasonable timer
            status = "✓ Reasonable"
        elif realistic_time <= 30:
            status = "⚠️  Challenging"
        else:
            status = "✗ Too Long"
        
        print(f"{factor:10.1f} | {realistic_path:11d} | {realistic_time:10.1f}s | {status}")
    
    print()
    print("=" * 60)
    print("ANALYSIS COMPLETE")

def test_cursor_speed_variations():
    """Test different cursor speeds to find optimal settings"""
    print("\nCURSOR SPEED ANALYSIS:")
    print("-" * 25)
    
    # Maximum maze parameters
    width, height = 50, 40
    manhattan_distance = (width - 2) + (height - 2)
    max_path_length = estimate_maximum_path_length(width, height)
    
    print("Move Delay | Max Path Time | Realistic Path Time | Recommended Timer")
    print("-" * 70)
    
    delays = [0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.12, 0.15]
    
    for delay in delays:
        max_time = max_path_length * delay
        realistic_time = manhattan_distance * 2.0 * delay  # 2x Manhattan distance
        recommended_timer = max(realistic_time * 1.5, 15)  # 50% buffer, minimum 15s
        
        print(f"{delay:8.2f}s | {max_time:12.1f}s | {realistic_time:18.1f}s | {recommended_timer:16.0f}s")
    
    print()
    print("Note: Current delay is 0.08s, which may be too slow for maximum-sized mazes")

if __name__ == "__main__":
    analyze_maximum_route()
    test_cursor_speed_variations() 