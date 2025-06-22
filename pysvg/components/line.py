from typing import Tuple
from typing_extensions import override

from pysvg.schema import AppearanceConfig, TransformConfig, BBox
from pysvg.components.base import BaseSVGComponent, ComponentConfig
from pydantic import Field


class LineConfig(ComponentConfig):
    """Geometry configuration for Line components."""

    x1: float = Field(default=0, ge=0, description="Line start X coordinate")
    y1: float = Field(default=0, ge=0, description="Line start Y coordinate")
    x2: float = Field(default=100, ge=0, description="Line end X coordinate")
    y2: float = Field(default=100, ge=0, description="Line end Y coordinate")

    @override
    def to_svg_dict(self) -> dict[str, str]:
        """Convert config parameters to SVG attributes dictionary."""
        attrs = self.model_dump(exclude_none=True)
        attrs = {k: str(v) for k, v in attrs.items()}
        return attrs


class Line(BaseSVGComponent):
    """
    SVG Line Component
    """

    def __init__(
        self,
        config: LineConfig | None = None,
        appearance: AppearanceConfig | None = None,
        transform: TransformConfig | None = None,
    ):
        super().__init__(
            config=config or LineConfig(),
            appearance=appearance or AppearanceConfig(),
            transform=transform or TransformConfig(),
        )

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        center_x = (self.config.x1 + self.config.x2) / 2
        center_y = (self.config.y1 + self.config.y2) / 2
        return (center_x, center_y)

    @override
    def get_bounding_box(self) -> BBox:
        return BBox(
            x=self.transform.translate[0] + min(self.config.x1, self.config.x2),
            y=self.transform.translate[1] + min(self.config.y1, self.config.y2),
            width=abs(self.config.x2 - self.config.x1),
            height=abs(self.config.y2 - self.config.y1),
        )

    @override
    def to_svg_element(self) -> str:
        attrs = self.get_attr_dict()
        attrs_ls = [f'{k}="{v}"' for k, v in attrs.items()]
        return f"<line {' '.join(attrs_ls)} />"

    def get_length(self) -> float:
        """
        Calculate the length of the line

        Returns:
            Line length
        """
        import math

        dx = self.config.x2 - self.config.x1
        dy = self.config.y2 - self.config.y1
        return math.sqrt(dx**2 + dy**2)

    def get_slope(self) -> float | None:
        """
        Calculate the slope of the line

        Returns:
            Line slope, or None if the line is vertical
        """
        dx = self.config.x2 - self.config.x1
        if dx == 0:
            return None  # Vertical line
        dy = self.config.y2 - self.config.y1
        return dy / dx

    def get_angle(self) -> float:
        """
        Calculate the angle of the line in degrees

        Returns:
            Line angle in degrees (0-360)
        """
        import math

        dx = self.config.x2 - self.config.x1
        dy = self.config.y2 - self.config.y1
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        return angle_deg if angle_deg >= 0 else angle_deg + 360
