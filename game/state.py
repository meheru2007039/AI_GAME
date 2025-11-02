from dataclasses import dataclass, field
from typing import Tuple, Optional, Set
import copy

@dataclass
class GameState:
    """
    Represents the complete state of the Treasure Duel game.
    """
    grid_size: int = 4
    human_pos: Tuple[int, int] = (0, 0)
    ai_pos: Tuple[int, int] = (3, 3)
    human_score: int = 0
    ai_score: int = 0
    treasures: dict = field(default_factory=dict)  # {(x, y): value}
    visited: Set[Tuple[int, int]] = field(default_factory=set)
    is_human_turn: bool = True

    def __post_init__(self):
        """Initialize visited cells with starting positions."""
        # Only set AI position if it's the default value (indicating first initialization)
        if self.ai_pos == (3, 3) and self.grid_size != 4:
            self.ai_pos = (self.grid_size - 1, self.grid_size - 1)
        # Only initialize visited if it's empty (indicating first initialization)
        if not self.visited:
            self.visited = {self.human_pos, self.ai_pos}

    def copy(self) -> 'GameState':
        """Create a deep copy of the game state."""
        return GameState(
            grid_size=self.grid_size,
            human_pos=self.human_pos,
            ai_pos=self.ai_pos,
            human_score=self.human_score,
            ai_score=self.ai_score,
            treasures=copy.deepcopy(self.treasures),
            visited=self.visited.copy(),
            is_human_turn=self.is_human_turn
        )

    def apply_move(self, move: Tuple[int, int]) -> 'GameState':
        """
        Apply a move and return a new game state.

        Args:
            move: (x, y) coordinates of the destination cell

        Returns:
            New GameState after applying the move
        """
        new_state = self.copy()

        # Update position based on whose turn it is
        if self.is_human_turn:
            new_state.human_pos = move
        else:
            new_state.ai_pos = move

        # Mark cell as visited
        new_state.visited.add(move)

        # Collect treasure if present
        if move in new_state.treasures:
            treasure_value = new_state.treasures[move]
            if self.is_human_turn:
                new_state.human_score += treasure_value
            else:
                new_state.ai_score += treasure_value
            # Remove collected treasure
            del new_state.treasures[move]

        # Switch turn
        new_state.is_human_turn = not self.is_human_turn

        return new_state

    def __hash__(self) -> int:
        """Generate hash for transposition table."""
        return hash((
            self.human_pos,
            self.ai_pos,
            self.human_score,
            self.ai_score,
            frozenset(self.treasures.items()),
            frozenset(self.visited),
            self.is_human_turn
        ))

    def __eq__(self, other) -> bool:
        """Check equality for transposition table."""
        if not isinstance(other, GameState):
            return False
        return (
            self.human_pos == other.human_pos and
            self.ai_pos == other.ai_pos and
            self.human_score == other.human_score and
            self.ai_score == other.ai_score and
            self.treasures == other.treasures and
            self.visited == other.visited and
            self.is_human_turn == other.is_human_turn
        )

    def get_score_difference(self) -> int:
        """Return score difference from AI perspective (AI - Human)."""
        return self.ai_score - self.human_score

    def get_current_player_pos(self) -> Tuple[int, int]:
        """Get the position of the current player."""
        return self.human_pos if self.is_human_turn else self.ai_pos