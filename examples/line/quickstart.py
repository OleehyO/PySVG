#!/usr/bin/env python3
"""
Line Component Quick Start Guide

This is a quick start guide for the Line component, demonstrating the most commonly used features:
1. Basic Creation
2. Appearance Customization
3. Basic Transformations
4. Getting Line Information
"""

from pysvg.components import Canvas, Line, LineConfig
from pysvg.schema import AppearanceConfig, Color


def basic_examples():
    """Basic usage examples"""
    print("=== Basic Usage Examples ===")

    # 1. Create basic line
    basic_line = Line(config=LineConfig(x1=0, y1=0, x2=100, y2=50))
    print(f"Basic line: {basic_line.to_svg_element()}")

    # 2. Horizontal line
    horizontal_line = Line(config=LineConfig(x1=10, y1=20, x2=110, y2=20))
    print(f"Horizontal line: {horizontal_line.to_svg_element()}")

    # 3. Vertical line
    vertical_line = Line(config=LineConfig(x1=50, y1=10, x2=50, y2=80))
    print(f"Vertical line: {vertical_line.to_svg_element()}")
    print()


def styling_examples():
    """Styling examples"""
    print("=== Styling Examples ===")

    # 1. Line with color and width
    styled_line = Line(
        config=LineConfig(x1=0, y1=0, x2=100, y2=100),
        appearance=AppearanceConfig(stroke=Color("red"), stroke_width=3),
    )
    print(f"Styled line: {styled_line.to_svg_element()}")

    # 2. Dashed line
    dashed_line = Line(
        config=LineConfig(x1=0, y1=20, x2=120, y2=20),
        appearance=AppearanceConfig(stroke=Color("blue"), stroke_width=2, stroke_dasharray=[10, 5]),
    )
    print(f"Dashed line: {dashed_line.to_svg_element()}")

    # 3. Dotted line
    dotted_line = Line(
        config=LineConfig(x1=0, y1=40, x2=120, y2=40),
        appearance=AppearanceConfig(stroke=Color("green"), stroke_width=2, stroke_dasharray=[2, 3]),
    )
    print(f"Dotted line: {dotted_line.to_svg_element()}")

    # 4. Thick line
    thick_line = Line(
        config=LineConfig(x1=0, y1=60, x2=120, y2=60),
        appearance=AppearanceConfig(stroke=Color("purple"), stroke_width=8, stroke_linecap="round"),
    )
    print(f"Thick line: {thick_line.to_svg_element()}")

    # 5. Transparent line
    transparent_line = Line(
        config=LineConfig(x1=20, y1=80, x2=100, y2=10),
        appearance=AppearanceConfig(stroke=Color("orange"), stroke_width=4, stroke_opacity=0.6),
    )
    print(f"Transparent line: {transparent_line.to_svg_element()}")
    print()


def transform_examples():
    """Transformation examples"""
    print("=== Transformation Examples ===")

    # 1. Translation
    moved_line = Line(
        config=LineConfig(x1=0, y1=0, x2=60, y2=40),
    ).move(50, 30)
    print(f"Translated line: {moved_line.to_svg_element()}")

    # 2. Rotation
    rotated_line = Line(
        config=LineConfig(x1=0, y1=0, x2=80, y2=0),
    ).rotate(45)
    print(f"Rotated line: {rotated_line.to_svg_element()}")

    # 3. Scaling
    scaled_line = Line(
        config=LineConfig(x1=0, y1=0, x2=50, y2=30),
    ).scale(1.5)
    print(f"Scaled line: {scaled_line.to_svg_element()}")

    # 4. Combined transformations
    combined_line = (
        Line(
            config=LineConfig(x1=0, y1=0, x2=60, y2=0),
            appearance=AppearanceConfig(stroke=Color("red"), stroke_width=3),
        )
        .rotate(30)
        .move(100, 50)
    )
    print(f"Combined transformed line: {combined_line.to_svg_element()}")
    print()


def info_examples():
    """Line information examples"""
    print("=== Line Information Examples ===")

    line = Line(config=LineConfig(x1=10, y1=20, x2=110, y2=80))

    # 1. Get center point (midpoint)
    center = line.central_point
    print(f"Line center point: {center}")

    # 2. Get bounding box
    bbox = line.get_bounding_box()
    print(f"Line bounding box (min_x, min_y, max_x, max_y): {bbox}")

    # 3. Get length
    length = line.get_length()
    print(f"Line length: {length:.2f}")

    # 4. Get slope
    slope = line.get_slope()
    print(f"Line slope: {slope}")

    # 5. Get angle
    angle = line.get_angle()
    print(f"Line angle: {angle:.2f}°")

    # 6. Vertical line slope
    vertical_line = Line(config=LineConfig(x1=50, y1=10, x2=50, y2=80))
    vertical_slope = vertical_line.get_slope()
    print(f"Vertical line slope: {vertical_slope}")
    print()


