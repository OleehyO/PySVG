from typing import Tuple
from typing_extensions import override

from pysvg.schema import AppearanceConfig, TransformConfig, BBox
from pysvg.components.base import BaseSVGComponent, ComponentConfig
from pydantic import Field


class RectangleConfig(ComponentConfig):
    """Geometry configuration for Rectangle components."""

    x: float = Field(default=0, description="Rectangle's left x coordinate")
    y: float = Field(default=0, description="Rectangle's top y coordinate")
    width: float = Field(default=200, ge=0, description="Rectangle width (must be non-negative)")
    height: float = Field(default=100, ge=0, description="Rectangle height (must be non-negative)")
    rx: float | None = Field(default=None, ge=0, description="X-axis radius for rounded corners")
    ry: float | None = Field(default=None, ge=0, description="Y-axis radius for rounded corners")

    @override
    def to_svg_dict(self) -> dict[str, str]:
        """Convert config parameters to SVG attributes dictionary."""
        attrs = self.model_dump(exclude_none=True)
        attrs = {k: str(v) for k, v in attrs.items()}
        return attrs


class Rectangle(BaseSVGComponent):
    """
    SVG Rectangle Component
    """

    def __init__(
        self,
        config: RectangleConfig | None = None,
        appearance: AppearanceConfig | None = None,
        transform: TransformConfig | None = None,
    ):
        super().__init__(
            config=config if config else RectangleConfig(),
            appearance=appearance if appearance else AppearanceConfig(),
            transform=transform if transform else TransformConfig(),
        )

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
        return f"<rect {' '.join(attrs_ls)} />"

    def has_rounded_corners(self) -> bool:
        """Check if rectangle has rounded corners"""
        return self.config.rx is not None or self.config.ry is not None
