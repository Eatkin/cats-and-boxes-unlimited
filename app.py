from cxb_unlimited.board import Cats
from cxb_unlimited.common import Coordinate as C
from cxb_unlimited.game import Game
from cxb_unlimited.tiles import Tile

TILES = [
    """
 #
#B
 #
         """,
    """
#
#
#
B#
         """,
    """
#B#
  #
         """,
    """
 #
B#
 #B
         """,
]
TILE_POSITIONS = [C(3, 2), C(0, 2), C(2, 0), C(0, 0)]


def main() -> None:
    tiles = [Tile.from_ascii(t, position=p) for t, p in zip(TILES, TILE_POSITIONS)]
    cats = Cats([C(0, 0), C(2, 1), C(3, 1), C(1, 3), C(2, 4)])
    game = Game(tiles=tiles, cats=cats)
    game.board.print()
    game.board.print_legend()


if __name__ == "__main__":
    main()
