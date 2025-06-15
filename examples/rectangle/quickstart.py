#!/usr/bin/env python3
"""
Rectangle Component Quick Start Guide

这是Rectangle组件的快速入门指南，展示最常用的功能：
1. 基础创建
2. 外观定制
3. 基础变换
4. 圆角矩形
5. 获取矩形信息
"""

from pysvg.components import Canvas, Rectangle, RectangleConfig
from pysvg.schema import AppearanceConfig, Color


def basic_examples():
    """基础使用示例"""
    print("=== 基础使用示例 ===")

    # 1. 创建基础矩形
    basic_rect = Rectangle(config=RectangleConfig(width=100, height=50))
    print(f"基础矩形: {basic_rect.to_svg_element()}")

    # 2. 指定位置的矩形
    positioned_rect = Rectangle(config=RectangleConfig(x=10, y=20, width=100, height=50))
    print(f"定位矩形: {positioned_rect.to_svg_element()}")
    print()


def styling_examples():
    """样式示例"""
    print("=== 样式示例 ===")

    # 1. 带颜色和边框的矩形
    styled_rect = Rectangle(
        config=RectangleConfig(width=100, height=50),
        appearance=AppearanceConfig(fill=Color("lightblue"), stroke=Color("navy"), stroke_width=2),
    )
    print(f"样式矩形: {styled_rect.to_svg_element()}")

    # 2. 半透明矩形
    transparent_rect = Rectangle(
        config=RectangleConfig(width=100, height=50),
        appearance=AppearanceConfig(
            fill=Color("skyblue"), fill_opacity=0.5, stroke=Color("blue"), stroke_width=2
        ),
    )
    print(f"透明矩形: {transparent_rect.to_svg_element()}")

    # 3. 虚线边框矩形
    dashed_rect = Rectangle(
        config=RectangleConfig(width=100, height=50),
        appearance=AppearanceConfig(
            fill=Color("lightgreen"), stroke=Color("green"), stroke_width=2, stroke_dasharray=[5, 3]
        ),
    )
    print(f"虚线矩形: {dashed_rect.to_svg_element()}")
    print()


def transform_examples():
    """变换示例"""
    print("=== 变换示例 ===")

    # 1. 平移
    moved_rect = Rectangle(
        config=RectangleConfig(width=80, height=40),
    ).move(50, 30)
    print(f"平移矩形: {moved_rect.to_svg_element()}")

    # 2. 旋转
    rotated_rect = Rectangle(
        config=RectangleConfig(width=80, height=40),
    ).rotate(45)
    print(f"旋转矩形: {rotated_rect.to_svg_element()}")

    # 3. 缩放
    scaled_rect = Rectangle(
        config=RectangleConfig(width=80, height=40),
    ).scale(1.5)
    print(f"缩放矩形: {scaled_rect.to_svg_element()}")
    print()


def rounded_corner_examples():
    """圆角矩形示例"""
    print("=== 圆角矩形示例 ===")

    # 1. 均匀圆角
    rounded_rect = Rectangle(
        config=RectangleConfig(width=100, height=50, rx=10, ry=10),
        appearance=AppearanceConfig(fill=Color("coral"), stroke=Color("darkred"), stroke_width=2),
    )
    print(f"圆角矩形: {rounded_rect.to_svg_element()}")

    # 2. 不同的水平和垂直圆角
    custom_rounded_rect = Rectangle(
        config=RectangleConfig(width=100, height=50, rx=20, ry=10),
        appearance=AppearanceConfig(
            fill=Color("lightpink"), stroke=Color("deeppink"), stroke_width=2
        ),
    )
    print(f"自定义圆角矩形: {custom_rounded_rect.to_svg_element()}")
    print()


def info_examples():
    """获取矩形信息示例"""
    print("=== 矩形信息示例 ===")

    rect = Rectangle(config=RectangleConfig(x=10, y=20, width=100, height=50))

    # 1. 获取中心点
    center = rect.central_point
    print(f"矩形中心点: {center}")

    # 2. 获取边界框
    bbox = rect.get_bounding_box()
    print(f"矩形边界框 (min_x, min_y, max_x, max_y): {bbox}")

    # 3. 检查是否有圆角
    has_rounded = rect.has_rounded_corners()
    print(f"是否有圆角: {has_rounded}")
    print()


def generate_demo_svg():
    """生成演示SVG文件"""
    print("=== 生成演示SVG ===")

    # 创建Canvas
    canvas = Canvas(width=600, height=300)

    # 创建示例矩形
    rectangles = [
        # 基础矩形
        Rectangle(
            config=RectangleConfig(width=100, height=50),
            appearance=AppearanceConfig(
                fill=Color("lightgray"), stroke=Color("black"), stroke_width=2
            ),
        ).move(50, 50),
        # 样式矩形
        Rectangle(
            config=RectangleConfig(width=100, height=50),
            appearance=AppearanceConfig(
                fill=Color("lightblue"), stroke=Color("navy"), stroke_width=2
            ),
        ).move(200, 50),
        # 圆角矩形
        Rectangle(
            config=RectangleConfig(width=100, height=50, rx=15, ry=15),
            appearance=AppearanceConfig(
                fill=Color("lightgreen"), stroke=Color("green"), stroke_width=2
            ),
        ).move(350, 50),
        # 半透明矩形
        Rectangle(
            config=RectangleConfig(width=100, height=50),
            appearance=AppearanceConfig(
                fill=Color("coral"), fill_opacity=0.5, stroke=Color("red"), stroke_width=2
            ),
        ).move(50, 150),
        # 旋转矩形
        Rectangle(
            config=RectangleConfig(width=100, height=50),
            appearance=AppearanceConfig(
                fill=Color("lightpink"), stroke=Color("deeppink"), stroke_width=2
            ),
        )
        .rotate(30)
        .move(200, 150),
        # 虚线矩形
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

    # 将矩形添加到canvas
    for rect in rectangles:
        canvas.add(rect)

    # 生成SVG文件
    canvas.save("quickstart.svg")

    print("已生成演示文件: quickstart.svg")


def main():
    """主函数"""
    print("Rectangle Component Quick Start Guide")
    print("=" * 40)

    basic_examples()
    styling_examples()
    transform_examples()
    rounded_corner_examples()
    info_examples()
    generate_demo_svg()

    print("=" * 40)
    print("快速入门指南完成！")
    print("查看生成的 quickstart.svg 文件。")


if __name__ == "__main__":
    main()
