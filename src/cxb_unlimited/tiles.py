from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from cxb_unlimited.common import BoardSize
from cxb_unlimited.common import Coordinate
from cxb_unlimited.exceptions import OutOfBoundsError

WHITESPACE = re.compile(r"\s+")


@dataclass(frozen=True)
class TileOrientation:
    """Single, immutable orientation of a tile"""

    tile: Tile
    solid: frozenset[Coordinate]
    boxes: frozenset[Coordinate]
    width: int
    height: int
    solid_mask: int
    box_mask: int

    @staticmethod
    def from_coords(
        tile: Tile,
        solid: Iterable[Coordinate],
        boxes: Iterable[Coordinate],
    ) -> TileOrientation:
        solid = frozenset(solid)
        boxes = frozenset(boxes)

        all_coords = solid | boxes

        max_x = max(c.x for c in all_coords)
        max_y = max(c.y for c in all_coords)

        width = max_x + 1
        height = max_y + 1

        solid_mask = 0
        box_mask = 0

        for c in solid:
            bit = c.y * width + c.x
            solid_mask |= 1 << bit

        for c in boxes:
            bit = c.y * width + c.x
            box_mask |= 1 << bit

        return TileOrientation(
            tile=tile,
            solid=solid,
            boxes=boxes,
            width=width,
            height=height,
            solid_mask=solid_mask,
            box_mask=box_mask,
        )


@dataclass(frozen=True)
class TilePlacement:
    """Represents a tile placed on a board
    Ensures bounds are not exceeded"""

    tile: Tile
    orientation: TileOrientation
    position: Coordinate
    board_size: BoardSize

    def __post_init__(self) -> None:
        px = self.position.x
        py = self.position.y

        if px < 0 or py < 0:
            raise OutOfBoundsError("Tile placement has negative coordinates")

        if px + self.orientation.width > self.board_size.width:
            raise OutOfBoundsError(
                f"Tile placement exceeds board width {self.board_size.width} - x coordinate is {px} and tile width is {self.orientation.width}"
            )

        if py + self.orientation.height > self.board_size.height:
            raise OutOfBoundsError(
                f"Tile placement exceeds board height {self.board_size.height} - y coordinate is {py} and tile height is {self.orientation.height}"
            )

    @property
    def solid_mask(self) -> int:
        return self._to_board_mask(self.orientation.solid)

    @property
    def box_mask(self) -> int:
        return self._to_board_mask(self.orientation.boxes)

    def _to_board_mask(self, coords: frozenset[Coordinate]) -> int:
        """Convert orientation coordinates to a bitmask on the board."""
        mask = 0
        for c in coords:
            idx = (self.position.y + c.y) * self.board_size.width + (
                self.position.x + c.x
            )
            mask |= 1 << idx
        return mask


class Tile:
    """
    Abstract definition of a tile.
    Holds all distinct orientations.
    """

    def __init__(
        self,
        solid: Iterable[Coordinate],
        boxes: Iterable[Coordinate],
    ) -> None:

        self._base_solid = tuple(solid)
        self._base_boxes = tuple(boxes)

        self.orientations: Tuple[TileOrientation, ...] = self._generate_orientations()

    @classmethod
    def from_ascii(cls, ascii_representation: str) -> Tile:
        """Construct the tile from an ascii representation of # for solid, B for box"""

        solid: List[Coordinate] = []
        boxes: List[Coordinate] = []

        leading_lines = 0
        ascii_lines = ascii_representation.split("\n")

        for y, line in enumerate(ascii_lines):

            if WHITESPACE.fullmatch(line) or len(line) == 0:
                leading_lines += 1
                continue

            yy = y - leading_lines

            for x, ch in enumerate(line):

                if ch == "#":
                    solid.append(Coordinate(x, yy))

                elif ch == "B":
                    boxes.append(Coordinate(x, yy))

        return cls(solid, boxes)

    def _generate_orientations(self) -> Tuple[TileOrientation, ...]:

        seen = set()
        orientations = []

        solid = self._base_solid
        boxes = self._base_boxes

        for _ in range(4):

            solid, boxes = self._normalize(solid, boxes)  # type: ignore

            key = (
                frozenset(solid),
                frozenset(boxes),
            )

            if key not in seen:
                seen.add(key)
                orientations.append(TileOrientation.from_coords(self, solid, boxes))

            solid, boxes = self._rotate_90(solid, boxes)  # type: ignore

        return tuple(orientations)

    @staticmethod
    def _rotate_90(
        solid: Iterable[Coordinate],
        boxes: Iterable[Coordinate],
    ) -> Tuple[List[Coordinate], List[Coordinate]]:
        """Uses rotation matrix"""

        def rot(c: Coordinate) -> Coordinate:
            return Coordinate(-c.y, c.x)

        return (
            [rot(c) for c in solid],
            [rot(c) for c in boxes],
        )

    @staticmethod
    def _normalize(
        solid: Iterable[Coordinate],
        boxes: Iterable[Coordinate],
    ) -> Tuple[List[Coordinate], List[Coordinate]]:
        """Calculates min x/y and subtracts from all coordinates
        This sets the top-left of the bounding box to (0, 0)"""

        def norm(c: Coordinate) -> Coordinate:
            return Coordinate(c.x - min_x, c.y - min_y)

        all_coords = list(solid) + list(boxes)

        min_x = min(c.x for c in all_coords)
        min_y = min(c.y for c in all_coords)

        return (
            [norm(c) for c in solid],
            [norm(c) for c in boxes],
        )

    @property
    def default_orientation(self) -> TileOrientation:
        """Returns a TileOrientation object in the initially defined state"""
        return self.orientations[0]

    def print_orientation(self, orientation: Optional[TileOrientation] = None) -> None:
        """
        Prints an ASCII representation of a tile orientation.
        '#' = solid, 'B' = box, '.' = empty.
        If no orientation is given, prints the default_orientation.
        """
        if orientation is None:
            orientation = self.default_orientation

        width = orientation.width
        height = orientation.height
        solid_coords = orientation.solid
        box_coords = orientation.boxes

        # Build grid row by row
        for y in range(height):
            row = []
            for x in range(width):
                coord = Coordinate(x, y)
                if coord in solid_coords:
                    row.append("#")
                elif coord in box_coords:
                    row.append("B")
                else:
                    row.append(".")
            print("".join(row))

    def print_all_orientations(self) -> None:
        for i, orient in enumerate(self.orientations):
            print(f"Orientation {i}:")
            self.print_orientation(orient)
