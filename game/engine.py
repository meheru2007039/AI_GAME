from typing import Tuple, Optional, Dict
from .state import GameState
from .rules import get_legal_moves, is_terminal
from .heuristic import evaluate_state

# Transposition table for memoization
transposition_table: Dict[int, Tuple[float, int]] = {}

# Simple opening book for 4x4 grid
OPENING_BOOK = {
    # Human at (0,0), AI at (3,3)
    ((0, 0), (3, 3), True): (1, 0),  # Human should move right first
    ((0, 0), (3, 3), False): (2, 3),  # AI should move left first
}


def clear_transposition_table():
    """Clear the transposition table (call between games)."""
    global transposition_table
    transposition_table = {}


def order_moves(state: GameState, moves: list) -> list:
    """
    Order moves for better alpha-beta pruning efficiency.

    Prioritizes moves that:
    1. Collect treasures (especially high-value ones)
    2. Move toward nearest treasure
    3. Maintain mobility

    Args:
        state: Current game state
        moves: List of legal moves

    Returns:
        Sorted list of moves (best first)
    """
    def move_priority(move):
        priority = 0

        # Highest priority: moves that collect treasure
        if move in state.treasures:
            priority += state.treasures[move] * 1000

        # Secondary: distance to nearest treasure after move
        if state.treasures:
            min_dist = float('inf')
            for treasure_pos in state.treasures.keys():
                dist = abs(move[0] - treasure_pos[0]) + abs(move[1] - treasure_pos[1])
                min_dist = min(min_dist, dist)
            priority -= min_dist

        return priority

    return sorted(moves, key=move_priority, reverse=True)


def minimax(state: GameState, depth: int, maximizing_player: bool) -> Tuple[float, Optional[Tuple[int, int]]]:
    """
    Basic minimax algorithm without pruning.

    Args:
        state: Current game state
        depth: Maximum search depth
        maximizing_player: True if AI (maximizing), False if human (minimizing)

    Returns:
        Tuple of (best_value, best_move)
    """
    # Terminal condition or depth limit
    if depth == 0 or is_terminal(state):
        return evaluate_state(state), None

    moves = get_legal_moves(state)

    # No moves available
    if not moves:
        return evaluate_state(state), None

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            new_state = state.apply_move(move)
            eval_score, _ = minimax(new_state, depth - 1, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_state = state.apply_move(move)
            eval_score, _ = minimax(new_state, depth - 1, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move


def quiescence_search(state: GameState, alpha: float, beta: float, 
                     maximizing_player: bool) -> float:
    """
    Quiescence search to handle positions with immediate captures.
    
    Args:
        state: Current game state
        alpha: Alpha value for pruning
        beta: Beta value for pruning
        maximizing_player: True if AI (maximizing), False if human (minimizing)
    
    Returns:
        Evaluation score
    """
    # Only search moves that collect treasures (immediate captures)
    moves = get_legal_moves(state)
    capture_moves = [move for move in moves if move in state.treasures]
    
    if not capture_moves:
        return evaluate_state(state)
    
    if maximizing_player:
        max_eval = evaluate_state(state)
        for move in capture_moves:
            new_state = state.apply_move(move)
            eval_score = quiescence_search(new_state, alpha, beta, False)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = evaluate_state(state)
        for move in capture_moves:
            new_state = state.apply_move(move)
            eval_score = quiescence_search(new_state, alpha, beta, True)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval


def alpha_beta(state: GameState, depth: int, alpha: float, beta: float, 
               maximizing_player: bool, use_tt: bool = True) -> Tuple[float, Optional[Tuple[int, int]]]:
    """
    Minimax with alpha-beta pruning and optional transposition table.

    Args:
        state: Current game state
        depth: Maximum search depth
        alpha: Alpha value for pruning
        beta: Beta value for pruning
        maximizing_player: True if AI (maximizing), False if human (minimizing)
        use_tt: Whether to use transposition table

    Returns:
        Tuple of (best_value, best_move)
    """
    # Check transposition table
    state_hash = hash(state)
    if use_tt and state_hash in transposition_table:
        cached_value, cached_depth = transposition_table[state_hash]
        if cached_depth >= depth:
            return cached_value, None

    # Terminal condition or depth limit
    if depth == 0 or is_terminal(state):
        if depth == 0 and not is_terminal(state):
            # Use quiescence search for better evaluation
            eval_score = quiescence_search(state, alpha, beta, maximizing_player)
        else:
            eval_score = evaluate_state(state)
        if use_tt:
            transposition_table[state_hash] = (eval_score, depth)
        return eval_score, None

    moves = get_legal_moves(state)

    # No moves available
    if not moves:
        eval_score = evaluate_state(state)
        if use_tt:
            transposition_table[state_hash] = (eval_score, depth)
        return eval_score, None

    # Move ordering for better pruning
    moves = order_moves(state, moves)

    best_move = moves[0]  # Default to first move

    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            new_state = state.apply_move(move)
            eval_score, _ = alpha_beta(new_state, depth - 1, alpha, beta, False, use_tt)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cutoff

        if use_tt:
            transposition_table[state_hash] = (max_eval, depth)
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_state = state.apply_move(move)
            eval_score, _ = alpha_beta(new_state, depth - 1, alpha, beta, True, use_tt)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cutoff

        if use_tt:
            transposition_table[state_hash] = (min_eval, depth)
        return min_eval, best_move


def get_best_move(state: GameState, depth: int = 4, use_alpha_beta: bool = True) -> Tuple[int, int]:
    """
    Get the best move for the current player using AI search.

    Args:
        state: Current game state
        depth: Search depth (default: 4)
        use_alpha_beta: Use alpha-beta pruning (True) or basic minimax (False)

    Returns:
        Best move as (x, y) tuple
    """
    is_maximizing = not state.is_human_turn  # AI is maximizing player
    
    # Early termination if only one move available
    moves = get_legal_moves(state)
    if len(moves) == 1:
        return moves[0]
    
    # Check opening book for early game positions
    if len(state.visited) <= 2:  # Very early game
        key = (state.human_pos, state.ai_pos, state.is_human_turn)
        if key in OPENING_BOOK:
            suggested_move = OPENING_BOOK[key]
            if suggested_move in moves:
                return suggested_move
    
    # Adaptive depth based on game phase
    if len(state.treasures) <= 2:  # Endgame
        depth = min(depth + 2, 8)
    elif len(state.treasures) <= 4:  # Midgame
        depth = min(depth + 1, 6)

    if use_alpha_beta:
        _, best_move = alpha_beta(state, depth, float('-inf'), float('inf'), is_maximizing)
    else:
        _, best_move = minimax(state, depth, is_maximizing)

    # Fallback to first legal move if no move found
    if best_move is None:
        if moves:
            best_move = moves[0]

    return best_move