def generate_demo_svg():
    """Generate demo SVG file"""
    print("=== Generate Demo SVG ===")

    # Create Canvas
    canvas = Canvas(width=600, height=400)

    # Create example lines
    lines = [
        # Basic line combination - Create grid effect
        # Horizontal lines
        Line(
            config=LineConfig(x1=50, y1=50, x2=550, y2=50),
            appearance=AppearanceConfig(stroke=Color("lightgray"), stroke_width=1),
        ),
        Line(
            config=LineConfig(x1=50, y1=100, x2=550, y2=100),
            appearance=AppearanceConfig(stroke=Color("lightgray"), stroke_width=1),
        ),
        Line(
            config=LineConfig(x1=50, y1=150, x2=550, y2=150),
            appearance=AppearanceConfig(stroke=Color("lightgray"), stroke_width=1),
        ),
        Line(
            config=LineConfig(x1=50, y1=200, x2=550, y2=200),
            appearance=AppearanceConfig(stroke=Color("lightgray"), stroke_width=1),
        ),
        Line(
            config=LineConfig(x1=50, y1=250, x2=550, y2=250),
            appearance=AppearanceConfig(stroke=Color("lightgray"), stroke_width=1),
        ),
        # Vertical lines
        Line(
            config=LineConfig(x1=100, y1=30, x2=100, y2=270),
            appearance=AppearanceConfig(stroke=Color("lightgray"), stroke_width=1),
        ),
        Line(
            config=LineConfig(x1=200, y1=30, x2=200, y2=270),
            appearance=AppearanceConfig(stroke=Color("lightgray"), stroke_width=1),
        ),
        Line(
            config=LineConfig(x1=300, y1=30, x2=300, y2=270),
            appearance=AppearanceConfig(stroke=Color("lightgray"), stroke_width=1),
        ),
        Line(
            config=LineConfig(x1=400, y1=30, x2=400, y2=270),
            appearance=AppearanceConfig(stroke=Color("lightgray"), stroke_width=1),
        ),
        Line(
            config=LineConfig(x1=500, y1=30, x2=500, y2=270),
            appearance=AppearanceConfig(stroke=Color("lightgray"), stroke_width=1),
        ),
        # Decorative lines
        # Diagonal lines
        Line(
            config=LineConfig(x1=80, y1=80, x2=180, y2=180),
            appearance=AppearanceConfig(stroke=Color("red"), stroke_width=3),
        ),
        Line(
            config=LineConfig(x1=180, y1=80, x2=80, y2=180),
            appearance=AppearanceConfig(stroke=Color("blue"), stroke_width=3),
        ),
        # Dashed line
        Line(
            config=LineConfig(x1=220, y1=80, x2=380, y2=120),
            appearance=AppearanceConfig(
                stroke=Color("green"), stroke_width=4, stroke_dasharray=[15, 8]
            ),
        ),
        # Dotted line
        Line(
            config=LineConfig(x1=220, y1=140, x2=380, y2=180),
            appearance=AppearanceConfig(
                stroke=Color("purple"), stroke_width=3, stroke_dasharray=[3, 5]
            ),
        ),
        # Thick line
        Line(
            config=LineConfig(x1=420, y1=80, x2=520, y2=180),
            appearance=AppearanceConfig(
                stroke=Color("orange"), stroke_width=8, stroke_linecap="round"
            ),
        ),
        # Transparent line
        Line(
            config=LineConfig(x1=520, y1=80, x2=420, y2=180),
            appearance=AppearanceConfig(stroke=Color("cyan"), stroke_width=6, stroke_opacity=0.6),
        ),
        # Create arrow effect (using multiple lines)
        # Arrow body
        Line(
            config=LineConfig(x1=100, y1=320, x2=200, y2=320),
            appearance=AppearanceConfig(stroke=Color("darkred"), stroke_width=4),
        ),
        # Arrow head
        Line(
            config=LineConfig(x1=200, y1=320, x2=185, y2=310),
            appearance=AppearanceConfig(stroke=Color("darkred"), stroke_width=4),
        ),
        Line(
            config=LineConfig(x1=200, y1=320, x2=185, y2=330),
            appearance=AppearanceConfig(stroke=Color("darkred"), stroke_width=4),
        ),
        # Wave line effect (using multiple short lines)
        Line(
            config=LineConfig(x1=250, y1=320, x2=270, y2=310),
            appearance=AppearanceConfig(stroke=Color("navy"), stroke_width=3),
        ),
        Line(
            config=LineConfig(x1=270, y1=310, x2=290, y2=330),
            appearance=AppearanceConfig(stroke=Color("navy"), stroke_width=3),
        ),
        Line(
            config=LineConfig(x1=290, y1=330, x2=310, y2=310),
            appearance=AppearanceConfig(stroke=Color("navy"), stroke_width=3),
        ),
        Line(
            config=LineConfig(x1=310, y1=310, x2=330, y2=330),
            appearance=AppearanceConfig(stroke=Color("navy"), stroke_width=3),
        ),
        Line(
            config=LineConfig(x1=330, y1=330, x2=350, y2=320),
            appearance=AppearanceConfig(stroke=Color("navy"), stroke_width=3),
        ),
        # Rotated line examples
        Line(
            config=LineConfig(x1=0, y1=0, x2=80, y2=0),
            appearance=AppearanceConfig(stroke=Color("gold"), stroke_width=3),
        )
        .rotate(15)
        .move(450, 320),
        Line(
            config=LineConfig(x1=0, y1=0, x2=80, y2=0),
            appearance=AppearanceConfig(stroke=Color("gold"), stroke_width=3),
        )
        .rotate(45)
        .move(450, 320),
        Line(
            config=LineConfig(x1=0, y1=0, x2=80, y2=0),
            appearance=AppearanceConfig(stroke=Color("gold"), stroke_width=3),
        )
        .rotate(75)
        .move(450, 320),
    ]

    # Add lines to canvas
    for line in lines:
        canvas.add(line)

    # Generate SVG file
    canvas.save("quickstart.svg")

    print("Demo file generated: quickstart.svg")


def main():
    """Main function"""
    print("Line Component Quick Start Guide")
    print("=" * 40)

    basic_examples()
    styling_examples()
    transform_examples()
    info_examples()
    generate_demo_svg()

    print("=" * 40)
    print("Quick Start Guide completed!")
    print("Check the generated quickstart.svg file.")


if __name__ == "__main__":
    main()
