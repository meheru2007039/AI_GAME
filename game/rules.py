from typing import List, Tuple, Optional
from game.state import GameState

def get_legal_moves(state: GameState) -> List[Tuple[int, int]]:
    """
    Generate all legal moves for the current player.

    A move is legal if:
    - It stays within grid boundaries
    - It's adjacent to current position (Manhattan distance = 1)
    - The cell hasn't been visited yet

    Args:
        state: Current game state

    Returns:
        List of (x, y) tuples representing legal destination cells
    """
    current_pos = state.get_current_player_pos()
    x, y = current_pos

    # Possible moves: up, down, left, right
    directions = [
        (x - 1, y),  # up
        (x + 1, y),  # down
        (x, y - 1),  # left
        (x, y + 1)   # right
    ]

    legal_moves = []
    for new_x, new_y in directions:
        # Check boundaries
        if 0 <= new_x < state.grid_size and 0 <= new_y < state.grid_size:
            # Check if not visited
            if (new_x, new_y) not in state.visited:
                legal_moves.append((new_x, new_y))

    return legal_moves


def is_terminal(state: GameState) -> bool:
    """
    Check if the game has reached a terminal state.

    The game ends when:
    - All treasures are collected, OR
    - Both players have no legal moves

    Args:
        state: Current game state

    Returns:
        True if game is over, False otherwise
    """
    # Check if all treasures collected
    if not state.treasures:
        return True

    # Check if current player has no moves
    if not get_legal_moves(state):
        # Switch turn temporarily to check other player
        temp_state = state.copy()
        temp_state.is_human_turn = not temp_state.is_human_turn

        # If other player also has no moves, game is over
        if not get_legal_moves(temp_state):
            return True

    return False


def get_winner(state: GameState) -> str:
    """
    Determine the winner of the game.

    Should only be called on terminal states.

    Args:
        state: Terminal game state

    Returns:
        'Human' if human wins, 'AI' if AI wins, 'Draw' if tied
    """
    if state.human_score > state.ai_score:
        return 'Human'
    elif state.ai_score > state.human_score:
        return 'AI'
    else:
        return 'Draw'


def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    """
    Calculate Manhattan distance between two positions.

    Args:
        pos1: First position (x1, y1)
        pos2: Second position (x2, y2)

    Returns:
        Manhattan distance
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def get_nearest_treasure(state: GameState, position: Tuple[int, int]) -> Tuple[Optional[Tuple[int, int]], float]:
    """
    Find the nearest treasure to a given position.

    Args:
        state: Current game state
        position: Position to measure from

    Returns:
        Tuple of (treasure_position, distance) or (None, float('inf')) if no treasures
    """
    if not state.treasures:
        return None, float('inf')

    nearest_treasure = None
    min_distance = float('inf')

    for treasure_pos in state.treasures.keys():
        dist = manhattan_distance(position, treasure_pos)
        if dist < min_distance:
            min_distance = dist
            nearest_treasure = treasure_pos

    return nearest_treasure, min_distance