#!/usr/bin/env python3
"""
PyFVG Demo: Drawing a Cute House Scene

This example demonstrates the basic usage of the pysvg package, including:
1. Canvas creation
2. Rectangle components (house body, door, windows)
3. Circle components (sun, decorations)
4. Polyline components (roof, cloud outlines)
5. Color and style configuration
6. Component position transformation
"""

from pysvg.components import Canvas, Rectangle, Circle, Polyline
from pysvg.components import RectangleConfig, CircleConfig, PolylineConfig
from pysvg.schema import AppearanceConfig, Color


def create_house_scene():
    """Create a house scene"""
    print("🏠 Starting to draw a cute house scene...")

    # Create an 800x600 canvas with light blue sky background
    canvas = Canvas(width=800, height=600)

    # === Sky and Sun ===
    print("☀️ Drawing the sun...")
    # Draw the sun
    sun = Circle(
        config=CircleConfig(r=40),
        appearance=AppearanceConfig(fill=Color("gold"), stroke=Color("orange"), stroke_width=3),
    ).move(650, 100)
    canvas.add(sun)

    # Light of sun
    sun_rays = [
        Polyline(
            config=PolylineConfig(points=[(620, 60), (610, 50)]),
            appearance=AppearanceConfig(stroke=Color("orange"), stroke_width=2),
        ),
        Polyline(
            config=PolylineConfig(points=[(680, 60), (690, 50)]),
            appearance=AppearanceConfig(stroke=Color("orange"), stroke_width=2),
        ),
        Polyline(
            config=PolylineConfig(points=[(700, 100), (720, 100)]),
            appearance=AppearanceConfig(stroke=Color("orange"), stroke_width=2),
        ),
        Polyline(
            config=PolylineConfig(points=[(680, 140), (690, 150)]),
            appearance=AppearanceConfig(stroke=Color("orange"), stroke_width=2),
        ),
        Polyline(
            config=PolylineConfig(points=[(620, 140), (610, 150)]),
            appearance=AppearanceConfig(stroke=Color("orange"), stroke_width=2),
        ),
        Polyline(
            config=PolylineConfig(points=[(600, 100), (580, 100)]),
            appearance=AppearanceConfig(stroke=Color("orange"), stroke_width=2),
        ),
    ]

    for ray in sun_rays:
        canvas.add(ray)

    # === Clouds ===
    print("☁️ Drawing clouds...")
    # Create clouds (multiple overlapping circles)
    cloud1_circles = [
        Circle(
            config=CircleConfig(r=25),
            appearance=AppearanceConfig(
                fill=Color("white"), stroke=Color("lightgray"), stroke_width=1
            ),
        ).move(150, 120),
        Circle(
            config=CircleConfig(r=30),
            appearance=AppearanceConfig(
                fill=Color("white"), stroke=Color("lightgray"), stroke_width=1
            ),
        ).move(180, 110),
        Circle(
            config=CircleConfig(r=20),
            appearance=AppearanceConfig(
                fill=Color("white"), stroke=Color("lightgray"), stroke_width=1
            ),
        ).move(200, 125),
        Circle(
            config=CircleConfig(r=22),
            appearance=AppearanceConfig(
                fill=Color("white"), stroke=Color("lightgray"), stroke_width=1
            ),
        ).move(125, 130),
    ]

    for cloud_circle in cloud1_circles:
        canvas.add(cloud_circle)

    # Second cloud
    cloud2_circles = [
        Circle(
            config=CircleConfig(r=20),
            appearance=AppearanceConfig(
                fill=Color("white"), stroke=Color("lightgray"), stroke_width=1
            ),
        ).move(450, 80),
        Circle(
            config=CircleConfig(r=25),
            appearance=AppearanceConfig(
                fill=Color("white"), stroke=Color("lightgray"), stroke_width=1
            ),
        ).move(470, 75),
        Circle(
            config=CircleConfig(r=18),
            appearance=AppearanceConfig(
                fill=Color("white"), stroke=Color("lightgray"), stroke_width=1
            ),
        ).move(490, 85),
    ]

    for cloud_circle in cloud2_circles:
        canvas.add(cloud_circle)

    # === Ground ===
    print("🌱 Drawing the ground...")
    ground = Rectangle(
        config=RectangleConfig(x=0, y=450, width=800, height=150),
        appearance=AppearanceConfig(fill=Color("lightgreen"), stroke=Color("none")),
    )
    canvas.add(ground)

    # === House Body ===
    print("🏠 Drawing house body...")
    # House walls
    house_body = Rectangle(
        config=RectangleConfig(x=250, y=250, width=200, height=200),
        appearance=AppearanceConfig(
            fill=Color("lightblue"), stroke=Color("darkblue"), stroke_width=3
        ),
    )
    canvas.add(house_body)

    # === Roof ===
    print("🔺 Drawing the roof...")
    roof = Polyline(
        config=PolylineConfig(
            points=[
                (230, 250),  # Left bottom corner
                (350, 180),  # Roof top point
                (470, 250),  # Right bottom corner
                (230, 250),  # Back to start to form a closed shape
            ]
        ),
        appearance=AppearanceConfig(fill=Color("darkred"), stroke=Color("maroon"), stroke_width=2),
    )
    canvas.add(roof)

    # === Door ===
    print("🚪 Drawing the door...")
    door = Rectangle(
        config=RectangleConfig(x=320, y=350, width=60, height=100),
        appearance=AppearanceConfig(
            fill=Color("brown"), stroke=Color("saddlebrown"), stroke_width=2
        ),
    )
    canvas.add(door)

    # Door handle
    door_handle = Circle(
        config=CircleConfig(r=3),
        appearance=AppearanceConfig(fill=Color("gold"), stroke=Color("orange"), stroke_width=1),
    ).move(365, 400)
    canvas.add(door_handle)

    # === Windows ===
    print("🪟 Drawing windows...")
    # Left window
    left_window = Rectangle(
        config=RectangleConfig(x=270, y=290, width=40, height=40),
        appearance=AppearanceConfig(
            fill=Color("lightcyan"), stroke=Color("darkblue"), stroke_width=2
        ),
    )
    canvas.add(left_window)

    # Left window cross
    left_window_cross_h = Rectangle(
        config=RectangleConfig(x=270, y=308, width=40, height=4),
        appearance=AppearanceConfig(fill=Color("darkblue"), stroke=Color("none")),
    )
    canvas.add(left_window_cross_h)

    left_window_cross_v = Rectangle(
        config=RectangleConfig(x=288, y=290, width=4, height=40),
        appearance=AppearanceConfig(fill=Color("darkblue"), stroke=Color("none")),
    )
    canvas.add(left_window_cross_v)

    # Right window
    right_window = Rectangle(
        config=RectangleConfig(x=390, y=290, width=40, height=40),
        appearance=AppearanceConfig(
            fill=Color("lightcyan"), stroke=Color("darkblue"), stroke_width=2
        ),
    )
    canvas.add(right_window)

    # Right window cross
    right_window_cross_h = Rectangle(
        config=RectangleConfig(x=390, y=308, width=40, height=4),
        appearance=AppearanceConfig(fill=Color("darkblue"), stroke=Color("none")),
    )
    canvas.add(right_window_cross_h)

    right_window_cross_v = Rectangle(
        config=RectangleConfig(x=408, y=290, width=4, height=40),
        appearance=AppearanceConfig(fill=Color("darkblue"), stroke=Color("none")),
    )
    canvas.add(right_window_cross_v)

    # === Decorative Flowers ===
    print("🌸 Drawing decorative flowers...")
    # Flower 1 (Left side)
    flower1_center = Circle(
        config=CircleConfig(r=8),
        appearance=AppearanceConfig(fill=Color("yellow"), stroke=Color("orange"), stroke_width=1),
    ).move(150, 420)
    canvas.add(flower1_center)

    # Petals
    flower1_petals = [
        Circle(
            config=CircleConfig(r=6),
            appearance=AppearanceConfig(
                fill=Color("pink"), stroke=Color("deeppink"), stroke_width=1
            ),
        ).move(135, 415),
        Circle(
            config=CircleConfig(r=6),
            appearance=AppearanceConfig(
                fill=Color("pink"), stroke=Color("deeppink"), stroke_width=1
            ),
        ).move(165, 415),
        Circle(
            config=CircleConfig(r=6),
            appearance=AppearanceConfig(
                fill=Color("pink"), stroke=Color("deeppink"), stroke_width=1
            ),
        ).move(150, 405),
        Circle(
            config=CircleConfig(r=6),
            appearance=AppearanceConfig(
                fill=Color("pink"), stroke=Color("deeppink"), stroke_width=1
            ),
        ).move(150, 435),
    ]

    for petal in flower1_petals:
        canvas.add(petal)

    # Flower 2 (Right side)
    flower2_center = Circle(
        config=CircleConfig(r=8),
        appearance=AppearanceConfig(fill=Color("yellow"), stroke=Color("orange"), stroke_width=1),
    ).move(550, 420)
    canvas.add(flower2_center)

    # Petals
    flower2_petals = [
        Circle(
            config=CircleConfig(r=6),
            appearance=AppearanceConfig(
                fill=Color("lightblue"), stroke=Color("blue"), stroke_width=1
            ),
        ).move(535, 415),
        Circle(
            config=CircleConfig(r=6),
            appearance=AppearanceConfig(
                fill=Color("lightblue"), stroke=Color("blue"), stroke_width=1
            ),
        ).move(565, 415),
        Circle(
            config=CircleConfig(r=6),
            appearance=AppearanceConfig(
                fill=Color("lightblue"), stroke=Color("blue"), stroke_width=1
            ),
        ).move(550, 405),
        Circle(
            config=CircleConfig(r=6),
            appearance=AppearanceConfig(
                fill=Color("lightblue"), stroke=Color("blue"), stroke_width=1
            ),
        ).move(550, 435),
    ]

    for petal in flower2_petals:
        canvas.add(petal)

    # === Path ===
    print("🛤️ Drawing the path...")
    path = Rectangle(
        config=RectangleConfig(x=320, y=450, width=60, height=150),
        appearance=AppearanceConfig(fill=Color("lightgray"), stroke=Color("gray"), stroke_width=2),
    )
    canvas.add(path)

    # Path decorative lines
    path_lines = [
        Rectangle(
            config=RectangleConfig(x=330, y=470, width=40, height=3),
            appearance=AppearanceConfig(fill=Color("white"), stroke=Color("none")),
        ),
        Rectangle(
            config=RectangleConfig(x=330, y=490, width=40, height=3),
            appearance=AppearanceConfig(fill=Color("white"), stroke=Color("none")),
        ),
        Rectangle(
            config=RectangleConfig(x=330, y=510, width=40, height=3),
            appearance=AppearanceConfig(fill=Color("white"), stroke=Color("none")),
        ),
        Rectangle(
            config=RectangleConfig(x=330, y=530, width=40, height=3),
            appearance=AppearanceConfig(fill=Color("white"), stroke=Color("none")),
        ),
        Rectangle(
            config=RectangleConfig(x=330, y=550, width=40, height=3),
            appearance=AppearanceConfig(fill=Color("white"), stroke=Color("none")),
        ),
    ]

    for line in path_lines:
        canvas.add(line)

    # Save SVG file
    output_file = "house.svg"
    canvas.save(output_file)

    print(f"🎉 House scene drawing completed! Saved as: {output_file}")

    # Print some statistics
    print("\n📊 PySVG Component Statistics:")
    print("- Canvas: 1 canvas (800x600)")
    print("- Rectangle: 15 rectangles (house body, door, windows, ground, path, etc.)")
    print("- Circle: 18 circles (sun, clouds, flowers, etc.)")
    print("- Polyline: 7 polylines (roof, sun rays)")
    print("- Various color and style configurations")
    print("- Component position transformations and layout")

    return output_file


def main():
    """Main function"""
    print("=" * 50)
    print("🎨 PyFVG House Scene Demo")
    print("=" * 50)
    print()

    # Create and save house scene
    svg_file = create_house_scene()

    print()
    print("=" * 50)
    print("✨ PySVG features demonstrated:")
    print("1. 🖼️  Canvas creation and configuration")
    print("2. 📐 Rectangle component usage")
    print("3. ⭕ Circle component usage")
    print("4. 📏 Polyline component usage")
    print("5. 🎨 Rich color configuration (Color)")
    print("6. 🖌️  Appearance style configuration (AppearanceConfig)")
    print("7. 📍 Component position movement (.move())")
    print("8. 🏗️  Complex scene component composition")
    print("9. 💾 SVG file output")
    print("=" * 50)

    print(f"\n🎯 Next steps you can take:")
    print(f"1. Open {svg_file} to view the drawing result")
    print("2. Modify colors, positions, sizes, and other parameters in the code")
    print("3. Add more decorative elements")
    print("4. Try other pysvg components (Ellipse, Line, etc.)")


if __name__ == "__main__":
    main()
