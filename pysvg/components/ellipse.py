from typing import Literal, Tuple
from typing_extensions import override

from pysvg.schema import AppearanceConfig, TransformConfig, BBox
from pysvg.components.base import BaseSVGComponent, ComponentConfig
from pydantic import Field


class EllipseConfig(ComponentConfig):
    """Geometry configuration for Ellipse components."""

    cx: float = Field(default=100, description="Ellipse center X coordinate")
    cy: float = Field(default=50, description="Ellipse center Y coordinate")
    rx: float = Field(default=100, gt=0, description="Ellipse X-axis radius (must be positive)")
    ry: float = Field(default=50, gt=0, description="Ellipse Y-axis radius (must be positive)")

    @override
    def to_svg_dict(self) -> dict[str, str]:
        """Convert config parameters to SVG attributes dictionary."""
        attrs = self.model_dump(exclude_none=True)
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
            config=config or EllipseConfig(),
            appearance=appearance or AppearanceConfig(),
            transform=transform or TransformConfig(),
        )

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        return (self.config.cx, self.config.cy)

    @override
    def get_bounding_box(self) -> BBox:
        return BBox(
            x=self.transform.translate[0] + self.config.cx - self.config.rx,
            y=self.transform.translate[1] + self.config.cy - self.config.ry,
            width=2 * self.config.rx,
            height=2 * self.config.ry,
        )

    @override
    def restrict_size(
        self, width: float, height: float, mode: Literal["fit", "force"] = "fit"
    ) -> "Ellipse":
        # For ellipse, width = 2*rx, height = 2*ry
        current_width = 2 * self.config.rx
        current_height = 2 * self.config.ry

        # Calculate scale factors for width and height
        width_scale = width / current_width
        height_scale = height / current_height

        # Use the smaller scale factor to ensure the ellipse fits within both limits
        scale_factor = min(width_scale, height_scale)

        if mode == "fit" and scale_factor >= 1.0:
            return self

        self.config.rx = self.config.rx * scale_factor
        self.config.ry = self.config.ry * scale_factor

        return self

    @override
    def to_svg_element(self) -> str:
        attrs = self.get_attr_dict()
        attrs_ls = [f'{k}="{v}"' for k, v in attrs.items()]
        return f"<ellipse {' '.join(attrs_ls)} />"

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
