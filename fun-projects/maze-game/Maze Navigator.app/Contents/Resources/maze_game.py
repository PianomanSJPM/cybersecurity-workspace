import pygame
import random
import sys
import time
import json
import os
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200  # Increased from 800
SCREEN_HEIGHT = 800  # Increased from 600
CELL_SIZE = 20  # Reduced from 25 to make tiles smaller
BASE_MAZE_WIDTH = 15  # Starting maze width
BASE_MAZE_HEIGHT = 10  # Starting maze height
MAX_MAZE_WIDTH = 50   # Maximum maze width (increased from 25)
MAX_MAZE_HEIGHT = 40  # Maximum maze height (increased from 20)
UI_HEADER_HEIGHT = 80  # Height for UI header area

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

class CellType(Enum):
    WALL = 0
    PATH = 1
    START = 2
    END = 3
    PLAYER = 4

class HighScoreManager:
    def __init__(self, filename="high_scores.json"):
        self.filename = filename
        self.scores = self.load_scores()
    
    def load_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def save_scores(self):
        """Save high scores to file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.scores, f, indent=2)
        except:
            pass
    
    def add_score(self, initials, score):
        """Add a new score and maintain top 10"""
        self.scores.append({"initials": initials.upper(), "score": score})
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:10]  # Keep only top 10
        self.save_scores()
    
    def is_high_score(self, score):
        """Check if score qualifies for high score list"""
        if len(self.scores) < 10:
            return True
        return score > min(s["score"] for s in self.scores)
    
    def get_rank(self, score):
        """Get the rank of a score (1-based)"""
        for i, s in enumerate(self.scores):
            if score >= s["score"]:
                return i + 1
        return len(self.scores) + 1

class MazeGame:
    def __init__(self):
        self.fullscreen = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Maze Navigator - Speed Challenge")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        
        self.maze = []
        self.player_pos = [1, 1]
        self.start_pos = [1, 1]
        self.end_pos = [MAX_MAZE_WIDTH - 2, MAX_MAZE_HEIGHT - 2]
        self.moves = 0
        self.game_won = False
        self.game_over = False
        
        # Timer system
        self.maze_count = 0
        self.base_time = 30  # 30 seconds for first maze (reduced from 60)
        self.time_reduction = 1  # 1 second less each maze (reduced from 2)
        self.time_remaining = self.base_time
        self.start_time = time.time()
        self.last_time = time.time()
        
        # Game state management
        self.game_started = False  # New: track if game has started
        self.timer_started = False  # New: track if timer has started
        self.showing_next_maze = False  # New: track if showing next maze screen
        self.next_maze_start_time = 0  # New: track when next maze screen started
        
        # Settings
        self.show_transitions = True  # New: control whether to show transition screens
        
        # Screen system
        self.current_screen = "title"  # New: track current screen (title, menu, game, high_scores, controls)
        self.menu_selection = 0  # New: track which menu option is selected
        
        # High score system
        self.high_score_manager = HighScoreManager()
        self.showing_high_scores = False
        self.entering_initials = False
        self.initials = ""
        self.final_score = 0
        
        # Initials input system
        self.initials_positions = [0, 0, 0]  # Current position for each letter (0-35: A-Z, 0-9)
        self.current_initial = 0  # Which initial we're editing (0, 1, or 2)
        self.available_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # 36 characters total
        
        # Menu system
        self.showing_menu = False
        self.adjusting_speed = False  # New: track if adjusting movement speed
        self.move_delay_min = 0.05
        self.move_delay_max = 0.15
        self.move_delay_step = 0.01
        
        # Continuous movement system
        self.keys_pressed = set()
        self.last_move_time = 0
        self.move_delay = 0.08  # Delay between moves in seconds (slightly faster)
        
        # Maze generation algorithm
        self.algorithm = random.choice(['recursive', 'kruskal', 'prim'])
        
        # Random seed for different mazes each time
        random.seed()
        self.generate_maze()
        
    def ensure_valid_menu_selection(self):
        """Ensure menu selection is within valid bounds for current menu options"""
        total_menu_options = 6 if not (self.current_screen == "game" or self.game_started) else 7
        if self.menu_selection >= total_menu_options:
            self.menu_selection = 0
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            # Get the screen info for fullscreen
            screen_info = pygame.display.Info()
            self.screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Update the display
        pygame.display.flip()
    
    def get_screen_dimensions(self):
        """Get current screen dimensions (works for both fullscreen and windowed)"""
        if self.fullscreen:
            return self.screen.get_size()
        else:
            return SCREEN_WIDTH, SCREEN_HEIGHT
    
    def calculate_maze_size(self):
        """Calculate the current maze size based on maze count"""
        # Group mazes: 1-5, 6-10, 11-15, 16-20, 21-25, 26-30, etc.
        # Use (maze_count - 1) // 5 to get the correct group
        # Allow unlimited progression up to MAX_MAZE_WIDTH x MAX_MAZE_HEIGHT
        size_increase = (self.maze_count - 1) // 5
        
        current_width = min(BASE_MAZE_WIDTH + size_increase, MAX_MAZE_WIDTH)
        current_height = min(BASE_MAZE_HEIGHT + size_increase, MAX_MAZE_HEIGHT)
        
        return current_width, current_height
    
    def generate_maze(self):
        """Generate a new maze using the selected algorithm"""
        # Calculate current maze size
        self.current_maze_width, self.current_maze_height = self.calculate_maze_size()
        
        # Initialize maze with walls (use current size, not max size)
        self.maze = [[CellType.WALL for _ in range(self.current_maze_width)] for _ in range(self.current_maze_height)]
        
        # Set start and end positions (ensure they're at odd positions for proper maze generation)
        self.start_pos = [1, 1]
        self.end_pos = [self.current_maze_width - 2, self.current_maze_height - 2]
        
        # Ensure end position is odd for proper maze generation
        if self.end_pos[0] % 2 == 0:
            self.end_pos[0] -= 1
        if self.end_pos[1] % 2 == 0:
            self.end_pos[1] -= 1
        
        # Generate maze based on algorithm
        if self.algorithm == "recursive":
            self._generate_recursive_maze()
        elif self.algorithm == "kruskal":
            self._generate_kruskal_maze()
        elif self.algorithm == "prim":
            self._generate_prim_maze()
        
        # Ensure start and end are paths
        self.maze[self.start_pos[1]][self.start_pos[0]] = CellType.START
        self.maze[self.end_pos[1]][self.end_pos[0]] = CellType.END
        
        # Reset player position
        self.player_pos = self.start_pos.copy()
        
        # Verify maze is solvable
        if not self._verify_maze_solvable():
            # If not solvable, regenerate with a different algorithm
            self.algorithm = random.choice(['recursive', 'kruskal', 'prim'])
            self.generate_maze()
    
    def _verify_maze_solvable(self):
        """Verify that the maze has a path from start to end"""
        # Simple flood fill to check connectivity
        visited = set()
        stack = [self.start_pos]
        
        while stack:
            x, y = stack.pop()
            if (x, y) == tuple(self.end_pos):
                return True
            
            if (x, y) in visited:
                continue
                
            visited.add((x, y))
            
            # Check all four directions
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.current_maze_width and 
                    0 <= ny < self.current_maze_height and
                    self.maze[ny][nx] in [CellType.PATH, CellType.START, CellType.END] and
                    (nx, ny) not in visited):
                    stack.append((nx, ny))
        
        return False
    
    def _generate_recursive_maze(self):
        """Generate maze using recursive backtracking - creates proper corridors"""
        def carve_path(x, y):
            self.maze[y][x] = CellType.PATH
            
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 < nx < self.current_maze_width - 1 and 0 < ny < self.current_maze_height - 1 and 
                    self.maze[ny][nx] == CellType.WALL):
                    # Carve the wall between current cell and next cell
                    self.maze[y + dy//2][x + dx//2] = CellType.PATH
                    carve_path(nx, ny)
        
        # Start from the start position to ensure connectivity
        carve_path(self.start_pos[0], self.start_pos[1])
        
        # Ensure end position is reachable by carving a path to it
        if self.maze[self.end_pos[1]][self.end_pos[0]] == CellType.WALL:
            # Find the closest path to the end and connect it
            self._connect_to_end()
        
    def _generate_kruskal_maze(self):
        """Generate maze using Kruskal's algorithm - ensures single-width corridors"""
        # Create list of all walls between cells
        walls = []
        for y in range(1, self.current_maze_height - 1, 2):
            for x in range(1, self.current_maze_width - 1, 2):
                self.maze[y][x] = CellType.PATH
                # Add walls to the right and down
                if x + 2 < self.current_maze_width - 1:
                    walls.append((x + 1, y, 'horizontal'))
                if y + 2 < self.current_maze_height - 1:
                    walls.append((x, y + 1, 'vertical'))
        
        # Shuffle walls
        random.shuffle(walls)
        
        # Union-find data structure
        parent = {}
        for y in range(1, self.current_maze_height - 1, 2):
            for x in range(1, self.current_maze_width - 1, 2):
                parent[(x, y)] = (x, y)
        
        def find(cell):
            if parent[cell] != cell:
                parent[cell] = find(parent[cell])
            return parent[cell]
        
        def union(cell1, cell2):
            parent[find(cell1)] = find(cell2)
        
        # Process walls
        for wall_x, wall_y, direction in walls:
            if direction == 'horizontal':
                cell1 = (wall_x - 1, wall_y)
                cell2 = (wall_x + 1, wall_y)
            else:  # vertical
                cell1 = (wall_x, wall_y - 1)
                cell2 = (wall_x, wall_y + 1)
            
            if find(cell1) != find(cell2):
                self.maze[wall_y][wall_x] = CellType.PATH
                union(cell1, cell2)
        
        # Ensure end position is reachable
        if self.maze[self.end_pos[1]][self.end_pos[0]] == CellType.WALL:
            self._connect_to_end()
        
    def _generate_prim_maze(self):
        """Generate maze using Prim's algorithm - creates proper maze structure"""
        # Initialize with walls
        for y in range(self.current_maze_height):
            for x in range(self.current_maze_width):
                if x % 2 == 1 and y % 2 == 1:
                    self.maze[y][x] = CellType.PATH
        
        # Start from the start position
        start_x, start_y = self.start_pos[0], self.start_pos[1]
        
        # List of frontier cells
        frontier = set()
        # Add initial cell's neighbors to frontier
        for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
            nx, ny = start_x + dx, start_y + dy
            if 0 < nx < self.current_maze_width - 1 and 0 < ny < self.current_maze_height - 1:
                frontier.add((nx, ny))
        
        # Process frontier cells
        while frontier:
            # Pick a random frontier cell
            fx, fy = random.choice(list(frontier))
            frontier.remove((fx, fy))
            
            # Find neighbors that are already part of the maze
            neighbors = []
            for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                nx, ny = fx + dx, fy + dy
                if (0 < nx < self.current_maze_width - 1 and 0 < ny < self.current_maze_height - 1 and 
                    self.maze[ny][nx] == CellType.PATH):
                    neighbors.append((nx, ny))
            
            if neighbors:
                # Connect to a random neighbor
                nx, ny = random.choice(neighbors)
                # Carve the wall between them
                wall_x = (fx + nx) // 2
                wall_y = (fy + ny) // 2
                self.maze[wall_y][wall_x] = CellType.PATH
                self.maze[fy][fx] = CellType.PATH
                
                # Add new frontier cells
                for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                    new_x, new_y = fx + dx, fy + dy
                    if (0 < new_x < self.current_maze_width - 1 and 0 < new_y < self.current_maze_height - 1 and 
                        self.maze[new_y][new_x] == CellType.WALL):
                        frontier.add((new_x, new_y))
        
        # Ensure end position is reachable
        if self.maze[self.end_pos[1]][self.end_pos[0]] == CellType.WALL:
            self._connect_to_end()
    
    def _connect_to_end(self):
        """Connect the end position to the existing maze using a simple pathfinding approach"""
        # Find the closest path cell to the end
        min_distance = float('inf')
        closest_path = None
        
        for y in range(self.current_maze_height):
            for x in range(self.current_maze_width):
                if self.maze[y][x] == CellType.PATH:
                    distance = abs(x - self.end_pos[0]) + abs(y - self.end_pos[1])
                    if distance < min_distance:
                        min_distance = distance
                        closest_path = (x, y)
        
        if closest_path:
            # Create a path from the closest path to the end
            current_x, current_y = closest_path
            target_x, target_y = self.end_pos[0], self.end_pos[1]
            
            while (current_x, current_y) != (target_x, target_y):
                # Move towards target
                if current_x < target_x:
                    current_x += 1
                elif current_x > target_x:
                    current_x -= 1
                elif current_y < target_y:
                    current_y += 1
                elif current_y > target_y:
                    current_y -= 1
                
                # Ensure we don't go out of bounds
                current_x = max(0, min(current_x, self.current_maze_width - 1))
                current_y = max(0, min(current_y, self.current_maze_height - 1))
                
                # Mark as path
                self.maze[current_y][current_x] = CellType.PATH
    
    def update_timer(self):
        """Update the timer and check for game over"""
        # Don't update timer during transition screens or non-game screens
        if self.showing_next_maze or self.current_screen != "game":
            return
            
        current_time = time.time()
        elapsed = current_time - self.last_time
        self.last_time = current_time
        
        if not self.game_won and not self.game_over and not self.entering_initials and self.timer_started:
            self.time_remaining -= elapsed
            
            if self.time_remaining <= 0:
                self.time_remaining = 0
                self.game_over = True
                self.handle_game_over()
    
    def handle_game_over(self):
        """Handle game over and check for high score"""
        self.final_score = self.maze_count
        
        if self.high_score_manager.is_high_score(self.final_score):
            self.entering_initials = True
        else:
            self.showing_high_scores = True
    
    def next_maze(self):
        """Move to the next maze"""
        # Timer calculation is now done in advance when player wins
        
        self.game_won = False
        self.moves = 0
        self.player_pos = self.start_pos.copy()
        self.maze_count += 1
        self.algorithm = random.choice(['recursive', 'kruskal', 'prim'])
        self.generate_maze()
        if self.show_transitions:
            self.showing_next_maze = True
            self.next_maze_start_time = time.time()
            self.game_started = False
            self.timer_started = False
        else:
            self.game_started = True
            self.timer_started = True
            self.last_time = time.time()
    
    def draw_start_screen(self):
        """Draw the title screen"""
        # Get current screen dimensions
        current_width, current_height = self.get_screen_dimensions()
        
        # Background
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.large_font.render("MAZE NAVIGATOR", True, GOLD)
        title_rect = title_text.get_rect(center=(current_width // 2, 200))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font.render("Speed Challenge", True, CYAN)
        subtitle_rect = subtitle_text.get_rect(center=(current_width // 2, 250))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Instructions
        start_text = self.font.render("Press ENTER to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(current_width // 2, 350))
        self.screen.blit(start_text, start_rect)
        
        menu_text = self.font.render("Press 'M' for Menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(current_width // 2, 400))
        self.screen.blit(menu_text, menu_rect)
        
        # High scores preview
        if self.high_score_manager.scores:
            scores_title = self.font.render("Top Score:", True, GOLD)
            scores_title_rect = scores_title.get_rect(center=(current_width // 2, 500))
            self.screen.blit(scores_title, scores_title_rect)
            
            top_score = self.high_score_manager.scores[0]
            score_text = self.font.render(f"{top_score['initials']} - {top_score['score']} mazes", True, SILVER)
            score_rect = score_text.get_rect(center=(current_width // 2, 530))
            self.screen.blit(score_text, score_rect)
    
    def draw_maze(self):
        """Draw the maze on the screen"""
        self.screen.fill(BLACK)
        
        # Get current screen dimensions
        current_width, current_height = self.get_screen_dimensions()
        
        # Draw UI header area
        header_rect = pygame.Rect(0, 0, current_width, UI_HEADER_HEIGHT)
        pygame.draw.rect(self.screen, (40, 40, 40), header_rect)  # Dark gray header
        pygame.draw.rect(self.screen, WHITE, header_rect, 2)  # White border
        
        # Calculate dynamic cell size to fit maze in available space
        available_width = current_width
        available_height = current_height - UI_HEADER_HEIGHT
        
        # Calculate cell size to fit the maze
        cell_size_x = available_width // self.current_maze_width
        cell_size_y = available_height // self.current_maze_height
        dynamic_cell_size = min(cell_size_x, cell_size_y)
        
        # Center the maze if it's smaller than available space
        maze_width_pixels = self.current_maze_width * dynamic_cell_size
        maze_height_pixels = self.current_maze_height * dynamic_cell_size
        offset_x = (available_width - maze_width_pixels) // 2
        offset_y = UI_HEADER_HEIGHT + (available_height - maze_height_pixels) // 2
        
        for y in range(self.current_maze_height):
            for x in range(self.current_maze_width):
                cell = self.maze[y][x]
                rect = pygame.Rect(
                    x * dynamic_cell_size + offset_x, 
                    y * dynamic_cell_size + offset_y, 
                    dynamic_cell_size, 
                    dynamic_cell_size
                )
                
                if cell == CellType.WALL:
                    pygame.draw.rect(self.screen, PURPLE, rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 2)
                elif cell == CellType.PATH:
                    pygame.draw.rect(self.screen, WHITE, rect)
                elif cell == CellType.START:
                    pygame.draw.rect(self.screen, GREEN, rect)
                elif cell == CellType.END:
                    pygame.draw.rect(self.screen, RED, rect)
        
        # Draw player (adjusted for dynamic cell size and centering)
        player_rect = pygame.Rect(
            self.player_pos[0] * dynamic_cell_size + offset_x + 5,
            self.player_pos[1] * dynamic_cell_size + offset_y + 5,
            dynamic_cell_size - 10,
            dynamic_cell_size - 10
        )
        pygame.draw.rect(self.screen, BLUE, player_rect)
        
        # Draw UI based on current screen
        if self.current_screen == "title":
            self.draw_start_screen()
        elif self.current_screen == "menu":
            self.draw_menu()
        elif self.current_screen == "high_scores":
            self.draw_high_scores_screen()
        elif self.current_screen == "controls":
            self.draw_controls_screen()
        elif self.entering_initials:
            self.draw_initials_screen()
        elif self.showing_next_maze:
            self.draw_next_maze_screen()
        else:
            self.draw_ui()
        
    def draw_ui(self):
        """Draw user interface elements"""
        # Get current screen dimensions
        current_width, current_height = self.get_screen_dimensions()
        
        # Draw stats in the header area (no background panels needed)
        
        # Left side stats
        maze_text = self.font.render(f"Maze: {self.maze_count + 1}", True, YELLOW)
        self.screen.blit(maze_text, (20, 15))
        
        size_text = self.small_font.render(f"Size: {self.current_maze_width}×{self.current_maze_height}", True, CYAN)
        self.screen.blit(size_text, (20, 45))
        
        # Center stats
        # Calculate difficulty level based on maze size progression
        size_increase = (self.maze_count - 1) // 5
        difficulty_level = size_increase + 1  # Start at level 1 for mazes 1-5
        
        # Use a cycling color scheme for difficulty levels beyond 6
        difficulty_colors = [GREEN, YELLOW, ORANGE, RED, PURPLE, GOLD, CYAN, PINK, SILVER, BRONZE]
        color_index = (difficulty_level - 1) % len(difficulty_colors)
        
        difficulty_text = self.font.render(f"Difficulty: {difficulty_level}", True, difficulty_colors[color_index])
        difficulty_rect = difficulty_text.get_rect(center=(current_width // 2, 30))
        self.screen.blit(difficulty_text, difficulty_rect)
        
        # Right side stats
        timer_color = GREEN if self.time_remaining > 20 else (ORANGE if self.time_remaining > 10 else RED)
        timer_text = self.font.render(f"Time: {self.time_remaining:.1f}s", True, timer_color)
        timer_rect = timer_text.get_rect()
        timer_rect.topright = (current_width - 20, 15)
        self.screen.blit(timer_text, timer_rect)
        
        # Debug: Print timer value occasionally to track what's being displayed
        if hasattr(self, '_last_debug_time') and time.time() - self._last_debug_time > 5.0:
            print(f"DEBUG: Display timer for Maze {self.maze_count + 1} = {self.time_remaining:.1f}s")
            self._last_debug_time = time.time()
        elif not hasattr(self, '_last_debug_time'):
            self._last_debug_time = time.time()
        
        moves_text = self.font.render(f"Moves: {self.moves}", True, CYAN)
        moves_rect = moves_text.get_rect()
        moves_rect.topright = (current_width - 20, 45)
        self.screen.blit(moves_text, moves_rect)
        
        # Menu indicator (small and unobtrusive)
        menu_text = self.small_font.render("Press M for menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(current_width // 2, 60))
        self.screen.blit(menu_text, menu_rect)
        
        # Menu overlay
        if self.showing_menu:
            self.draw_menu()
        
        # Win message (keep as overlay for emphasis)
        if self.game_won:
            # Create semi-transparent overlay for better readability
            overlay = pygame.Surface((current_width, current_height))
            overlay.set_alpha(180)  # Semi-transparent
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            win_text = self.font.render(f"MAZE {self.maze_count + 1} COMPLETE!", True, GREEN)
            text_rect = win_text.get_rect(center=(current_width // 2, current_height // 2 - 30))
            self.screen.blit(win_text, text_rect)
            
            next_text = self.small_font.render("Press SPACE for next maze", True, YELLOW)
            next_rect = next_text.get_rect(center=(current_width // 2, current_height // 2 + 10))
            self.screen.blit(next_text, next_rect)
        
        # Game over message (keep as overlay for emphasis)
        if self.game_over:
            # Create semi-transparent overlay for better readability
            overlay = pygame.Surface((current_width, current_height))
            overlay.set_alpha(180)  # Semi-transparent
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("TIME'S UP!", True, RED)
            text_rect = game_over_text.get_rect(center=(current_width // 2, current_height // 2 - 30))
            self.screen.blit(game_over_text, text_rect)
            
            score_text = self.font.render(f"Final Score: {self.maze_count} mazes", True, YELLOW)
            score_rect = score_text.get_rect(center=(current_width // 2, current_height // 2 + 10))
            self.screen.blit(score_text, score_rect)
            
            restart_text = self.small_font.render("Press BACKSPACE to return to title screen", True, WHITE)
            restart_rect = restart_text.get_rect(center=(current_width // 2, current_height // 2 + 40))
            self.screen.blit(restart_text, restart_rect)
    
    def draw_initials_screen(self):
        """Draw the initials input screen"""
        # Get current screen dimensions
        current_width, current_height = self.get_screen_dimensions()
        
        # Background
        overlay = pygame.Surface((current_width, current_height))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Title
        title_text = self.large_font.render("NEW HIGH SCORE!", True, GOLD)
        title_rect = title_text.get_rect(center=(current_width // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Score
        score_text = self.font.render(f"Score: {self.final_score} mazes", True, YELLOW)
        score_rect = score_text.get_rect(center=(current_width // 2, 200))
        self.screen.blit(score_text, score_rect)
        
        # Rank
        rank = self.high_score_manager.get_rank(self.final_score)
        rank_text = self.font.render(f"Rank: #{rank}", True, CYAN)
        rank_rect = rank_text.get_rect(center=(current_width // 2, 240))
        self.screen.blit(rank_text, rank_rect)
        
        # Instructions
        instruction_text = self.font.render("Use Arrow Keys to select letters, ENTER to confirm", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(current_width // 2, 280))
        self.screen.blit(instruction_text, instruction_rect)
        
        # Initials display with scrolling selection
        initials_display = ""
        for i in range(3):
            char = self.available_chars[self.initials_positions[i]]
            if i == self.current_initial:
                # Highlight current selection
                initials_display += f"[{char}]"
            else:
                initials_display += f" {char} "
        
        initials_text = self.large_font.render(initials_display, True, GREEN)
        initials_rect = initials_text.get_rect(center=(current_width // 2, 350))
        self.screen.blit(initials_text, initials_rect)
        
        # Character selection display
        char_display = ""
        for i, char in enumerate(self.available_chars):
            if i == self.initials_positions[self.current_initial]:
                char_display += f"[{char}]"
            else:
                char_display += f" {char} "
        
        # Split into multiple lines for better display
        chars_per_line = 18
        for line_num in range(2):
            start_idx = line_num * chars_per_line
            end_idx = start_idx + chars_per_line
            line_chars = char_display[start_idx * 3:end_idx * 3]  # Each char takes 3 spaces
            
            char_line_text = self.small_font.render(line_chars, True, WHITE)
            char_line_rect = char_line_text.get_rect(center=(current_width // 2, 420 + line_num * 25))
            self.screen.blit(char_line_text, char_line_rect)
        
        # Submit instruction
        submit_text = self.small_font.render("Press ENTER to submit", True, WHITE)
        submit_rect = submit_text.get_rect(center=(current_width // 2, 480))
        self.screen.blit(submit_text, submit_rect)
    
    def draw_high_scores_screen(self):
        """Draw the high scores screen"""
        # Get current screen dimensions
        current_width, current_height = self.get_screen_dimensions()
        
        # Background
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.large_font.render("HIGH SCORES", True, GOLD)
        title_rect = title_text.get_rect(center=(current_width // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # High scores list (top 10 only)
        y_offset = 150
        for i, score_data in enumerate(self.high_score_manager.scores[:10]):  # Only show top 10
            rank_color = GOLD if i == 0 else (SILVER if i == 1 else (BRONZE if i == 2 else WHITE))
            rank_text = self.font.render(f"{i+1:2d}. {score_data['initials']} - {score_data['score']}", True, rank_color)
            rank_rect = rank_text.get_rect(center=(current_width // 2, y_offset + i * 30))
            self.screen.blit(rank_text, rank_rect)
        
        # Return instruction
        return_text = self.small_font.render("Press BACKSPACE to return to menu", True, CYAN)
        return_rect = return_text.get_rect(center=(current_width // 2, current_height - 50))
        self.screen.blit(return_text, return_rect)
    
    def draw_menu(self):
        """Draw the main menu screen"""
        current_width, current_height = self.get_screen_dimensions()
        self.screen.fill(BLACK)
        title_text = self.large_font.render("GAME MENU", True, GOLD)
        title_rect = title_text.get_rect(center=(current_width // 2, 100))
        self.screen.blit(title_text, title_rect)

        # Build menu options
        menu_options = [
            "Full Screen",
            "Toggle Transition Screen (" + ("ON" if self.show_transitions else "OFF") + ")",
            "High Scores",
            "Controls",
            "Adjust Movement Speed",  # New option
            "Return to Title Screen"
        ]
        if self.current_screen == "game" or self.game_started:
            menu_options.append("Back to Game")
        menu_options.append("Quit Game")

        for i, option in enumerate(menu_options):
            color = YELLOW if i == self.menu_selection else WHITE
            prefix = "> " if i == self.menu_selection else "  "
            text = self.font.render(prefix + option, True, color)
            text_rect = text.get_rect(center=(current_width // 2, 200 + i * 50))
            self.screen.blit(text, text_rect)
        nav_text = self.small_font.render("Use UP/DOWN arrows to navigate, ENTER to select", True, CYAN)
        nav_rect = nav_text.get_rect(center=(current_width // 2, current_height - 100))
        self.screen.blit(nav_text, nav_rect)
    
    def draw_next_maze_screen(self):
        """Draw the next maze screen with countdown"""
        # Get current screen dimensions
        current_width, current_height = self.get_screen_dimensions()
        
        # Background
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.large_font.render(f"MAZE {self.maze_count + 1}", True, GOLD)
        title_rect = title_text.get_rect(center=(current_width // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Calculate countdown (3 seconds total)
        elapsed = time.time() - self.next_maze_start_time
        if elapsed >= 3.0:
            # Auto-advance after 3 seconds
            self.showing_next_maze = False
            self.game_started = True
            self.timer_started = True
            self.last_time = time.time()  # Start timer immediately
            print(f"DEBUG: Transition ended - Timer started with {self.time_remaining:.1f}s remaining")
            return
        
        # Show countdown
        countdown_number = 3 - int(elapsed)
        countdown_text = self.large_font.render(str(countdown_number), True, YELLOW)
        countdown_rect = countdown_text.get_rect(center=(current_width // 2, 250))
        self.screen.blit(countdown_text, countdown_rect)
        
        # Instructions
        instruction_text = self.font.render("Press SPACE to start immediately", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(current_width // 2, 350))
        self.screen.blit(instruction_text, instruction_rect)
    
    def move_player(self, dx, dy):
        """Move the player if the destination is valid"""
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        if (0 <= new_x < self.current_maze_width and 0 <= new_y < self.current_maze_height and
            self.maze[new_y][new_x] != CellType.WALL):
            self.player_pos = [new_x, new_y]
            self.moves += 1
            
            # Check if player reached the end
            if self.player_pos == self.end_pos:
                self.game_won = True
    
    def handle_continuous_movement(self):
        """Handle continuous movement based on currently pressed keys"""
        current_time = time.time()
        
        # Only move if enough time has passed since last move
        if current_time - self.last_move_time < self.move_delay:
            return
        
        # Check for movement keys and move in the first direction found
        # Arrow keys and WASD keys both work for movement
        if pygame.K_UP in self.keys_pressed or pygame.K_w in self.keys_pressed:
            self.move_player(0, -1)
            self.last_move_time = current_time
        elif pygame.K_DOWN in self.keys_pressed or pygame.K_s in self.keys_pressed:
            self.move_player(0, 1)
            self.last_move_time = current_time
        elif pygame.K_LEFT in self.keys_pressed or pygame.K_a in self.keys_pressed:
            self.move_player(-1, 0)
            self.last_move_time = current_time
        elif pygame.K_RIGHT in self.keys_pressed or pygame.K_d in self.keys_pressed:
            self.move_player(1, 0)
            self.last_move_time = current_time
    
    def reset_game(self):
        """Reset the entire game to initial state"""
        show_transitions = self.show_transitions
        self.maze_count = 0
        
        # Calculate timer for Maze 1 using the same algorithm as other mazes
        maze_number = 1
        if maze_number % 10 == 1:  # Maze 1, 11, 21, 31, etc.
            self.time_remaining = self.base_time
        else:
            mazes_since_reset = (maze_number - 1) % 10
            self.time_remaining = max(20, self.base_time - (mazes_since_reset * self.time_reduction))
        
        print(f"DEBUG: reset_game() - Maze 1 timer calculated as {self.time_remaining}s")
        
        self.game_started = False
        self.timer_started = False
        self.showing_next_maze = False
        self.current_screen = "title"
        self.menu_selection = 0
        self.moves = 0
        self.game_won = False
        self.game_over = False
        self.entering_initials = False
        self.showing_high_scores = False
        self.initials = ""
        self.player_pos = self.start_pos.copy()
        self.last_time = time.time()
        self.show_transitions = show_transitions
        random.seed()
        self.generate_maze()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if self.adjusting_speed:
                        # Handle adjustment screen controls ONLY
                        if event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE]:
                            self.adjusting_speed = False
                        elif event.key == pygame.K_LEFT:
                            self.move_delay = max(self.move_delay_min, round(self.move_delay - self.move_delay_step, 2))
                        elif event.key == pygame.K_RIGHT:
                            self.move_delay = min(self.move_delay_max, round(self.move_delay + self.move_delay_step, 2))
                        elif event.key == pygame.K_RETURN:
                            self.adjusting_speed = False
                        continue  # Prevent further event processing while adjusting speed
                    
                    if event.key == pygame.K_q:
                        running = False
                    elif self.current_screen == "title":
                        # Title screen controls
                        if event.key == pygame.K_RETURN:
                            # Start the game with countdown
                            self.reset_game()
                            self.current_screen = "game"
                            self.showing_next_maze = True
                            self.next_maze_start_time = time.time()
                            self.game_started = False
                            self.timer_started = False
                            self.last_time = time.time()
                        elif event.key == pygame.K_m:
                            # Open menu
                            self.current_screen = "menu"
                            self.menu_selection = 0
                            self.ensure_valid_menu_selection()
                    elif self.current_screen == "menu":
                        total_menu_options = 7 if (self.current_screen == "game" or self.game_started) else 8
                        if event.key == pygame.K_UP:
                            self.menu_selection = (self.menu_selection - 1) % total_menu_options
                        elif event.key == pygame.K_DOWN:
                            self.menu_selection = (self.menu_selection + 1) % total_menu_options
                        elif event.key == pygame.K_RETURN:
                            if self.menu_selection == 0:  # Full Screen
                                self.toggle_fullscreen()
                            elif self.menu_selection == 1:  # Toggle Transition Screen
                                self.show_transitions = not self.show_transitions
                            elif self.menu_selection == 2:  # High Scores
                                self.current_screen = "high_scores"
                            elif self.menu_selection == 3:  # Controls
                                self.current_screen = "controls"
                            elif self.menu_selection == 4:  # Adjust Movement Speed
                                self.adjusting_speed = True
                            elif self.menu_selection == 5:  # Return to Title Screen
                                self.reset_game()
                                self.current_screen = "title"
                            elif self.menu_selection == 6 and (self.current_screen == "game" or self.game_started):  # Back to Game
                                self.current_screen = "game"
                                if self.game_started:
                                    self.timer_started = True
                                    self.last_time = time.time()
                            elif (self.menu_selection == 6 and not (self.current_screen == "game" or self.game_started)) or (self.menu_selection == 7 and (self.current_screen == "game" or self.game_started)):
                                running = False
                    elif self.current_screen == "high_scores":
                        # High scores screen - backspace to return to title screen
                        if event.key == pygame.K_BACKSPACE:
                            self.reset_game()
                            self.current_screen = "title"
                    elif self.current_screen == "controls":
                        # Controls screen - backspace to return
                        if event.key == pygame.K_BACKSPACE:
                            self.current_screen = "menu"
                    elif event.key == pygame.K_SPACE and self.game_won:
                        # Calculate timer for the next maze before starting transition
                        # When player wins Maze 1, maze_count is 0, so next_maze_number should be 2
                        next_maze_number = self.maze_count + 2  # +2 because we want the NEXT maze after the current one
                        
                        # Check if we've reached maximum size (50x40)
                        max_size_reached = (BASE_MAZE_WIDTH + ((next_maze_number - 1) // 5)) >= MAX_MAZE_WIDTH or (BASE_MAZE_HEIGHT + ((next_maze_number - 1) // 5)) >= MAX_MAZE_HEIGHT
                        
                        # Reset to full time every 10 mazes (1, 11, 21, 31, 41, etc.)
                        if next_maze_number % 10 == 1:  # Maze 1, 11, 21, 31, etc.
                            self.time_remaining = self.base_time
                            print(f"DEBUG: Pre-calculated Maze {next_maze_number} - Timer reset to {self.time_remaining}s")
                        elif max_size_reached:
                            # After reaching max size, reduce timer by 1s each maze until 20s minimum
                            mazes_since_reset = (next_maze_number - 1) % 10
                            self.time_remaining = max(20, self.base_time - (mazes_since_reset * self.time_reduction))
                            print(f"DEBUG: Pre-calculated Maze {next_maze_number} - Max size reached, timer: {self.time_remaining}s")
                        else:
                            # Normal progression: calculate timer based on maze number within current 10-maze cycle
                            mazes_since_reset = (next_maze_number - 1) % 10
                            self.time_remaining = max(20, self.base_time - (mazes_since_reset * self.time_reduction))
                            print(f"DEBUG: Pre-calculated Maze {next_maze_number} - Normal progression, mazes_since_reset={mazes_since_reset}, timer: {self.time_remaining}s")
                        
                        self.next_maze()
                    elif event.key == pygame.K_SPACE and self.showing_next_maze:
                        # Start the next maze
                        self.showing_next_maze = False
                        self.game_started = True
                        self.timer_started = True
                        self.last_time = time.time()  # Start timer immediately
                        print(f"DEBUG: SPACE pressed - Timer started with {self.time_remaining:.1f}s remaining")
                    elif self.entering_initials:
                        if event.key == pygame.K_RETURN:
                            # Submit the initials
                            initials = ""
                            for pos in self.initials_positions:
                                initials += self.available_chars[pos]
                            self.high_score_manager.add_score(initials, self.final_score)
                            self.entering_initials = False
                            self.showing_high_scores = True
                        elif event.key == pygame.K_LEFT:
                            # Move to previous initial
                            self.current_initial = (self.current_initial - 1) % 3
                        elif event.key == pygame.K_RIGHT:
                            # Move to next initial
                            self.current_initial = (self.current_initial + 1) % 3
                        elif event.key == pygame.K_UP:
                            # Scroll up through characters
                            self.initials_positions[self.current_initial] = (self.initials_positions[self.current_initial] - 1) % len(self.available_chars)
                        elif event.key == pygame.K_DOWN:
                            # Scroll down through characters
                            self.initials_positions[self.current_initial] = (self.initials_positions[self.current_initial] + 1) % len(self.available_chars)
                    elif self.showing_high_scores:
                        self.showing_high_scores = False
                    elif self.game_over:
                        # Game over screen - backspace to return to title screen
                        if event.key == pygame.K_BACKSPACE:
                            self.reset_game()
                            self.current_screen = "title"
                    elif self.current_screen == "game" and not self.game_won and not self.game_over and not self.showing_next_maze:
                        # Add movement keys to the pressed set (for both start screen and gameplay)
                        if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                            self.keys_pressed.add(event.key)
                
                elif event.type == pygame.KEYUP:
                    # Remove movement keys from the pressed set
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                        self.keys_pressed.discard(event.key)
            
            # Handle continuous movement
            if self.current_screen == "game" and not self.game_won and not self.game_over and not self.showing_next_maze:
                # Handle continuous movement if game has started
                if self.game_started:
                    self.handle_continuous_movement()
            
            # Drawing logic
            if self.adjusting_speed:
                self.draw_adjust_speed_screen()
                pygame.display.flip()
                self.clock.tick(60)
            else:
                self.update_timer()
                self.draw_maze()
                pygame.display.flip()
                self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

    def draw_controls_screen(self):
        """Draw the controls screen"""
        # Get current screen dimensions
        current_width, current_height = self.get_screen_dimensions()
        
        # Background
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.large_font.render("CONTROLS", True, GOLD)
        title_rect = title_text.get_rect(center=(current_width // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Controls list
        controls = [
            "Arrow Keys or WASD - Move player",
            "SPACEBAR - Continue to next maze",
            "M - Open menu",
            "ENTER - Select menu option",
            "BACKSPACE - Return to previous screen",
            "Q - Quit game"
        ]
        
        for i, control in enumerate(controls):
            text = self.font.render(control, True, WHITE)
            text_rect = text.get_rect(center=(current_width // 2, 180 + i * 50))
            self.screen.blit(text, text_rect)
        
        # Return instruction
        close_text = self.small_font.render("Press BACKSPACE to return to menu", True, CYAN)
        close_rect = close_text.get_rect(center=(current_width // 2, current_height - 50))
        self.screen.blit(close_text, close_rect)

    def draw_adjust_speed_screen(self):
        current_width, current_height = self.get_screen_dimensions()
        self.screen.fill(BLACK)
        title_text = self.large_font.render("ADJUST MOVEMENT SPEED", True, GOLD)
        title_rect = title_text.get_rect(center=(current_width // 2, 120))
        self.screen.blit(title_text, title_rect)
        speed_text = self.font.render(f"Current: {self.move_delay:.2f} seconds per move", True, CYAN)
        speed_rect = speed_text.get_rect(center=(current_width // 2, 220))
        self.screen.blit(speed_text, speed_rect)
        range_text = self.small_font.render(f"Range: {self.move_delay_min:.2f} - {self.move_delay_max:.2f} (lower = faster)", True, WHITE)
        range_rect = range_text.get_rect(center=(current_width // 2, 260))
        self.screen.blit(range_text, range_rect)
        instr_text = self.small_font.render("Use LEFT/RIGHT to adjust, ENTER to confirm, BACKSPACE/ESC to cancel", True, YELLOW)
        instr_rect = instr_text.get_rect(center=(current_width // 2, 320))
        self.screen.blit(instr_text, instr_rect)

if __name__ == "__main__":
    game = MazeGame()
    game.run() 