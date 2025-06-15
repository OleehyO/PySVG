#!/usr/bin/env python3
"""
Polyline Component Quick Start Guide

This is a quick start guide for the Polyline component, demonstrating the most commonly used features:
1. Basic creation
2. Appearance customization
3. Basic transformations
4. Getting polyline information
"""

from pysvg.components import Canvas, Polyline, PolylineConfig
from pysvg.schema import AppearanceConfig, Color


def basic_examples():
    """Basic usage examples"""
    print("=== Basic Usage Examples ===")

    # 1. Create basic polyline
    basic_polyline = Polyline(
        config=PolylineConfig(points=[(0, 0), (50, 30), (100, 10), (150, 50)])
    )
    print(f"Basic polyline: {basic_polyline.to_svg_element()}")

    # 2. Triangle polyline
    triangle_polyline = Polyline(config=PolylineConfig(points=[(50, 10), (10, 80), (90, 80)]))
    print(f"Triangle polyline: {triangle_polyline.to_svg_element()}")

    # 3. Zigzag polyline
    zigzag_polyline = Polyline(
        config=PolylineConfig(points=[(0, 50), (20, 20), (40, 50), (60, 20), (80, 50), (100, 20)])
    )
    print(f"Zigzag polyline: {zigzag_polyline.to_svg_element()}")
    print()


def styling_examples():
    """Styling examples"""
    print("=== Styling Examples ===")

    # 1. Polyline with color and width
    styled_polyline = Polyline(
        config=PolylineConfig(points=[(0, 20), (30, 5), (60, 35), (90, 10), (120, 40)]),
        appearance=AppearanceConfig(stroke=Color("red"), stroke_width=3, fill=Color("none")),
    )
    print(f"Styled polyline: {styled_polyline.to_svg_element()}")

    # 2. Dashed polyline
    dashed_polyline = Polyline(
        config=PolylineConfig(points=[(0, 0), (40, 40), (80, 0), (120, 40), (160, 0)]),
        appearance=AppearanceConfig(
            stroke=Color("blue"), stroke_width=2, stroke_dasharray=[10, 5], fill=Color("none")
        ),
    )
    print(f"Dashed polyline: {dashed_polyline.to_svg_element()}")

    # 3. Filled polyline (creates closed shape effect)
    filled_polyline = Polyline(
        config=PolylineConfig(points=[(20, 20), (60, 10), (80, 40), (40, 50), (20, 20)]),
        appearance=AppearanceConfig(
            stroke=Color("green"), stroke_width=2, fill=Color("lightgreen"), fill_opacity=0.7
        ),
    )
    print(f"Filled polyline: {filled_polyline.to_svg_element()}")

    # 4. Thick polyline
    thick_polyline = Polyline(
        config=PolylineConfig(points=[(0, 30), (50, 10), (100, 50), (150, 30)]),
        appearance=AppearanceConfig(
            stroke=Color("purple"), stroke_width=8, stroke_linecap="round", fill=Color("none")
        ),
    )
    print(f"Thick polyline: {thick_polyline.to_svg_element()}")

    # 5. Semi-transparent polyline
    transparent_polyline = Polyline(
        config=PolylineConfig(points=[(10, 10), (50, 60), (90, 20), (130, 70), (170, 30)]),
        appearance=AppearanceConfig(
            stroke=Color("orange"), stroke_width=4, stroke_opacity=0.6, fill=Color("none")
        ),
    )
    print(f"Transparent polyline: {transparent_polyline.to_svg_element()}")
    print()


def dynamic_creation_examples():
    """Dynamic creation examples"""
    print("=== Dynamic Creation Examples ===")

    # 1. Add points step by step
    dynamic_polyline = Polyline()
    dynamic_polyline.add_point(0, 20)
    dynamic_polyline.add_point(30, 50)
    dynamic_polyline.add_point(60, 10)
    dynamic_polyline.add_point(90, 40)
    print(f"Dynamic polyline with added points: {dynamic_polyline.to_svg_element()}")

    # 2. Add points in batch
    batch_polyline = Polyline()
    batch_polyline.add_points([(0, 0), (25, 40), (50, 20), (75, 60), (100, 30)])
    print(f"Batch polyline with added points: {batch_polyline.to_svg_element()}")

    # 3. Generate mathematical function polyline (sine wave)
    import math

    sine_points = []
    for x in range(0, 360, 10):
        y = 50 + 30 * math.sin(math.radians(x))
        sine_points.append((x / 2, y))
    sine_polyline = Polyline(config=PolylineConfig(points=sine_points))
    print(f"Sine wave polyline: {sine_polyline.to_svg_element()}")
    print()


