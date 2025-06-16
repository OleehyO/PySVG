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
    SVGConfig,
    SVGContent,
    TextConfig,
    TextContent,
)
from pysvg.schema import Color, SVGCode


def text_examples():
    """Text component examples"""
    print("=== Text Component Examples ===")

    # 1. Basic text
    basic_text = TextContent(config=TextConfig(text="Hello pysvg!", x=100, y=50))
    print(f"Basic text: {basic_text.to_svg_element()}")

    # 2. Custom styled text
    styled_text = TextContent(
        config=TextConfig(
            text="Styled Text",
            x=100,
            y=100,
            font_size=24,
            font_family="Times New Roman",
            color=Color("blue"),
        )
    )
    print(f"Styled text: {styled_text.to_svg_element()}")

    # 3. Alignment examples
    aligned_text = TextContent(
        config=TextConfig(
            text="Right Aligned",
            x=200,
            y=150,
            text_anchor="end",  # Right aligned
            dominant_baseline="hanging",  # Top aligned
        )
    )
    print(f"Aligned text: {aligned_text.to_svg_element()}")
    print()


def image_examples():
    """Image component examples"""
    print("=== Image Component Examples ===")

    # 1. Basic image
    basic_image = ImageContent(
        config=ImageConfig(href="demo.png", x=50, y=50, width=100, height=100)
    )
    print(f"Basic image: {basic_image.to_svg_element()}")

    # 2. Image with adjusted size and position
    positioned_image = ImageContent(
        config=ImageConfig(
            href="demo.png",
            x=200,
            y=50,
            width=150,
            height=100,
            preserveAspectRatio="xMidYMid slice",  # Fill mode
        )
    )
    print(f"Positioned image: {positioned_image.to_svg_element()}")

    # 3. Image with transform
    transformed_image = (
        ImageContent(
            config=ImageConfig(href="demo.png", x=400, y=50, width=100, height=100),
        )
        .rotate(45)
        .scale(0.8)
    )
    print(f"Transformed image: {transformed_image.to_svg_element()}")
    print()


def svg_examples():
    """SVG component examples"""
    print("=== SVG Component Examples ===")

    # 1. Basic SVG content
    basic_svg = SVGContent(
        config=SVGConfig(
            x=50,
            y=50,
            width=100,
            height=100,
            svg_content=SVGCode('<circle cx="50" cy="50" r="40" fill="red"/>'),
        )
    )
    print(f"Basic SVG: {basic_svg.to_svg_element()}")

    # 2. Using existing SVG file
    with open("demo.svg", "r") as f:
        svg_content = f.read()

    file_svg = SVGContent(
        config=SVGConfig(x=200, y=50, width=150, height=150, svg_content=SVGCode(svg_content))
    )
    print(f"File SVG: {file_svg.to_svg_element()}")

    # 3. SVG with transform
    transformed_svg = (
        SVGContent(
            config=SVGConfig(
                x=400,
                y=50,
                width=100,
                height=100,
                svg_content=SVGCode('<rect x="25" y="25" width="50" height="50" fill="blue"/>'),
            ),
        )
        .rotate(30)
        .scale(1.2)
    )
    print(f"Transformed SVG: {transformed_svg.to_svg_element()}")
    print()


def generate_demo_svg():
    """Generate demo SVG file"""
    print("=== Generate Demo SVG ===")

    # Create Canvas
    canvas = Canvas(width=800, height=600)

    # Add title
    title = TextContent(
        config=TextConfig(
            text="Content Components Demo",
            x=400,
            y=50,
            font_size=24,
            font_family="Arial",
            color=Color("darkblue"),
        )
    )
    canvas.add(title)

    # Add text examples
    text_components = [
        TextContent(
            config=TextConfig(
                text="Left aligned", x=100, y=150, text_anchor="start", color=Color("purple")
            )
        ),
        TextContent(
            config=TextConfig(
                text="Center aligned", x=400, y=150, font_size=20, color=Color("green")
            )
        ),
        TextContent(
            config=TextConfig(
                text="Right aligned", x=700, y=150, text_anchor="end", color=Color("red")
            )
        ),
    ]

    # Add image examples
    image_components = [
        ImageContent(config=ImageConfig(href="demo.png", x=100, y=200, width=150, height=150)),
        ImageContent(
            config=ImageConfig(href="demo.png", x=325, y=200, width=150, height=150),
        ).rotate(45),
        ImageContent(
            config=ImageConfig(
                href="demo.svg",
                x=550,
                y=200,
                width=150,
                height=150,
                preserveAspectRatio="xMidYMid slice",
            )
        ),
    ]

    # Add SVG examples
    svg_components = [
        SVGContent(
            config=SVGConfig(
                x=100,
                y=400,
                width=150,
                height=150,
                svg_content=SVGCode(
                    '<circle cx="75" cy="75" r="50" fill="orange" stroke="red" stroke-width="2"/>'
                ),
            )
        ),
        SVGContent(
            config=SVGConfig(
                x=325,
                y=400,
                width=150,
                height=150,
                svg_content=SVGCode(
                    '<rect x="25" y="25" width="100" height="100" fill="lightblue" stroke="blue" stroke-width="2"/>'
                ),
            )
        ),
        SVGContent(
            config=SVGConfig(
                x=550,
                y=400,
                width=150,
                height=150,
                svg_content=SVGCode(
                    '<polygon points="75,25 125,125 25,125" fill="lightgreen" stroke="green" stroke-width="2"/>'
                ),
            )
        ),
    ]

    # Add all components to canvas
    for component in text_components + image_components + svg_components:
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
    svg_examples()
    generate_demo_svg()

    print("=" * 40)
    print("Quick start guide completed!")
    print("Check the generated quickstart.svg file.")


if __name__ == "__main__":
    main()
