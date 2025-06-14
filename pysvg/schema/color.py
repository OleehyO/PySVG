import re

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_serializer,
    model_validator,
    ConfigDict,
)

from pysvg.constants import SVG_NONE


class Color(BaseModel):
    """SVG color type that supports multiple color formats"""

    model_config = ConfigDict(extra="forbid")

    value: str = Field(..., description="Color value")

    def __init__(self, value: str | dict | None = None, **data):
        if isinstance(value, str):
            super().__init__(value=value)
        else:
            super().__init__(value=value, **data)

    @model_validator(mode="before")
    @classmethod
    def validate_input(cls, data):
        """Allow initialization with a single string argument"""
        if isinstance(data, str):
            return {"value": data}
        return data

    @field_validator("value")
    def validate_color(cls, v: str) -> str:
        """Validate color format"""
        if v is None:
            return v

        v = v.strip()

        # Special values
        if v.lower() in [SVG_NONE, "transparent", "currentcolor", "inherit"]:
            return v.lower()

        # CSS color names (basic colors)
        css_colors = {
            "black",
            "silver",
            "gray",
            "white",
            "maroon",
            "red",
            "purple",
            "fuchsia",
            "green",
            "lime",
            "olive",
            "yellow",
            "navy",
            "blue",
            "teal",
            "aqua",
            "orange",
            "aliceblue",
            "antiquewhite",
            "aquamarine",
            "azure",
            "beige",
            "bisque",
            "blanchedalmond",
            "blueviolet",
            "brown",
            "burlywood",
            "cadetblue",
            "chartreuse",
            "chocolate",
            "coral",
            "cornflowerblue",
            "cornsilk",
            "crimson",
            "cyan",
            "darkblue",
            "darkcyan",
            "darkgoldenrod",
            "darkgray",
            "darkgreen",
            "darkkhaki",
            "darkmagenta",
            "darkolivegreen",
            "darkorange",
            "darkorchid",
            "darkred",
            "darksalmon",
            "darkseagreen",
            "darkslateblue",
            "darkslategray",
            "darkturquoise",
            "darkviolet",
            "deeppink",
            "deepskyblue",
            "dimgray",
            "dodgerblue",
            "firebrick",
            "floralwhite",
            "forestgreen",
            "gainsboro",
            "ghostwhite",
            "gold",
            "goldenrod",
            "greenyellow",
            "honeydew",
            "hotpink",
            "indianred",
            "indigo",
            "ivory",
            "khaki",
            "lavender",
            "lavenderblush",
            "lawngreen",
            "lemonchiffon",
            "lightblue",
            "lightcoral",
            "lightcyan",
            "lightgoldenrodyellow",
            "lightgray",
            "lightgreen",
            "lightpink",
            "lightsalmon",
            "lightseagreen",
            "lightskyblue",
            "lightslategray",
            "lightsteelblue",
            "lightyellow",
            "limegreen",
            "linen",
            "magenta",
            "mediumaquamarine",
            "mediumblue",
            "mediumorchid",
            "mediumpurple",
            "mediumseagreen",
            "mediumslateblue",
            "mediumspringgreen",
            "mediumturquoise",
            "mediumvioletred",
            "midnightblue",
            "mintcream",
            "mistyrose",
            "moccasin",
            "navajowhite",
            "oldlace",
            "olivedrab",
            "orangered",
            "orchid",
            "palegoldenrod",
            "palegreen",
            "paleturquoise",
            "palevioletred",
            "papayawhip",
            "peachpuff",
            "peru",
            "pink",
            "plum",
            "powderblue",
            "rosybrown",
            "royalblue",
            "saddlebrown",
            "salmon",
            "sandybrown",
            "seagreen",
            "seashell",
            "sienna",
            "skyblue",
            "slateblue",
            "slategray",
            "snow",
            "springgreen",
            "steelblue",
            "tan",
            "thistle",
            "tomato",
            "turquoise",
            "violet",
            "wheat",
            "whitesmoke",
            "yellowgreen",
        }

        if v.lower() in css_colors:
            return v.lower()

        # Hexadecimal colors (#RGB, #RRGGBB, #RGBA, #RRGGBBAA)
        hex_pattern = r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{8})$"
        if re.match(hex_pattern, v):
            return v.upper()

        # RGB/RGBA function format
        rgb_pattern = r"^rgba?\s*\(\s*(\d+(?:\.\d+)?%?)\s*,\s*(\d+(?:\.\d+)?%?)\s*,\s*(\d+(?:\.\d+)?%?)(?:\s*,\s*(\d+(?:\.\d+)?))?\s*\)$"
        if re.match(rgb_pattern, v, re.IGNORECASE):
            return v.lower()

        # HSL/HSLA function format
        hsl_pattern = r"^hsla?\s*\(\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?%)\s*,\s*(\d+(?:\.\d+)?%)(?:\s*,\s*(\d+(?:\.\d+)?))?\s*\)$"
        if re.match(hsl_pattern, v, re.IGNORECASE):
            return v.lower()

        raise ValueError(
            f"Invalid color format: '{v}'. Supported formats: color names, #hex, rgb(), rgba(), hsl(), hsla(), 'none', 'transparent'"
        )

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f'Color("{self.value}")'

    @model_serializer
    def serialize_model(self) -> str:
        """Serialize the Color object as a string value instead of a dict"""
        return self.value
