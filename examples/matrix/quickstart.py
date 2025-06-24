#!/usr/bin/env python3
"""
Matrix Component Quick Start Guide

This is a quick start guide for the Matrix component, demonstrating the most common features:
1. Basic matrix creation
2. Element mapping
3. Appearance customization
4. Adding captions
5. Font settings
6. Method chaining
7. Comprehensive examples
"""

from pysvg.components import Matrix, MatrixConfig, Circle, CircleConfig, Polyline, PolylineConfig
from pysvg.components.content import TextContent, TextConfig
from pysvg.schema import AppearanceConfig, Color
from pysvg.components.canvas import Canvas


def basic_matrix_examples():
    """Basic matrix examples"""
    print("=== Basic Matrix Examples ===")

    # 1. Simple numeric matrix
    simple_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    simple_matrix = Matrix(data=simple_data, config=MatrixConfig(cell_size=50))
    print(f"Simple matrix: {simple_matrix.to_svg_element()}")

    # 2. String matrix
    string_data = [["A", "B", "C"], ["D", "E", "F"]]

    string_matrix = Matrix(data=string_data, config=MatrixConfig(cell_size=60))
    print(f"String matrix: {string_matrix.to_svg_element()}")
    print()


def element_mapping_examples():
    """Element mapping examples"""
    print("=== Element Mapping Examples ===")

    # Original data
    data = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]

    # Element mapping: 0 -> "Empty", 1 -> "Full"
    element_map = {
        0: TextContent("Empty"),
        1: TextContent("Full"),
    }

    mapped_matrix = Matrix(data=data, element_map=element_map, config=MatrixConfig(cell_size=60))
    print(f"Mapped matrix: {mapped_matrix.to_svg_element()}")
    print()


def background_map_example():
    """Background map example"""
    print("=== Background Map Example ===")

    data = [[1, 2, 3], [4, 5, 6]]

    # Using element appearance mapping
    bgmap = {
        1: AppearanceConfig(fill=Color("red"), stroke=Color("darkred"), stroke_width=2),
        2: AppearanceConfig(fill=Color("green"), stroke=Color("darkgreen"), stroke_width=2),
        3: AppearanceConfig(fill=Color("blue"), stroke=Color("darkblue"), stroke_width=2),
        4: AppearanceConfig(fill=Color("yellow"), stroke=Color("orange"), stroke_width=2),
        5: AppearanceConfig(fill=Color("purple"), stroke=Color("darkmagenta"), stroke_width=2),
        6: AppearanceConfig(fill=Color("cyan"), stroke=Color("darkcyan"), stroke_width=2),
    }

    element_appearance_example = Matrix(
        data=data,
        background_map=bgmap,
        config=MatrixConfig(cell_size=70),
    )
    print(f"Element appearance mapping: {element_appearance_example.to_svg_element()}")
    print()


def caption_examples():
    """Caption examples"""
    print("=== Caption Examples ===")

    data = [[1, 2], [3, 4]]
    caption = "Example Matrix"

    # Top caption
    top_caption_matrix = Matrix(
        data=data,
        caption=caption,
        caption_font_size=16,
        caption_font_color=Color("black"),
        caption_location="top",
        config=MatrixConfig(cell_size=60),
    ).move_by(0, 100)
    print(f"Top caption: {top_caption_matrix.to_svg_element()}")

    # Bottom caption
    down_caption_matrix = Matrix(
        data=data,
        caption=caption,
        caption_font_size=16,
        caption_font_color=Color("black"),
        caption_location="bottom",
        config=MatrixConfig(cell_size=60),
    )
    print(f"Bottom caption: {down_caption_matrix.to_svg_element()}")

    # Left caption
    left_caption_matrix = Matrix(
        data=data,
        caption=caption,
        caption_font_size=16,
        caption_font_color=Color("black"),
        caption_location="left",
        config=MatrixConfig(cell_size=60),
    ).move_by(300, 0)
    print(f"Left caption: {left_caption_matrix.to_svg_element()}")

    # Right caption
    right_caption_matrix = Matrix(
        data=data,
        caption=caption,
        caption_font_size=16,
        caption_font_color=Color("black"),
        caption_location="right",
        config=MatrixConfig(cell_size=60),
    ).move(200, 200)
    print(f"Right caption: {right_caption_matrix.to_svg_element()}")
    print()


def comprehensive_example():
    """Comprehensive example"""
    print("=== Comprehensive Example ===")

    # Create a complex matrix example
    data = [[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]]

    # Element mapping
    element_map = {
        0: TextContent("○"),
        1: TextContent("●", config=TextConfig(color=Color("gray"))),
    }

    # Element appearance mapping
    element_appearance_map = {
        0: AppearanceConfig(fill=Color("white"), stroke=Color("black"), stroke_width=2),
        1: AppearanceConfig(fill=Color("black"), stroke=Color("gray"), stroke_width=2),
    }

    # Caption text
    caption = "Checkerboard Pattern"

    # Create comprehensive matrix
    comprehensive_matrix = Matrix(
        data=data,
        element_map=element_map,
        background_map=element_appearance_map,
        caption=caption,
        caption_font_size=18,
        caption_font_color=Color("darkblue"),
        caption_location="top",
        config=MatrixConfig(cell_size=60),
    )

    print(f"Comprehensive example: {comprehensive_matrix.to_svg_element()}")
    print()

    return comprehensive_matrix


