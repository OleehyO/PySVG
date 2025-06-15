from typing import Literal, Tuple
from pydantic import Field
from typing_extensions import override

from pysvg.schema import TransformConfig, Color, SVGCode, BBox, ComponentConfig
from pysvg.components.base import BaseSVGComponent


class TextConfig(ComponentConfig):
    """Geometry configuration for Text components"""

    x: float = Field(
        default=0, description="Text x position , central(default) or left-upper corner)"
    )
    y: float = Field(
        default=0, description="Text y position , central(default) or left-upper corner)"
    )
    text: str = Field(default="", description="Text content to display")
    font_size: float = Field(default=12, ge=0, description="Font size")
    font_family: str = Field(default="Arial", description="Font family")
    color: Color = Field(default=Color("black"), description="Text color")
    text_anchor: Literal["start", "middle", "end"] = Field(
        default="middle", description="Text alignment"
    )
    dominant_baseline: Literal["auto", "middle", "hanging", "central"] = Field(
        default="central", description="Vertical text alignment"
    )

    @override
    def to_svg_dict(self) -> dict[str, str]:
        attrs = self.model_dump(exclude_none=True)
        attrs = {k: str(v) for k, v in attrs.items()}
        attrs = {
            k.replace("_", "-")
            if k in ["text_anchor", "dominant_baseline", "font_size", "font_family"]
            else k: v
            for k, v in attrs.items()
        }
        if "color" in attrs:
            attrs["fill"] = attrs.pop("color")
        if "text" in attrs:
            del attrs["text"]
        return attrs


class ImageConfig(ComponentConfig):
    """Geometry configuration for Image components"""

    x: float = Field(default=0, description="Image x position")
    y: float = Field(default=0, description="Image y position")
    width: float = Field(default=200, ge=0, description="Image width")
    height: float = Field(default=200, ge=0, description="Image height")
    href: str = Field(description="Image path or URL")
    preserveAspectRatio: str = Field(
        default="xMidYMid meet", description="How to preserve aspect ratio"
    )

    @override
    def to_svg_dict(self) -> dict[str, str]:
        attrs = self.model_dump(exclude_none=True)
        attrs = {k: str(v) for k, v in attrs.items()}
        return attrs


class SVGConfig(ComponentConfig):
    """Geometry configuration for SVG components"""

    x: float = Field(default=0, description="SVG x position")
    y: float = Field(default=0, description="SVG y position")
    width: float = Field(default=200, ge=0, description="SVG width")
    height: float = Field(default=200, ge=0, description="SVG height")
    svg_content: SVGCode = Field(description="Raw SVG component code")

    @override
    def to_svg_dict(self) -> dict[str, str]:
        attrs = self.model_dump(exclude_none=True)
        attrs = {k: str(v) for k, v in attrs.items()}
        del attrs["svg_content"]
        attrs.update({"viewBox": f"0 0 {self.width} {self.height}"})
        return attrs


class TextContent(BaseSVGComponent):
    """Text content component for SVG"""

    def __init__(self, config: TextConfig, transform: TransformConfig | None = None):
        super().__init__(config=config, transform=transform if transform else TransformConfig())

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        if self.config.text_anchor == "middle" and self.config.dominant_baseline == "central":
            return (self.config.x, self.config.y)
        else:
            raise RuntimeWarning(
                "When text_anchor or dominant_baseline is not middle or central, we can't determine the relative central point of the text"
            )

    @override
    def get_bounding_box(self) -> BBox:
        raise RuntimeWarning(
            "Can't get bounding box of text content since we can't determine the size of the text"
        )

    @override
    def to_svg_element(self) -> str:
        attrs = self.get_attr_dict()
        attrs_ls = [f'{k}="{v}"' for k, v in attrs.items()]
        return f"<text {' '.join(attrs_ls)}>{self.config.text}</text>"


class ImageContent(BaseSVGComponent):
    """Image content component for SVG"""

    def __init__(self, config: ImageConfig, transform: TransformConfig | None = None):
        super().__init__(config=config, transform=transform if transform else TransformConfig())

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        center_x = self.config.x + self.config.width / 2
        center_y = self.config.y + self.config.height / 2
        return (center_x, center_y)

    @override
    def get_bounding_box(self) -> BBox:
        return BBox(
            x=self.config.x,
            y=self.config.y,
            width=self.config.width,
            height=self.config.height,
        )

    @override
    def to_svg_element(self) -> str:
        attrs = self.get_attr_dict()
        attrs_ls = [f'{k}="{v}"' for k, v in attrs.items()]
        return f"<image {' '.join(attrs_ls)} />"


class SVGContent(BaseSVGComponent):
    """SVG content component for nested SVG"""

    def __init__(self, config: SVGConfig, transform: TransformConfig | None = None):
        super().__init__(config=config, transform=transform if transform else TransformConfig())

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        center_x = self.config.x + self.config.width / 2
        center_y = self.config.y + self.config.height / 2
        return (center_x, center_y)

    @override
    def get_bounding_box(self) -> BBox:
        return BBox(
            x=self.config.x,
            y=self.config.y,
            width=self.config.width,
            height=self.config.height,
        )

    @override
    def to_svg_element(self) -> str:
        attrs = self.get_attr_dict()
        attrs_ls = [f'{k}="{v}"' for k, v in attrs.items()]
        return f"<svg {' '.join(attrs_ls)}>{self.config.svg_content}</svg>"
