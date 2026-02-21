from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Tuple

from cxb_unlimited.common import BoardSize
from cxb_unlimited.common import Coordinate
from cxb_unlimited.tiles import Tile


@dataclass(frozen=True)
class Cats:
    """Holds list of relative coordinates and outputs bitmasks"""

    cats: List[Coordinate] = field(default_factory=list)

    def to_bitmask(self, board_width: int) -> int:
        bitmask = 0
        for cat in self.cats:
            shift = cat.x + cat.y * board_width
            bitmask |= 1 << shift

        return bitmask


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
        self.solid_bitmask = 0
        self.box_bitmask = 0
        for tile in self.tiles:
            p = tile.position
            for coord in tile.solid:
                shift = p.x + coord.x + (p.y + coord.y) * self.size.width
                self.solid_bitmask |= 1 << shift

            for coord in tile.boxes:
                shift = p.x + coord.x + (p.y + coord.y) * self.size.width
                self.box_bitmask |= 1 << shift

    def print(self) -> None:
        """ASCII visualisation of the board"""
        for y in range(self.size.height):
            for x in range(self.size.width):
                idx = x + y * self.size.width
                bit = 1 << idx
                solid = self.solid_bitmask & bit
                box = self.box_bitmask & bit
                cat = self.cat_bitmask & bit
                if solid:
                    print("#", end="")
                elif box and cat:
                    print("O", end="")
                elif box:
                    print("B", end="")
                elif cat:
                    print("C", end="")
                else:
                    print(".", end="")

            print("")

    def print_legend(self) -> None:
        """Print out the legend for how to read the board"""
        print("ASCII Map Legend")
        for symbol, meaning in self.legend:
            print(f"{symbol:>2} : {meaning}")
