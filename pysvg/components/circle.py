from typing import Tuple
from typing_extensions import override

from pysvg.schema import AppearanceConfig, TransformConfig
from pysvg.components.base import BaseSVGComponent, BaseSVGConfig
from pydantic import Field


class CircleConfig(BaseSVGConfig):
    """Geometry configuration for Circle components."""

    cx: float = Field(default=50, description="Circle center X coordinate")
    cy: float = Field(default=50, description="Circle center Y coordinate")
    r: float = Field(default=50, ge=0, description="Circle radius (must be non-negative)")

    @override
    def to_svg_dict(self) -> dict[str, str]:
        """Convert config parameters to SVG attributes dictionary."""
        attrs = super().to_svg_dict()
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
            config=config if config else CircleConfig(),
            appearance=appearance if appearance else AppearanceConfig(),
            transform=transform if transform else TransformConfig(),
        )

    @override
    @property
    def central_point(self) -> Tuple[float, float]:
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
        attrs = {}
        attrs.update(self.config.to_svg_dict())
        attrs.update(self.appearance.to_svg_dict())
        attrs.update(self.transform.to_svg_dict())
        attr_strings = [f'{key}="{value}"' for key, value in attrs.items()]
        return f"<circle {' '.join(attr_strings)} />"

    def get_bounding_box(self) -> Tuple[float, float, float, float]:
        """
        Get circle's bounding box (without considering transformations)

        Returns:
            (min_x, min_y, max_x, max_y) bounding box coordinates
        """
        return (
            self.config.cx - self.config.r,
            self.config.cy - self.config.r,
            self.config.cx + self.config.r,
            self.config.cy + self.config.r,
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
