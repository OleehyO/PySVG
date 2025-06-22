#!/usr/bin/env python3
"""
Content Components Quick Start Guide

This is a quick start guide for Content components, demonstrating the usage of three content components:
1. Text - Text content
2. Image - Image content
3. SVG - Nested SVG content

Each component showcases basic usage and advanced features.
"""

from pysvg.components import (
    Canvas,
    ImageConfig,
    ImageContent,
    TextConfig,
    TextContent,
)
from pysvg.schema import Color


def text_examples():
    """Text component examples"""
    print("=== Text Component Examples ===")

    # 1. Basic text
    basic_text = TextContent("Hello pysvg!", config=TextConfig(x=100, y=50))
    print(f"Basic text: {basic_text.to_svg_element()}")

    # 2. Custom styled text
    styled_text = TextContent(
        "Styled Text",
        config=TextConfig(
            x=100,
            y=100,
            font_size=24,
            font_family="Times New Roman",
            color=Color("blue"),
        ),
    )
    print(f"Styled text: {styled_text.to_svg_element()}")

    # 3. Alignment examples
    aligned_text = TextContent(
        "Right Aligned",
        config=TextConfig(
            x=200,
            y=150,
            text_anchor="end",  # Right aligned
            dominant_baseline="hanging",  # Top aligned
        ),
    )
    print(f"Aligned text: {aligned_text.to_svg_element()}")
    print()


def image_examples():
    """Image component examples"""
    print("=== Image Component Examples ===")

    # 1. Basic image
    basic_image = ImageContent("demo.png", config=ImageConfig(x=50, y=50, width=100, height=100))
    print(f"Basic image: {basic_image.to_svg_element()}")

    # 2. Image with adjusted size and position
    positioned_image = ImageContent(
        "demo.png",
        config=ImageConfig(
            x=200,
            y=50,
            width=150,
            height=100,
            preserveAspectRatio="xMidYMid slice",  # Fill mode
        ),
    )
    print(f"Positioned image: {positioned_image.to_svg_element()}")

    # 3. Image with transform
    transformed_image = (
        ImageContent(
            "demo.png",
            config=ImageConfig(x=400, y=50, width=100, height=100),
        )
        .rotate(45)
        .scale(0.8)
    )
    print(f"Transformed image: {transformed_image.to_svg_element()}")
    print()


def generate_demo_svg():
    """Generate demo SVG file"""
    print("=== Generate Demo SVG ===")

    # Create Canvas
    canvas = Canvas(width=800, height=300)

    # Add text examples
    text_components = [
        TextContent(
            "Left aligned",
            config=TextConfig(
                x=100,
                y=100,
                font_size=20,
                text_anchor="start",
                color=Color("purple"),
            ),
        ),
        TextContent(
            "Center aligned", config=TextConfig(x=400, y=100, font_size=20, color=Color("green"))
        ),
        TextContent(
            "Right aligned",
            config=TextConfig(
                x=700,
                y=100,
                font_size=20,
                text_anchor="end",
                color=Color("red"),
            ),
        ),
    ]

    # Add image/svg examples
    image_components = [
        ImageContent("demo.png", config=ImageConfig(x=100, y=150, width=150, height=150)),
        ImageContent(
            "demo.png",
            config=ImageConfig(x=325, y=150, width=150, height=150),
        ).rotate(45),
        ImageContent(
            "demo.svg",
            config=ImageConfig(
                x=550,
                y=150,
                width=150,
                height=150,
                preserveAspectRatio="xMidYMid slice",
            ),
        ),
    ]

    # Add all components to canvas
    for component in text_components + image_components:
        canvas.add(component)

    # Generate SVG file
    canvas.save("quickstart.svg")

    print("Demo file generated: quickstart.svg")


def main():
    """Main function"""
    print("Content Components Quick Start Guide")
    print("=" * 40)

    text_examples()
    image_examples()
    generate_demo_svg()

    print("=" * 40)
    print("Quick start guide completed!")
    print("Check the generated quickstart.svg file.")


if __name__ == "__main__":
    main()
