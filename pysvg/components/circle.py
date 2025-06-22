from typing import Tuple
from typing_extensions import override

from pysvg.schema import AppearanceConfig, TransformConfig, BBox
from pysvg.components.base import BaseSVGComponent, ComponentConfig
from pydantic import Field


class CircleConfig(ComponentConfig):
    """Geometry configuration for Circle components."""

    cx: float = Field(default=50, description="Circle center X coordinate")
    cy: float = Field(default=50, description="Circle center Y coordinate")
    r: float = Field(default=50, ge=0, description="Circle radius (must be non-negative)")

    @override
    def to_svg_dict(self) -> dict[str, str]:
        attrs = self.model_dump(exclude_none=True)
        attrs = {k: str(v) for k, v in attrs.items()}
        return attrs


class Circle(BaseSVGComponent):
    """
    SVG Circle Component
    """

    def __init__(
        self,
        config: CircleConfig | None = None,
        appearance: AppearanceConfig | None = None,
        transform: TransformConfig | None = None,
    ):
        super().__init__(
            config=config or CircleConfig(),
            appearance=appearance or AppearanceConfig(),
            transform=transform or TransformConfig(),
        )

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        return (self.config.cx, self.config.cy)

    @override
    def restrict_size(self, max_width: float, max_height: float) -> "Circle":
        # For a circle, both width and height equal the diameter (2 * r)
        current_diameter = 2 * self.config.r

        # Calculate scale factors for both dimensions
        width_scale = max_width / current_diameter if current_diameter > max_width else 1.0
        height_scale = max_height / current_diameter if current_diameter > max_height else 1.0

        # Use the smaller scale to ensure the circle fits within both limits
        scale_factor = min(width_scale, height_scale)

        if scale_factor < 1.0:
            # Apply uniform scale to maintain circle shape
            self.scale(scale_factor)

        return self

    @override
    def to_svg_element(self) -> str:
        """
        Generate complete SVG circle element string

        Returns:
            XML string of SVG circle element
        """
        attrs = self.get_attr_dict()
        attrs_ls = [f'{k}="{v}"' for k, v in attrs.items()]
        return f"<circle {' '.join(attrs_ls)} />"

    @override
    def get_bounding_box(self) -> BBox:
        return BBox(
            x=self.transform.translate[0] + self.config.cx - self.config.r,
            y=self.transform.translate[1] + self.config.cy - self.config.r,
            width=2 * self.config.r,
            height=2 * self.config.r,
        )

    def get_area(self) -> float:
        """
        Calculate the area of the circle

        Returns:
            Circle area
        """
        import math

        return math.pi * self.config.r**2

    def get_circumference(self) -> float:
        """
        Calculate the circumference of the circle

        Returns:
            Circle circumference
        """
        import math

        return 2 * math.pi * self.config.r
