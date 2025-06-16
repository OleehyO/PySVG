#!/usr/bin/env python3
"""
Ellipse Component Quick Start Guide

This is a quick start guide for the Ellipse component, demonstrating the most common features:
1. Basic Creation
2. Appearance Customization
3. Basic Transformations
4. Getting Ellipse Information
"""

from pysvg.components import Canvas, Ellipse, EllipseConfig
from pysvg.schema import AppearanceConfig, Color


def basic_examples():
    """Basic usage examples"""
    print("=== Basic Usage Examples ===")

    # 1. Create basic ellipse
    basic_ellipse = Ellipse(config=EllipseConfig(rx=60, ry=40))
    print(f"Basic ellipse: {basic_ellipse.to_svg_element()}")

    # 2. Positioned ellipse
    positioned_ellipse = Ellipse(config=EllipseConfig(cx=100, cy=80, rx=50, ry=30))
    print(f"Positioned ellipse: {positioned_ellipse.to_svg_element()}")

    # 3. Circle (rx == ry)
    circle_ellipse = Ellipse(config=EllipseConfig(cx=50, cy=50, rx=40, ry=40))
    print(f"Circle ellipse: {circle_ellipse.to_svg_element()}")
    print()


def styling_examples():
    """Styling examples"""
    print("=== Styling Examples ===")

    # 1. Ellipse with color and border
    styled_ellipse = Ellipse(
        config=EllipseConfig(rx=50, ry=30),
        appearance=AppearanceConfig(fill=Color("lightblue"), stroke=Color("navy"), stroke_width=3),
    )
    print(f"Styled ellipse: {styled_ellipse.to_svg_element()}")

    # 2. Semi-transparent ellipse
    transparent_ellipse = Ellipse(
        config=EllipseConfig(rx=45, ry=25),
        appearance=AppearanceConfig(
            fill=Color("skyblue"), fill_opacity=0.6, stroke=Color("blue"), stroke_width=2
        ),
    )
    print(f"Transparent ellipse: {transparent_ellipse.to_svg_element()}")

    # 3. Dashed border ellipse
    dashed_ellipse = Ellipse(
        config=EllipseConfig(rx=40, ry=20),
        appearance=AppearanceConfig(
            fill=Color("lightgreen"), stroke=Color("green"), stroke_width=3, stroke_dasharray=[8, 4]
        ),
    )
    print(f"Dashed ellipse: {dashed_ellipse.to_svg_element()}")

    # 4. Outline only ellipse (no fill)
    outline_ellipse = Ellipse(
        config=EllipseConfig(rx=35, ry=15),
        appearance=AppearanceConfig(fill=Color("none"), stroke=Color("red"), stroke_width=2),
    )
    print(f"Outline ellipse: {outline_ellipse.to_svg_element()}")

    # 5. Vertical ellipse (ry > rx)
    vertical_ellipse = Ellipse(
        config=EllipseConfig(rx=20, ry=50),
        appearance=AppearanceConfig(fill=Color("lavender"), stroke=Color("purple"), stroke_width=2),
    )
    print(f"Vertical ellipse: {vertical_ellipse.to_svg_element()}")
    print()


def transform_examples():
    """Transformation examples"""
    print("=== Transform Examples ===")

    # 1. Translation
    moved_ellipse = Ellipse(
        config=EllipseConfig(rx=40, ry=25),
    ).move(80, 60)
    print(f"Translated ellipse: {moved_ellipse.to_svg_element()}")

    # 2. Rotation
    rotated_ellipse = Ellipse(
        config=EllipseConfig(rx=50, ry=20),
    ).rotate(45)
    print(f"Rotated ellipse: {rotated_ellipse.to_svg_element()}")

    # 3. Scaling
    scaled_ellipse = Ellipse(
        config=EllipseConfig(rx=30, ry=15),
    ).scale(1.5)
    print(f"Scaled ellipse: {scaled_ellipse.to_svg_element()}")

    # 4. Non-uniform scaling
    non_uniform_scaled = Ellipse(
        config=EllipseConfig(rx=25, ry=25),
    ).scale((2.0, 0.8))
    print(f"Non-uniform scaled ellipse: {non_uniform_scaled.to_svg_element()}")

    # 5. Combined transformations
    combined_ellipse = (
        Ellipse(
            config=EllipseConfig(rx=30, ry=20),
            appearance=AppearanceConfig(
                fill=Color("orange"), stroke=Color("darkorange"), stroke_width=2
            ),
        )
        .rotate(30)
        .move(100, 50)
        .scale(1.2)
    )
    print(f"Combined transformed ellipse: {combined_ellipse.to_svg_element()}")
    print()


