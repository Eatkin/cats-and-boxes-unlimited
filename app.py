from cxb_unlimited.game import Cats
from cxb_unlimited.game import Coordinate as C
from cxb_unlimited.game import Game
from cxb_unlimited.game import Tile

def main() -> None:
    tiles = [
            # Standard tetronimo tile
            Tile(solid=[C(0, 0), C(2, 0), C(1, 1)],
                 boxes=[C(1,0)],
                 position=C(0, 3)
                 ),
            ]
    cats = Cats([
            C(3, 0)
            ])
    game = Game(tiles=tiles, cats=cats)
    game.board.print()
    game.board.print_legend()

if __name__ == "__main__":
    main()
