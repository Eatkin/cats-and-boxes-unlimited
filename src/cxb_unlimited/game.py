from typing import List
from typing import Optional

from cxb_unlimited.board import Board
from cxb_unlimited.board import Cats
from cxb_unlimited.common import BoardSize
from cxb_unlimited.common import Coordinate
from cxb_unlimited.common import Move
from cxb_unlimited.exceptions import BoardSetupError
from cxb_unlimited.exceptions import ValidationError
from cxb_unlimited.tiles import Tile
from cxb_unlimited.tiles import TilePlacement


class Game:
    """Cats and Boxes Game State"""

    def __init__(
        self,
        tiles: List[Tile],
        cats: Optional[Cats] = None,
        size: Optional[BoardSize] = None,
    ):
        if size is None:
            size = BoardSize()
        if cats is None:
            cats = Cats()  # Empty cat obj
        # Board configuration
        self.size = size
        self.cats = cats
        self.board = Board(size=self.size, cats=self.cats)
        self.tiles = tiles

        # Play-related functions
        self.history: List[Move]

    def setup_board(self, tile_coordinates: List[Coordinate]) -> None:
        """Place tiles on board
        Tile coordinates should be the top left position of the tiles bounding box
        It uses the tile's initial orientation"""
        if self.board.tiles:
            raise BoardSetupError(
                "You are trying to set up a board that already has tiles on it"
            )
        tile_placements: List[TilePlacement] = []
        for tile, pos in zip(self.tiles, tile_coordinates):
            tp = TilePlacement(
                tile=tile,
                orientation=tile.default_orientation,
                position=pos,
                board_size=self.size,
            )
            tile_placements.append(tp)

        self.board.tiles = tile_placements
        self.board.calculate_bitmasks()

        if not self.board.validate():
            raise ValidationError("Invalid board starting configuration")
