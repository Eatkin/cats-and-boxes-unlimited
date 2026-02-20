from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Optional
from typing import Tuple

@dataclass
class Coordinate:
    x: int
    y: int

@dataclass
class Tile:
    """Holds lists of relative coordinates"""
    solid: List[Coordinate]
    boxes: List[Coordinate]
    position: Coordinate = field(default_factory=lambda: Coordinate(0, 0))
    rotation: int = 0

@dataclass(frozen=True)
class Cats:
    """Holds list of relative coordinates and outputs bitmasks"""
    cats: List[Coordinate] = field(default_factory=list)

    def to_bitmask(self, board_width: int):
        bitmask = 0
        for cat in self.cats:
            shift = cat.x + cat.y * board_width
            bitmask |= (1 << shift)

        return bitmask

@dataclass(frozen=True)
class BoardSize:
    """Wrapper for dimensions"""
    width: int = 5
    height: int = 5

class Board:
    """Contains positions for cats, boxes and tiles"""
    legend: List[Tuple[str, str]] = [
        ("C", "Cat"),
        ("B", "Box"),
        ("O", "Cat in Box"),
        (".", "Empty"),
        ("#", "Tile wall"),
    ]

    def __init__(self, size: BoardSize, tiles: List[Tile], cats: Cats) -> None:
        self.size = size
        self.tiles = tiles
        self.solid_bitmask = 0
        self.box_bitmask = 0
        self.cat_bitmask = cats.to_bitmask(self.size.width)
        self.calculate_bitmasks()

    def validate(self) -> bool:
        """Validates the board setup
        No overlapping tiles, no tiles over cats, no tiles out of bounds"""
        return True

    def calculate_bitmasks(self) -> None:
        # TODO: Handle rotation
        self.solid_bitmask = 0
        self.box_bitmask = 0
        for tile in self.tiles:
            p = tile.position
            for coord in tile.solid:
                shift = p.x + coord.x + (p.y + coord.y) * self.size.width
                self.solid_bitmask |= (1 << shift)

            for coord in tile.boxes:
                shift = p.x + coord.x + (p.y + coord.y) * self.size.width
                self.box_bitmask |= (1 << shift)

    def at_pos(self, x: int, y: int, bitmask: int):
        shift = x + y * self.size.width
        return bitmask & (1<<shift)

    def print(self) -> None:
        """ASCII visualisation of the board"""
        for y in range(self.size.height):
            for x in range(self.size.width):
                if self.at_pos(x, y, self.solid_bitmask):
                    print("#", end="")
                elif self.at_pos(x, y, self.box_bitmask):
                    if self.at_pos(x, y, self.cat_bitmask):
                        print('O', end="")
                    else:
                        print('B', end="")
                elif self.at_pos(x, y, self.cat_bitmask):
                    print('C', end="")
                else:
                    print(".", end="")

            print("")

    def print_legend(self) -> None:
        """Print out the legend for how to read the board"""
        print("ASCII Map Legend")
        for symbol, meaning in self.legend:
            print(f"{symbol:>2} : {meaning}")


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

class ValidationError(Exception):
    pass


class Game:
    """Cats and Boxes Game State"""
    def __init__(self, tiles=List[Tile], cats: Optional[Cats]=None, size: Optional[BoardSize]=None):
        if size is None:
            size = BoardSize()
        if cats is None:
            cats = Cats() # Empty cat obj
        self.size = size
        self.cats = cats
        self.tiles = tiles
        self.history: List[Move]

        # Create a board and set it up
        self.board = self._seed_board()

    def _seed_board(self) -> Board:
        board = Board(size=self.size, tiles=self.tiles, cats=self.cats)
        if not board.validate():
            raise ValidationError("Invalid initial board state")
        return board
