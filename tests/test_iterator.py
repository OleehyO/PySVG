import pytest
from pysvg.utils.iterator import MatrixIterator


class TestMatrix2DIterator:
    """Test cases for Matrix2DIterator class"""

    def test_init_valid_params(self):
        """Test iterator initialization with valid parameters"""
        iterator = MatrixIterator(3, 4, "Rl2rCt2b")
        assert iterator.nrows == 3
        assert iterator.ncols == 4
        assert iterator.mode == "Rl2rCt2b"
        assert iterator._total_elements == 12

    def test_init_invalid_params(self):
        """Test iterator initialization with invalid parameters"""
        with pytest.raises(ValueError, match="nrows and ncols must be positive integers"):
            MatrixIterator(0, 3, "Rl2rCt2b")

        with pytest.raises(ValueError, match="nrows and ncols must be positive integers"):
            MatrixIterator(3, 0, "Rl2rCt2b")

        with pytest.raises(ValueError, match="nrows and ncols must be positive integers"):
            MatrixIterator(-1, 3, "Rl2rCt2b")

    def test_iter_protocol(self):
        """Test that iterator protocol works correctly"""
        iterator = MatrixIterator(2, 2, "Rl2rCt2b")

        # Test __iter__ returns self
        assert iter(iterator) is iterator

        # Test iteration
        positions = list(iterator)
        assert len(positions) == 4
        assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in positions)

    def test_multiple_iterations(self):
        """Test that iterator can be used multiple times"""
        iterator = MatrixIterator(2, 2, "Rl2rCt2b")

        first_run = list(iterator)
        second_run = list(iterator)

        assert first_run == second_run
        assert first_run == [(0, 0), (0, 1), (1, 0), (1, 1)]


class TestIterationModes:
    """Test all iteration modes with known expected results"""

    @pytest.mark.parametrize(
        "nrows,ncols,mode,expected",
        [
            # 3x3 square matrix tests
            (
                3,
                3,
                "Rl2rCt2b",
                [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
            ),
            (
                3,
                3,
                "Rl2rCb2t",
                [(2, 0), (2, 1), (2, 2), (1, 0), (1, 1), (1, 2), (0, 0), (0, 1), (0, 2)],
            ),
            (
                3,
                3,
                "Rr2lCt2b",
                [(0, 2), (0, 1), (0, 0), (1, 2), (1, 1), (1, 0), (2, 2), (2, 1), (2, 0)],
            ),
            (
                3,
                3,
                "Rr2lCb2t",
                [(2, 2), (2, 1), (2, 0), (1, 2), (1, 1), (1, 0), (0, 2), (0, 1), (0, 0)],
            ),
            (
                3,
                3,
                "Ct2bRl2r",
                [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)],
            ),
            (
                3,
                3,
                "Ct2bRr2l",
                [(0, 2), (1, 2), (2, 2), (0, 1), (1, 1), (2, 1), (0, 0), (1, 0), (2, 0)],
            ),
            (
                3,
                3,
                "Cb2tRl2r",
                [(2, 0), (1, 0), (0, 0), (2, 1), (1, 1), (0, 1), (2, 2), (1, 2), (0, 2)],
            ),
            (
                3,
                3,
                "Cb2tRr2l",
                [(2, 2), (1, 2), (0, 2), (2, 1), (1, 1), (0, 1), (2, 0), (1, 0), (0, 0)],
            ),
            # 2x3 rectangle tests
            (2, 3, "Rl2rCt2b", [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]),
            (2, 3, "Ct2bRl2r", [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)]),
            # Single row tests
            (1, 4, "Rl2rCt2b", [(0, 0), (0, 1), (0, 2), (0, 3)]),
            (1, 4, "Rr2lCt2b", [(0, 3), (0, 2), (0, 1), (0, 0)]),
            # Single column tests
            (4, 1, "Rl2rCt2b", [(0, 0), (1, 0), (2, 0), (3, 0)]),
            (4, 1, "Rl2rCb2t", [(3, 0), (2, 0), (1, 0), (0, 0)]),
        ],
    )
    def test_iteration_modes(self, nrows, ncols, mode, expected):
        """Test specific iteration modes with known expected results"""
        iterator = MatrixIterator(nrows, ncols, mode)
        result = list(iterator)
        assert result == expected

    def test_invalid_mode(self):
        """Test that invalid mode raises error"""
        iterator = MatrixIterator(3, 3, "InvalidMode")
        with pytest.raises(ValueError, match="Unsupported mode: InvalidMode"):
            list(iterator)