def info_examples():
    """Examples of getting ellipse information"""
    print("=== Ellipse Information Examples ===")

    ellipse = Ellipse(config=EllipseConfig(cx=50, cy=60, rx=40, ry=25))

    # 1. Get center point
    center = ellipse.central_point
    print(f"Ellipse center point: {center}")

    # 2. Get bounding box
    bbox = ellipse.get_bounding_box()
    print(f"Ellipse bounding box (min_x, min_y, max_x, max_y): {bbox}")

    # 3. Get area
    area = ellipse.get_area()
    print(f"Ellipse area: {area:.2f}")

    # 4. Get circumference (approximate)
    circumference = ellipse.get_circumference()
    print(f"Ellipse circumference (approximate): {circumference:.2f}")

    # 5. Check if circle
    is_circle = ellipse.is_circle()
    print(f"Is circle: {is_circle}")

    # 6. Get eccentricity
    eccentricity = ellipse.get_eccentricity()
    print(f"Ellipse eccentricity: {eccentricity:.3f}")

    # 7. Circle information
    circle_ellipse = Ellipse(config=EllipseConfig(cx=0, cy=0, rx=30, ry=30))
    print(f"Circle ellipse is circle: {circle_ellipse.is_circle()}")
    print(f"Circle ellipse eccentricity: {circle_ellipse.get_eccentricity():.3f}")
    print()


