from typing import Literal, Tuple
from typing_extensions import override

from pysvg.schema import AppearanceConfig, TransformConfig, BBox
from pysvg.components.base import BaseSVGComponent, ComponentConfig
from pydantic import Field


class RectangleConfig(ComponentConfig):
    """Geometry configuration for Rectangle components."""

    x: float = Field(default=0, description="Rectangle's left x coordinate")
    y: float = Field(default=0, description="Rectangle's top y coordinate")
    width: float = Field(default=200, gt=0, description="Rectangle width (must be non-negative)")
    height: float = Field(default=100, gt=0, description="Rectangle height (must be non-negative)")
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
            config=config or RectangleConfig(),
            appearance=appearance or AppearanceConfig(),
            transform=transform or TransformConfig(),
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
            x=self.transform.translate[0] + self.config.x,
            y=self.transform.translate[1] + self.config.y,
            width=self.config.width,
            height=self.config.height,
        )

    @override
    def restrict_size(
        self, width: float, height: float, mode: Literal["fit", "force"] = "fit"
    ) -> "Rectangle":
        current_width = self.config.width
        current_height = self.config.height

        # Calculate scale factors for width and height
        width_scale = width / current_width
        height_scale = height / current_height

        # Use the smaller scale factor to ensure the rectangle fits within both limits
        scale_factor = min(width_scale, height_scale)

        if mode == "fit" and scale_factor >= 1.0:
            return self

        self.config.width = current_width * scale_factor
        self.config.height = current_height * scale_factor
        if self.config.rx is not None:
            self.config.rx = self.config.rx * scale_factor
        if self.config.ry is not None:
            self.config.ry = self.config.ry * scale_factor

        return self

    @override
    def to_svg_element(self) -> str:
        attrs = self.get_attr_dict()
        attrs_ls = [f'{k}="{v}"' for k, v in attrs.items()]
        return f"<rect {' '.join(attrs_ls)} />"

    def has_rounded_corners(self) -> bool:
        """Check if rectangle has rounded corners"""
        return self.config.rx is not None or self.config.ry is not None
