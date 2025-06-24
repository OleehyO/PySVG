from typing import Literal, Iterator


class MatrixIterator:
    """
    Iterator specialized for iterating over a 2D matrix (list of list)

    Supports 8 different iteration modes:
    - Rl2rCt2b: Row-first, left to right, top to bottom
    - Rl2rCb2t: Row-first, left to right, bottom to top
    - Rr2lCt2b: Row-first, right to left, top to bottom
    - Rr2lCb2t: Row-first, right to left, bottom to top
    - Ct2bRl2r: Column-first, top to bottom, left to right
    - Ct2bRr2l: Column-first, top to bottom, right to left
    - Cb2tRl2r: Column-first, bottom to top, left to right
    - Cb2tRr2l: Column-first, bottom to top, right to left
    """

    def __init__(
        self,
        nrows: int,
        ncols: int,
        mode: Literal[
            "Rl2rCt2b",
            "Rl2rCb2t",
            "Rr2lCt2b",
            "Rr2lCb2t",
            "Ct2bRl2r",
            "Ct2bRr2l",
            "Cb2tRl2r",
            "Cb2tRr2l",
        ],
    ):
        """
        Initialize the matrix iterator

        Args:
            nrows: Number of rows in the matrix
            ncols: Number of columns in the matrix
            mode: Iteration mode
        """
        if nrows <= 0 or ncols <= 0:
            raise ValueError("nrows and ncols must be positive integers")

        self.nrows = nrows
        self.ncols = ncols
        self.mode = mode
        self._current_index = 0
        self._total_elements = nrows * ncols

    def __iter__(self) -> Iterator[tuple[int, int]]:
        """Return the iterator itself"""
        self._current_index = 0
        return self

    def __next__(self) -> tuple[int, int]:
        """Return the next position coordinates (row, col)"""
        if self._current_index >= self._total_elements:
            raise StopIteration

        row, col = self._get_position(self._current_index)
        self._current_index += 1
        return row, col

    def _get_position(self, index: int) -> tuple[int, int]:
        """Calculate actual row-column coordinates based on current index and iteration mode"""
        if self.mode == "Rl2rCt2b":
            # Row-first, left to right, top to bottom
            row = index // self.ncols
            col = index % self.ncols

        elif self.mode == "Rl2rCb2t":
            # Row-first, left to right, bottom to top
            row = (self.nrows - 1) - (index // self.ncols)
            col = index % self.ncols

        elif self.mode == "Rr2lCt2b":
            # Row-first, right to left, top to bottom
            row = index // self.ncols
            col = (self.ncols - 1) - (index % self.ncols)

        elif self.mode == "Rr2lCb2t":
            # Row-first, right to left, bottom to top
            row = (self.nrows - 1) - (index // self.ncols)
            col = (self.ncols - 1) - (index % self.ncols)

        elif self.mode == "Ct2bRl2r":
            # Column-first, top to bottom, left to right
            col = index // self.nrows
            row = index % self.nrows

        elif self.mode == "Ct2bRr2l":
            # Column-first, top to bottom, right to left
            col = (self.ncols - 1) - (index // self.nrows)
            row = index % self.nrows

        elif self.mode == "Cb2tRl2r":
            # Column-first, bottom to top, left to right
            col = index // self.nrows
            row = (self.nrows - 1) - (index % self.nrows)

        elif self.mode == "Cb2tRr2l":
            # Column-first, bottom to top, right to left
            col = (self.ncols - 1) - (index // self.nrows)
            row = (self.nrows - 1) - (index % self.nrows)

        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

        return row, col

    def to_list(self) -> list[tuple[int, int]]:
        """Return a list of all positions for debugging"""
        return list(MatrixIterator(self.nrows, self.ncols, self.mode))


class MatrixBoardIterator:
    """
    Iterator for iterating over the border/edge of a 2D matrix in clockwise direction

    The iteration follows this clockwise order:
    1. Top row: left to right
    2. Right column: top to bottom (excluding top-right corner)
    3. Bottom row: right to left (excluding bottom-right corner, only if more than 1 row)
    4. Left column: bottom to top (excluding corners, only if more than 1 column)
    """

    def __init__(self, nrows: int, ncols: int):
        """
        Initialize the matrix border iterator

        Args:
            nrows: Number of rows in the matrix
            ncols: Number of columns in the matrix
        """
        if nrows <= 0 or ncols <= 0:
            raise ValueError("nrows and ncols must be positive integers")

        self.nrows = nrows
        self.ncols = ncols
        self._current_index = 0
        self._border_positions = self._generate_border_positions()

    def _generate_border_positions(self) -> list[tuple[int, int]]:
        """Generate all border positions in clockwise order"""
        positions = []

        # Special case: single cell
        if self.nrows == 1 and self.ncols == 1:
            return [(0, 0)]

        # Special case: single row
        if self.nrows == 1:
            return [(0, col) for col in range(self.ncols)]

        # Special case: single column
        if self.ncols == 1:
            return [(row, 0) for row in range(self.nrows)]

        # General case: multi-row, multi-column
        # 1. Top row: left to right
        for col in range(self.ncols):
            positions.append((0, col))

        # 2. Right column: top to bottom (excluding top-right corner)
        for row in range(1, self.nrows):
            positions.append((row, self.ncols - 1))

        # 3. Bottom row: right to left (excluding bottom-right corner)
        for col in range(self.ncols - 2, -1, -1):
            positions.append((self.nrows - 1, col))

        # 4. Left column: bottom to top (excluding corners)
        for row in range(self.nrows - 2, 0, -1):
            positions.append((row, 0))

        return positions

    def __iter__(self) -> Iterator[tuple[int, int]]:
        """Return the iterator itself"""
        self._current_index = 0
        return self

    def __next__(self) -> tuple[int, int]:
        """Return the next border position coordinates (row, col)"""
        if self._current_index >= len(self._border_positions):
            raise StopIteration

        position = self._border_positions[self._current_index]
        self._current_index += 1
        return position

    def to_list(self) -> list[tuple[int, int]]:
        """Return a list of all border positions for debugging"""
        return list(MatrixBoardIterator(self.nrows, self.ncols))
