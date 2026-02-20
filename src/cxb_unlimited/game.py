import re
from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Optional
from typing import Tuple

WHITESPACE = re.compile(r'\s+')

@dataclass
class Coordinate:
    x: int
    y: int

class Tile:
    """Holds lists of relative coordinates"""
    def __init__(self, solid: List[Coordinate], boxes: List[Coordinate], rotation: int = 0, position: Optional[Coordinate]=None) -> None:
        self.solid = solid
        self.boxes = boxes
        self.rotation = rotation
        self.position = position if position is not None else Coordinate(0,0)

    @classmethod
    def from_ascii(cls, ascii_representation: str, **kwargs):
        solid = []
        boxes = []
        leading_lines = 0
        ascii_lines = ascii_representation.split("\n")
        for y, line in enumerate(ascii_lines):
            # Ignore any blank lines - allows easier formatting
            if WHITESPACE.fullmatch(line) or len(line) == 0:
                leading_lines += 1
                continue
            # Adjust y to remove leading lines
            yy = y - leading_lines
            for x, ch in enumerate(line):
                if ch == "#":
                    solid.append(Coordinate(x,yy))
                elif ch == "B":
                    boxes.append(Coordinate(x,yy))

        return cls(solid=solid, boxes=boxes, **kwargs)

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

    def print(self) -> None:
        """ASCII visualisation of the board"""
        for y in range(self.size.height):
            for x in range(self.size.width):
                idx = x + y * self.size.width
                bit = (1 << idx)
                solid = self.solid_bitmask & bit
                box = self.box_bitmask & bit
                cat = self.cat_bitmask & bit
                if solid:
                    print("#", end="")
                elif box and cat:
                    print('O', end="")
                elif box:
                    print('B', end="")
                elif cat:
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
