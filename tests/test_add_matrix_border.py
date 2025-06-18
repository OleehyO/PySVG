"""Pytest tests for add_matrix_border function in matrix.py"""

import pytest
from pysvg.utils.matrix import add_matrix_border


class TestAddMatrixBorder:
    """Test class for add_matrix_border function"""

    def test_add_border_top(self):
        """Test adding border to top only"""
        matrix = [[1, 2], [3, 4]]
        result = add_matrix_border(matrix, 0, "t")
        expected = [[0, 0], [1, 2], [3, 4]]
        assert result == expected

    def test_add_border_bottom(self):
        """Test adding border to bottom only"""
        matrix = [[1, 2], [3, 4]]
        result = add_matrix_border(matrix, 0, "b")
        expected = [[1, 2], [3, 4], [0, 0]]
        assert result == expected

    def test_add_border_left(self):
        """Test adding border to left only"""
        matrix = [[1, 2], [3, 4]]
        result = add_matrix_border(matrix, 0, "l")
        expected = [[0, 1, 2], [0, 3, 4]]
        assert result == expected

    def test_add_border_right(self):
        """Test adding border to right only"""
        matrix = [[1, 2], [3, 4]]
        result = add_matrix_border(matrix, 0, "r")
        expected = [[1, 2, 0], [3, 4, 0]]
        assert result == expected

    def test_add_border_top_bottom(self):
        """Test adding border to top and bottom"""
        matrix = [[1, 2], [3, 4]]
        result = add_matrix_border(matrix, 0, "tb")
        expected = [[0, 0], [1, 2], [3, 4], [0, 0]]
        assert result == expected

    def test_add_border_top_left(self):
        """Test adding border to top and left"""
        matrix = [[1, 2], [3, 4]]
        result = add_matrix_border(matrix, 0, "tl")
        expected = [[0, 0, 0], [0, 1, 2], [0, 3, 4]]
        assert result == expected

    def test_add_border_top_right(self):
        """Test adding border to top and right"""
        matrix = [[1, 2], [3, 4]]
        result = add_matrix_border(matrix, 0, "tr")
        expected = [[0, 0, 0], [1, 2, 0], [3, 4, 0]]
        assert result == expected

    def test_add_border_bottom_left(self):
        """Test adding border to bottom and left"""
        matrix = [[1, 2], [3, 4]]
        result = add_matrix_border(matrix, 0, "bl")
        expected = [[0, 1, 2], [0, 3, 4], [0, 0, 0]]
        assert result == expected

    def test_add_border_bottom_right(self):
        """Test adding border to bottom and right"""
        matrix = [[1, 2], [3, 4]]
        result = add_matrix_border(matrix, 0, "br")
        expected = [[1, 2, 0], [3, 4, 0], [0, 0, 0]]
        assert result == expected

    def test_add_border_top_left_right(self):
        """Test adding border to top, left and right"""
        matrix = [[1, 2], [3, 4]]
        result = add_matrix_border(matrix, 0, "tlr")
        expected = [[0, 0, 0, 0], [0, 1, 2, 0], [0, 3, 4, 0]]
        assert result == expected

    def test_add_border_bottom_left_right(self):
        """Test adding border to bottom, left and right"""
        matrix = [[1, 2], [3, 4]]
        result = add_matrix_border(matrix, 0, "blr")
        expected = [[0, 1, 2, 0], [0, 3, 4, 0], [0, 0, 0, 0]]
        assert result == expected

    def test_add_border_full(self):
        """Test adding border to all four sides"""
        matrix = [[1, 2], [3, 4]]
        result = add_matrix_border(matrix, 0, "full")
        expected = [[0, 0, 0, 0], [0, 1, 2, 0], [0, 3, 4, 0], [0, 0, 0, 0]]
        assert result == expected


class TestAddMatrixBorderEdgeCases:
    """Test edge cases for add_matrix_border function"""

    def test_empty_matrix(self):
        """Test with empty matrix"""
        empty_matrix = []
        result = add_matrix_border(empty_matrix, 0, "full")
        assert result == []

    def test_single_row_matrix(self):
        """Test with single row matrix"""
        single_row = [[1, 2, 3]]
        result = add_matrix_border(single_row, 0, "full")
        expected = [[0, 0, 0, 0, 0], [0, 1, 2, 3, 0], [0, 0, 0, 0, 0]]
        assert result == expected

    def test_single_column_matrix(self):
        """Test with single column matrix"""
        single_col = [[1], [2], [3]]
        result = add_matrix_border(single_col, 0, "full")
        expected = [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 3, 0], [0, 0, 0]]
        assert result == expected

    def test_single_element_matrix(self):
        """Test with single element matrix"""
        single_elem = [[42]]
        result = add_matrix_border(single_elem, 0, "full")
        expected = [[0, 0, 0], [0, 42, 0], [0, 0, 0]]
        assert result == expected

    def test_different_padding_elements(self):
        """Test with different types of padding elements"""
        matrix = [[1, 2], [3, 4]]

        # Test with string padding
        result_str = add_matrix_border(matrix, "X", "full")
        expected_str = [
            ["X", "X", "X", "X"],
            ["X", 1, 2, "X"],
            ["X", 3, 4, "X"],
            ["X", "X", "X", "X"],
        ]
        assert result_str == expected_str

        # Test with None padding
        result_none = add_matrix_border(matrix, None, "full")
        expected_none = [
            [None, None, None, None],
            [None, 1, 2, None],
            [None, 3, 4, None],
            [None, None, None, None],
        ]
        assert result_none == expected_none

        # Test with negative number padding
        result_neg = add_matrix_border(matrix, -1, "full")
        expected_neg = [[-1, -1, -1, -1], [-1, 1, 2, -1], [-1, 3, 4, -1], [-1, -1, -1, -1]]
        assert result_neg == expected_neg

    def test_original_matrix_unchanged(self):
        """Test that original matrix is not modified"""
        original_matrix = [[1, 2], [3, 4]]
        original_copy = [row[:] for row in original_matrix]  # Deep copy for comparison

        add_matrix_border(original_matrix, 0, "full")

        # Original matrix should remain unchanged
        assert original_matrix == original_copy


class TestAddMatrixBorderParameterized:
    """Parametrized tests for add_matrix_border function"""

    @pytest.mark.parametrize(
        "mode,expected",
        [
            ("t", [[0, 0], [1, 2], [3, 4]]),
            ("b", [[1, 2], [3, 4], [0, 0]]),
            ("l", [[0, 1, 2], [0, 3, 4]]),
            ("r", [[1, 2, 0], [3, 4, 0]]),
            ("tb", [[0, 0], [1, 2], [3, 4], [0, 0]]),
            ("tl", [[0, 0, 0], [0, 1, 2], [0, 3, 4]]),
            ("tr", [[0, 0, 0], [1, 2, 0], [3, 4, 0]]),
            ("bl", [[0, 1, 2], [0, 3, 4], [0, 0, 0]]),
            ("br", [[1, 2, 0], [3, 4, 0], [0, 0, 0]]),
            ("tlr", [[0, 0, 0, 0], [0, 1, 2, 0], [0, 3, 4, 0]]),
            ("blr", [[0, 1, 2, 0], [0, 3, 4, 0], [0, 0, 0, 0]]),
            ("full", [[0, 0, 0, 0], [0, 1, 2, 0], [0, 3, 4, 0], [0, 0, 0, 0]]),
        ],
    )
    def test_all_modes(self, mode, expected):
        """Test all border modes with parametrized inputs"""
        matrix = [[1, 2], [3, 4]]
        result = add_matrix_border(matrix, 0, mode)
        assert result == expected
