# Cats and Boxes Unlimited

Cats and Boxes Unlimited is a project aiming to simulate the excellent tile packing puzzle game by Smart Games, [Cats and Boxes](https://www.smartgames.eu/uk/one-player-games/cats-boxes) (it really is excellent and I recommend buying it).

The project is currently being actively worked on. In its current state it can create an initial board state (see `app.py`).

The project will likely be updated faster than I am updating this readme.

The goals of the project are:

- Allow the game to be extended with arbitrary board sizes, number of cats and tile shapes (done)
- Allow relaxation of constraints that the original game enforces (cats cannot start in boxes, always use all four tiles, always use all five cats)
- Generate all legal moves
- Create a BFS solver to solve puzzles in the minimum number of moves
- Exhaustively generate all puzzle starting states with the number of moves to solve

## Setup and Usage

Cats and Boxes Unlimited is structured to separate **game logic** from **board state**. You primarily interact with the `Game` class in `cxb_unlimited.game`.

### Setup

Ensure you have Python >3.10. I use 3.13.11.

Setup your virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e . # Install the package in editable mode - this let's you import from the cxb_unlimited module
```

An overall flow for how to set up a board is defined in `app.py`, step by step below.

### Creating a Board

You first define your tiles and cats, then create a `Game` instance:

```python
from cxb_unlimited.common import BoardSize, Coordinate
from cxb_unlimited.tiles import Tile
from cxb_unlimited.board import Cats
from cxb_unlimited.game import Game
```

# Define the tiles (ASCII representation)

A hash `#` represents a solid tile and a B `B` represents a box. Tiles can be composed from ASCII to allow visual creation. Blank lines are ignored.

```python
tile1 = Tile.from_ascii(
 """
##
#B
 """
)
tile2 = Tile.from_ascii(
 """
 B#
##
"""
)
```

# Define cats

```python
cats = Cats([Coordinate(0, 0), Coordinate(4, 0), Coordinate(2, 2)])
```

# Create the game

```python
game = Game(
tiles=[tile1, tile2],
cats=cats,
size=BoardSize(width=5, height=5) # Board size defaults to (5, 5) if not given
)
```

### Placing Tiles

Use `setup_board` to position the tiles on the board. Tiles use their **default orientation** i.e. the orientation they were in when they were defined:

# Top-left coordinates for each tile

The top-left coordinate refers to the top-left of a bounding rectangle.

```python
tile_positions = [Coordinate(0, 0), Coordinate(2, 0)]
```

# Place tiles on the board

```python
game.setup_board(tile_positions)
```

# Print the board

```python
game.board.print()
```

The board will print an ASCII representation with the legend:

- `C` – Cat
- `B` – Box
- `O` – Cat in Box
- `#` – Tile wall
- `.` – Empty space

You can also print the legend at any time:

```python
game.board.print_legend()
```

### Working With Orientations

Each `Tile` automatically generates all distinct rotations:

# Print all orientations for a tile

```python
tile.print_all_orientations()
```

Or to print only the initial orientation:

```python
tile.print_orientation()
```

### Game Logic

- **Tiles are movable** within the game, but cats are static.
- The `Board` object only stores state and reports validity.
- `Game` handles moves, validation, and history tracking.

# Example: check board validity

```python
if game.board.validate():
    print("Board is valid")
```

## File Structure

Here’s an overview of the project layout to help you orient yourself:

```
.
├── app.py                       # Entry point for running the application
├── pyproject.toml               # Project configuration and dependencies
├── README.md                    # This file
├── src
│   └── cxb_unlimited
│       ├── __init__.py
│       ├── board.py             # Board state, cats, bitmask calculations, printing
│       ├── common.py            # Shared utilities and dataclasses (Coordinate, BoardSize)
│       ├── exceptions.py        # Custom exceptions (ValidationError, OutOfBoundsError, etc.)
│       ├── game.py              # Game class, move handling, setup, history
│       └── tiles.py             # Tile abstraction, TileOrientation, TilePlacement, rotations
```
