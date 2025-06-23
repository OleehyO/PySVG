from typing import Literal, Tuple
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
    def get_bounding_box(self) -> BBox:
        return BBox(
            x=self.transform.translate[0] + self.config.cx - self.config.r,
            y=self.transform.translate[1] + self.config.cy - self.config.r,
            width=2 * self.config.r,
            height=2 * self.config.r,
        )

    @override
    def restrict_size(
        self, width: float, height: float, mode: Literal["fit", "force"] = "fit"
    ) -> "Circle":
        # For a circle, both width and height equal the diameter (2 * r)
        current_diameter = 2 * self.config.r

        # Use the smaller dimension to ensure the circle fits within both limits
        target_diameter = min(width, height)

        if mode == "fit":
            # Only scale down if the current diameter is larger than target
            if current_diameter > target_diameter:
                self.config.r = target_diameter / 2
        elif mode == "force":
            # Scale to exactly match the target diameter, regardless of current size
            self.config.r = target_diameter / 2

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
