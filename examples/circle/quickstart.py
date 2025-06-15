#!/usr/bin/env python3
"""
Circle Component Quick Start Guide

这是Circle组件的快速入门指南，展示最常用的功能：
1. 基础创建
2. 外观定制
3. 基础变换
4. 获取圆形信息
"""

from pysvg.components import Canvas, Circle, CircleConfig
from pysvg.schema import AppearanceConfig, Color


def basic_examples():
    """基础使用示例"""
    print("=== 基础使用示例 ===")

    # 1. 创建基础圆形
    basic_circle = Circle(config=CircleConfig(r=50))
    print(f"基础圆形: {basic_circle.to_svg_element()}")

    # 2. 指定位置的圆形
    positioned_circle = Circle(config=CircleConfig(cx=100, cy=100, r=30))
    print(f"定位圆形: {positioned_circle.to_svg_element()}")
    print()


def styling_examples():
    """样式示例"""
    print("=== 样式示例 ===")

    # 1. 带颜色和边框的圆形
    styled_circle = Circle(
        config=CircleConfig(r=40),
        appearance=AppearanceConfig(fill=Color("lightblue"), stroke=Color("navy"), stroke_width=3),
    )
    print(f"样式圆形: {styled_circle.to_svg_element()}")

    # 2. 半透明圆形
    transparent_circle = Circle(
        config=CircleConfig(r=35),
        appearance=AppearanceConfig(
            fill=Color("skyblue"), fill_opacity=0.6, stroke=Color("blue"), stroke_width=2
        ),
    )
    print(f"透明圆形: {transparent_circle.to_svg_element()}")

    # 3. 虚线边框圆形
    dashed_circle = Circle(
        config=CircleConfig(r=30),
        appearance=AppearanceConfig(
            fill=Color("lightgreen"), stroke=Color("green"), stroke_width=3, stroke_dasharray=[8, 4]
        ),
    )
    print(f"虚线圆形: {dashed_circle.to_svg_element()}")

    # 4. 仅边框圆形（无填充）
    outline_circle = Circle(
        config=CircleConfig(r=25),
        appearance=AppearanceConfig(fill=Color("none"), stroke=Color("red"), stroke_width=2),
    )
    print(f"轮廓圆形: {outline_circle.to_svg_element()}")
    print()


def transform_examples():
    """变换示例"""
    print("=== 变换示例 ===")

    # 1. 平移
    moved_circle = Circle(
        config=CircleConfig(r=30),
    ).move(80, 60)
    print(f"平移圆形: {moved_circle.to_svg_element()}")

    # 2. 缩放
    scaled_circle = Circle(
        config=CircleConfig(r=20),
    ).scale(2.0)
    print(f"缩放圆形: {scaled_circle.to_svg_element()}")

    # 3. 组合变换
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
    print(f"组合变换圆形: {combined_circle.to_svg_element()}")
    print()


def info_examples():
    """获取圆形信息示例"""
    print("=== 圆形信息示例 ===")

    circle = Circle(config=CircleConfig(cx=50, cy=60, r=40))

    # 1. 获取中心点
    center = circle.central_point
    print(f"圆形中心点: {center}")

    # 2. 获取边界框
    bbox = circle.get_bounding_box()
    print(f"圆形边界框 (min_x, min_y, max_x, max_y): {bbox}")

    # 3. 获取面积
    area = circle.get_area()
    print(f"圆形面积: {area:.2f}")

    # 4. 获取周长
    circumference = circle.get_circumference()
    print(f"圆形周长: {circumference:.2f}")
    print()


def generate_demo_svg():
    """生成演示SVG文件"""
    print("=== 生成演示SVG ===")

    # 创建Canvas
    canvas = Canvas(width=600, height=400)

    # 创建示例圆形
    circles = [
        # 基础圆形
        Circle(
            config=CircleConfig(r=30),
            appearance=AppearanceConfig(
                fill=Color("lightgray"), stroke=Color("black"), stroke_width=2
            ),
        ).move(80, 80),
        # 样式圆形
        Circle(
            config=CircleConfig(r=35),
            appearance=AppearanceConfig(
                fill=Color("lightblue"), stroke=Color("navy"), stroke_width=3
            ),
        ).move(200, 80),
        # 渐变效果圆形（使用半透明）
        Circle(
            config=CircleConfig(r=40),
            appearance=AppearanceConfig(
                fill=Color("coral"), fill_opacity=0.7, stroke=Color("red"), stroke_width=2
            ),
        ).move(350, 80),
        # 大圆形
        Circle(
            config=CircleConfig(r=45),
            appearance=AppearanceConfig(
                fill=Color("lightgreen"), stroke=Color("green"), stroke_width=3
            ),
        ).move(500, 80),
        # 虚线圆形
        Circle(
            config=CircleConfig(r=30),
            appearance=AppearanceConfig(
                fill=Color("lightpink"),
                stroke=Color("deeppink"),
                stroke_width=3,
                stroke_dasharray=[10, 5],
            ),
        ).move(80, 200),
        # 仅轮廓圆形
        Circle(
            config=CircleConfig(r=35),
            appearance=AppearanceConfig(fill=Color("none"), stroke=Color("purple"), stroke_width=4),
        ).move(200, 200),
        # 缩放圆形
        Circle(
            config=CircleConfig(r=20),
            appearance=AppearanceConfig(fill=Color("gold"), stroke=Color("orange"), stroke_width=2),
        )
        .scale(1.8)
        .move(350, 200),
        # 小圆形组合
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
        # 大型半透明圆形作为背景
        Circle(
            config=CircleConfig(r=60),
            appearance=AppearanceConfig(
                fill=Color("yellow"), fill_opacity=0.3, stroke=Color("orange"), stroke_width=1
            ),
        ).move(150, 320),
        # 中等圆形
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

    # 将圆形添加到canvas
    for circle in circles:
        canvas.add(circle)

    # 生成SVG文件
    canvas.save("quickstart.svg")

    print("已生成演示文件: quickstart.svg")


def main():
    """主函数"""
    print("Circle Component Quick Start Guide")
    print("=" * 40)

    basic_examples()
    styling_examples()
    transform_examples()
    info_examples()
    generate_demo_svg()

    print("=" * 40)
    print("快速入门指南完成！")
    print("查看生成的 quickstart.svg 文件。")


if __name__ == "__main__":
    main()