def generate_demo_svg():
    """Generate demo SVG file"""
    print("=== Generating Demo SVG ===")

    # Create canvas
    canvas = Canvas(width=750, height=500)

    # 1. Basic numeric matrix
    simple_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    simple_matrix = Matrix(data=simple_data, config=MatrixConfig(cell_size=50)).move_by(50, 50)
    canvas.add(simple_matrix)

    # 2. Colored matrix
    colored_data = [["R", "G", "B"], ["C", "M", "Y"]]
    bgmap = {
        "R": AppearanceConfig(fill=Color("red"), stroke=Color("darkred"), stroke_width=2),
        "G": AppearanceConfig(fill=Color("green"), stroke=Color("darkgreen"), stroke_width=2),
        "B": AppearanceConfig(fill=Color("blue"), stroke=Color("darkblue"), stroke_width=2),
        "C": AppearanceConfig(fill=Color("cyan"), stroke=Color("darkcyan"), stroke_width=2),
        "M": AppearanceConfig(fill=Color("magenta"), stroke=Color("darkmagenta"), stroke_width=2),
        "Y": AppearanceConfig(fill=Color("yellow"), stroke=Color("orange"), stroke_width=2),
    }
    colored_matrix = (
        Matrix(
            data=colored_data,
            background_map=bgmap,
            config=MatrixConfig(cell_size=60),
        )
    ).move_by(260, 50)
    canvas.add(colored_matrix)

    # 3. Matrix with caption
    caption_data = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
    element_map = {
        0: TextContent("○"),
        1: TextContent("●"),
    }
    caption = "Pattern Matrix"
    caption_matrix = Matrix(
        data=caption_data,
        element_map=element_map,
        caption=caption,
        caption_location="top",
        caption_font_size=20,
        caption_font_color=Color("navy"),
        config=MatrixConfig(cell_size=50),
    ).move_by(500, 50)
    canvas.add(caption_matrix)

    # 4. SVG content matrix
    circle = Circle(
        config=CircleConfig(cx=20, cy=20, r=12), appearance=AppearanceConfig(fill=Color("red"))
    )
    triangle = Polyline(
        config=PolylineConfig(points=[(20, 8), (8, 32), (32, 32)]),
        appearance=AppearanceConfig(fill=Color("blue")),
    )
    data = [["circle-component", "triangle-component"], ["Circle", "Triangle"]]
    element_map = {
        "circle-component": circle,
        "triangle-component": triangle,
    }
    svg_matrix = Matrix(
        data=data, element_map=element_map, config=MatrixConfig(cell_size=70)
    ).move_by(50, 250)
    canvas.add(svg_matrix)

    # 5. Large matrix example
    large_data = [[i + j * 5 + 1 for i in range(5)] for j in range(4)]
    appearance = AppearanceConfig(fill=Color("lightblue"), stroke=Color("blue"), stroke_width=1)
    bgmap = {i: appearance for i in range(1, 21)}
    large_matrix = (
        Matrix(data=large_data, background_map=bgmap, config=MatrixConfig(cell_size=40))
    ).move_by(250, 250)
    canvas.add(large_matrix)

    # 6. Checkerboard pattern (comprehensive example)
    checkerboard_data = [
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
    ]
    checkerboard_map = {
        0: TextContent(""),
        1: TextContent(""),
    }
    checkerboard_appearance = {
        0: AppearanceConfig(fill=Color("white"), stroke=Color("black"), stroke_width=1),
        1: AppearanceConfig(fill=Color("black"), stroke=Color("gray"), stroke_width=1),
    }
    checkerboard_caption = "Checkerboard Pattern"
    checkerboard_matrix = Matrix(
        data=checkerboard_data,
        element_map=checkerboard_map,
        background_map=checkerboard_appearance,
        caption=checkerboard_caption,
        caption_location="bottom",
        caption_font_size=18,
        caption_font_color=Color("darkgreen"),
        config=MatrixConfig(cell_size=40),
    )
    checkerboard_matrix.move_by(500, 250)
    canvas.add(checkerboard_matrix)

    # Generate and save SVG file
    canvas.save("quickstart.svg")

    print("SVG file has been generated: quickstart.svg")


def main():
    """Main function"""
    print("Matrix Component Quick Start Guide")
    print("=" * 50)

    # Run all examples
    basic_matrix_examples()
    element_mapping_examples()
    background_map_example()
    caption_examples()
    comprehensive_example()

    # Generate demo SVG
    generate_demo_svg()

    print("\nAll examples completed!")
    print("Check the generated quickstart.svg file to see the visual effects.")


if __name__ == "__main__":
    main()
