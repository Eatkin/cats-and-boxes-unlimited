from __future__ import annotations
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
        self.history: List[Move] = []

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

        self.board.set_tiles(tile_placements)

        if not self.board.validate():
            raise ValidationError("Invalid board starting configuration")

    def get_legal_moves(self) -> List[Move]:
        """Returns a list of legal moves that can be made"""
        tile_placements_original = self.board.tiles
        tile_placements_copy = tile_placements_original[:]
        legal_moves: List[Move] = []
        # It's the rarely seen quad for loop
        for tile_idx, tile in enumerate(self.tiles):
            current_placement = tile_placements_original[tile_idx]
            current_pos = current_placement.position
            current_orientation_idx = current_placement.orientation.idx
            for orientation_idx, orientation in enumerate(tile.orientations):
                for x in range(self.size.width - orientation.width + 1):
                    for y in range(self.size.height - orientation.height + 1):
                        pos = Coordinate(x, y)
                        # Ignore start position
                        if orientation_idx == current_orientation_idx and current_pos == pos:
                            continue

                        tp = TilePlacement(
                                tile=tile,
                                orientation=orientation,
                                position=pos,
                                board_size=self.size
                                )
                        # Sub the tile_placements and place on board
                        tile_placements_copy[tile_idx] = tp
                        self.board.set_tiles(tile_placements_copy)
                        if self.board.validate():
                            move = Move(tile_idx, current_orientation_idx, orientation_idx, current_pos, pos)
                            legal_moves.append(move)

            # Reset tile placement
            tile_placements_copy[tile_idx] = current_placement
                

        return legal_moves

    def copy(self) -> Game:
        """Return a deep copy of the game with the same board state and tiles."""
        new_game = Game(
            tiles=self.tiles,
            cats=self.cats, 
            size=self.size 
        )

        # Copy current board tile placements
        new_game.board.set_tiles([TilePlacement(
            tile=tp.tile,
            orientation=tp.orientation,
            position=tp.position,
            board_size=new_game.size
        ) for tp in self.board.tiles])

        # Copy move history
        new_game.history = self.history[:]

        return new_game

    def apply_move(self, move: Move) -> None:
        """Apply a move by updating the appropriate tile placement on the board."""
        # Copy the current tile placements
        tile_placements = self.board.tiles[:]

        # Create a new TilePlacement for the moved tile
        tp = TilePlacement(
            tile=self.tiles[move.tile_idx],
            orientation=self.tiles[move.tile_idx].orientations[move.orientation_idx_dest],
            position=move.pos_dest,
            board_size=self.size
        )

        tile_placements[move.tile_idx] = tp

        # Set new placements on board
        self.board.set_tiles(tile_placements)

        # Append move to history
        self.history.append(move)
