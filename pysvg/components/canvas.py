from typing import List, Tuple
from pathlib import Path
from pysvg.schema import ComponentConfig
from pysvg.components.base import BaseSVGComponent, BBox
from pysvg.utils import resolve_path, mkdir
from pydantic import Field
from typing_extensions import override


class CanvasConfig(ComponentConfig):
    """Canvas configuration for Canvas component."""

    width: float = Field(ge=0, description="Canvas width")
    height: float = Field(ge=0, description="Canvas height")
    viewbox: tuple[int, int, int, int] | None = Field(
        default=None,
        description="Optional viewbox (min_x, min_y, width, height) for the SVG viewBox",
    )

    @override
    def to_svg_dict(self) -> dict[str, str]:
        """Convert config parameters to SVG attributes dictionary."""
        attrs = {
            "width": str(self.width),
            "height": str(self.height),
        }
        if self.viewbox is not None:
            attrs["viewBox"] = " ".join(str(x) for x in self.viewbox)
        else:
            attrs["viewBox"] = f"0 0 {self.width} {self.height}"

        attrs.update(
            {"xmlns": "http://www.w3.org/2000/svg", "xmlns:xlink": "http://www.w3.org/1999/xlink"}
        )
        return attrs


class Canvas(BaseSVGComponent):
    """
    A canvas component that can contain and manage other SVG components.
    The canvas acts as a container and can render all its child components.
    """

    def __init__(
        self,
        width: float,
        height: float,
        viewbox: tuple[int, int, int, int] | None = None,
    ):
        config = CanvasConfig(width=width, height=height, viewbox=viewbox)

        super().__init__(config=config)
        self.components: List[BaseSVGComponent] = []

    @property
    @override
    def central_point_relative(self) -> Tuple[float, float]:
        return (
            self.config.width / 2,
            self.config.height / 2,
        )

    @override
    def get_bounding_box(self) -> BBox:
        return BBox(
            x=0,
            y=0,
            width=self.config.width,
            height=self.config.height,
        )

    @override
    def to_svg_element(self) -> str:
        """
        Generate the complete SVG element string including all child components.

        Returns:
            Complete SVG element as XML string
        """
        # Start with XML declaration and SVG opening tag with namespace and viewBox
        svg_attrs = self.get_attr_dict()

        # Convert attributes to string
        attrs_str = " ".join([f'{k}="{v}"' for k, v in svg_attrs.items() if v is not None])

        # Start with XML declaration
        svg = '<?xml version="1.0" encoding="UTF-8"?>\n'

        # Add SVG tag
        svg += f"<svg {attrs_str}>\n"

        # Add all child components
        for component in self.components:
            svg += f"    {component.to_svg_element()}\n"

        # Close SVG tag
        svg += "</svg>"

        return svg

    def add(self, component: BaseSVGComponent) -> "Canvas":
        """
        Add a component to the canvas.

        Args:
            component: The SVG component to add

        Returns:
            Self for method chaining
        """
        self.components.append(component)
        return self

    def save(self, file_path: str | Path) -> None:
        """
        Save the SVG content to a file.

        Args:
            file_path: Path to save the SVG file (must have .svg extension)

        Raises:
            ValueError: If the file path doesn't have .svg extension
        """
        # Convert to Path object for easier handling
        path = resolve_path(file_path, as_path=True)

        # Validate file extension
        if path.suffix != ".svg":
            raise ValueError(f"File path must have .svg extension, got: {path.suffix}")

        # Create parent directories if they don't exist
        mkdir(path.parent)

        # Write SVG content to file
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_svg_element())
