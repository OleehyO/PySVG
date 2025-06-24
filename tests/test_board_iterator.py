import pytest
from pysvg.utils.iterator import MatrixBoardIterator


class TestMatrix2DBoardIterator:
    """Test cases for Matrix2DBoardIterator class"""

    def test_init_valid_params(self):
        """Test iterator initialization with valid parameters"""
        iterator = MatrixBoardIterator(3, 4)
        assert iterator.nrows == 3
        assert iterator.ncols == 4
        assert len(iterator._border_positions) == 10  # 2*3 + 2*4 - 4 = 10

    def test_init_invalid_params(self):
        """Test iterator initialization with invalid parameters"""
        with pytest.raises(ValueError, match="nrows and ncols must be positive integers"):
            MatrixBoardIterator(0, 3)

        with pytest.raises(ValueError, match="nrows and ncols must be positive integers"):
            MatrixBoardIterator(3, 0)

        with pytest.raises(ValueError, match="nrows and ncols must be positive integers"):
            MatrixBoardIterator(-1, 3)

    def test_iter_protocol(self):
        """Test that iterator protocol works correctly"""
        iterator = MatrixBoardIterator(2, 2)

        # Test __iter__ returns self
        assert iter(iterator) is iterator

        # Test iteration
        positions = list(iterator)
        assert len(positions) == 4
        assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in positions)

    def test_multiple_iterations(self):
        """Test that iterator can be used multiple times"""
        iterator = MatrixBoardIterator(3, 3)

        first_run = list(iterator)
        second_run = list(iterator)

        assert first_run == second_run


class TestBorderElements:
    """Test border element count calculations"""

    @pytest.mark.parametrize(
        "nrows,ncols,expected_count",
        [
            (1, 1, 1),  # Single cell
            (1, 5, 5),  # Single row
            (5, 1, 5),  # Single column
            (2, 2, 4),  # 2x2 square
            (3, 3, 8),  # 3x3 square: 2*3 + 2*3 - 4 = 8
            (3, 4, 10),  # 3x4 rectangle: 2*3 + 2*4 - 4 = 10
            (4, 4, 12),  # 4x4 square: 2*4 + 2*4 - 4 = 12
            (5, 6, 18),  # 5x6 rectangle: 2*5 + 2*6 - 4 = 18
            (6, 3, 14),  # 6x3 rectangle: 2*6 + 2*3 - 4 = 14
        ],
    )
    def test_border_element_count(self, nrows, ncols, expected_count):
        """Test that correct number of border elements are generated"""
        iterator = MatrixBoardIterator(nrows, ncols)
        positions = list(iterator)
        assert len(positions) == expected_count

    def test_all_positions_unique(self):
        """Test that all border positions are unique"""
        iterator = MatrixBoardIterator(5, 6)
        positions = list(iterator)
        assert len(set(positions)) == len(positions)

    def test_positions_within_bounds(self):
        """Test that all positions are within matrix bounds"""
        nrows, ncols = 4, 5
        iterator = MatrixBoardIterator(nrows, ncols)
        positions = list(iterator)

        for row, col in positions:
            assert 0 <= row < nrows
            assert 0 <= col < ncols


class TestClockwiseIteration:
    """Test clockwise iteration patterns for known cases"""

    def test_2x2_matrix(self):
        """Test 2x2 matrix border iteration"""
        iterator = MatrixBoardIterator(2, 2)
        positions = list(iterator)
        expected = [(0, 0), (0, 1), (1, 1), (1, 0)]
        assert positions == expected

    def test_3x3_matrix(self):
        """Test 3x3 matrix border iteration"""
        iterator = MatrixBoardIterator(3, 3)
        positions = list(iterator)
        expected = [
            (0, 0),
            (0, 1),
            (0, 2),  # Top row: left to right
            (1, 2),
            (2, 2),  # Right column: top to bottom (excluding corner)
            (2, 1),
            (2, 0),  # Bottom row: right to left (excluding corner)
            (1, 0),  # Left column: bottom to top (excluding corners)
        ]
        assert positions == expected

    def test_3x4_rectangle(self):
        """Test 3x4 rectangle border iteration"""
        iterator = MatrixBoardIterator(3, 4)
        positions = list(iterator)
        expected = [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),  # Top row
            (1, 3),
            (2, 3),  # Right column
            (2, 2),
            (2, 1),
            (2, 0),  # Bottom row
            (1, 0),  # Left column
        ]
        assert positions == expected

    def test_4x3_rectangle(self):
        """Test 4x3 rectangle border iteration"""
        iterator = MatrixBoardIterator(4, 3)
        positions = list(iterator)
        expected = [
            (0, 0),
            (0, 1),
            (0, 2),  # Top row
            (1, 2),
            (2, 2),
            (3, 2),  # Right column
            (3, 1),
            (3, 0),  # Bottom row
            (2, 0),
            (1, 0),  # Left column
        ]
        assert positions == expected


