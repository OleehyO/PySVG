from typing import Any, Literal


def add_matrix_border(
    data: list[list[Any]],
    pad_elem: Any,
    mode: Literal["t", "b", "l", "r", "tb", "tl", "tr", "bl", "br", "tlr", "blr", "full"],
) -> list[list[Any]]:
    """
    Add border to a matrix with specified padding element and mode.

    Args:
        data: Input matrix (list of list)
        pad_elem: Element used for padding
        mode: Padding mode
            - t: top
            - b: bottom
            - l: left
            - r: right
            - tb: top + bottom
            - tl: top + left
            - tr: top + right
            - bl: bottom + left
            - br: bottom + right
            - tlr: top + left + right
            - blr: bottom + left + right
            - full: all four sides

    Returns:
        Matrix with added border

    Example:
        >>> matrix = [[1, 2], [3, 4]]
        >>> add_matrix_border(matrix, 0, "full")
        [[0, 0, 0, 0], [0, 1, 2, 0], [0, 3, 4, 0], [0, 0, 0, 0]]
    """
    if not data or not data[0]:
        return data

    # Deep copy original data
    result = [row[:] for row in data]
    rows = len(result)
    cols = len(result[0]) if result else 0

    # Parse directions from mode
    add_top = "t" in mode
    add_bottom = "b" in mode
    add_left = "l" in mode
    add_right = "r" in mode

    if mode == "full":
        add_top = add_bottom = add_left = add_right = True

    # Add left and right borders first (so we can calculate new column count correctly)
    if add_left or add_right:
        for i in range(rows):
            if add_left:
                result[i] = [pad_elem] + result[i]
            if add_right:
                result[i] = result[i] + [pad_elem]

    # Update column count (since we may have added left/right borders)
    new_cols = len(result[0]) if result else 0

    # Add top border
    if add_top:
        top_row = [pad_elem] * new_cols
        result = [top_row] + result

    # Add bottom border
    if add_bottom:
        bottom_row = [pad_elem] * new_cols
        result = result + [bottom_row]

    return result
