#!/usr/bin/env python3
"""
Cell Component Quick Start Guide

This is a quick start guide for the Cell component, demonstrating the most commonly used features:
1. Basic creation
2. Adding text content
3. Adding image content
4. Adding SVG content
5. Appearance customization
6. Basic transformations
7. Method chaining
"""

from pysvg.components import Cell, CellConfig
from pysvg.components.content import TextConfig, ImageConfig, SVGConfig
from pysvg.schema import AppearanceConfig, Color, SVGCode
from pysvg.components.canvas import Canvas
from pysvg.components.content import TextContent


def basic_examples():
    """Basic usage examples"""
    print("=== Basic Usage Examples ===")

    # 1. Cell with specified position and size
    positioned_cell = Cell(config=CellConfig(width=100, height=50)).move(10, 20)
    print(f"Positioned cell: {positioned_cell.to_svg_element()}")

    # 2. Cell with appearance
    styled_cell = Cell(
        config=CellConfig(width=100, height=50),
        rectangle_appearance=AppearanceConfig(
            fill=Color(value="lightblue"), stroke=Color(value="navy"), stroke_width=2
        ),
    ).move(10, 20)
    print(f"Styled cell: {styled_cell.to_svg_element()}")
    print()


def content_examples():
    """Content examples"""
    print("=== Content Examples ===")

    # 1. Text content
    text_cell = Cell(
        config=CellConfig(
            width=120,
            height=60,
            text_content=TextConfig(text="Hello World", font_size=16, color=Color("darkblue")),
        ),
        rectangle_appearance=AppearanceConfig(
            fill=Color(value="lightcyan"), stroke=Color(value="blue"), stroke_width=1
        ),
    )
    print(f"Text cell: {text_cell.to_svg_element()}")

    # 2. Image content
    image_cell = Cell(
        config=CellConfig(
            width=100,
            height=60,
            image_content=ImageConfig(href="demo.png"),
            content_padding=5,
        ),
        rectangle_appearance=AppearanceConfig(
            fill=Color(value="white"), stroke=Color(value="gray"), stroke_width=2
        ),
    ).move(130, 0)
    print(f"Image cell: {image_cell.to_svg_element()}")

    # 3. SVG content
    svg_cell = Cell(
        config=CellConfig(
            width=100,
            height=60,
            svg_content=SVGConfig(
                svg_content=SVGCode(
                    '<circle cx="40" cy="25" r="20" fill="red" stroke="darkred" stroke-width="2"/>'
                )
            ),
        ),
        rectangle_appearance=AppearanceConfig(
            fill=Color(value="lightyellow"), stroke=Color(value="orange"), stroke_width=2
        ),
    ).move(240, 0)
    print(f"SVG cell: {svg_cell.to_svg_element()}")
    print()


def styling_examples():
    """Styling examples"""
    print("=== Styling Examples ===")

    # 1. Rounded cell
    rounded_cell = Cell(
        config=CellConfig(
            width=100,
            height=50,
            rx=15,
            ry=15,  # Rounded corners
            text_content=TextConfig(text="Rounded"),
        ),
        rectangle_appearance=AppearanceConfig(
            fill=Color("coral"), stroke=Color("darkred"), stroke_width=2
        ),
    ).move(0, 80)
    print(f"Rounded cell: {rounded_cell.to_svg_element()}")

    # 2. Transparent effect
    transparent_cell = Cell(
        config=CellConfig(
            width=100, height=50, text_content=TextConfig(text="Transparent", color="black")
        ),
        rectangle_appearance=AppearanceConfig(
            fill=Color("skyblue"),
            fill_opacity=0.5,  # Semi-transparent
            stroke=Color("blue"),
            stroke_width=2,
        ),
    ).move(110, 80)
    print(f"Transparent cell: {transparent_cell.to_svg_element()}")

    # 3. Dashed border
    dashed_cell = Cell(
        config=CellConfig(width=100, height=50, text_content=TextConfig(text="Dashed")),
        rectangle_appearance=AppearanceConfig(
            fill=Color("lightgreen"),
            stroke=Color("green"),
            stroke_width=3,
            stroke_dasharray=[5, 3],  # Dashed line
        ),
    ).move(220, 80)
    print(f"Dashed cell: {dashed_cell.to_svg_element()}")
    print()