def generate_demo_svg():
    """Generate demo SVG file"""
    print("=== Generate Demo SVG ===")

    # Create Canvas
    canvas = Canvas(width=770, height=470, viewbox=[0, 0, 700, 450])

    # Create example ellipses
    ellipses = [
        # Basic ellipse
        Ellipse(
            config=EllipseConfig(rx=40, ry=25),
            appearance=AppearanceConfig(
                fill=Color("lightgray"), stroke=Color("black"), stroke_width=2
            ),
        ).move(80, 80),
        # Styled ellipse
        Ellipse(
            config=EllipseConfig(rx=45, ry=30),
            appearance=AppearanceConfig(
                fill=Color("lightblue"), stroke=Color("navy"), stroke_width=3
            ),
        ).move(200, 80),
        # Vertical ellipse
        Ellipse(
            config=EllipseConfig(rx=25, ry=50),
            appearance=AppearanceConfig(
                fill=Color("lightgreen"), stroke=Color("green"), stroke_width=2
            ),
        ).move(350, 80),
        # Circle (special case of ellipse)
        Ellipse(
            config=EllipseConfig(rx=35, ry=35),
            appearance=AppearanceConfig(
                fill=Color("lightcoral"), stroke=Color("red"), stroke_width=2
            ),
        ).move(480, 80),
        # Very flat ellipse
        Ellipse(
            config=EllipseConfig(rx=60, ry=15),
            appearance=AppearanceConfig(
                fill=Color("lightyellow"), stroke=Color("orange"), stroke_width=2
            ),
        ).move(600, 80),
        # Semi-transparent ellipse
        Ellipse(
            config=EllipseConfig(rx=50, ry=35),
            appearance=AppearanceConfig(
                fill=Color("lightpink"), fill_opacity=0.6, stroke=Color("deeppink"), stroke_width=2
            ),
        ).move(80, 200),
        # Dashed ellipse
        Ellipse(
            config=EllipseConfig(rx=45, ry=25),
            appearance=AppearanceConfig(
                fill=Color("lavender"),
                stroke=Color("purple"),
                stroke_width=3,
                stroke_dasharray=[12, 6],
            ),
        ).move(200, 200),
        # Outline only ellipse
        Ellipse(
            config=EllipseConfig(rx=40, ry=30),
            appearance=AppearanceConfig(fill=Color("none"), stroke=Color("teal"), stroke_width=4),
        ).move(350, 200),
        # Rotated ellipse
        Ellipse(
            config=EllipseConfig(rx=50, ry=20),
            appearance=AppearanceConfig(
                fill=Color("gold"), stroke=Color("darkorange"), stroke_width=2
            ),
        )
        .rotate(45)
        .move(480, 200),
        # Scaled ellipse
        Ellipse(
            config=EllipseConfig(rx=25, ry=25),
            appearance=AppearanceConfig(
                fill=Color("lightsteelblue"), stroke=Color("steelblue"), stroke_width=2
            ),
        )
        .scale((2.0, 1.2))
        .move(500, 200),
        # Create petal effect (multiple rotated ellipses)
        Ellipse(
            config=EllipseConfig(rx=60, ry=15),
            appearance=AppearanceConfig(
                fill=Color("pink"), fill_opacity=0.7, stroke=Color("hotpink"), stroke_width=1
            ),
        )
        .rotate(0)
        .move(150, 350),
        Ellipse(
            config=EllipseConfig(rx=60, ry=15),
            appearance=AppearanceConfig(
                fill=Color("pink"), fill_opacity=0.7, stroke=Color("hotpink"), stroke_width=1
            ),
        )
        .rotate(30)
        .move(150, 350),
        Ellipse(
            config=EllipseConfig(rx=60, ry=15),
            appearance=AppearanceConfig(
                fill=Color("pink"), fill_opacity=0.7, stroke=Color("hotpink"), stroke_width=1
            ),
        )
        .rotate(60)
        .move(150, 350),
        Ellipse(
            config=EllipseConfig(rx=60, ry=15),
            appearance=AppearanceConfig(
                fill=Color("pink"), fill_opacity=0.7, stroke=Color("hotpink"), stroke_width=1
            ),
        )
        .rotate(90)
        .move(150, 350),
        Ellipse(
            config=EllipseConfig(rx=60, ry=15),
            appearance=AppearanceConfig(
                fill=Color("pink"), fill_opacity=0.7, stroke=Color("hotpink"), stroke_width=1
            ),
        )
        .rotate(120)
        .move(150, 350),
        Ellipse(
            config=EllipseConfig(rx=60, ry=15),
            appearance=AppearanceConfig(
                fill=Color("pink"), fill_opacity=0.7, stroke=Color("hotpink"), stroke_width=1
            ),
        )
        .rotate(150)
        .move(150, 350),
        # Center circle
        Ellipse(
            config=EllipseConfig(rx=15, ry=15),
            appearance=AppearanceConfig(
                fill=Color("yellow"), stroke=Color("orange"), stroke_width=2
            ),
        ).move(150, 350),
        # Concentric ellipses
        Ellipse(
            config=EllipseConfig(rx=80, ry=50),
            appearance=AppearanceConfig(
                fill=Color("lightcyan"), stroke=Color("cyan"), stroke_width=2
            ),
        ).move(400, 350),
        Ellipse(
            config=EllipseConfig(rx=60, ry=37),
            appearance=AppearanceConfig(
                fill=Color("lightblue"), stroke=Color("blue"), stroke_width=2
            ),
        ).move(400, 350),
        Ellipse(
            config=EllipseConfig(rx=40, ry=25),
            appearance=AppearanceConfig(
                fill=Color("lightsteelblue"), stroke=Color("steelblue"), stroke_width=2
            ),
        ).move(400, 350),
        Ellipse(
            config=EllipseConfig(rx=20, ry=12),
            appearance=AppearanceConfig(fill=Color("white"), stroke=Color("navy"), stroke_width=1),
        ).move(400, 350),
        # Ellipse chain
        Ellipse(
            config=EllipseConfig(rx=30, ry=15),
            appearance=AppearanceConfig(
                fill=Color("lightseagreen"), stroke=Color("seagreen"), stroke_width=2
            ),
        ).move(550, 320),
        Ellipse(
            config=EllipseConfig(rx=30, ry=15),
            appearance=AppearanceConfig(
                fill=Color("lightseagreen"), stroke=Color("seagreen"), stroke_width=2
            ),
        ).move(600, 350),
        Ellipse(
            config=EllipseConfig(rx=30, ry=15),
            appearance=AppearanceConfig(
                fill=Color("lightseagreen"), stroke=Color("seagreen"), stroke_width=2
            ),
        ).move(550, 380),
        Ellipse(
            config=EllipseConfig(rx=30, ry=15),
            appearance=AppearanceConfig(
                fill=Color("lightseagreen"), stroke=Color("seagreen"), stroke_width=2
            ),
        ).move(500, 350),
    ]

    # Add ellipses to canvas
    for ellipse in ellipses:
        canvas.add(ellipse)

    # Generate SVG file
    canvas.save("quickstart.svg")

    print("Demo file generated: quickstart.svg")


def main():
    """Main function"""
    print("Ellipse Component Quick Start Guide")
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
