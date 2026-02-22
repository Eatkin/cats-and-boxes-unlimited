from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Tuple

from cxb_unlimited.common import BoardSize
from cxb_unlimited.common import Coordinate
from cxb_unlimited.tiles import TilePlacement


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

    def __init__(self, size: BoardSize, cats: Cats) -> None:
        self.size = size
        self.tiles: List[TilePlacement] = []
        self.solid_bitmask = 0
        self.box_bitmask = 0
        self.cat_bitmask = cats.to_bitmask(self.size.width)

    def validate(self) -> bool:
        """Validates the board setup
        No overlapping tiles, no tiles over cats, no tiles out of bounds"""
        combined_solid = 0
        combined_box = 0

        for placement in self.tiles:
            # overlap with other solids
            if combined_solid & placement.solid_mask:
                return False

            # solid overlapping box
            if combined_box & placement.solid_mask:
                return False

            # overlap with other boxes
            if combined_box & placement.box_mask:
                return False

            # overlap with cats
            if placement.solid_mask & self.cat_bitmask:
                return False

            combined_solid |= placement.solid_mask
            combined_box |= placement.box_mask

        return True

    def calculate_bitmasks(self) -> None:
        self.solid_bitmask = 0
        self.box_bitmask = 0

        for placement in self.tiles:
            self.solid_bitmask |= placement.solid_mask
            self.box_bitmask |= placement.box_mask

    def print(self) -> None:
        """ASCII visualisation of the board"""

        width = self.size.width
        height = self.size.height

        solid_mask = self.solid_bitmask
        box_mask = self.box_bitmask
        cat_mask = self.cat_bitmask

        for y in range(height):
            row_chars = []

            for x in range(width):
                idx = x + y * width
                bit = 1 << idx

                if solid_mask & bit:
                    row_chars.append("#")
                elif (box_mask & bit) and (cat_mask & bit):
                    row_chars.append("O")
                elif box_mask & bit:
                    row_chars.append("B")
                elif cat_mask & bit:
                    row_chars.append("C")
                else:
                    row_chars.append(".")

            print("".join(row_chars))

    def print_legend(self) -> None:
        """Print out the legend for how to read the board"""
        print("ASCII Map Legend")
        for symbol, meaning in self.legend:
            print(f"{symbol:>2} : {meaning}")
