#!/usr/bin/env python3
"""
Maze Navigator - Difficulty Analysis Test
========================================

This script analyzes whether mazes become too difficult to complete within the time limits.
It considers:
- Maze size and complexity
- Optimal path length
- Player movement speed
- Time constraints
- Realistic completion scenarios
"""

import math

def calculate_maze_size(maze_count):
    """Calculate maze size for a given maze count"""
    size_increase = (maze_count - 1) // 5
    current_width = min(15 + size_increase, 50)
    current_height = min(10 + size_increase, 40)
    return current_width, current_height

def calculate_timer(maze_number):
    """Calculate timer for a given maze number"""
    base_time = 30
    time_reduction = 1  # 1 second less each maze (reduced from 2)
    
    if maze_number % 10 == 1:
        return base_time
    else:
        mazes_since_reset = (maze_number - 1) % 10
        return max(20, base_time - (mazes_since_reset * time_reduction))  # 20s minimum (increased from 5)

def estimate_optimal_path_length(width, height):
    """Estimate the optimal path length from start to end"""
    # In a maze, the optimal path is roughly the Manhattan distance
    # But mazes have walls, so we need to account for detours
    # A reasonable estimate is 1.5-2x the Manhattan distance
    
    manhattan_distance = (width - 2) + (height - 2)  # Start at (1,1), end at (width-2, height-2)
    
    # Factor in maze complexity (walls force detours)
    complexity_factor = 1.8  # Conservative estimate
    
    return int(manhattan_distance * complexity_factor)

def calculate_movement_time(path_length, move_delay=0.08):
    """Calculate time needed to traverse the path"""
    # Each move takes move_delay seconds
    return path_length * move_delay