def transform_examples():
    """Transform examples"""
    print("=== Transform Examples ===")

    # 1. Translation
    moved_cell = Cell(
        config=CellConfig(width=80, height=40, text_content=TextConfig(text="Moved", font_size=10)),
    ).move(150, 170)
    print(f"Moved cell: {moved_cell.to_svg_element()}")

    # 2. Rotation
    rotated_cell = (
        Cell(
            config=CellConfig(
                width=80, height=40, text_content=TextConfig(text="Rotated", font_size=10)
            ),
        )
        .move(50, 150)
        .rotate(30)
    )
    print(f"Rotated cell: {rotated_cell.to_svg_element()}")

    # 3. Scaling
    scaled_cell = (
        Cell(
            config=CellConfig(
                width=80, height=40, text_content=TextConfig(text="Scaled", font_size=10)
            ),
        )
        .scale(1.5)
        .move(250, 150)
    )
    print(f"Scaled cell: {scaled_cell.to_svg_element()}")
    print()


def chaining_examples():
    """Method chaining examples"""
    print("=== Method Chaining Examples ===")

    # Create cell and chain transform methods
    chained_cell = Cell(
        config=CellConfig(
            width=100,
            height=50,
            text_content=TextConfig(text="Chained"),
        ),
        rectangle_appearance=AppearanceConfig(
            fill=Color("purple"), stroke=Color("darkblue"), stroke_width=2
        ),
    )

    # Method chaining: move -> rotate -> scale
    chained_cell.move(200, 250).rotate(15).scale(1.2)
    print(f"Chained cell: {chained_cell.to_svg_element()}")

    # Reset transform
    chained_cell.reset_transform()
    print(f"Reset cell: {chained_cell.to_svg_element()}")
    print()


def utility_examples():
    """Utility method examples"""
    print("=== Utility Method Examples ===")

    # Create a cell with content
    test_cell = Cell(
        config=CellConfig(
            width=100,
            height=60,
            text_content=TextConfig(text="Test Cell"),
            content_padding=10,
        ),
        rectangle_appearance=AppearanceConfig(
            fill=Color("lightblue"), stroke=Color("blue"), stroke_width=2
        ),
    ).move(10, 300)

    # Test various utility methods
    print(f"SVG output: {test_cell.to_svg_element()}")
    print()


def generate_demo_svg():
    """Generate demo SVG file"""
    print("=== Generate Demo SVG ===")

    # Create Canvas
    canvas = Canvas(width=600, height=100, viewbox=(0, 0, 550, 80))

    # Add labels
    labels = [("Basic", 70), ("Text", 200), ("Rounded", 330), ("Rotated", 450)]

    for text, x in labels:
        label = TextContent(
            config=TextConfig(
                x=x,
                y=100,
                text=text,
                font_size=10,
                font_family="Arial",
                color=Color("gray"),
                text_anchor="middle",
            )
        )
        canvas.add(label)

    # Create example cells
    cells = [
        # Basic example
        Cell(
            config=CellConfig(width=100, height=50),
            rectangle_appearance=AppearanceConfig(fill="lightgray", stroke="black"),
        ).move(20, 20),
        # Text cell
        Cell(
            config=CellConfig(
                width=120,
                height=50,
                text_content=TextConfig(text="Text Cell", font_size=14),
            ),
            rectangle_appearance=AppearanceConfig(fill=Color("lightblue"), stroke=Color("blue")),
        ).move(140, 20),
        # Rounded cell
        Cell(
            config=CellConfig(
                width=100,
                height=50,
                rx=15,
                ry=15,
                text_content=TextConfig(text="Rounded"),
            ),
            rectangle_appearance=AppearanceConfig(fill=Color("lightgreen"), stroke=Color("green")),
        ).move(280, 20),
        # Rotated cell
        Cell(
            config=CellConfig(width=100, height=50, text_content=TextConfig(text="Rotated")),
            rectangle_appearance=AppearanceConfig(fill=Color("lightcoral"), stroke=Color("red")),
        )
        .move(400, 20)
        .rotate(15),
    ]

    # Add cells to canvas
    for cell in cells:
        canvas.add(cell)

    # Generate SVG file
    canvas.save("quickstart.svg")

    print("Demo file generated: quickstart.svg")


def main():
    """Main function"""
    print("Cell Component Quick Start Guide")
    print("=" * 40)

    basic_examples()
    content_examples()
    styling_examples()
    transform_examples()
    chaining_examples()
    utility_examples()
    generate_demo_svg()

    print("=" * 40)
    print("Quick start guide completed!")
    print("Check the generated quick_start.svg file.")


if __name__ == "__main__":
    main()
