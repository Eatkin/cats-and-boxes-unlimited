from typing import List
from typing import Optional

from cxb_unlimited.board import Board
from cxb_unlimited.board import Cats
from cxb_unlimited.common import BoardSize
from cxb_unlimited.common import Move
from cxb_unlimited.exceptions import ValidationError
from cxb_unlimited.tiles import Tile


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
