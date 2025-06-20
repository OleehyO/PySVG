from typing import List, Tuple
from typing_extensions import override

from pysvg.schema import AppearanceConfig, TransformConfig
from pysvg.components.base import BaseSVGComponent, BaseSVGConfig
from pydantic import Field, field_validator


class PolylineConfig(BaseSVGConfig):
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
            config=config if config else PolylineConfig(),
            appearance=appearance if appearance else AppearanceConfig(),
            transform=transform if transform else TransformConfig(),
        )

    @override
    @property
    def central_point(self) -> Tuple[float, float]:
        if not self.config.points:
            return (0, 0)

        total_x = sum(x for x, y in self.config.points)
        total_y = sum(y for x, y in self.config.points)
        count = len(self.config.points)

        return (total_x / count, total_y / count)

    @override
    def restrict_size(self, max_width: float, max_height: float) -> "Polyline":
        """
        Restrict the size of the polyline to a maximum width and height.

        Args:
            max_width: Maximum width
            max_height: Maximum height

        Returns:
            Self for method chaining
        """
        # Calculate current bounding box dimensions
        min_x, min_y, max_x, max_y = self.get_bounding_box()
        current_width = max_x - min_x
        current_height = max_y - min_y

        # Handle edge case: if polyline has no area (all points are the same)
        if current_width == 0 and current_height == 0:
            return self  # No scaling needed for a point

        # Calculate scale factors for both dimensions
        width_scale = max_width / current_width if current_width > max_width else 1.0
        height_scale = max_height / current_height if current_height > max_height else 1.0

        # Use the smaller scale to ensure the polyline fits within both limits
        scale_factor = min(width_scale, height_scale)

        if scale_factor < 1.0:
            # Apply uniform scale to maintain polyline proportions
            self.scale(scale_factor)

        return self

    @override
    def to_svg_element(self) -> str:
        """
        Generate complete SVG polyline element string

        Returns:
            XML string of SVG polyline element
        """
        attrs = {}
        attrs.update(self.config.to_svg_dict())
        attrs.update(self.appearance.to_svg_dict())
        attrs.update(self.transform.to_svg_dict())
        attr_strings = [f'{key}="{value}"' for key, value in attrs.items()]
        return f"<polyline {' '.join(attr_strings)} />"

    def get_bounding_box(self) -> Tuple[float, float, float, float]:
        """
        Get polyline's bounding box (without considering transformations)

        Returns:
            (min_x, min_y, max_x, max_y) bounding box coordinates
        """
        if not self.config.points:
            return (0, 0, 0, 0)

        x_coords = [x for x, y in self.config.points]
        y_coords = [y for x, y in self.config.points]

        return (min(x_coords), min(y_coords), max(x_coords), max(y_coords))

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
