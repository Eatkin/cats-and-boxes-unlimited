from collections import deque
from dataclasses import dataclass
from typing import List
from typing import Optional
from typing import Tuple

from cxb_unlimited.common import Move
from cxb_unlimited.game import Game


@dataclass(frozen=True)
class TileState:
    """Immutable state of a single tile for BFS"""

    x: int
    y: int
    orientation_idx: int


@dataclass(frozen=True)
class GameState:
    """Immutable representation of a game board for BFS"""

    tiles: Tuple[TileState, ...]


def bfs_solve(game: Game, max_depth: Optional[int] = None) -> Optional[List[Move]]:
    """
    BFS solver for Cats and Boxes Unlimited.
    Returns the shortest sequence of moves to solve the puzzle, or None if unsolvable.
    """
    visited: set[GameState] = set()

    queue: deque[Tuple[Game, List[Move]]] = deque()
    initial_tiles = tuple(
        TileState(tp.position.x, tp.position.y, tp.orientation.idx)
        for tp in game.board.tiles
    )
    initial_state = GameState(initial_tiles)
    queue.append((game, []))
    visited.add(initial_state)

    while queue:
        current_game, path = queue.popleft()

        # Check if solved
        if current_game.board.solved:
            return path

        if max_depth is not None and len(path) >= max_depth:
            continue

        for move in current_game.get_legal_moves():
            new_game = current_game.copy()
            new_game.apply_move(move)

            state_hash = GameState(
                tuple(
                    TileState(tp.position.x, tp.position.y, tp.orientation.idx)
                    for tp in new_game.board.tiles
                )
            )
            if state_hash not in visited:
                visited.add(state_hash)
                queue.append((new_game, path + [move]))

    return None  # No solution found
