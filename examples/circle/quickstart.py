#!/usr/bin/env python3
"""
Circle Component Quick Start Guide

This is a quick start guide for the Circle component, demonstrating the most common features:
1. Basic Creation
2. Appearance Customization
3. Basic Transformations
4. Getting Circle Information
"""

from pysvg.components import Canvas, Circle, CircleConfig
from pysvg.schema import AppearanceConfig, Color


def basic_examples():
    """Basic usage examples"""
    print("=== Basic Usage Examples ===")

    # 1. Create a basic circle
    basic_circle = Circle(config=CircleConfig(r=50))
    print(f"Basic circle: {basic_circle.to_svg_element()}")

    # 2. Circle with specified position
    positioned_circle = Circle(config=CircleConfig(cx=100, cy=100, r=30))
    print(f"Positioned circle: {positioned_circle.to_svg_element()}")
    print()


def styling_examples():
    """Styling examples"""
    print("=== Styling Examples ===")

    # 1. Circle with color and border
    styled_circle = Circle(
        config=CircleConfig(r=40),
        appearance=AppearanceConfig(fill=Color("lightblue"), stroke=Color("navy"), stroke_width=3),
    )
    print(f"Styled circle: {styled_circle.to_svg_element()}")

    # 2. Semi-transparent circle
    transparent_circle = Circle(
        config=CircleConfig(r=35),
        appearance=AppearanceConfig(
            fill=Color("skyblue"), fill_opacity=0.6, stroke=Color("blue"), stroke_width=2
        ),
    )
    print(f"Transparent circle: {transparent_circle.to_svg_element()}")

    # 3. Circle with dashed border
    dashed_circle = Circle(
        config=CircleConfig(r=30),
        appearance=AppearanceConfig(
            fill=Color("lightgreen"), stroke=Color("green"), stroke_width=3, stroke_dasharray=[8, 4]
        ),
    )
    print(f"Dashed circle: {dashed_circle.to_svg_element()}")

    # 4. Outline-only circle (no fill)
    outline_circle = Circle(
        config=CircleConfig(r=25),
        appearance=AppearanceConfig(fill=Color("none"), stroke=Color("red"), stroke_width=2),
    )
    print(f"Outline circle: {outline_circle.to_svg_element()}")
    print()


def transform_examples():
    """Transformation examples"""
    print("=== Transformation Examples ===")

    # 1. Translation
    moved_circle = Circle(
        config=CircleConfig(r=30),
    ).move(80, 60)
    print(f"Translated circle: {moved_circle.to_svg_element()}")

    # 2. Scaling
    scaled_circle = Circle(
        config=CircleConfig(r=20),
    ).scale(2.0)
    print(f"Scaled circle: {scaled_circle.to_svg_element()}")

    # 3. Combined transformations
    combined_circle = (
        Circle(
            config=CircleConfig(r=25),
            appearance=AppearanceConfig(
                fill=Color("orange"), stroke=Color("darkorange"), stroke_width=2
            ),
        )
        .move(100, 50)
        .scale(1.5)
    )
    print(f"Combined transformed circle: {combined_circle.to_svg_element()}")
    print()


def info_examples():
    """Examples of getting circle information"""
    print("=== Circle Information Examples ===")

    circle = Circle(config=CircleConfig(cx=50, cy=60, r=40))

    # 1. Get center point
    center = circle.central_point
    print(f"Circle center point: {center}")

    # 2. Get bounding box
    bbox = circle.get_bounding_box()
    print(f"Circle bounding box (min_x, min_y, max_x, max_y): {bbox}")

    # 3. Get area
    area = circle.get_area()
    print(f"Circle area: {area:.2f}")

    # 4. Get circumference
    circumference = circle.get_circumference()
    print(f"Circle circumference: {circumference:.2f}")
    print()


def generate_demo_svg():
    """Generate demo SVG file"""
    print("=== Generate Demo SVG ===")

    # Create Canvas
    canvas = Canvas(width=600, height=440, viewbox=(80, 80, 520, 360))

    # Create example circles
    circles = [
        # Basic circle
        Circle(
            config=CircleConfig(r=30),
            appearance=AppearanceConfig(
                fill=Color("lightgray"), stroke=Color("black"), stroke_width=2
            ),
        ).move(80, 80),
        # Styled circle
        Circle(
            config=CircleConfig(r=35),
            appearance=AppearanceConfig(
                fill=Color("lightblue"), stroke=Color("navy"), stroke_width=3
            ),
        ).move(200, 80),
        # Gradient effect circle (using semi-transparency)
        Circle(
            config=CircleConfig(r=40),
            appearance=AppearanceConfig(
                fill=Color("coral"), fill_opacity=0.7, stroke=Color("red"), stroke_width=2
            ),
        ).move(350, 80),
        # Large circle
        Circle(
            config=CircleConfig(r=45),
            appearance=AppearanceConfig(
                fill=Color("lightgreen"), stroke=Color("green"), stroke_width=3
            ),
        ).move(500, 80),
        # Dashed circle
        Circle(
            config=CircleConfig(r=30),
            appearance=AppearanceConfig(
                fill=Color("lightpink"),
                stroke=Color("deeppink"),
                stroke_width=3,
                stroke_dasharray=[10, 5],
            ),
        ).move(80, 200),
        # Outline-only circle
        Circle(
            config=CircleConfig(r=35),
            appearance=AppearanceConfig(fill=Color("none"), stroke=Color("purple"), stroke_width=4),
        ).move(200, 200),
        # Scaled circle
        Circle(
            config=CircleConfig(r=20),
            appearance=AppearanceConfig(fill=Color("gold"), stroke=Color("orange"), stroke_width=2),
        )
        .scale(1.8)
        .move(350, 200),
        # Small circle combination
        Circle(
            config=CircleConfig(r=15),
            appearance=AppearanceConfig(
                fill=Color("skyblue"), stroke=Color("blue"), stroke_width=1
            ),
        ).move(480, 180),
        Circle(
            config=CircleConfig(r=15),
            appearance=AppearanceConfig(
                fill=Color("lightcyan"), stroke=Color("teal"), stroke_width=1
            ),
        ).move(520, 180),
        Circle(
            config=CircleConfig(r=15),
            appearance=AppearanceConfig(
                fill=Color("lavender"), stroke=Color("indigo"), stroke_width=1
            ),
        ).move(500, 220),
        # Large semi-transparent circle as background
        Circle(
            config=CircleConfig(r=60),
            appearance=AppearanceConfig(
                fill=Color("yellow"), fill_opacity=0.3, stroke=Color("orange"), stroke_width=1
            ),
        ).move(150, 320),
        # Medium circles
        Circle(
            config=CircleConfig(r=25),
            appearance=AppearanceConfig(
                fill=Color("lightsteelblue"), stroke=Color("steelblue"), stroke_width=2
            ),
        ).move(350, 320),
        Circle(
            config=CircleConfig(r=25),
            appearance=AppearanceConfig(
                fill=Color("mistyrose"), stroke=Color("rosybrown"), stroke_width=2
            ),
        ).move(450, 320),
    ]

    # Add circles to canvas
    for circle in circles:
        canvas.add(circle)

    # Generate SVG file
    canvas.save("quickstart.svg")

    print("Demo file generated: quickstart.svg")


def main():
    """Main function"""
    print("Circle Component Quick Start Guide")
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
