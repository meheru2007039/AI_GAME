from typing import Tuple
from .state import GameState
from .rules import get_legal_moves, get_nearest_treasure, manhattan_distance

def fuzzy_distance_score(distance: float, max_distance: float = 10.0) -> float:
    """
    Fuzzy membership function for distance evaluation.

    Close distance = high score (good)
    Far distance = low score (bad)

    Args:
        distance: Distance to treasure
        max_distance: Maximum expected distance

    Returns:
        Fuzzy score between 0 and 1
    """
    if distance == float('inf'):
        return 0.0

    # Normalize distance
    normalized = min(distance / max_distance, 1.0)

    # Inverse relationship: closer = better
    return 1.0 - normalized


def fuzzy_mobility_score(num_moves: int, max_moves: int = 4) -> float:
    """
    Fuzzy membership function for mobility evaluation.

    More available moves = higher score (more options)

    Args:
        num_moves: Number of legal moves available
        max_moves: Maximum possible moves

    Returns:
        Fuzzy score between 0 and 1
    """
    return min(num_moves / max_moves, 1.0)


def fuzzy_score_difference(score_diff: int, max_diff: float = 20.0) -> float:
    """
    Fuzzy membership function for score difference.

    Positive difference (AI ahead) = high score
    Negative difference (AI behind) = low score

    Args:
        score_diff: AI score - Human score
        max_diff: Maximum expected score difference

    Returns:
        Fuzzy score between 0 and 1
    """
    # Normalize to [-1, 1] then shift to [0, 1]
    normalized = max(-1.0, min(1.0, score_diff / max_diff))
    return (normalized + 1.0) / 2.0


def evaluate_state(state: GameState) -> float:
    """
    Evaluation function combining multiple heuristics with fuzzy logic.

    Considers:
    1. Current score difference (most important)
    2. Distance to nearest treasure
    3. Mobility (number of available moves)
    4. Treasure values within reach

    Args:
        state: Game state to evaluate

    Returns:
        Evaluation score (higher = better for AI)
    """
    # Terminal state evaluation
    if not state.treasures:
        score_diff = state.get_score_difference()
        if score_diff > 0:
            return 1000.0  # AI wins
        elif score_diff < 0:
            return -1000.0  # Human wins
        else:
            return 0.0  # Draw

    # Base score: current score difference
    score_diff = state.get_score_difference()

    # Factor 1: Score difference (weight: 0.5)
    fuzzy_score = fuzzy_score_difference(score_diff, max_diff=20.0)
    weighted_score = fuzzy_score * 0.5

    # Factor 2: Distance to nearest treasure for AI (weight: 0.25)
    ai_nearest, ai_dist = get_nearest_treasure(state, state.ai_pos)
    fuzzy_ai_dist = fuzzy_distance_score(ai_dist, max_distance=state.grid_size * 2)
    weighted_score += fuzzy_ai_dist * 0.25

    # Factor 3: Distance to nearest treasure for Human (weight: -0.15)
    # Penalize if human is close to treasure
    human_nearest, human_dist = get_nearest_treasure(state, state.human_pos)
    fuzzy_human_dist = fuzzy_distance_score(human_dist, max_distance=state.grid_size * 2)
    weighted_score -= fuzzy_human_dist * 0.15

    # Factor 4: Mobility - AI moves vs Human moves (weight: 0.1)
    temp_state = state.copy()
    temp_state.is_human_turn = False
    ai_moves = len(get_legal_moves(temp_state))

    temp_state.is_human_turn = True
    human_moves = len(get_legal_moves(temp_state))

    mobility_advantage = (ai_moves - human_moves) / 4.0  # Normalize
    weighted_score += mobility_advantage * 0.1

    # Convert to actual score range
    final_score = score_diff + (weighted_score * 20.0)

    return final_score


def evaluate_simple(state: GameState) -> float:
    """
    Simple evaluation function based only on score difference.
    Useful for testing or shallow searches.

    Args:
        state: Game state to evaluate

    Returns:
        Score difference (AI - Human)
    """
    return float(state.get_score_difference())