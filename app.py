from cxb_unlimited.board import Cats
from cxb_unlimited.common import Coordinate as C
from cxb_unlimited.game import Game
from cxb_unlimited.solvers import bfs_solve
from cxb_unlimited.tiles import Tile

TILES = [
    """
B#
 #B
 #
         """,
    """
  #
##B
         """,
    """
#B#
  #
         """,
    """
 #
#B
 #
 """,
]
TILE_POSITIONS = [C(2, 2), C(0, 3), C(1, 0), C(0, 1)]


def main() -> None:
    tiles = [Tile.from_ascii(t) for t in TILES]
    cats = Cats([C(0, 0), C(2, 1), C(4, 1), C(0, 3), C(4, 4)])
    game = Game(tiles=tiles, cats=cats)
    game.setup_board(TILE_POSITIONS)
    game.board.print()
    game.board.print_legend()

    moves = bfs_solve(game)
    print("Solved in", len(moves), "moves!")
    for move in moves:
        print(move)


if __name__ == "__main__":
    main()