class TestEdgeCases:
    """Test edge cases and special matrix shapes"""

    def test_single_cell(self):
        """Test 1x1 matrix"""
        iterator = MatrixBoardIterator(1, 1)
        positions = list(iterator)
        assert positions == [(0, 0)]

    def test_single_row(self):
        """Test single row matrices"""
        iterator = MatrixBoardIterator(1, 5)
        positions = list(iterator)
        expected = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
        assert positions == expected

    def test_single_column(self):
        """Test single column matrices"""
        iterator = MatrixBoardIterator(5, 1)
        positions = list(iterator)
        expected = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        assert positions == expected

    def test_wide_rectangle(self):
        """Test very wide rectangle (1 row, many columns)"""
        iterator = MatrixBoardIterator(1, 10)
        positions = list(iterator)
        assert len(positions) == 10
        assert positions[0] == (0, 0)
        assert positions[-1] == (0, 9)

    def test_tall_rectangle(self):
        """Test very tall rectangle (many rows, 1 column)"""
        iterator = MatrixBoardIterator(10, 1)
        positions = list(iterator)
        assert len(positions) == 10
        assert positions[0] == (0, 0)
        assert positions[-1] == (9, 0)


class TestBorderVisualization:
    """Test that border iteration produces correct visual patterns"""

    def test_4x4_visualization(self):
        """Test 4x4 matrix border visualization"""
        iterator = MatrixBoardIterator(4, 4)
        positions = list(iterator)

        # Create visualization matrix
        matrix = [["." for _ in range(4)] for _ in range(4)]
        for i, (row, col) in enumerate(positions):
            matrix[row][col] = str(i)

        expected = [
            ["0", "1", "2", "3"],
            ["b", ".", ".", "4"],
            ["a", ".", ".", "5"],
            ["9", "8", "7", "6"],
        ]

        # Check that border elements are numbered sequentially
        border_chars = set()
        for row in matrix:
            for cell in row:
                if cell != ".":
                    border_chars.add(cell)

        # Should have exactly 12 border elements for 4x4
        assert len(border_chars) == 12

    def test_5x6_visualization(self):
        """Test 5x6 matrix border visualization"""
        iterator = MatrixBoardIterator(5, 6)
        positions = list(iterator)

        # Create visualization matrix
        matrix = [["." for _ in range(6)] for _ in range(5)]
        for i, (row, col) in enumerate(positions):
            matrix[row][col] = f"{i:2d}"

        # Check that only border positions are filled
        border_count = 0
        for row in range(5):
            for col in range(6):
                if matrix[row][col] != ".":
                    border_count += 1
                    # Check if it's actually a border position
                    is_border = row == 0 or row == 4 or col == 0 or col == 5
                    assert is_border, f"Non-border position ({row}, {col}) was marked"

        assert border_count == 18  # 2*5 + 2*6 - 4 = 18


class TestToListMethod:
    """Test the to_list convenience method"""

    def test_to_list_same_as_iteration(self):
        """Test that to_list produces same result as direct iteration"""
        iterator = MatrixBoardIterator(3, 4)
        positions_from_iter = list(iterator)
        positions_from_method = iterator.to_list()

        assert positions_from_iter == positions_from_method

    def test_to_list_multiple_calls(self):
        """Test that to_list can be called multiple times"""
        iterator = MatrixBoardIterator(3, 3)

        first_call = iterator.to_list()
        second_call = iterator.to_list()

        assert first_call == second_call


class TestLargeMatrices:
    """Test behavior with larger matrices"""

    @pytest.mark.parametrize(
        "nrows,ncols",
        [
            (10, 10),
            (20, 15),
            (5, 100),
            (100, 5),
        ],
    )
    def test_large_matrices(self, nrows, ncols):
        """Test that iterator works correctly with large matrices"""
        iterator = MatrixBoardIterator(nrows, ncols)
        positions = list(iterator)

        # Check expected count
        if nrows == 1:
            expected_count = ncols
        elif ncols == 1:
            expected_count = nrows
        else:
            expected_count = 2 * nrows + 2 * ncols - 4

        assert len(positions) == expected_count

        # Check all positions are unique
        assert len(set(positions)) == len(positions)

        # Check all positions are within bounds
        for row, col in positions:
            assert 0 <= row < nrows
            assert 0 <= col < ncols

        # Check that only border positions are included
        for row, col in positions:
            is_border = row == 0 or row == nrows - 1 or col == 0 or col == ncols - 1
            assert is_border, f"Non-border position ({row}, {col}) included"