class TestMatrixShapes:
    """Test different matrix shapes and edge cases"""

    @pytest.mark.parametrize(
        "nrows,ncols",
        [
            (1, 1),  # Single cell
            (1, 10),  # Single row
            (10, 1),  # Single column
            (2, 5),  # Wide rectangle
            (5, 2),  # Tall rectangle
            (100, 100),  # Large square
        ],
    )
    def test_various_shapes(self, nrows, ncols):
        """Test iterator works with various matrix shapes"""
        iterator = MatrixIterator(nrows, ncols, "Rl2rCt2b")
        positions = list(iterator)

        # Check total count
        assert len(positions) == nrows * ncols

        # Check all positions are unique
        assert len(set(positions)) == len(positions)

        # Check all positions are within bounds
        for row, col in positions:
            assert 0 <= row < nrows
            assert 0 <= col < ncols

    def test_single_cell_matrix(self):
        """Test edge case of 1x1 matrix"""
        iterator = MatrixIterator(1, 1, "Rl2rCt2b")
        positions = list(iterator)
        assert positions == [(0, 0)]

    def test_to_list_method(self):
        """Test the to_list convenience method"""
        iterator = MatrixIterator(2, 2, "Rl2rCt2b")
        positions_from_iter = list(iterator)
        positions_from_method = iterator.to_list()

        assert positions_from_iter == positions_from_method


class TestMatrixVisualization:
    """Test that iteration produces correct visual patterns"""

    def test_row_first_left_to_right_top_to_bottom(self):
        """Test Rl2rCt2b produces correct numbering pattern"""
        iterator = MatrixIterator(3, 3, "Rl2rCt2b")
        positions = list(iterator)

        # Create visualization matrix
        matrix = [[-1 for _ in range(3)] for _ in range(3)]
        for i, (row, col) in enumerate(positions):
            matrix[row][col] = i

        expected = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        assert matrix == expected

    def test_column_first_top_to_bottom_left_to_right(self):
        """Test Ct2bRl2r produces correct numbering pattern"""
        iterator = MatrixIterator(3, 3, "Ct2bRl2r")
        positions = list(iterator)

        # Create visualization matrix
        matrix = [[-1 for _ in range(3)] for _ in range(3)]
        for i, (row, col) in enumerate(positions):
            matrix[row][col] = i

        expected = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
        assert matrix == expected

    def test_rectangular_matrix_visualization(self):
        """Test visualization works correctly for non-square matrices"""
        iterator = MatrixIterator(2, 4, "Rl2rCt2b")
        positions = list(iterator)

        # Create visualization matrix
        matrix = [[-1 for _ in range(4)] for _ in range(2)]
        for i, (row, col) in enumerate(positions):
            matrix[row][col] = i

        expected = [[0, 1, 2, 3], [4, 5, 6, 7]]
        assert matrix == expected


class TestIteratorBehavior:
    """Test iterator behavior and edge cases"""

    def test_iterator_exhaustion(self):
        """Test that iterator properly exhausts and raises StopIteration"""
        iterator = MatrixIterator(2, 2, "Rl2rCt2b")

        # Manually iterate to test StopIteration
        positions = []
        while True:
            try:
                pos = next(iterator)
                positions.append(pos)
            except StopIteration:
                break

        assert len(positions) == 4
        assert positions == [(0, 0), (0, 1), (1, 0), (1, 1)]

    def test_iterator_reset_on_iter_call(self):
        """Test that calling __iter__ resets the iterator"""
        iterator = MatrixIterator(2, 2, "Rl2rCt2b")

        # Partially consume iterator
        first_pos = next(iterator)
        assert first_pos == (0, 0)

        # Reset by calling __iter__
        iter(iterator)

        # Should start from beginning again
        reset_first_pos = next(iterator)
        assert reset_first_pos == (0, 0)


if __name__ == "__main__":
    pytest.main([__file__])
