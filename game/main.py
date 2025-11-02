import random
from .state import GameState
from .rules import get_legal_moves, is_terminal, get_winner
from .engine import get_best_move, clear_transposition_table

def initialize_game(grid_size: int = 4, num_treasures: int = 5, 
                   treasure_range: tuple = (-3, 10)) -> GameState:
    """
    Initialize a new game with random treasure placement.

    Args:
        grid_size: Size of the grid (default 4x4)
        num_treasures: Number of treasures to place
        treasure_range: (min_value, max_value) for treasure values

    Returns:
        Initial GameState
    """
    state = GameState(grid_size=grid_size)

    # Generate random treasure positions (excluding starting positions)
    available_cells = []
    for x in range(grid_size):
        for y in range(grid_size):
            if (x, y) not in [(0, 0), (grid_size-1, grid_size-1)]:
                available_cells.append((x, y))

    # Randomly select treasure positions
    treasure_positions = random.sample(available_cells, min(num_treasures, len(available_cells)))

    # Assign random values to treasures
    treasures = {}
    for pos in treasure_positions:
        value = random.randint(treasure_range[0], treasure_range[1])
        treasures[pos] = value

    state.treasures = treasures
    return state


def print_game_state(state: GameState):
    """Print the current game state in a readable format."""
    print("\n" + "="*50)
    print(f"Human Score: {state.human_score} | AI Score: {state.ai_score}")
    print(f"Score Difference: {state.ai_score - state.human_score:+d} (AI perspective)")
    print(f"Current Turn: {'Human' if state.is_human_turn else 'AI'}")
    print(f"Treasures Remaining: {len(state.treasures)}")
    print(f"Cells Visited: {len(state.visited)}/{state.grid_size * state.grid_size}")
    print("="*50)

    # Print grid
    for x in range(state.grid_size):
        row = []
        for y in range(state.grid_size):
            pos = (x, y)
            if pos == state.human_pos:
                row.append(" H ")
            elif pos == state.ai_pos:
                row.append(" A ")
            elif pos in state.visited:
                row.append(" # ")
            elif pos in state.treasures:
                value = state.treasures[pos]
                if value >= 0:
                    row.append(f"+{value:1d} ")
                else:
                    row.append(f"{value:2d} ")
            else:
                row.append(" . ")
        print("|".join(row))

    print("\nLegend: H=Human, A=AI, #=Visited, .=Empty, Numbers=Treasures")
    print("="*50)


def play_human_turn(state: GameState) -> GameState:
    """
    Handle human player's turn with input validation.

    Args:
        state: Current game state

    Returns:
        New game state after human move
    """
    legal_moves = get_legal_moves(state)

    if not legal_moves:
        print("No legal moves available!")
        return state

    print(f"\nYour position: {state.human_pos}")
    print("Legal moves:")
    for i, move in enumerate(legal_moves, 1):
        treasure_info = ""
        if move in state.treasures:
            treasure_info = f" (Treasure: {state.treasures[move]:+d})"
        print(f"  {i}. {move}{treasure_info}")

    while True:
        try:
            choice = input(f"\nSelect move (1-{len(legal_moves)}): ").strip()
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(legal_moves):
                selected_move = legal_moves[choice_idx]
                return state.apply_move(selected_move)
            else:
                print(f"Invalid choice. Enter a number between 1 and {len(legal_moves)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nGame interrupted.")
            exit(0)


def play_ai_turn(state: GameState, depth: int = 4) -> GameState:
    """
    Handle AI turn using minimax with alpha-beta pruning.

    Args:
        state: Current game state
        depth: Search depth for AI

    Returns:
        New game state after AI move
    """
    print("\nAI is thinking...")
    best_move = get_best_move(state, depth=depth, use_alpha_beta=True)

    if best_move:
        print(f"AI moves to: {best_move}")
        if best_move in state.treasures:
            print(f"AI collects treasure: {state.treasures[best_move]:+d}")
        return state.apply_move(best_move)
    else:
        print("AI has no legal moves!")
        return state


def play_game(grid_size: int = 4, num_treasures: int = 5, ai_depth: int = 4, 
              mode: str = 'human_vs_ai'):
    """
    Main game loop.

    Args:
        grid_size: Size of the game grid
        num_treasures: Number of treasures to place
        ai_depth: Search depth for AI
        mode: 'human_vs_ai' or 'ai_vs_ai'
    """
    print("\n" + "="*50)
    print("TREASURE DUEL - AI Strategy Game")
    print("="*50)

    # Initialize game
    clear_transposition_table()
    state = initialize_game(grid_size, num_treasures)

    print_game_state(state)

    # Game loop
    turn_count = 0
    while not is_terminal(state):
        turn_count += 1
        print(f"\n--- Turn {turn_count} ---")

        if state.is_human_turn:
            if mode == 'human_vs_ai':
                state = play_human_turn(state)
            else:  # ai_vs_ai
                print("AI (Human side) is thinking...")
                best_move = get_best_move(state, depth=ai_depth, use_alpha_beta=True)
                if best_move:
                    print(f"AI (Human side) moves to: {best_move}")
                    state = state.apply_move(best_move)
        else:
            state = play_ai_turn(state, depth=ai_depth)

        print_game_state(state)
        
        # Additional turn summary
        if not is_terminal(state):
            legal_moves = get_legal_moves(state)
            print(f"Legal moves available: {len(legal_moves)}")
            if legal_moves:
                print(f"Next player can move to: {legal_moves}")

        # Safety limit
        if turn_count > 100:
            print("\nTurn limit reached!")
            break

    # Game over
    print("\n" + "="*50)
    print("GAME OVER!")
    print("="*50)
    winner = get_winner(state)
    print(f"Winner: {winner}")
    print(f"Final Score - Human: {state.human_score}, AI: {state.ai_score}")
    print("="*50)


def main():
    """Main entry point."""
    print("Welcome to Treasure Duel!")
    print("\nGame Modes:")
    print("1. Human vs AI")
    print("2. AI vs AI (Demo)")

    try:
        mode_choice = input("\nSelect mode (1 or 2): ").strip()

        if mode_choice == '1':
            mode = 'human_vs_ai'
        elif mode_choice == '2':
            mode = 'ai_vs_ai'
        else:
            print("Invalid choice. Defaulting to Human vs AI.")
            mode = 'human_vs_ai'

        # Game configuration
        grid_size = 4
        num_treasures = 5
        ai_depth = 4

        play_game(grid_size, num_treasures, ai_depth, mode)

    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()