from cxb_unlimited.board import Cats
from cxb_unlimited.common import Coordinate as C
from cxb_unlimited.game import Game
from cxb_unlimited.tiles import Tile

TILES = [
    """
 #
B#
 #B
         """,
    """
#B
 #
 #
         """,
    """
#B#
  #
         """,
    """
 #
#B#
         """,
]
TILE_POSITIONS = [C(0, 0), C(2, 0), C(2, 3), C(0, 3)]


def main() -> None:
    tiles = [Tile.from_ascii(t) for t in TILES]
    cats = Cats([C(0, 0), C(4, 0), C(2, 1), C(0, 3), C(3, 4)])
    game = Game(tiles=tiles, cats=cats)
    game.setup_board(TILE_POSITIONS)
    game.board.calculate_bitmasks()
    game.board.validate()
    game.board.print()
    game.board.print_legend()


if __name__ == "__main__":
    main()
