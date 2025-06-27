#!/usr/bin/env python3
"""
Maze Navigator - New Timer Mechanics Test
========================================

This script tests the updated timer mechanics:
- 1 second reduction per maze (instead of 2)
- 20 second minimum timer (instead of 5)
"""

def calculate_timer(maze_number):
    """Calculate timer for a given maze number with new mechanics"""
    base_time = 30
    time_reduction = 1  # 1 second less each maze
    
    if maze_number % 10 == 1:  # Maze 1, 11, 21, 31, etc.
        return base_time
    else:
        mazes_since_reset = (maze_number - 1) % 10
        return max(20, base_time - (mazes_since_reset * time_reduction))

def test_new_timer_mechanics():
    """Test the new timer mechanics"""
    print("MAZE NAVIGATOR - NEW TIMER MECHANICS TEST")
    print("=" * 50)
    print()
    
    print("NEW TIMER PARAMETERS:")
    print("-" * 25)
    print("Base time: 30 seconds")
    print("Time reduction: 1 second per maze")
    print("Minimum timer: 20 seconds")
    print("Reset every: 10 mazes")
    print()
    
    print("TIMER PROGRESSION TEST:")
    print("-" * 25)
    print("Maze | Timer | Status")
    print("-" * 20)
    
    # Test first 20 mazes
    for maze_num in range(1, 21):
        timer = calculate_timer(maze_num)
        status = "✓ Good" if timer >= 20 else "✗ Too Low"
        print(f"{maze_num:4d} | {timer:5.0f}s | {status}")
    
    print()
    
    # Test some critical mazes
    print("CRITICAL MAZES TEST:")
    print("-" * 20)
    print("Maze | Timer | Status")
    print("-" * 20)
    
    critical_mazes = [30, 40, 50, 100, 150, 170, 176]
    for maze_num in critical_mazes:
        timer = calculate_timer(maze_num)
        status = "✓ Good" if timer >= 20 else "✗ Too Low"
        print(f"{maze_num:4d} | {timer:5.0f}s | {status}")
    
    print()
    
    # Test the 10-maze cycle
    print("10-MAZE CYCLE TEST:")
    print("-" * 20)
    print("Cycle | Start Maze | End Maze | Timer Range")
    print("-" * 45)
    
    for cycle in range(1, 6):
        start_maze = (cycle - 1) * 10 + 1
        end_maze = cycle * 10
        start_timer = calculate_timer(start_maze)
        end_timer = calculate_timer(end_maze)
        print(f"{cycle:5d} | {start_maze:10d} | {end_maze:8d} | {start_timer:.0f}s - {end_timer:.0f}s")
    
    print()
    
    # Verify minimum timer is never violated
    print("MINIMUM TIMER VERIFICATION:")
    print("-" * 30)
    
    min_timer_found = float('inf')
    min_timer_maze = 0
    
    for maze_num in range(1, 200):
        timer = calculate_timer(maze_num)
        if timer < min_timer_found:
            min_timer_found = timer
            min_timer_maze = maze_num
    
    print(f"Lowest timer found: {min_timer_found:.0f}s (Maze {min_timer_maze})")
    
    if min_timer_found >= 20:
        print("✓ SUCCESS: Minimum timer of 20s is never violated")
    else:
        print("✗ FAILURE: Timer falls below 20s minimum")
    
    print()
    
    # Compare with old mechanics
    print("COMPARISON WITH OLD MECHANICS:")
    print("-" * 35)
    print("Maze | Old Timer | New Timer | Improvement")
    print("-" * 45)
    
    def old_calculate_timer(maze_number):
        """Old timer calculation for comparison"""
        base_time = 30
        time_reduction = 2  # 2 seconds less each maze
        
        if maze_number % 10 == 1:
            return base_time
        else:
            mazes_since_reset = (maze_number - 1) % 10
            return max(5, base_time - (mazes_since_reset * time_reduction))
    
    comparison_mazes = [10, 20, 30, 40, 50, 100, 150, 170]
    for maze_num in comparison_mazes:
        old_timer = old_calculate_timer(maze_num)
        new_timer = calculate_timer(maze_num)
        improvement = new_timer - old_timer
        print(f"{maze_num:4d} | {old_timer:9.0f}s | {new_timer:9.0f}s | {improvement:+6.0f}s")
    
    print()
    print("=" * 50)
    print("TEST COMPLETE")

if __name__ == "__main__":
    test_new_timer_mechanics() 