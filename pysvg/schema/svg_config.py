from typing import Any, List, Literal, Tuple, Union
from abc import abstractmethod, ABC

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing_extensions import override

from pysvg.constants import SVG_NONE

from .color import Color


class BaseSVGConfig(BaseModel, ABC):
    """Base configuration for SVG graphics"""

    model_config = ConfigDict(extra="forbid")

    @abstractmethod
    def to_svg_dict(self) -> dict[str, str]:
        """Convert config parameters to SVG attributes dictionary."""
        raise NotImplementedError("Not implemented")


class ComponentConfig(BaseSVGConfig):
    """Base configuration for all components"""

    @override
    def to_svg_dict(self) -> dict[str, str]:
        """**Different component has different attributes name**, so this method is not implemented"""
        raise NotImplementedError("Not implemented")


class AppearanceConfig(BaseSVGConfig):
    """Appearance configuration for SVG graphics"""

    # Fill color - set to "none" for no fill instead of SVG default "black"
    fill: Color = Color(SVG_NONE)

    # Fill opacity
    fill_opacity: float = Field(1.0, ge=0.0, le=1.0)

    # Stroke color
    stroke: Color = Color("black")

    # Stroke width
    stroke_width: float = Field(1.0, ge=0.0)

    # Stroke opacity
    stroke_opacity: float = Field(1.0, ge=0.0, le=1.0)

    # Stroke dash pattern, representing lengths of solid and blank segments
    stroke_dasharray: List[float] | None = None

    # Stroke line cap style
    stroke_linecap: Literal["butt", "round", "square"] = "butt"

    @field_validator("stroke_dasharray")
    def validate_stroke_dasharray(cls, v):
        if v is not None:
            # Validate that all values in the list are non-negative
            for val in v:
                if val < 0:
                    raise ValueError(f"stroke_dasharray values must be non-negative, got {val}")
        return v

    @override
    def to_svg_dict(self) -> dict[str, str]:
        """Convert to SVG attributes dictionary using Pydantic serialization"""
        data = self.model_dump(exclude_none=True)
        svg_attrs = {}

        # Handle attribute name mapping and special conversions
        attr_mapping = {
            "fill_opacity": "fill-opacity",
            "stroke_width": "stroke-width",
            "stroke_opacity": "stroke-opacity",
            "stroke_dasharray": "stroke-dasharray",
            "stroke_linecap": "stroke-linecap",
        }

        for key, value in data.items():
            svg_key = attr_mapping.get(key, key)

            # Special handling for different types of values
            if key == "stroke_dasharray":
                assert isinstance(value, list)
                svg_attrs[svg_key] = ",".join(map(str, value))
            else:
                svg_attrs[svg_key] = str(value)

        return svg_attrs

    def reset(self) -> None:
        """Reset the appearance to the default values"""
        self.fill = Color(SVG_NONE)
        self.fill_opacity = 1.0
        self.stroke = Color("black")
        self.stroke_width = 1.0
        self.stroke_opacity = 1.0
        self.stroke_dasharray = None
        self.stroke_linecap = "butt"


class TransformConfig(BaseSVGConfig):
    """Transform configuration for SVG graphics"""

    # Translation transform. Format: (tx, ty) representing translation amounts in x and y directions
    translate: Tuple[float, float] = (0, 0)

    # Rotation transform. Can be an angle value (rotate around origin) or triple (angle, cx, cy) (rotate around specified point)
    rotate: Union[float, Tuple[float, float, float]] = (0, 0, 0)

    # X-axis skew transform angle
    skew_x: float = 0

    # Y-axis skew transform angle
    skew_y: float = 0

    @override
    def to_svg_dict(self) -> dict[str, str]:
        """Generate SVG transform attribute value"""
        transform_parts = []

        if self.translate is not None:
            tx, ty = self.translate
            transform_parts.append(f"translate({tx},{ty})")

        if self.rotate is not None:
            if isinstance(self.rotate, (int, float)):
                transform_parts.append(f"rotate({self.rotate})")
            else:
                angle, cx, cy = self.rotate
                transform_parts.append(f"rotate({angle},{cx},{cy})")

        if self.skew_x is not None:
            transform_parts.append(f"skewX({self.skew_x})")

        if self.skew_y is not None:
            transform_parts.append(f"skewY({self.skew_y})")

        return {"transform": " ".join(transform_parts) if transform_parts else SVG_NONE}

    def reset(self) -> None:
        """Reset the transform to the default values"""
        self.translate = (0, 0)
        self.rotate = (0, 0, 0)
        self.skew_x = 0
        self.skew_y = 0
        return self