def analyze_difficulty():
    """Analyze maze difficulty progression"""
    print("MAZE NAVIGATOR - DIFFICULTY ANALYSIS")
    print("=" * 60)
    print()
    
    print("ANALYSIS PARAMETERS:")
    print("-" * 25)
    print("Player movement delay: 0.08 seconds per move")
    print("Optimal path estimate: 1.8x Manhattan distance")
    print("Safety margin: 20% extra time for suboptimal paths")
    print()
    
    print("MAZE DIFFICULTY PROGRESSION:")
    print("-" * 35)
    print("Maze | Size  | Timer | Est.Path | Move.Time | Safe.Time | Status")
    print("-" * 75)
    
    critical_mazes = []
    impossible_mazes = []
    
    for maze_num in range(1, 200):
        width, height = calculate_maze_size(maze_num)
        timer = calculate_timer(maze_num)
        
        # Skip if we've reached max size
        if width == 50 and height == 40:
            break
        
        # Calculate path length and movement time
        path_length = estimate_optimal_path_length(width, height)
        move_time = calculate_movement_time(path_length)
        
        # Add 20% safety margin for suboptimal paths
        safe_time = move_time * 1.2
        
        # Determine status
        if safe_time <= timer * 0.5:  # Very comfortable
            status = "Easy"
        elif safe_time <= timer * 0.8:  # Comfortable
            status = "Comfortable"
        elif safe_time <= timer:  # Challenging but possible
            status = "Challenging"
        elif safe_time <= timer * 1.2:  # Very difficult
            status = "Very Hard"
            critical_mazes.append(maze_num)
        else:  # Likely impossible
            status = "IMPOSSIBLE"
            impossible_mazes.append(maze_num)
        
        # Print every 10th maze and critical ones
        if maze_num % 10 == 1 or maze_num <= 20 or status in ["Very Hard", "IMPOSSIBLE"]:
            print(f"{maze_num:4d} | {width:2d}×{height:2d} | {timer:5.0f}s | {path_length:8d} | {move_time:8.1f}s | {safe_time:8.1f}s | {status}")
    
    print()
    
    # Summary analysis
    print("CRITICAL ANALYSIS:")
    print("-" * 20)
    
    if critical_mazes:
        print(f"⚠️  Very difficult mazes (need >80% of time): {len(critical_mazes)}")
        print(f"   First critical maze: {critical_mazes[0]}")
        print(f"   Critical mazes: {critical_mazes[:10]}{'...' if len(critical_mazes) > 10 else ''}")
    else:
        print("✓ No very difficult mazes found")
    
    if impossible_mazes:
        print(f"🚨 IMPOSSIBLE mazes (need >100% of time): {len(impossible_mazes)}")
        print(f"   First impossible maze: {impossible_mazes[0]}")
        print(f"   Impossible mazes: {impossible_mazes[:10]}{'...' if len(impossible_mazes) > 10 else ''}")
    else:
        print("✓ No impossible mazes found")
    
    print()
    
    # Performance analysis
    print("PERFORMANCE ANALYSIS:")
    print("-" * 25)
    
    # Find when mazes become very large
    large_mazes = []
    for maze_num in range(1, 200):
        width, height = calculate_maze_size(maze_num)
        if width * height > 1000:  # More than 1000 cells
            large_mazes.append(maze_num)
            if len(large_mazes) == 1:
                print(f"First large maze (>1000 cells): Maze {maze_num} ({width}×{height} = {width*height} cells)")
    
    if large_mazes:
        print(f"Total large mazes: {len(large_mazes)}")
        print("⚠️  Large mazes may impact performance on slower devices")
    
    print()
    
    # Recommendations
    print("RECOMMENDATIONS:")
    print("-" * 15)
    
    if impossible_mazes:
        print("1. 🚨 CRITICAL: Increase minimum timer to prevent impossible mazes")
        print("2. Consider reducing time reduction from 2s to 1.5s per maze")
        print("3. Add more frequent timer resets (every 5 mazes instead of 10)")
    
    if critical_mazes:
        print("4. ⚠️  Consider adding difficulty settings")
        print("5. Implement power-ups or time bonuses")
        print("6. Add practice mode with no time limit")
    
    print("7. Test with actual players to validate difficulty curve")
    print("8. Consider capping maze size for better performance")
    
    print()
    
    # Detailed analysis of specific mazes
    print("DETAILED ANALYSIS - CRITICAL MAZES:")
    print("-" * 40)
    
    if critical_mazes or impossible_mazes:
        problem_mazes = critical_mazes + impossible_mazes
        for maze_num in problem_mazes[:5]:  # Show first 5
            width, height = calculate_maze_size(maze_num)
            timer = calculate_timer(maze_num)
            path_length = estimate_optimal_path_length(width, height)
            move_time = calculate_movement_time(path_length)
            safe_time = move_time * 1.2
            
            print(f"Maze {maze_num}: {width}×{height} | Timer: {timer}s | Need: {safe_time:.1f}s | Deficit: {safe_time - timer:.1f}s")
    else:
        print("No critical mazes found - difficulty curve is well-balanced!")
    
    print()
    print("=" * 60)
    print("ANALYSIS COMPLETE")

def test_player_scenarios():
    """Test different player skill levels"""
    print("\nPLAYER SKILL SCENARIO ANALYSIS:")
    print("-" * 35)
    
    scenarios = [
        ("Expert Player", 1.0, "Takes optimal path"),
        ("Skilled Player", 1.2, "Minor detours"),
        ("Average Player", 1.5, "Some backtracking"),
        ("Novice Player", 2.0, "Many detours"),
        ("Beginner Player", 2.5, "Frequent backtracking")
    ]
    
    print("Skill Level | Time Factor | Description | Critical Maze")
    print("-" * 65)
    
    for skill, factor, desc in scenarios:
        # Find first maze where this skill level would struggle
        critical_maze = None
        for maze_num in range(1, 200):
            width, height = calculate_maze_size(maze_num)
            if width == 50 and height == 40:
                break
                
            timer = calculate_timer(maze_num)
            path_length = estimate_optimal_path_length(width, height)
            move_time = calculate_movement_time(path_length)
            required_time = move_time * factor
            
            if required_time > timer:
                critical_maze = maze_num
                break
        
        if critical_maze:
            print(f"{skill:12s} | {factor:10.1f} | {desc:11s} | Maze {critical_maze}")
        else:
            print(f"{skill:12s} | {factor:10.1f} | {desc:11s} | Never")
    
    print()

if __name__ == "__main__":
    analyze_difficulty()
    test_player_scenarios() 