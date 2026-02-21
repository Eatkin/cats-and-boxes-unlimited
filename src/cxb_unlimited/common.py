from dataclasses import dataclass


@dataclass
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
    """Placeholder before we implement movement
    Expected structure:
    Pos src
    Rot src
    Pos dest
    Rot dest
    So we can apply rotation and positioning
    """

    pass