def transform_examples():
    """Transformation examples"""
    print("=== Transformation Examples ===")

    # 1. Translation
    moved_polyline = Polyline(
        config=PolylineConfig(points=[(0, 0), (30, 20), (60, 10), (90, 30)]),
    ).move(50, 40)
    print(f"Moved polyline: {moved_polyline.to_svg_element()}")

    # 2. Rotation
    rotated_polyline = Polyline(
        config=PolylineConfig(points=[(0, 0), (50, 0), (50, 30), (0, 30)]),
    ).rotate(45)
    print(f"Rotated polyline: {rotated_polyline.to_svg_element()}")

    # 3. Scaling
    scaled_polyline = Polyline(
        config=PolylineConfig(points=[(0, 0), (20, 15), (40, 5), (60, 20)]),
    ).scale(1.5)
    print(f"Scaled polyline: {scaled_polyline.to_svg_element()}")

    # 4. Combined transformation
    combined_polyline = (
        Polyline(
            config=PolylineConfig(points=[(0, 0), (30, 20), (60, 0), (90, 20)]),
            appearance=AppearanceConfig(stroke=Color("red"), stroke_width=3, fill=Color("none")),
        )
        .rotate(30)
        .move(100, 50)
        .scale(1.2)
    )
    print(f"Combined transformation polyline: {combined_polyline.to_svg_element()}")
    print()


def info_examples():
    """Polyline information examples"""
    print("=== Polyline Information Examples ===")

    polyline = Polyline(
        config=PolylineConfig(points=[(10, 20), (50, 10), (90, 40), (130, 20), (170, 50)])
    )

    # 1. Get central point (centroid)
    center = polyline.central_point
    print(f"Polyline central point: {center}")

    # 2. Get bounding box
    bbox = polyline.get_bounding_box()
    print(f"Polyline bounding box (min_x, min_y, max_x, max_y): {bbox}")

    # 3. Get total length
    total_length = polyline.get_total_length()
    print(f"Polyline total length: {total_length:.2f}")

    # 4. Get segment lengths
    segment_lengths = polyline.get_segment_lengths()
    print(f"Segment lengths: {[f'{length:.2f}' for length in segment_lengths]}")

    # 5. Get point count
    point_count = polyline.get_point_count()
    print(f"Polyline point count: {point_count}")

    # 6. Dynamic operation example
    test_polyline = Polyline()
    test_polyline.add_point(0, 0).add_point(30, 20).add_point(60, 10)
    print(f"Point count after dynamic creation: {test_polyline.get_point_count()}")

    test_polyline.clear_points()
    print(f"Point count after clearing: {test_polyline.get_point_count()}")
    print()


