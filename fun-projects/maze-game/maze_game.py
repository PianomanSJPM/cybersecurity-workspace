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
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 40
MAZE_WIDTH = SCREEN_WIDTH // CELL_SIZE
MAZE_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Maze Navigator - Speed Challenge")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        
        self.maze = []
        self.player_pos = [1, 1]
        self.start_pos = [1, 1]
        self.end_pos = [MAZE_WIDTH - 2, MAZE_HEIGHT - 2]
        self.moves = 0
        self.game_won = False
        self.game_over = False
        
        # Timer system
        self.maze_count = 0
        self.base_time = 30  # 30 seconds for first maze (reduced from 60)
        self.time_reduction = 3  # 3 seconds less each maze (increased from 5)
        self.time_remaining = self.base_time
        self.start_time = time.time()
        self.last_time = time.time()
        
        # High score system
        self.high_score_manager = HighScoreManager()
        self.showing_high_scores = False
        self.entering_initials = False
        self.initials = ""
        self.final_score = 0
        
        # Maze generation algorithm
        self.algorithm = random.choice(['recursive', 'kruskal', 'prim'])
        
        # Random seed for different mazes each time
        random.seed()
        self.generate_maze()
        
    def generate_maze(self):
        """Generate a new maze using the selected algorithm"""
        # Initialize maze with walls
        self.maze = [[CellType.WALL for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
        
        # Set start and end positions (ensure they're at odd positions for proper maze generation)
        self.start_pos = [1, 1]
        self.end_pos = [MAZE_WIDTH - 2, MAZE_HEIGHT - 2]
        
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
        
    def _generate_recursive_maze(self):
        """Generate maze using recursive backtracking - creates proper corridors"""
        def carve_path(x, y):
            self.maze[y][x] = CellType.PATH
            
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 < nx < MAZE_WIDTH - 1 and 0 < ny < MAZE_HEIGHT - 1 and 
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
        for y in range(1, MAZE_HEIGHT - 1, 2):
            for x in range(1, MAZE_WIDTH - 1, 2):
                self.maze[y][x] = CellType.PATH
                # Add walls to the right and down
                if x + 2 < MAZE_WIDTH - 1:
                    walls.append((x + 1, y, 'horizontal'))
                if y + 2 < MAZE_HEIGHT - 1:
                    walls.append((x, y + 1, 'vertical'))
        
        # Shuffle walls
        random.shuffle(walls)
        
        # Union-find data structure
        parent = {}
        for y in range(1, MAZE_HEIGHT - 1, 2):
            for x in range(1, MAZE_WIDTH - 1, 2):
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
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if x % 2 == 1 and y % 2 == 1:
                    self.maze[y][x] = CellType.PATH
        
        # Start from the start position
        start_x, start_y = self.start_pos[0], self.start_pos[1]
        
        # List of frontier cells
        frontier = set()
        # Add initial cell's neighbors to frontier
        for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
            nx, ny = start_x + dx, start_y + dy
            if 0 < nx < MAZE_WIDTH - 1 and 0 < ny < MAZE_HEIGHT - 1:
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
                if (0 < nx < MAZE_WIDTH - 1 and 0 < ny < MAZE_HEIGHT - 1 and 
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
                    if (0 < new_x < MAZE_WIDTH - 1 and 0 < new_y < MAZE_HEIGHT - 1 and 
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
        
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
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
                current_x = max(0, min(current_x, MAZE_WIDTH - 1))
                current_y = max(0, min(current_y, MAZE_HEIGHT - 1))
                
                # Mark as path
                self.maze[current_y][current_x] = CellType.PATH
    
    def update_timer(self):
        """Update the timer and check for game over"""
        current_time = time.time()
        elapsed = current_time - self.last_time
        self.last_time = current_time
        
        if not self.game_won and not self.game_over and not self.entering_initials:
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
        """Move to the next maze with reduced time"""
        self.maze_count += 1
        # Calculate new time: base_time - (maze_count * reduction), minimum 10 seconds
        new_time = max(10, self.base_time - (self.maze_count * self.time_reduction))
        self.time_remaining = new_time
        self.game_won = False
        self.game_over = False
        self.moves = 0
        self.player_pos = self.start_pos.copy()
        self.last_time = time.time()
        self.generate_maze()
        
    def draw_maze(self):
        """Draw the maze on the screen"""
        self.screen.fill(BLACK)
        
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                cell = self.maze[y][x]
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if cell == CellType.WALL:
                    pygame.draw.rect(self.screen, PURPLE, rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 2)
                elif cell == CellType.PATH:
                    pygame.draw.rect(self.screen, WHITE, rect)
                elif cell == CellType.START:
                    pygame.draw.rect(self.screen, GREEN, rect)
                elif cell == CellType.END:
                    pygame.draw.rect(self.screen, RED, rect)
        
        # Draw player
        player_rect = pygame.Rect(
            self.player_pos[0] * CELL_SIZE + 5,
            self.player_pos[1] * CELL_SIZE + 5,
            CELL_SIZE - 10,
            CELL_SIZE - 10
        )
        pygame.draw.rect(self.screen, BLUE, player_rect)
        
        # Draw UI
        if self.entering_initials:
            self.draw_initials_screen()
        elif self.showing_high_scores:
            self.draw_high_scores_screen()
        else:
            self.draw_ui()
        
    def draw_ui(self):
        """Draw user interface elements"""
        # Timer display
        timer_color = GREEN if self.time_remaining > 20 else (ORANGE if self.time_remaining > 10 else RED)
        timer_text = self.font.render(f"Time: {self.time_remaining:.1f}s", True, timer_color)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 200, 10))
        
        # Maze counter
        maze_text = self.font.render(f"Maze: {self.maze_count + 1}", True, YELLOW)
        self.screen.blit(maze_text, (10, 10))
        
        # Timer info (debug)
        next_time = max(10, self.base_time - ((self.maze_count + 1) * self.time_reduction))
        timer_info_text = self.small_font.render(f"Next: {next_time}s", True, CYAN)
        self.screen.blit(timer_info_text, (SCREEN_WIDTH - 200, 40))
        
        # Moves counter
        moves_text = self.font.render(f"Moves: {self.moves}", True, CYAN)
        self.screen.blit(moves_text, (10, 50))
        
        # Instructions
        instructions = [
            "Use Arrow Keys to move",
            "Find the red exit!",
            "Press SPACE to continue",
            "Press R to restart game",
            "Press H to view high scores",
            "Press Q to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            self.screen.blit(text, (10, SCREEN_HEIGHT - 160 + i * 20))
        
        # Win message
        if self.game_won:
            win_text = self.font.render(f"MAZE {self.maze_count + 1} COMPLETE!", True, GREEN)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(win_text, text_rect)
            
            next_text = self.small_font.render("Press SPACE for next maze", True, YELLOW)
            next_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            self.screen.blit(next_text, next_rect)
        
        # Game over message
        if self.game_over:
            game_over_text = self.font.render("TIME'S UP!", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(game_over_text, text_rect)
            
            score_text = self.font.render(f"Final Score: {self.maze_count} mazes", True, YELLOW)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            self.screen.blit(score_text, score_rect)
            
            restart_text = self.small_font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(restart_text, restart_rect)
    
    def draw_initials_screen(self):
        """Draw the initials input screen"""
        # Background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Title
        title_text = self.large_font.render("NEW HIGH SCORE!", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Score
        score_text = self.font.render(f"Score: {self.final_score} mazes", True, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(score_text, score_rect)
        
        # Rank
        rank = self.high_score_manager.get_rank(self.final_score)
        rank_text = self.font.render(f"Rank: #{rank}", True, CYAN)
        rank_rect = rank_text.get_rect(center=(SCREEN_WIDTH // 2, 240))
        self.screen.blit(rank_text, rank_rect)
        
        # Instructions
        instruction_text = self.font.render("Enter your 3-letter initials:", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(instruction_text, instruction_rect)
        
        # Initials input box
        initials_text = self.large_font.render(self.initials + "_" * (3 - len(self.initials)), True, GREEN)
        initials_rect = initials_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        self.screen.blit(initials_text, initials_rect)
        
        # Submit instruction
        submit_text = self.small_font.render("Press ENTER to submit", True, WHITE)
        submit_rect = submit_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(submit_text, submit_rect)
    
    def draw_high_scores_screen(self):
        """Draw the high scores screen"""
        # Background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Title
        title_text = self.large_font.render("HIGH SCORES", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Your score
        your_score_text = self.font.render(f"Your Score: {self.final_score} mazes", True, YELLOW)
        your_score_rect = your_score_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.screen.blit(your_score_text, your_score_rect)
        
        # High scores list
        y_offset = 180
        for i, score_data in enumerate(self.high_score_manager.scores):
            rank_color = GOLD if i == 0 else (SILVER if i == 1 else (BRONZE if i == 2 else WHITE))
            rank_text = self.font.render(f"{i+1:2d}. {score_data['initials']} - {score_data['score']}", True, rank_color)
            rank_rect = rank_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * 30))
            self.screen.blit(rank_text, rank_rect)
        
        # Instructions
        instruction_text = self.small_font.render("Press R to restart or Q to quit", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(instruction_text, instruction_rect)
    
    def move_player(self, dx, dy):
        """Move the player if the destination is valid"""
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        if (0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and
            self.maze[new_y][new_x] != CellType.WALL):
            self.player_pos = [new_x, new_y]
            self.moves += 1
            
            # Check if player reached the end
            if self.player_pos == self.end_pos:
                self.game_won = True
    
    def reset_game(self):
        """Reset the entire game to initial state"""
        self.maze_count = 0
        self.time_remaining = self.base_time
        self.moves = 0
        self.game_won = False
        self.game_over = False
        self.entering_initials = False
        self.showing_high_scores = False
        self.initials = ""
        self.player_pos = self.start_pos.copy()
        self.last_time = time.time()
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
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_h and not self.game_over and not self.game_won:
                        self.showing_high_scores = True
                    elif event.key == pygame.K_SPACE and self.game_won:
                        self.next_maze()
                    elif self.entering_initials:
                        if event.key == pygame.K_RETURN and len(self.initials) == 3:
                            self.high_score_manager.add_score(self.initials, self.final_score)
                            self.entering_initials = False
                            self.showing_high_scores = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.initials = self.initials[:-1]
                        elif len(self.initials) < 3 and event.unicode.isalpha():
                            self.initials += event.unicode.upper()
                    elif self.showing_high_scores:
                        self.showing_high_scores = False
                    elif not self.game_won and not self.game_over:
                        if event.key == pygame.K_UP:
                            self.move_player(0, -1)
                        elif event.key == pygame.K_DOWN:
                            self.move_player(0, 1)
                        elif event.key == pygame.K_LEFT:
                            self.move_player(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            self.move_player(1, 0)
            
            self.update_timer()
            self.draw_maze()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MazeGame()
    game.run() 