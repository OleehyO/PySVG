from typing import Tuple

from pysvg.schema import AppearanceConfig, TransformConfig
from pysvg.components.base import BaseSVGComponent, BBox
from pysvg.components.rectangle import Rectangle, RectangleConfig
from pysvg.components.content import (
    TextContent,
    ImageContent,
    SVGContent,
    TextConfig,
    ImageConfig,
    SVGConfig,
)
from pydantic import Field
from typing_extensions import override


class CellConfig(RectangleConfig):
    """Geometry configuration for Cell components, extends Rectangle config."""

    # Content configuration - only one type of content is allowed
    text_content: TextConfig | None = Field(default=None, description="Text content config")
    image_content: ImageConfig | None = Field(default=None, description="Image content config")
    svg_content: SVGConfig | None = Field(default=None, description="SVG content config")

    # Content positioning
    content_padding: float = Field(default=5, ge=0, description="Padding around content")

    def model_post_init(self, __context):
        """Validate that only one type of content is specified"""
        content_types = [
            self.text_content is not None,
            self.image_content is not None,
            self.svg_content is not None,
        ]
        if sum(content_types) > 1:
            raise ValueError("Only one type of content (text, image, or svg) can be specified")

    @override
    def to_svg_dict(self) -> dict[str, str]:
        raise NotImplementedError("CellConfig is not implemented")


class Cell(BaseSVGComponent):
    """
    Cell Component - A rectangle that can contain text, images, or SVG content
    """

    def __init__(
        self,
        config: CellConfig,
        rectangle_appearance: AppearanceConfig | None = None,
        transform: TransformConfig | None = None,
    ):
        super().__init__(
            config=config,
            transform=transform if transform else TransformConfig(),
        )

        # Create underlying rectangle component
        self._rectangle = Rectangle(
            config=RectangleConfig(
                x=self.config.x,
                y=self.config.y,
                width=self.config.width,
                height=self.config.height,
                rx=self.config.rx,
                ry=self.config.ry,
            ),
            appearance=rectangle_appearance,
            transform=transform,
        )

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        center_x = self.config.x + self.config.width / 2
        center_y = self.config.y + self.config.height / 2
        return (center_x, center_y)

    @override
    def get_bounding_box(self) -> BBox:
        return self._rectangle.get_bounding_box()

    @override
    def to_svg_element(self) -> str:
        """
        Generate complete SVG element string for the cell with its content

        Returns:
            XML string of SVG group element containing rectangle and content
        """
        elements = []

        # Add the rectangle background
        elements.append(self._rectangle.to_svg_element())

        # Add content based on type
        if self.config.text_content is not None:
            elements.append(self._render_text_content())
        elif self.config.image_content is not None:
            elements.append(self._render_image_content())
        elif self.config.svg_content is not None:
            elements.append(self._render_svg_content())

        # Wrap in a group if we have transform or multiple elements
        if len(elements) > 1 or self.has_transform():
            transform_attr = ""
            if self.has_transform():
                transform_dict = self.transform.to_svg_dict()
                if "transform" in transform_dict and transform_dict["transform"] != "none":
                    transform_attr = f' transform="{transform_dict["transform"]}"'
            return f"<g{transform_attr}>{''.join(elements)}</g>"
        else:
            return elements[0] if elements else self._rectangle.to_svg_element()

    def _render_text_content(self) -> str:
        """Render text content centered in the cell"""
        # Calculate text position
        text_x = self.config.x + self.config.width / 2
        text_y = self.config.y + self.config.height / 2

        # Create text component with calculated position
        text_config = TextConfig(
            x=text_x,
            y=text_y,
            text=self.config.text_content.text,
            font_size=self.config.text_content.font_size,
            font_family=self.config.text_content.font_family,
            color=self.config.text_content.color,
            text_anchor=self.config.text_content.text_anchor,
            dominant_baseline=self.config.text_content.dominant_baseline,
        )

        text_component = TextContent(config=text_config)
        return text_component.to_svg_element()

    def _render_image_content(self) -> str:
        """Render image content centered in the cell"""
        # Calculate image dimensions considering padding
        available_width = self.config.width - 2 * self.config.content_padding
        available_height = self.config.height - 2 * self.config.content_padding

        # Center the image in the cell
        img_x = self.config.x + self.config.content_padding
        img_y = self.config.y + self.config.content_padding

        # Create image component with calculated position and size
        image_config = ImageConfig(
            x=img_x,
            y=img_y,
            width=available_width,
            height=available_height,
            href=self.config.image_content.href,
            preserveAspectRatio=self.config.image_content.preserveAspectRatio,
        )

        image_component = ImageContent(config=image_config)
        return image_component.to_svg_element()

    def _render_svg_content(self) -> str:
        """Render SVG content centered in the cell"""
        # Calculate SVG dimensions considering padding
        available_width = self.config.width - 2 * self.config.content_padding
        available_height = self.config.height - 2 * self.config.content_padding

        # Center the SVG in the cell
        svg_x = self.config.x + self.config.content_padding
        svg_y = self.config.y + self.config.content_padding

        # Create SVG component with calculated position and size
        svg_config = SVGConfig(
            x=svg_x,
            y=svg_y,
            width=available_width,
            height=available_height,
            svg_content=self.config.svg_content.svg_content,
        )

        svg_component = SVGContent(config=svg_config)
        return svg_component.to_svg_element()

    def get_bounding_box(self) -> Tuple[float, float, float, float]:
        """
        Get cell's bounding box (same as underlying rectangle)

        Returns:
            (min_x, min_y, max_x, max_y) bounding box coordinates
        """
        return self._rectangle.get_bounding_box()

    def has_content(self) -> bool:
        """Check if cell has any content"""
        return any(
            [
                self.config.text_content is not None,
                self.config.image_content is not None,
                self.config.svg_content is not None,
            ]
        )

    def get_content_type(self) -> str | None:
        """Get the type of content in the cell"""
        if self.config.text_content is not None:
            return "text"
        elif self.config.image_content is not None:
            return "image"
        elif self.config.svg_content is not None:
            return "svg"
        return None
