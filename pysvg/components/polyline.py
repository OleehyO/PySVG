from typing import List, Tuple, Literal
from typing_extensions import override

from pysvg.schema import AppearanceConfig, TransformConfig, BBox
from pysvg.components.base import BaseSVGComponent, ComponentConfig
from pydantic import Field, field_validator


class PolylineConfig(ComponentConfig):
    """Geometry configuration for Polyline components."""

    points: List[Tuple[float, float]] = Field(
        default_factory=list, description="List of (x, y) coordinate tuples defining the polyline"
    )

    @field_validator("points")
    def validate_points(cls, v):
        if not v:
            raise ValueError("Polyline must have at least one point")
        for i, point in enumerate(v):
            if not isinstance(point, (tuple, list)) or len(point) != 2:
                raise ValueError(f"Point {i} must be a tuple/list of two numbers, got {point}")
            if not all(isinstance(coord, (int, float)) for coord in point):
                raise ValueError(f"Point {i} coordinates must be numbers, got {point}")
        return v

    @override
    def to_svg_dict(self) -> dict[str, str]:
        """Convert config parameters to SVG attributes dictionary."""
        attrs = {}
        if self.points:
            points_str = " ".join(f"{x},{y}" for x, y in self.points)
            attrs["points"] = points_str
        return attrs


class Polyline(BaseSVGComponent):
    """
    SVG Polyline Component
    """

    def __init__(
        self,
        config: PolylineConfig | None = None,
        appearance: AppearanceConfig | None = None,
        transform: TransformConfig | None = None,
    ):
        super().__init__(
            config=config or PolylineConfig(),
            appearance=appearance or AppearanceConfig(),
            transform=transform or TransformConfig(),
        )

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        if not self.config.points:
            return (0, 0)

        total_x = sum(x for x, y in self.config.points)
        total_y = sum(y for x, y in self.config.points)
        count = len(self.config.points)

        return (total_x / count, total_y / count)

    @override
    def get_bounding_box(self) -> BBox:
        if not self.config.points:
            return BBox(x=0, y=0, width=0, height=0)

        x_coords = [x for x, y in self.config.points]
        y_coords = [y for x, y in self.config.points]

        return BBox(
            x=self.transform.translate[0] + min(x_coords),
            y=self.transform.translate[1] + min(y_coords),
            width=max(x_coords) - min(x_coords),
            height=max(y_coords) - min(y_coords),
        )

    @override
    def restrict_size(
        self, width: float, height: float, mode: Literal["fit", "force"] = "fit"
    ) -> "Polyline":
        if not self.config.points:
            return self

        current_width = self.get_bounding_box().width
        current_height = self.get_bounding_box().height

        # Calculate scale factors for width and height
        width_scale = width / current_width if current_width > 0 else float("inf")
        height_scale = height / current_height if current_height > 0 else float("inf")

        # Use the smaller scale factor to ensure the polyline fits within both limits
        scale_factor = min(width_scale, height_scale)

        if mode == "fit" and scale_factor >= 1.0:
            return self

        # Get current center point
        center_x, center_y = self.central_point_relative

        # Scale all points relative to the center
        scaled_points = []
        for x, y in self.config.points:
            # Calculate offset from center
            dx = x - center_x
            dy = y - center_y

            # Scale the offset
            scaled_dx = dx * scale_factor
            scaled_dy = dy * scale_factor

            # Calculate new position
            new_x = center_x + scaled_dx
            new_y = center_y + scaled_dy

            scaled_points.append((new_x, new_y))

        self.config.points = scaled_points
        return self

    @override
    def to_svg_element(self) -> str:
        attrs = self.get_attr_dict()
        attrs_ls = [f'{k}="{v}"' for k, v in attrs.items()]
        return f"<polyline {' '.join(attrs_ls)} />"

    def get_total_length(self) -> float:
        """
        Calculate the total length of the polyline

        Returns:
            Total polyline length
        """
        if len(self.config.points) < 2:
            return 0.0

        import math

        total_length = 0.0

        for i in range(len(self.config.points) - 1):
            x1, y1 = self.config.points[i]
            x2, y2 = self.config.points[i + 1]
            dx = x2 - x1
            dy = y2 - y1
            segment_length = math.sqrt(dx**2 + dy**2)
            total_length += segment_length

        return total_length

    def get_segment_lengths(self) -> List[float]:
        """
        Calculate the length of each segment in the polyline

        Returns:
            List of segment lengths
        """
        if len(self.config.points) < 2:
            return []

        import math

        lengths = []

        for i in range(len(self.config.points) - 1):
            x1, y1 = self.config.points[i]
            x2, y2 = self.config.points[i + 1]
            dx = x2 - x1
            dy = y2 - y1
            segment_length = math.sqrt(dx**2 + dy**2)
            lengths.append(segment_length)

        return lengths

    def add_point(self, x: float, y: float) -> "Polyline":
        """
        Add a point to the polyline

        Args:
            x: X coordinate of the new point
            y: Y coordinate of the new point

        Returns:
            Self for method chaining
        """
        self.config.points.append((x, y))
        return self

    def add_points(self, points: List[Tuple[float, float]]) -> "Polyline":
        """
        Add multiple points to the polyline

        Args:
            points: List of (x, y) coordinate tuples

        Returns:
            Self for method chaining
        """
        self.config.points.extend(points)
        return self

    def clear_points(self) -> "Polyline":
        """
        Clear all points from the polyline

        Returns:
            Self for method chaining
        """
        self.config.points.clear()
        return self

    def get_point_count(self) -> int:
        """
        Get the number of points in the polyline

        Returns:
            Number of points
        """
        return len(self.config.points)
