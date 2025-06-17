#!/usr/bin/env python3
"""
Rectangle Component Quick Start Guide

This is a quick start guide for the Rectangle component, demonstrating the most common features:
1. Basic Creation
2. Appearance Customization
3. Basic Transformations
4. Rounded Rectangles
5. Getting Rectangle Information
"""

from pysvg.components import Canvas, Rectangle, RectangleConfig
from pysvg.schema import AppearanceConfig, Color


def basic_examples():
    """Basic usage examples"""
    print("=== Basic Usage Examples ===")

    # 1. Create a basic rectangle
    basic_rect = Rectangle(config=RectangleConfig(width=100, height=50))
    print(f"Basic rectangle: {basic_rect.to_svg_element()}")

    # 2. Rectangle with specified position
    positioned_rect = Rectangle(config=RectangleConfig(x=10, y=20, width=100, height=50))
    print(f"Positioned rectangle: {positioned_rect.to_svg_element()}")
    print()


def styling_examples():
    """Styling examples"""
    print("=== Styling Examples ===")

    # 1. Rectangle with color and border
    styled_rect = Rectangle(
        config=RectangleConfig(width=100, height=50),
        appearance=AppearanceConfig(fill=Color("lightblue"), stroke=Color("navy"), stroke_width=2),
    )
    print(f"Styled rectangle: {styled_rect.to_svg_element()}")

    # 2. Semi-transparent rectangle
    transparent_rect = Rectangle(
        config=RectangleConfig(width=100, height=50),
        appearance=AppearanceConfig(
            fill=Color("skyblue"), fill_opacity=0.5, stroke=Color("blue"), stroke_width=2
        ),
    )
    print(f"Transparent rectangle: {transparent_rect.to_svg_element()}")

    # 3. Rectangle with dashed border
    dashed_rect = Rectangle(
        config=RectangleConfig(width=100, height=50),
        appearance=AppearanceConfig(
            fill=Color("lightgreen"), stroke=Color("green"), stroke_width=2, stroke_dasharray=[5, 3]
        ),
    )
    print(f"Dashed rectangle: {dashed_rect.to_svg_element()}")
    print()


def transform_examples():
    """Transformation examples"""
    print("=== Transformation Examples ===")

    # 1. Translation
    moved_rect = Rectangle(
        config=RectangleConfig(width=80, height=40),
    ).move(50, 30)
    print(f"Translated rectangle: {moved_rect.to_svg_element()}")

    # 2. Rotation
    rotated_rect = Rectangle(
        config=RectangleConfig(width=80, height=40),
    ).rotate(45)
    print(f"Rotated rectangle: {rotated_rect.to_svg_element()}")

    # 3. Scaling
    scaled_rect = Rectangle(
        config=RectangleConfig(width=80, height=40),
    ).scale(1.5)
    print(f"Scaled rectangle: {scaled_rect.to_svg_element()}")
    print()


def rounded_corner_examples():
    """Rounded rectangle examples"""
    print("=== Rounded Rectangle Examples ===")

    # 1. Uniform rounded corners
    rounded_rect = Rectangle(
        config=RectangleConfig(width=100, height=50, rx=10, ry=10),
        appearance=AppearanceConfig(fill=Color("coral"), stroke=Color("darkred"), stroke_width=2),
    )
    print(f"Rounded rectangle: {rounded_rect.to_svg_element()}")

    # 2. Different horizontal and vertical corner radii
    custom_rounded_rect = Rectangle(
        config=RectangleConfig(width=100, height=50, rx=20, ry=10),
        appearance=AppearanceConfig(
            fill=Color("lightpink"), stroke=Color("deeppink"), stroke_width=2
        ),
    )
    print(f"Custom rounded rectangle: {custom_rounded_rect.to_svg_element()}")
    print()


def info_examples():
    """Rectangle information examples"""
    print("=== Rectangle Information Examples ===")

    rect = Rectangle(config=RectangleConfig(x=10, y=20, width=100, height=50))

    # 1. Get center point
    center = rect.central_point
    print(f"Rectangle center point: {center}")

    # 2. Get bounding box
    bbox = rect.get_bounding_box()
    print(f"Rectangle bounding box (min_x, min_y, max_x, max_y): {bbox}")

    # 3. Check for rounded corners
    has_rounded = rect.has_rounded_corners()
    print(f"Has rounded corners: {has_rounded}")
    print()


def generate_demo_svg():
    """Generate demo SVG file"""
    print("=== Generate Demo SVG ===")

    # Create Canvas
    canvas = Canvas(width=460, height=230)

    # Create example rectangles
    rectangles = [
        # Basic rectangle
        Rectangle(
            config=RectangleConfig(width=100, height=50),
            appearance=AppearanceConfig(
                fill=Color("lightgray"), stroke=Color("black"), stroke_width=2
            ),
        ).move(50, 50),
        # Styled rectangle
        Rectangle(
            config=RectangleConfig(width=100, height=50),
            appearance=AppearanceConfig(
                fill=Color("lightblue"), stroke=Color("navy"), stroke_width=2
            ),
        ).move(200, 50),
        # Rounded rectangle
        Rectangle(
            config=RectangleConfig(width=100, height=50, rx=15, ry=15),
            appearance=AppearanceConfig(
                fill=Color("lightgreen"), stroke=Color("green"), stroke_width=2
            ),
        ).move(350, 50),
        # Semi-transparent rectangle
        Rectangle(
            config=RectangleConfig(width=100, height=50),
            appearance=AppearanceConfig(
                fill=Color("coral"), fill_opacity=0.5, stroke=Color("red"), stroke_width=2
            ),
        ).move(50, 150),
        # Rotated rectangle
        Rectangle(
            config=RectangleConfig(width=100, height=50),
            appearance=AppearanceConfig(
                fill=Color("lightpink"), stroke=Color("deeppink"), stroke_width=2
            ),
        )
        .rotate(30)
        .move(200, 150),
        # Dashed rectangle
        Rectangle(
            config=RectangleConfig(width=100, height=50),
            appearance=AppearanceConfig(
                fill=Color("lavender"),
                stroke=Color("purple"),
                stroke_width=2,
                stroke_dasharray=[5, 3],
            ),
        ).move(350, 150),
    ]

    # Add rectangles to canvas
    for rect in rectangles:
        canvas.add(rect)

    # Generate SVG file
    canvas.save("quickstart.svg")

    print("Demo file generated: quickstart.svg")


def main():
    """Main function"""
    print("Rectangle Component Quick Start Guide")
    print("=" * 40)

    basic_examples()
    styling_examples()
    transform_examples()
    rounded_corner_examples()
    info_examples()
    generate_demo_svg()

    print("=" * 40)
    print("Quick Start Guide completed!")
    print("Check the generated quickstart.svg file.")


if __name__ == "__main__":
    main()
