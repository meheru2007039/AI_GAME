import pygame
import sys
from game.state import GameState
from game.rules import get_legal_moves, is_terminal, get_winner
from game.engine import get_best_move, clear_transposition_table
import random

# Color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (100, 100, 100)
BLUE = (100, 150, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
GOLD = (255, 215, 0)
PURPLE = (200, 100, 255)
VISITED_COLOR = (150, 150, 200)
VISITED_BORDER = (100, 100, 150)

# Game constants
GRID_SIZE = 4
CELL_SIZE = 120
GRID_OFFSET = 40
SCOREBOARD_WIDTH = 350  # Width for the scoreboard section
GRID_WIDTH = GRID_SIZE * CELL_SIZE  # Total grid width
WINDOW_WIDTH = GRID_OFFSET + GRID_WIDTH + GRID_OFFSET + SCOREBOARD_WIDTH  # Fixed calculation
WINDOW_HEIGHT = GRID_SIZE * CELL_SIZE + GRID_OFFSET * 2

class PygameUI:
    """Graphical user interface for Treasure Duel using Pygame."""

    def __init__(self, grid_size=4, num_treasures=5, ai_depth=4):
        """Initialize pygame and game state."""
        pygame.init()

        self.grid_size = grid_size
        self.num_treasures = num_treasures
        self.ai_depth = ai_depth

        # Setup display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Treasure Duel - AI Strategy Game")

        # Fonts
        self.font_xlarge = pygame.font.Font(None, 80)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)

        # Game state
        self.state = None
        self.selected_move = None
        self.legal_moves = []
        self.game_over = False
        self.game_started = False
        self.game_state = "start"

        # Clock for FPS
        self.clock = pygame.time.Clock()

        # Scoreboard x-position (right side of grid) - Fixed calculation
        self.scoreboard_x = GRID_OFFSET + GRID_WIDTH + 20

    def initialize_game(self):
        """Initialize a new game."""
        clear_transposition_table()
        self.state = GameState(grid_size=self.grid_size)

        # Generate random treasures
        available_cells = []
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if (x, y) not in [(0, 0), (self.grid_size-1, self.grid_size-1)]:
                    available_cells.append((x, y))

        treasure_positions = random.sample(available_cells, min(self.num_treasures, len(available_cells)))
        treasures = {}
        for pos in treasure_positions:
            value = random.randint(-3, 10)
            treasures[pos] = value

        self.state.treasures = treasures
        self.game_over = False
        self.game_started = False
        self.game_state = "start"
        self.update_legal_moves()

    def update_legal_moves(self):
        """Update the list of legal moves for current player."""
        if self.state and not is_terminal(self.state):
            self.legal_moves = get_legal_moves(self.state)
            if not self.legal_moves:
                temp_state = self.state.copy()
                temp_state.is_human_turn = not temp_state.is_human_turn
                other_moves = get_legal_moves(temp_state)
                if not other_moves:
                    self.game_state = "no_moves"
                    self.game_over = True
                else:
                    self.state.is_human_turn = not self.state.is_human_turn
                    self.legal_moves = get_legal_moves(self.state)
        else:
            self.legal_moves = []
            if self.state and is_terminal(self.state):
                self.game_state = "game_over"
                self.game_over = True

    def grid_to_screen(self, grid_pos):
        """Convert grid coordinates to screen coordinates."""
        x, y = grid_pos
        screen_x = GRID_OFFSET + y * CELL_SIZE
        screen_y = GRID_OFFSET + x * CELL_SIZE
        return screen_x, screen_y

    def screen_to_grid(self, screen_pos):
        """Convert screen coordinates to grid coordinates."""
        screen_x, screen_y = screen_pos
        x = (screen_y - GRID_OFFSET) // CELL_SIZE
        y = (screen_x - GRID_OFFSET) // CELL_SIZE

        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return (x, y)
        return None

    def draw_grid(self):
        """Draw the game grid."""
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                pos = (x, y)
                screen_x, screen_y = self.grid_to_screen(pos)

                # Determine cell color
                if pos in self.state.visited:
                    color = VISITED_COLOR
                elif self.game_state == "playing" and pos in self.legal_moves:
                    color = GREEN
                else:
                    color = LIGHT_GRAY

                # Draw cell
                pygame.draw.rect(self.screen, color, 
                               (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
                border_color = VISITED_BORDER if pos in self.state.visited else BLACK
                pygame.draw.rect(self.screen, border_color, 
                               (screen_x, screen_y, CELL_SIZE, CELL_SIZE), 3)

                # Draw treasures
                if pos in self.state.treasures:
                    value = self.state.treasures[pos]
                    treasure_color = GOLD if value > 0 else RED
                    pygame.draw.circle(self.screen, treasure_color,
                                     (screen_x + CELL_SIZE//2, screen_y + CELL_SIZE//2),
                                     CELL_SIZE//4)

                    text = self.font_small.render(f"{value:+d}", True, BLACK)
                    text_rect = text.get_rect(center=(screen_x + CELL_SIZE//2, 
                                                      screen_y + CELL_SIZE//2))
                    self.screen.blit(text, text_rect)

        # Draw players
        human_x, human_y = self.grid_to_screen(self.state.human_pos)
        pygame.draw.circle(self.screen, BLUE,
                         (human_x + CELL_SIZE//2, human_y + CELL_SIZE//2),
                         CELL_SIZE//3)
        text = self.font_medium.render("H", True, WHITE)
        text_rect = text.get_rect(center=(human_x + CELL_SIZE//2, human_y + CELL_SIZE//2))
        self.screen.blit(text, text_rect)

        ai_x, ai_y = self.grid_to_screen(self.state.ai_pos)
        pygame.draw.circle(self.screen, PURPLE,
                         (ai_x + CELL_SIZE//2, ai_y + CELL_SIZE//2),
                         CELL_SIZE//3)
        text = self.font_medium.render("A", True, WHITE)
        text_rect = text.get_rect(center=(ai_x + CELL_SIZE//2, ai_y + CELL_SIZE//2))
        self.screen.blit(text, text_rect)

    def draw_start_screen(self):
        """Draw the start screen overlay."""
        if self.game_state != "start":
            return

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        title = self.font_large.render("TREASURE DUEL", True, GOLD)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 120))
        self.screen.blit(title, title_rect)

        subtitle = self.font_medium.render("AI Strategy Game", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 80))
        self.screen.blit(subtitle, subtitle_rect)

        instructions = [
            "Collect treasures to increase score",
            "Watch out for negative values!",
            "Human (Blue H) vs AI (Purple A)",
            "",
            "Click anywhere to start!",
            "Press R to restart anytime"
        ]

        for i, instruction in enumerate(instructions):
            text = self.font_small.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 20 + i * 28))
            self.screen.blit(text, text_rect)

    def draw_scoreboard(self):
        """Draw the scoreboard next to the game grid (similar to screenshot)."""
        # Scoreboard background box
        board_x = self.scoreboard_x + 10
        board_y = GRID_OFFSET + 80
        board_width = 300
        board_height = 160

        # Outer border
        pygame.draw.rect(self.screen, BLACK, 
                        (board_x - 5, board_y - 5, board_width + 10, board_height + 10), 4)
        pygame.draw.rect(self.screen, WHITE, 
                        (board_x, board_y, board_width, board_height))

        # Player labels section
        label_y = board_y + 25
        human_label = self.font_medium.render("Human:", True, BLUE)
        self.screen.blit(human_label, (board_x + 15, label_y))

        # Human score - large display
        human_score_text = self.font_xlarge.render(str(self.state.human_score), True, BLUE)
        human_score_rect = human_score_text.get_rect(center=(board_x + 75, label_y + 50))
        self.screen.blit(human_score_text, human_score_rect)

        # VS divider
        vs_x = board_x + board_width // 2
        vs_text = self.font_large.render("VS", True, BLACK)
        vs_rect = vs_text.get_rect(center=(vs_x, board_y + board_height // 2))
        self.screen.blit(vs_text, vs_rect)

        # AI label and score
        ai_label_x = board_x + board_width - 110
        ai_label = self.font_medium.render("AI:", True, PURPLE)
        self.screen.blit(ai_label, (ai_label_x, label_y))

        ai_score_text = self.font_xlarge.render(str(self.state.ai_score), True, PURPLE)
        ai_score_rect = ai_score_text.get_rect(center=(ai_label_x + 50, label_y + 50))
        self.screen.blit(ai_score_text, ai_score_rect)

        # Turn indicator below scoreboard
        status_y = board_y + board_height + 25
        if self.game_state == "playing":
            if self.state.is_human_turn:
                status_text = "Your Turn! Click a GREEN cell"
                status_color = BLUE
            else:
                status_text = "AI Thinking..."
                status_color = PURPLE
        elif self.game_state == "game_over":
            winner = get_winner(self.state)
            if winner == "Human":
                status_text = "YOU WIN!"
                status_color = GREEN
            elif winner == "AI":
                status_text = "AI WINS!"
                status_color = RED
            else:
                status_text = "DRAW!"
                status_color = GOLD
        else:
            status_text = "Ready to play"
            status_color = BLACK

        status = self.font_small.render(status_text, True, status_color)
        status_rect = status.get_rect(center=(board_x + board_width//2, status_y))
        self.screen.blit(status, status_rect)

        # Additional game info
        info_y = status_y + 35
        treasures_text = f"Treasures: {len(self.state.treasures)}"
        treasures = self.font_small.render(treasures_text, True, BLACK)
        treasures_rect = treasures.get_rect(center=(board_x + board_width//2, info_y))
        self.screen.blit(treasures, treasures_rect)

        # Instructions
        instr_y = info_y + 35
        restart_text = "Press R to restart"
        restart = self.font_tiny.render(restart_text, True, DARK_GRAY)
        restart_rect = restart.get_rect(center=(board_x + board_width//2, instr_y))
        self.screen.blit(restart, restart_rect)

    def handle_click(self, pos):
        """Handle mouse click events."""
        if self.game_state == "start":
            self.game_started = True
            self.game_state = "playing"
            return

        if self.game_over or self.game_state != "playing":
            return

        if not self.state.is_human_turn:
            return

        grid_pos = self.screen_to_grid(pos)
        if grid_pos and grid_pos in self.legal_moves:
            self.state = self.state.apply_move(grid_pos)
            self.update_legal_moves()

            if is_terminal(self.state):
                self.game_state = "game_over"
                self.game_over = True

    def ai_move(self):
        """Execute AI move."""
        if not self.state.is_human_turn and not self.game_over and self.game_state == "playing":
            best_move = get_best_move(self.state, depth=self.ai_depth, use_alpha_beta=True)
            if best_move:
                pygame.time.delay(500)
                self.state = self.state.apply_move(best_move)
                self.update_legal_moves()

                if is_terminal(self.state):
                    self.game_state = "game_over"
                    self.game_over = True

    def run(self):
        """Main game loop."""
        self.initialize_game()

        running = True
        while running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.initialize_game()

            if not self.state.is_human_turn and not self.game_over and self.game_started:
                self.ai_move()

            # Drawing
            self.screen.fill(WHITE)
            self.draw_grid()
            self.draw_scoreboard()  # New scoreboard layout
            self.draw_start_screen()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

def main():
    """Entry point for pygame UI."""
    ui = PygameUI(grid_size=4, num_treasures=5, ai_depth=4)
    ui.run()

if __name__ == "__main__":
    main()
