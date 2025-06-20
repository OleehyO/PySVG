from typing import Tuple
from typing_extensions import override

from pysvg.schema import AppearanceConfig, TransformConfig
from pysvg.components.base import BaseSVGComponent, BaseSVGConfig
from pydantic import Field


class EllipseConfig(BaseSVGConfig):
    """Geometry configuration for Ellipse components."""

    cx: float = Field(default=100, description="Ellipse center X coordinate")
    cy: float = Field(default=50, description="Ellipse center Y coordinate")
    rx: float = Field(default=100, ge=0, description="Ellipse X-axis radius (must be non-negative)")
    ry: float = Field(default=50, ge=0, description="Ellipse Y-axis radius (must be non-negative)")

    @override
    def to_svg_dict(self) -> dict[str, str]:
        """Convert config parameters to SVG attributes dictionary."""
        attrs = super().to_svg_dict()
        attrs = {k: str(v) for k, v in attrs.items()}
        return attrs


class Ellipse(BaseSVGComponent):
    """
    SVG Ellipse Component
    """

    def __init__(
        self,
        config: EllipseConfig | None = None,
        appearance: AppearanceConfig | None = None,
        transform: TransformConfig | None = None,
    ):
        super().__init__(
            config=config if config is not None else EllipseConfig(),
            appearance=appearance if appearance is not None else AppearanceConfig(),
            transform=transform if transform is not None else TransformConfig(),
        )

    @property
    def central_point(self) -> Tuple[float, float]:
        """
        Get the central point of the ellipse.

        Returns:
            Tuple of (center_x, center_y) coordinates
        """
        return (self.config.cx, self.config.cy)

    def to_svg_element(self) -> str:
        """
        Generate complete SVG ellipse element string

        Returns:
            XML string of SVG ellipse element
        """
        attrs = {}
        attrs.update(self.config.to_svg_dict())
        attrs.update(self.appearance.to_svg_dict())
        attrs.update(self.transform.to_svg_dict())
        attr_strings = [f'{key}="{value}"' for key, value in attrs.items()]
        return f"<ellipse {' '.join(attr_strings)} />"

    def get_bounding_box(self) -> Tuple[float, float, float, float]:
        """
        Get ellipse's bounding box (without considering transformations)

        Returns:
            (min_x, min_y, max_x, max_y) bounding box coordinates
        """
        return (
            self.config.cx - self.config.rx,
            self.config.cy - self.config.ry,
            self.config.cx + self.config.rx,
            self.config.cy + self.config.ry,
        )

    def get_area(self) -> float:
        """
        Calculate the area of the ellipse

        Returns:
            Ellipse area
        """
        import math

        return math.pi * self.config.rx * self.config.ry

    def get_circumference(self) -> float:
        """
        Calculate the approximate circumference of the ellipse using Ramanujan's approximation

        Returns:
            Ellipse circumference (approximate)
        """
        import math

        a = self.config.rx
        b = self.config.ry
        # Ramanujan's approximation for ellipse circumference
        h = ((a - b) / (a + b)) ** 2
        return math.pi * (a + b) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))

    def is_circle(self) -> bool:
        """
        Check if the ellipse is actually a circle (rx == ry)

        Returns:
            True if the ellipse is a circle, False otherwise
        """
        return (
            abs(self.config.rx - self.config.ry) < 1e-9
        )  # Use small epsilon for floating point comparison

    def get_eccentricity(self) -> float:
        """
        Calculate the eccentricity of the ellipse

        Returns:
            Ellipse eccentricity (0 for circle, approaching 1 for very elongated ellipse)
        """
        import math

        a = max(self.config.rx, self.config.ry)  # Semi-major axis
        b = min(self.config.rx, self.config.ry)  # Semi-minor axis
        if a == 0:
            return 0
        return math.sqrt(1 - (b / a) ** 2)
