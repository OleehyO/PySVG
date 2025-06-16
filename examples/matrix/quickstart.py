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

from pathlib import Path
from pysvg.components import Matrix, MatrixConfig
from pysvg.components.content import TextContent, TextConfig
from pysvg.schema import AppearanceConfig, Color, SVGCode
from pysvg.components.canvas import Canvas


def basic_matrix_examples():
    """Basic matrix examples"""
    print("=== Basic Matrix Examples ===")

    # 1. Simple numeric matrix
    simple_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    simple_matrix = Matrix(data=simple_data, config=MatrixConfig(x=10, y=10, cell_size=50))
    print(f"Simple matrix: {simple_matrix.to_svg_element()}")

    # 2. String matrix
    string_data = [["A", "B", "C"], ["D", "E", "F"]]

    string_matrix = Matrix(data=string_data, config=MatrixConfig(x=200, y=10, cell_size=60))
    print(f"String matrix: {string_matrix.to_svg_element()}")
    print()


def element_mapping_examples():
    """Element mapping examples"""
    print("=== Element Mapping Examples ===")

    # Original data
    data = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]

    # Element mapping: 0 -> "Empty", 1 -> "Full"
    element_map = {0: "Empty", 1: "Full"}

    mapped_matrix = Matrix(
        data=data, element_map=element_map, config=MatrixConfig(x=10, y=150, cell_size=60)
    )
    print(f"Mapped matrix: {mapped_matrix.to_svg_element()}")
    print()


def appearance_examples():
    """Appearance customization examples"""
    print("=== Appearance Examples ===")

    data = [[1, 2, 3], [4, 5, 6]]

    # 1. Using appearance matrix
    appearance_matrix = [
        [
            AppearanceConfig(fill=Color("lightblue"), stroke=Color("blue")),
            AppearanceConfig(fill=Color("lightgreen"), stroke=Color("green")),
            AppearanceConfig(fill=Color("lightcoral"), stroke=Color("red")),
        ],
        [
            AppearanceConfig(fill=Color("lightyellow"), stroke=Color("orange")),
            AppearanceConfig(fill=Color("lightpink"), stroke=Color("purple")),
            AppearanceConfig(fill=Color("lightgray"), stroke=Color("black")),
        ],
    ]

    appearance_matrix_example = Matrix(
        data=data,
        appearance_matrix=appearance_matrix,
        config=MatrixConfig(x=10, y=280, cell_size=70),
    )
    print(f"Appearance matrix: {appearance_matrix_example.to_svg_element()}")

    # 2. Using element appearance mapping
    element_appearance_map = {
        1: AppearanceConfig(fill=Color("red"), stroke=Color("darkred"), stroke_width=2),
        2: AppearanceConfig(fill=Color("green"), stroke=Color("darkgreen"), stroke_width=2),
        3: AppearanceConfig(fill=Color("blue"), stroke=Color("darkblue"), stroke_width=2),
        4: AppearanceConfig(fill=Color("yellow"), stroke=Color("orange"), stroke_width=2),
        5: AppearanceConfig(fill=Color("purple"), stroke=Color("darkmagenta"), stroke_width=2),
        6: AppearanceConfig(fill=Color("cyan"), stroke=Color("darkcyan"), stroke_width=2),
    }

    element_appearance_example = Matrix(
        data=data,
        element_appearance_map=element_appearance_map,
        config=MatrixConfig(x=250, y=280, cell_size=70),
    )
    print(f"Element appearance mapping: {element_appearance_example.to_svg_element()}")
    print()


def caption_examples():
    """Caption examples"""
    print("=== Caption Examples ===")

    data = [[1, 2], [3, 4]]

    # Create captions for different positions
    caption = TextContent(
        config=TextConfig(text="Example Matrix", font_size=16, color=Color("black"))
    )

    # Top caption
    top_caption_matrix = Matrix(
        data=data,
        caption=caption,
        caption_location="top",
        config=MatrixConfig(x=10, y=450, cell_size=60),
    )
    print(f"Top caption: {top_caption_matrix.to_svg_element()}")

    # Bottom caption
    down_caption_matrix = Matrix(
        data=data,
        caption=caption,
        caption_location="down",
        config=MatrixConfig(x=150, y=450, cell_size=60),
    )
    print(f"Bottom caption: {down_caption_matrix.to_svg_element()}")

    # Left caption
    left_caption_matrix = Matrix(
        data=data,
        caption=caption,
        caption_location="left",
        config=MatrixConfig(x=320, y=450, cell_size=60),
    )
    print(f"Left caption: {left_caption_matrix.to_svg_element()}")

    # Right caption
    right_caption_matrix = Matrix(
        data=data,
        caption=caption,
        caption_location="right",
        config=MatrixConfig(x=450, y=450, cell_size=60),
    )
    print(f"Right caption: {right_caption_matrix.to_svg_element()}")
    print()


def font_styling_examples():
    """Font styling examples"""
    print("=== Font Styling Examples ===")

    data = [["Hello", "World"], ["Font", "Style"]]

    # Create matrix with custom font
    font_matrix = Matrix(data=data, config=MatrixConfig(x=10, y=600, cell_size=80))

    # Set font styles
    font_matrix.set_font_family("Arial").set_font_size(16).set_font_color(Color("darkblue"))

    print(f"Font styling: {font_matrix.to_svg_element()}")
    print()


