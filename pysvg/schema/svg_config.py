from typing import Any, List, Literal, Tuple, Union
from abc import abstractmethod, ABC

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing_extensions import override

from .color import Color
from pysvg.constants import SVG_NONE

# NOTE: DO NOT CHANGE THESE DEFAULT VALUES
TRANSLATE_DEFAULT = (0, 0)
ROTATE_DEFAULT = (0, 0, 0)
SKEW_X_DEFAULT = 0
SKEW_Y_DEFAULT = 0

FILL_DEFAULT = Color(SVG_NONE)
FILL_OPACITY_DEFAULT = 1

STROKE_DEFAULT = Color(SVG_NONE)
STROKE_WIDTH_DEFAULT = 1
STROKE_OPACITY_DEFAULT = 1
STROKE_DASHARRAY_DEFAULT = []
STROKE_LINECAP_DEFAULT = "butt"


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
    fill: Color = Field(default=FILL_DEFAULT)

    # Fill opacity
    fill_opacity: float = Field(default=FILL_OPACITY_DEFAULT, ge=0.0, le=1.0)

    # Stroke color
    stroke: Color = Field(default=STROKE_DEFAULT)

    # Stroke width
    stroke_width: float = Field(default=STROKE_WIDTH_DEFAULT, ge=0.0)

    # Stroke opacity
    stroke_opacity: float = Field(default=STROKE_OPACITY_DEFAULT, ge=0.0, le=1.0)

    # Stroke dash pattern, representing lengths of solid and blank segments
    stroke_dasharray: List[float] = Field(default=STROKE_DASHARRAY_DEFAULT)

    # Stroke line cap style
    stroke_linecap: Literal["butt", "round", "square"] = Field(default=STROKE_LINECAP_DEFAULT)

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
            if key not in self.model_fields_set:
                continue

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
        return AppearanceConfig()


class TransformConfig(BaseSVGConfig):
    """Transform configuration for SVG graphics"""

    # Translation transform. Format: (tx, ty) representing translation amounts in x and y directions
    translate: Tuple[float, float] = Field(default=TRANSLATE_DEFAULT)

    # Rotation transform. Can be an angle value (rotate around origin) or triple (angle, cx, cy) (rotate around specified point)
    rotate: Union[float, Tuple[float, float, float]] = Field(default=ROTATE_DEFAULT)

    # X-axis skew transform angle
    skew_x: float = Field(default=SKEW_X_DEFAULT)

    # Y-axis skew transform angle
    skew_y: float = Field(default=SKEW_Y_DEFAULT)

    @override
    def to_svg_dict(self) -> dict[str, str]:
        """Generate SVG transform attribute value"""
        transform_parts = []

        if "translate" in self.model_fields_set and self.translate != TRANSLATE_DEFAULT:
            tx, ty = self.translate
            transform_parts.append(f"translate({tx},{ty})")

        if "rotate" in self.model_fields_set and self.rotate != ROTATE_DEFAULT:
            if isinstance(self.rotate, (int, float)):
                transform_parts.append(f"rotate({self.rotate})")
            else:
                angle, cx, cy = self.rotate
                transform_parts.append(f"rotate({angle},{cx},{cy})")

        if "skew_x" in self.model_fields_set and self.skew_x != SKEW_X_DEFAULT:
            transform_parts.append(f"skewX({self.skew_x})")

        if "skew_y" in self.model_fields_set and self.skew_y != SKEW_Y_DEFAULT:
            transform_parts.append(f"skewY({self.skew_y})")

        if transform_parts:
            return {"transform": " ".join(transform_parts)}
        else:
            return {}

    def reset(self) -> None:
        """Reset the transform to the default values"""
        return TransformConfig()

    def have_set(self) -> bool:
        return len(self.model_fields_set) != 0
