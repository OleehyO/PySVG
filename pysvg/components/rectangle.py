from typing import Tuple
from typing_extensions import override

from pysvg.schema import AppearanceConfig, TransformConfig
from pysvg.components.base import BaseSVGComponent, BaseSVGConfig
from pydantic import Field


class RectangleConfig(BaseSVGConfig):
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
        attrs = super().to_svg_dict()
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
    def central_point(self) -> Tuple[float, float]:
        center_x = self.config.x + self.config.width / 2
        center_y = self.config.y + self.config.height / 2
        return (center_x, center_y)

    @override
    def restrict_size(self, max_width: float, max_height: float) -> "Rectangle":
        current_width = self.config.width
        current_height = self.config.height

        # Calculate scale factors for both dimensions
        width_scale = max_width / current_width if current_width > max_width else 1.0
        height_scale = max_height / current_height if current_height > max_height else 1.0

        # Use the smaller scale to ensure the image fits within both limits
        scale_factor = min(width_scale, height_scale)

        if scale_factor < 1.0:
            # Apply uniform scale to maintain aspect ratio
            self.scale(scale_factor)

        return self

    @override
    def to_svg_element(self) -> str:
        """
        Generate complete SVG rect element string

        Returns:
            XML string of SVG rect element
        """
        attrs = {}
        attrs.update(self.config.to_svg_dict())
        attrs.update(self.appearance.to_svg_dict())
        attrs.update(self.transform.to_svg_dict())
        attr_strings = [f'{key}="{value}"' for key, value in attrs.items()]
        return f"<rect {' '.join(attr_strings)} />"

    def has_rounded_corners(self) -> bool:
        """Check if rectangle has rounded corners"""
        return self.config.rx is not None or self.config.ry is not None

    def get_bounding_box(self) -> Tuple[float, float, float, float]:
        """
        Get rectangle's bounding box (without considering transformations)

        Returns:
            (min_x, min_y, max_x, max_y) bounding box coordinates
        """
        return (
            self.config.x,
            self.config.y,
            self.config.x + self.config.width,
            self.config.y + self.config.height,
        )
