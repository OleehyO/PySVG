#!/usr/bin/env python3
"""
Matrix Border as Number Example

This example demonstrates how to use the Matrix component's border_as_number method
to create matrices with coordinate labels. Particularly suitable for scenarios like
game boards, charts, etc. that require coordinate labeling.

Main features:
1. Basic border labeling functionality
2. Custom border text styling
3. Different border position examples
4. Game board application examples
"""

from pathlib import Path
from pysvg.components import Matrix, MatrixConfig
from pysvg.components.content import TextContent, TextConfig
from pysvg.schema import AppearanceConfig, Color
from pysvg.components.canvas import Canvas


def chess_board_example():
    """Chess board example - demonstrates main usage of border_as_number"""
    print("=== Chess Board Example ===")

    # Create chess board data, first row and column as coordinate labels
    chess_data = [
        ["", "A", "B", "C", "D", "E", "F", "G", "H", "I"],
        ["9", "X", ".", ".", ".", "X", ".", ".", ".", "."],
        ["8", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        ["7", ".", "O", ".", "O", ".", ".", "X", ".", "."],
        ["6", ".", ".", ".", "X", ".", ".", ".", ".", "O"],
        ["5", "O", ".", "X", "O", "X", ".", ".", ".", "."],
        ["4", ".", "X", "O", "O", ".", "O", ".", ".", "."],
        ["3", ".", ".", "X", "O", "X", ".", ".", ".", "."],
        ["2", ".", ".", ".", "X", ".", ".", ".", ".", "."],
        ["1", ".", "O", ".", "O", ".", ".", "X", ".", "."],
    ]

    # Set appearance for pieces and empty spaces
    element_appearance_map = {
        "X": AppearanceConfig(fill=Color("lightblue"), stroke=Color("gray"), stroke_width=1),
        "O": AppearanceConfig(fill=Color("white"), stroke=Color("gray"), stroke_width=1),
        ".": AppearanceConfig(fill=Color("lightgray"), stroke=Color("gray"), stroke_width=1),
    }

    # Create Matrix, set border_as_number during initialization
    matrix = Matrix(
        data=chess_data,
        element_appearance_map=element_appearance_map,
        border_as_number="upperleft",  # Use upper left corner for coordinate labels
        coord_font_size=16,  # Coordinate text font size
        coord_font_family="Arial",  # Coordinate text font family
        coord_color=Color("darkblue"),  # Coordinate text color
        config=MatrixConfig(x=50, y=50, cell_size=40),
    )

    print(f"Chess board matrix size: {len(chess_data)}x{len(chess_data[0])}")
    print("✓ First row and column as coordinate labels")
    print("✓ Coordinate label elements: no fill, no border, dark blue text")
    print("✓ Pieces X/O and empty spaces . have different appearance settings")
    print(f"Chess board SVG: {matrix.to_svg_element()[:200]}...")
    print()

    return matrix


def custom_border_style_example():
    """Custom border style example"""
    print("=== Custom Border Style Example ===")

    # Simple 3x3 data grid
    data = [["", "Col1", "Col2"], ["Row1", "DataA", "DataB"], ["Row2", "DataC", "DataD"]]

    # Create Matrix with custom coordinate style
    matrix = Matrix(
        data=data,
        border_as_number="upperleft",
        coord_font_size=18,  # Larger font
        coord_font_family="Times",  # Different font family
        coord_color=Color("red"),  # Red coordinate text
        config=MatrixConfig(x=500, y=50, cell_size=60),
    )

    # Set appearance for data cells
    matrix.set_global_appearance(
        AppearanceConfig(fill=Color("lightyellow"), stroke=Color("blue"), stroke_width=2)
    )

    print("✓ Using Times font, 18px size, red coordinate text")
    print("✓ Data cells: light yellow fill, blue border")
    print("✓ Demonstrates border style has highest priority (not affected by global appearance)")
    print(f"Custom border style SVG: {matrix.to_svg_element()}")
    print()

    return matrix


def different_border_positions_example():
    """Different border positions example"""
    print("=== Four Border Position Examples ===")

    # Base data
    base_data = (
        # Upper left
        [
            ["", "C1", "C2", "C3"],
            ["R1", "A", "B", "C"],
            ["R2", "D", "E", "F"],
            ["R3", "G", "H", "I"],
        ],
        # Upper right
        [
            ["C1", "C2", "C3", ""],
            ["A", "B", "C", "R1"],
            ["D", "E", "F", "R2"],
            ["G", "H", "I", "R3"],
        ],
        # Lower left
        [
            ["R1", "A", "B", "C"],
            ["R2", "D", "E", "F"],
            ["R3", "G", "H", "I"],
            ["", "C1", "C2", "C3"],
        ],
        # Lower right
        [
            ["A", "B", "C", "R1"],
            ["D", "E", "F", "R2"],
            ["G", "H", "I", "R3"],
            ["C1", "C2", "C3", ""],
        ],
    )

    matrices = []
    positions = ["upperleft", "upperright", "lowerleft", "lowerright"]
    position_names = ["Upper Left", "Upper Right", "Lower Left", "Lower Right"]
    colors = [Color("purple"), Color("green"), Color("orange"), Color("navy")]

    for i, (position, name, color) in enumerate(zip(positions, position_names, colors)):
        print(f"✓ {name} border labeling")

        matrix = Matrix(
            data=base_data[i],
            border_as_number=position,
            coord_color=color,
            coord_font_size=14,
            config=MatrixConfig(x=50 + i * 250, y=500, cell_size=35),
        )

        # Set appearance for data area
        matrix.set_global_appearance(
            AppearanceConfig(fill=Color("lightcyan"), stroke=Color("gray"), stroke_width=1)
        )

        print(f"{name} border SVG: {matrix.to_svg_element()}")
        matrices.append(matrix)

    print()
    return matrices


def game_board_with_caption_example():
    """Game board with caption example"""
    print("=== Gomoku Game Board Example ===")

    # Gomoku board (simplified)
    gomoku_data = [
        ["", "A", "B", "C", "D", "E"],
        ["5", ".", ".", "O", ".", "."],
        ["4", ".", "X", "O", "X", "."],
        ["3", ".", "O", "X", "O", "."],
        ["2", "X", ".", "X", ".", "."],
        ["1", ".", ".", ".", ".", "."],
    ]

    # Set piece appearance
    element_appearance_map = {
        "X": AppearanceConfig(fill=Color("lightpink"), stroke=Color("gray"), stroke_width=1),
        "O": AppearanceConfig(fill=Color("white"), stroke=Color("gray"), stroke_width=2),
        ".": AppearanceConfig(fill=Color("burlywood"), stroke=Color("saddlebrown"), stroke_width=1),
    }

    # Create title
    caption = TextContent(
        config=TextConfig(
            text="Gomoku Game Board", font_size=20, font_family="Arial", color=Color("darkgreen")
        )
    )

    matrix = Matrix(
        data=gomoku_data,
        element_appearance_map=element_appearance_map,
        border_as_number="upperleft",
        coord_font_size=14,
        coord_color=Color("saddlebrown"),
        caption=caption,
        caption_location="top",
        config=MatrixConfig(x=750, y=100, cell_size=45),
    )

    print("✓ Gomoku board with coordinate labels")
    print("✓ Black pieces X, white pieces O, empty spaces in brown")
    print("✓ Brown coordinate text, matching game theme")
    print("✓ Top caption")
    print(f"Gomoku game board SVG: {matrix.to_svg_element()}")
    print()

    return matrix


def priority_demonstration_example():
    """Priority demonstration example"""
    print("=== Border Style Priority Demonstration ===")

    data = [["", "Col1", "Col2"], ["Row1", "Data1", "Data2"], ["Row2", "Data3", "Data4"]]

    # Create Matrix, set border_as_number first
    matrix = Matrix(
        data=data,
        border_as_number="upperleft",
        coord_font_size=16,
        coord_color=Color("red"),
        config=MatrixConfig(x=500, y=250, cell_size=50),
    )

    # Then set global appearance (should not affect border elements)
    matrix.set_global_appearance(
        AppearanceConfig(fill=Color("yellow"), stroke=Color("black"), stroke_width=3)
    )

    # Set font (should also not affect border elements)
    matrix.set_font_size(20)
    matrix.set_font_color(Color("blue"))
    matrix.set_font_family("Times")

    print("✓ Border elements: red, 16px size (unchanged)")
    print("✓ Data elements: blue, 20px, Times font, yellow fill")
    print("✓ Proves border style has highest priority")
    print(f"Priority demonstration SVG: {matrix.to_svg_element()}")
    print()

    return matrix


def generate_demo_svg():
    """Generate demonstration SVG file"""
    print("=== Generate Demo SVG ===")

    # Create canvas
    canvas = Canvas(width=1020, height=640)

    # Add title
    title = TextContent(
        config=TextConfig(
            x=600,
            y=25,
            text="Matrix Border as Number Feature Demonstration",
            font_size=24,
            font_family="Arial",
            color=Color("darkblue"),
            text_anchor="middle",
        )
    )
    canvas.add(title)

    # Add various examples
    chess_matrix = chess_board_example()
    canvas.add(chess_matrix)

    custom_matrix = custom_border_style_example()
    canvas.add(custom_matrix)

    # Add different position examples
    position_matrices = different_border_positions_example()
    for matrix in position_matrices:
        canvas.add(matrix)

    # Add game board example
    gomoku_matrix = game_board_with_caption_example()
    canvas.add(gomoku_matrix)

    # Add priority demonstration
    priority_matrix = priority_demonstration_example()
    canvas.add(priority_matrix)

    # Generate and save SVG file
    output_path = Path(__file__).parent / "border_as_number_demo.svg"
    canvas.save(output_path)

    print(f"Demo SVG saved to: {output_path}")
    print(f"File size: {output_path.stat().st_size / 1024:.1f} KB")

    return output_path


def main():
    """Main function, run all examples"""
    print("Matrix Border as Number Feature Demonstration")
    print("=" * 50)

    # Run various examples
    chess_matrix = chess_board_example()
    custom_matrix = custom_border_style_example()
    position_matrices = different_border_positions_example()
    gomoku_matrix = game_board_with_caption_example()
    priority_matrix = priority_demonstration_example()

    # Generate demo SVG
    generate_demo_svg()

    print(f"=== Summary ===")
    print("✓ border_as_number feature set during initialization")
    print("✓ Supports four border position modes")
    print("✓ Border element styles have highest priority")
    print("✓ Customizable border text font, size, color")
    print("✓ Automatic validation of border elements as text content")
    print("✓ Border element positions automatically optimized for matrix center")

    print("\nAll examples completed!")
    print("View the generated border_as_number_demo.svg file to see the visual effects.")


if __name__ == "__main__":
    main()