def method_chaining_examples():
    """Method chaining examples"""
    print("=== Method Chaining Examples ===")

    data = [["A", "B"], ["C", "D"]]

    # Chain method calls to set various properties
    chained_matrix = (
        Matrix(data=data, config=MatrixConfig(x=200, y=600))
        .set_cell_size(90)
        .set_pad(10)
        .set_font_size(20)
        .set_font_color(Color("white"))
        .set_global_appearance(
            AppearanceConfig(fill=Color("navy"), stroke=Color("gold"), stroke_width=3)
        )
    )

    print(f"Method chaining: {chained_matrix.to_svg_element()}")
    print()


def svg_content_examples():
    """SVG content examples"""
    print("=== SVG Content Examples ===")

    # Create matrix with SVG content
    svg_circle = SVGCode(
        '<circle cx="25" cy="25" r="15" fill="red" stroke="darkred" stroke-width="2"/>'
    )
    svg_rect = SVGCode(
        '<rect x="10" y="10" width="30" height="30" fill="blue" stroke="darkblue" stroke-width="2"/>'
    )

    svg_data = [[svg_circle, "Text"], ["Mixed", svg_rect]]

    svg_matrix = Matrix(data=svg_data, config=MatrixConfig(x=350, y=600, cell_size=80))

    print(f"SVG content: {svg_matrix.to_svg_element()}")
    print()


def comprehensive_example():
    """Comprehensive example"""
    print("=== Comprehensive Example ===")

    # Create a complex matrix example
    data = [[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]]

    # Element mapping
    element_map = {0: "○", 1: "●"}

    # Element appearance mapping
    element_appearance_map = {
        0: AppearanceConfig(fill=Color("white"), stroke=Color("black"), stroke_width=2),
        1: AppearanceConfig(fill=Color("black"), stroke=Color("gray"), stroke_width=2),
    }

    # Caption text
    caption = TextContent(
        config=TextConfig(text="Checkerboard Pattern", font_size=18, color=Color("darkblue"))
    )

    # Create comprehensive matrix
    comprehensive_matrix = (
        Matrix(
            data=data,
            element_map=element_map,
            element_appearance_map=element_appearance_map,
            caption=caption,
            caption_location="top",
            config=MatrixConfig(x=50, y=750, cell_size=60),
        )
        .set_font_size(24)
        .set_font_color(Color("white"))
    )

    print(f"Comprehensive example: {comprehensive_matrix.to_svg_element()}")
    print()

    return comprehensive_matrix


def generate_demo_svg():
    """Generate demo SVG file"""
    print("=== Generating Demo SVG ===")

    # Create canvas
    canvas = Canvas(width=800, height=1200)

    # 1. Basic numeric matrix
    simple_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    simple_matrix = Matrix(data=simple_data, config=MatrixConfig(x=50, y=50, cell_size=50))
    canvas.add(simple_matrix)

    # 2. Colored matrix
    colored_data = [["R", "G", "B"], ["C", "M", "Y"]]
    element_appearance_map = {
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
            element_appearance_map=element_appearance_map,
            config=MatrixConfig(x=250, y=50, cell_size=60),
        )
        .set_font_size(18)
        .set_font_color(Color("white"))
    )
    canvas.add(colored_matrix)

    # 3. Matrix with caption
    caption_data = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
    element_map = {0: "○", 1: "●"}
    caption = TextContent(
        config=TextConfig(text="Pattern Matrix", font_size=16, color=Color("navy"))
    )
    caption_matrix = Matrix(
        data=caption_data,
        element_map=element_map,
        caption=caption,
        caption_location="top",
        config=MatrixConfig(x=500, y=50, cell_size=50),
    ).set_font_size(20)
    canvas.add(caption_matrix)

    # 4. SVG content matrix
    svg_circle = SVGCode('<circle cx="20" cy="20" r="12" fill="red"/>')
    svg_triangle = SVGCode('<polygon points="20,8 8,32 32,32" fill="blue"/>')
    svg_data = [[svg_circle, svg_triangle], ["Circle", "Triangle"]]
    svg_matrix = Matrix(
        data=svg_data, config=MatrixConfig(x=50, y=250, cell_size=70)
    ).set_font_size(12)
    canvas.add(svg_matrix)

    # 5. Large matrix example
    large_data = [[i + j * 5 + 1 for i in range(5)] for j in range(4)]
    large_matrix = (
        Matrix(data=large_data, config=MatrixConfig(x=250, y=250, cell_size=40))
        .set_font_size(14)
        .set_global_appearance(
            AppearanceConfig(fill=Color("lightblue"), stroke=Color("blue"), stroke_width=1)
        )
    )
    canvas.add(large_matrix)

    # 6. Checkerboard pattern (comprehensive example)
    checkerboard_data = [
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
    ]
    checkerboard_map = {0: " ", 1: " "}
    checkerboard_appearance = {
        0: AppearanceConfig(fill=Color("white"), stroke=Color("black"), stroke_width=1),
        1: AppearanceConfig(fill=Color("black"), stroke=Color("gray"), stroke_width=1),
    }
    checkerboard_caption = TextContent(
        config=TextConfig(text="Checkerboard Pattern", font_size=18, color=Color("darkgreen"))
    )
    checkerboard_matrix = Matrix(
        data=checkerboard_data,
        element_map=checkerboard_map,
        element_appearance_map=checkerboard_appearance,
        caption=checkerboard_caption,
        caption_location="down",
        config=MatrixConfig(x=500, y=250, cell_size=40),
    )
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
    appearance_examples()
    caption_examples()
    font_styling_examples()
    method_chaining_examples()
    svg_content_examples()
    comprehensive_example()

    # Generate demo SVG
    generate_demo_svg()

    print("\nAll examples completed!")
    print("Check the generated quickstart.svg file to see the visual effects.")


if __name__ == "__main__":
    main()