def generate_demo_svg():
    """Generate demo SVG file"""
    print("=== Generate Demo SVG ===")

    # Create Canvas
    canvas = Canvas(width=590, height=290, viewbox=(50, 30, 590, 290))

    # Create example polylines
    polylines = []

    # 1. Basic geometric shapes
    # Triangle
    triangle = Polyline(
        config=PolylineConfig(points=[(80, 50), (50, 100), (110, 100), (80, 50)]),
        appearance=AppearanceConfig(
            stroke=Color("red"), stroke_width=2, fill=Color("lightcoral"), fill_opacity=0.3
        ),
    )
    polylines.append(triangle)

    # Trapezoid
    trapezoid = Polyline(
        config=PolylineConfig(points=[(150, 70), (200, 70), (220, 100), (130, 100), (150, 70)]),
        appearance=AppearanceConfig(
            stroke=Color("blue"), stroke_width=2, fill=Color("lightblue"), fill_opacity=0.3
        ),
    )
    polylines.append(trapezoid)

    # Five-pointed star outline
    star_outer = Polyline(
        config=PolylineConfig(
            points=[
                (300, 30),
                (310, 60),
                (340, 60),
                (320, 80),
                (330, 110),
                (300, 95),
                (270, 110),
                (280, 80),
                (260, 60),
                (290, 60),
                (300, 30),
            ]
        ),
        appearance=AppearanceConfig(
            stroke=Color("gold"), stroke_width=2, fill=Color("yellow"), fill_opacity=0.6
        ),
    )
    polylines.append(star_outer)

    # 2. Wave and zigzag patterns
    # Zigzag wave
    zigzag = Polyline(
        config=PolylineConfig(
            points=[
                (50, 180),
                (70, 150),
                (90, 180),
                (110, 150),
                (130, 180),
                (150, 150),
                (170, 180),
                (190, 150),
                (210, 180),
            ]
        ),
        appearance=AppearanceConfig(stroke=Color("lightgreen"), stroke_width=3, fill=Color("none")),
    )
    polylines.append(zigzag)

    # Square wave
    square_wave = Polyline(
        config=PolylineConfig(
            points=[
                (250, 180),
                (250, 150),
                (280, 150),
                (280, 180),
                (310, 180),
                (310, 150),
                (340, 150),
                (340, 180),
                (370, 180),
            ]
        ),
        appearance=AppearanceConfig(stroke=Color("purple"), stroke_width=3, fill=Color("none")),
    )
    polylines.append(square_wave)

    # 3. Mathematical function graphics
    # Sine wave
    import math

    sine_points = []
    for x in range(0, 100, 5):
        y = 250 + 30 * math.sin(x * math.pi / 50)
        sine_points.append((x + 50, y))

    sine_wave = Polyline(
        config=PolylineConfig(points=sine_points),
        appearance=AppearanceConfig(stroke=Color("darkblue"), stroke_width=2, fill=Color("none")),
    )
    polylines.append(sine_wave)

    # 4. Decorative patterns
    # Arrow
    arrow = Polyline(
        config=PolylineConfig(
            points=[
                (400, 80),
                (450, 80),
                (450, 70),
                (470, 85),
                (450, 100),
                (450, 90),
                (400, 90),
                (400, 80),
            ]
        ),
        appearance=AppearanceConfig(
            stroke=Color("darkred"), stroke_width=2, fill=Color("red"), fill_opacity=0.7
        ),
    )
    polylines.append(arrow)

    # Heart (approximate)
    heart = Polyline(
        config=PolylineConfig(
            points=[
                (550, 80),
                (540, 70),
                (530, 70),
                (520, 80),
                (530, 90),
                (550, 110),
                (570, 90),
                (580, 80),
                (570, 70),
                (560, 70),
                (550, 80),
            ]
        ),
        appearance=AppearanceConfig(
            stroke=Color("deeppink"), stroke_width=2, fill=Color("pink"), fill_opacity=0.6
        ),
    )
    polylines.append(heart)

    # 5. Complex patterns
    # Spiral approximation
    spiral_points = []
    for i in range(0, 100, 1):
        angle = i * 0.3
        radius = i * 0.4
        x = 210 + radius * math.cos(angle)
        y = 250 + radius * math.sin(angle)
        spiral_points.append((x, y))

    spiral = Polyline(
        config=PolylineConfig(points=spiral_points),
        appearance=AppearanceConfig(stroke=Color("darkgreen"), stroke_width=2, fill=Color("none")),
    )
    polylines.append(spiral)

    # Flower shape
    flower_points = []
    center_x, center_y = 320, 250
    for angle in range(0, 360, 15):
        # Alternating inner and outer radius to create petal effect
        radius = 40 if angle % 30 == 0 else 25
        rad = math.radians(angle)
        x = center_x + radius * math.cos(rad)
        y = center_y + radius * math.sin(rad)
        flower_points.append((x, y))
    flower_points.append(flower_points[0])  # Close

    flower = Polyline(
        config=PolylineConfig(points=flower_points),
        appearance=AppearanceConfig(
            stroke=Color("magenta"), stroke_width=2, fill=Color("lightpink"), fill_opacity=0.4
        ),
    )
    polylines.append(flower)

    # 6. Dashed pattern
    # Dashed wave
    wave_points = []
    for x in range(0, 180, 5):
        y = 170 + 20 * math.sin(x * math.pi / 30)
        wave_points.append((x + 400, y))

    dashed_wave = Polyline(
        config=PolylineConfig(points=wave_points),
        appearance=AppearanceConfig(
            stroke=Color("teal"), stroke_width=3, stroke_dasharray=[8, 4], fill=Color("none")
        ),
    )
    polylines.append(dashed_wave)

    # 7. Transformation examples
    # Rotated rectangle outline
    rotated_rect = (
        Polyline(
            config=PolylineConfig(points=[(0, 0), (60, 0), (60, 40), (0, 40), (0, 0)]),
            appearance=AppearanceConfig(
                stroke=Color("navy"), stroke_width=2, fill=Color("lightsteelblue"), fill_opacity=0.5
            ),
        )
        .rotate(30)
        .move(420, 230)
    )
    polylines.append(rotated_rect)

    # Scaled triangle
    scaled_triangle = (
        Polyline(
            config=PolylineConfig(points=[(0, 0), (30, 0), (15, 25), (0, 0)]),
            appearance=AppearanceConfig(
                stroke=Color("darkviolet"), stroke_width=2, fill=Color("violet"), fill_opacity=0.4
            ),
        )
        .scale(2.0)
        .move(520, 230)
    )
    polylines.append(scaled_triangle)

    # Add all polylines to canvas
    for polyline in polylines:
        canvas.add(polyline)

    # Generate SVG file
    canvas.save("quickstart.svg")

    print("Demo file generated: quickstart.svg")


def main():
    """Main function"""
    print("Polyline Component Quick Start Guide")
    print("=" * 40)

    basic_examples()
    styling_examples()
    dynamic_creation_examples()
    transform_examples()
    info_examples()
    generate_demo_svg()

    print("=" * 40)
    print("Quick start guide completed!")
    print("Check the generated quickstart.svg file.")


if __name__ == "__main__":
    main()
