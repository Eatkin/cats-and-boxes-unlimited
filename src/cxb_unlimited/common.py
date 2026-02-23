from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int


@dataclass(frozen=True)
class BoardSize:
    """Wrapper for dimensions"""

    width: int = 5
    height: int = 5


@dataclass(frozen=True)
class Move:
    """Representation of a move that can be undone
    Record by indices
    """
    tile_idx: int
    orientation_idx_src: int
    orientation_idx_dest: int
    pos_src: Coordinate
    pos_dest: Coordinate
