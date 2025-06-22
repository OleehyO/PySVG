from typing import Literal, Tuple
from pydantic import Field
from typing_extensions import override

from pysvg.schema import TransformConfig, Color, BBox, ComponentConfig
from pysvg.components.base import BaseSVGComponent
from pysvg.logger import get_logger

_logger = get_logger(__name__)


class TextConfig(ComponentConfig):
    """Geometry configuration for Text components"""

    x: float = Field(
        default=0, description="Text x position , central(default) or left-upper corner)"
    )
    y: float = Field(
        default=0, description="Text y position , central(default) or left-upper corner)"
    )
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
        return attrs


class ImageConfig(ComponentConfig):
    """Geometry configuration for Image components"""

    x: float = Field(default=0, description="Image x position")
    y: float = Field(default=0, description="Image y position")
    width: float = Field(default=200, ge=0, description="Image width")
    height: float = Field(default=200, ge=0, description="Image height")
    preserveAspectRatio: str = Field(
        default="xMidYMid meet", description="How to preserve aspect ratio"
    )

    @override
    def to_svg_dict(self) -> dict[str, str]:
        attrs = self.model_dump(exclude_none=True)
        attrs = {k: str(v) for k, v in attrs.items()}
        return attrs


class TextContent(BaseSVGComponent):
    """Text content component for SVG"""

    def __init__(
        self, text: str, config: TextConfig | None = None, transform: TransformConfig | None = None
    ):
        super().__init__(config=config or TextConfig(), transform=transform or TransformConfig())
        self.text = text

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        if self.config.dominant_baseline != "central":
            raise RuntimeWarning(
                "When dominant_baseline is not central, we can't determine the relative central point of the text"
            )

        if self.config.text_anchor == "start":
            _logger.warning(
                "Text anchor is start, which means we will use the **middle left part** of the text box as the center point",
            )
        elif self.config.text_anchor == "end":
            _logger.warning(
                "Text anchor is end, which means we will use the **middle right part** of the text box as the center point"
            )

        return (self.config.x, self.config.y)

    @override
    def get_bounding_box(self) -> BBox:
        raise RuntimeWarning(
            "Can't get bounding box of text content since we can't determine the size of the text"
        )

    @override
    def to_svg_element(self) -> str:
        attrs = self.get_attr_dict()
        attrs_ls = [f'{k}="{v}"' for k, v in attrs.items()]
        return f"<text {' '.join(attrs_ls)}>{self.text}</text>"


class ImageContent(BaseSVGComponent):
    """Image content component for SVG"""

    def __init__(
        self, href: str, config: ImageConfig | None = None, transform: TransformConfig | None = None
    ):
        super().__init__(config=config or ImageConfig(), transform=transform or TransformConfig())
        self.href = href

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        center_x = self.config.x + self.config.width / 2
        center_y = self.config.y + self.config.height / 2
        return (center_x, center_y)

    @override
    def get_bounding_box(self) -> BBox:
        return BBox(
            x=self.transform.translate[0] + self.config.x,
            y=self.transform.translate[1] + self.config.y,
            width=self.config.width,
            height=self.config.height,
        )

    @override
    def to_svg_element(self) -> str:
        attrs = self.get_attr_dict()
        attrs["href"] = self.href
        attrs_ls = [f'{k}="{v}"' for k, v in attrs.items()]
        return f"<image {' '.join(attrs_ls)} />"
