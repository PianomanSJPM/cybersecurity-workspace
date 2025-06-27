#!/usr/bin/env python3
"""
Maze Navigator - Maximum Maze Size Progression Test
==================================================

This script calculates how many mazes it would take to reach the maximum maze size
and estimates the time required for a player to achieve this.

Constants from maze_game.py:
- BASE_MAZE_WIDTH = 15, BASE_MAZE_HEIGHT = 10
- MAX_MAZE_WIDTH = 50, MAX_MAZE_HEIGHT = 40
- Size increases every 5 mazes
- Timer starts at 30s, reduces by 2s per maze, resets every 10 mazes
"""

def calculate_maze_size(maze_count):
    """Calculate maze size for a given maze count"""
    # Group mazes: 1-5, 6-10, 11-15, 16-20, 21-25, 26-30, etc.
    size_increase = (maze_count - 1) // 5
    
    current_width = min(15 + size_increase, 50)   # BASE_MAZE_WIDTH + size_increase, MAX_MAZE_WIDTH
    current_height = min(10 + size_increase, 40)  # BASE_MAZE_HEIGHT + size_increase, MAX_MAZE_HEIGHT
    
    return current_width, current_height

def calculate_timer(maze_number):
    """Calculate timer for a given maze number"""
    base_time = 30
    time_reduction = 2
    
    # Reset to full time every 10 mazes (1, 11, 21, 31, etc.)
    if maze_number % 10 == 1:
        return base_time
    else:
        mazes_since_reset = (maze_number - 1) % 10
        return max(5, base_time - (mazes_since_reset * time_reduction))

def test_progression():
    """Test the maze progression system"""
    print("MAZE NAVIGATOR - MAXIMUM MAZE SIZE PROGRESSION TEST")
    print("=" * 60)
    print()
    
    # Find when we reach maximum size
    max_width_reached = False
    max_height_reached = False
    max_size_maze = None
    
    print("MAZE SIZE PROGRESSION:")
    print("-" * 40)
    
    for maze_num in range(1, 200):  # Test up to 200 mazes
        width, height = calculate_maze_size(maze_num)
        timer = calculate_timer(maze_num)
        
        # Check if we've reached maximum size
        if width == 50 and not max_width_reached:
            max_width_reached = True
            print(f"✓ MAX WIDTH (50) reached at Maze {maze_num}")
        
        if height == 40 and not max_height_reached:
            max_height_reached = True
            print(f"✓ MAX HEIGHT (40) reached at Maze {maze_num}")
        
        if width == 50 and height == 40 and max_size_maze is None:
            max_size_maze = maze_num
            print(f"✓ MAX SIZE (50×40) reached at Maze {maze_num}")
            print()
            break
        
        # Print every 10th maze for overview
        if maze_num % 10 == 1 or maze_num <= 20:
            print(f"Maze {maze_num:3d}: {width:2d}×{height:2d} | Timer: {timer:2.0f}s")
    
    if max_size_maze is None:
        print("ERROR: Maximum size not reached within 200 mazes!")
        return
    
    print("DETAILED ANALYSIS:")
    print("-" * 40)
    
    # Calculate total time required
    total_time = 0
    total_mazes = max_size_maze
    
    print(f"Total mazes to reach max size: {total_mazes}")
    print()
    
    print("TIMER ANALYSIS:")
    print("-" * 20)
    
    # Group by 10-maze cycles
    for cycle in range(0, (total_mazes + 9) // 10):
        start_maze = cycle * 10 + 1
        end_maze = min((cycle + 1) * 10, total_mazes)
        
        cycle_time = 0
        print(f"Cycle {cycle + 1} (Mazes {start_maze}-{end_maze}):")
        
        for maze_num in range(start_maze, end_maze + 1):
            timer = calculate_timer(maze_num)
            cycle_time += timer
            print(f"  Maze {maze_num:2d}: {timer:2.0f}s")
        
        total_time += cycle_time
        print(f"  Cycle total: {cycle_time:.0f}s")
        print()
    
    print(f"TOTAL TIME REQUIRED: {total_time:.0f} seconds ({total_time/60:.1f} minutes)")
    print()
    
    # Realistic assessment
    print("REALISTIC ASSESSMENT:")
    print("-" * 25)
    
    # Assume average player takes 50% of available time per maze
    realistic_time = total_time * 0.5
    print(f"Assuming player uses 50% of available time per maze:")
    print(f"Realistic time: {realistic_time:.0f}s ({realistic_time/60:.1f} minutes)")
    print(f"Realistic time: {realistic_time/3600:.1f} hours")
    print()
    
    # Difficulty assessment
    print("DIFFICULTY ASSESSMENT:")
    print("-" * 25)
    
    # Check timer at max size
    max_size_timer = calculate_timer(max_size_maze)
    print(f"Timer at max size (Maze {max_size_maze}): {max_size_timer}s")
    
    if max_size_timer <= 5:
        print("⚠️  WARNING: Timer is very low (≤5s) at max size!")
        print("   This may be extremely difficult for most players.")
    elif max_size_timer <= 10:
        print("⚠️  CAUTION: Timer is low (≤10s) at max size.")
        print("   This will be challenging for most players.")
    else:
        print("✓ Timer at max size is reasonable.")
    
    print()
    
    # Performance considerations
    print("PERFORMANCE CONSIDERATIONS:")
    print("-" * 30)
    
    max_cells = 50 * 40  # 2000 cells
    print(f"Maximum maze size: 50×40 = {max_cells} cells")
    
    if max_cells > 1000:
        print("⚠️  Large maze size may impact performance on slower devices.")
        print("   Consider optimizing maze generation algorithms.")
    
    print()
    
    # Recommendations
    print("RECOMMENDATIONS:")
    print("-" * 15)
    
    if max_size_timer <= 5:
        print("1. Consider increasing minimum timer to 8-10 seconds")
        print("2. Add more time resets (every 5 mazes instead of 10)")
        print("3. Implement difficulty settings")
    
    if max_cells > 1000:
        print("4. Consider capping maze size at 40×30 for better performance")
        print("5. Optimize maze generation for larger sizes")
    
    print("6. Test with actual players to validate difficulty curve")
    print("7. Consider adding power-ups or time bonuses")
    
    print()
    print("=" * 60)
    print("TEST COMPLETE")

if __name__ == "__main__":
    test_progression() 