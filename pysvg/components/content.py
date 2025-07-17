from typing import Literal, Tuple
from pydantic import Field
from typing_extensions import override

from pysvg.schema import TransformConfig, Color, BBox, ComponentConfig
from pysvg.components.base import BaseSVGComponent
from pysvg.logger import get_logger
import xml.etree.ElementTree as ET
from pathlib import Path
import hashlib


class TextConfig(ComponentConfig):
    """Geometry configuration for Text components"""

    x: float = Field(
        default=0, description="Text x position , central(default) or left-upper corner)"
    )
    y: float = Field(
        default=0, description="Text y position , central(default) or left-upper corner)"
    )
    font_size: float = Field(default=12, ge=0, description="Font size")
    font_family: str = Field(default="Arial", description="Font family")
    color: Color = Field(default=Color("black"), description="Text color")
    text_anchor: Literal["start", "middle", "end"] = Field(
        default="middle", description="Text alignment"
    )
    dominant_baseline: Literal["auto", "middle", "hanging", "central"] = Field(
        default="central", description="Vertical text alignment"
    )

    @override
    def to_svg_dict(self) -> dict[str, str]:
        attrs = self.model_dump(exclude_none=True)
        attrs = {k: str(v) for k, v in attrs.items()}
        attrs = {
            k.replace("_", "-")
            if k in ["text_anchor", "dominant_baseline", "font_size", "font_family"]
            else k: v
            for k, v in attrs.items()
        }
        if "color" in attrs:
            attrs["fill"] = attrs.pop("color")
        return attrs


class ImageConfig(ComponentConfig):
    """Geometry configuration for Image components"""

    x: float = Field(default=0, description="Image x position")
    y: float = Field(default=0, description="Image y position")
    width: float = Field(default=200, ge=0, description="Image width")
    height: float = Field(default=200, ge=0, description="Image height")
    preserveAspectRatio: str = Field(
        default="xMidYMid meet", description="How to preserve aspect ratio"
    )

    @override
    def to_svg_dict(self) -> dict[str, str]:
        attrs = self.model_dump(exclude_none=True)
        attrs = {k: str(v) for k, v in attrs.items()}
        return attrs


class TextContent(BaseSVGComponent):
    """Text content component for SVG"""

    def __init__(
        self, text: str, config: TextConfig | None = None, transform: TransformConfig | None = None
    ):
        super().__init__(config=config or TextConfig(), transform=transform or TransformConfig())
        self.text = text

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        _logger = get_logger(self.__class__.__name__)
        if self.config.dominant_baseline != "central":
            raise RuntimeWarning(
                "When dominant_baseline is not central, we can't determine the relative central point of the text"
            )

        if self.config.text_anchor == "start":
            _logger.warning(
                "Text anchor is start, which means we will use the **middle left part** of the text box as the center point",
            )
        elif self.config.text_anchor == "end":
            _logger.warning(
                "Text anchor is end, which means we will use the **middle right part** of the text box as the center point"
            )

        return (self.config.x, self.config.y)

    @override
    def get_bounding_box(self) -> BBox:
        raise RuntimeWarning(
            "Can't get bounding box of text content since we can't determine the size of the text"
        )

    @override
    def restrict_size(
        self, width: float, height: float, mode: Literal["fit", "force"] = "fit"
    ) -> "TextContent":
        raise RuntimeWarning(
            "Can't restrict size of text content since we can't determine the size of the text"
        )

    @override
    def to_svg_element(self) -> str:
        attrs = self.get_attr_dict()
        attrs_ls = [f'{k}="{v}"' for k, v in attrs.items()]
        return f"<text {' '.join(attrs_ls)}>{self.text}</text>"


class ImageContent(BaseSVGComponent):
    """Image content component for SVG"""

    def __init__(
        self, href: str, config: ImageConfig | None = None, transform: TransformConfig | None = None
    ):
        super().__init__(config=config or ImageConfig(), transform=transform or TransformConfig())
        self.href = href

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        center_x = self.config.x + self.config.width / 2
        center_y = self.config.y + self.config.height / 2
        return (center_x, center_y)

    @override
    def get_bounding_box(self) -> BBox:
        return BBox(
            x=self.transform.translate[0] + self.config.x,
            y=self.transform.translate[1] + self.config.y,
            width=self.config.width,
            height=self.config.height,
        )

    @override
    def restrict_size(
        self, width: float, height: float, mode: Literal["fit", "force"] = "fit"
    ) -> "ImageContent":
        ratio = min(width / self.config.width, height / self.config.height)
        if mode == "fit" and ratio >= 1.0:
            return self
        self.config.width = self.config.width * ratio
        self.config.height = self.config.height * ratio
        return self

    @override
    def to_svg_element(self) -> str:
        attrs = self.get_attr_dict()
        attrs["href"] = self.href
        attrs_ls = [f'{k}="{v}"' for k, v in attrs.items()]
        return f"<image {' '.join(attrs_ls)} />"


class SVGContent(BaseSVGComponent):
    """SVG content component for embedding external SVG files"""

    def __init__(
        self,
        svg_file_path: str | Path,
        config: ImageConfig | None = None,
        transform: TransformConfig | None = None,
    ):
        super().__init__(config=config or ImageConfig(), transform=transform or TransformConfig())
        self.svg_file_path = Path(svg_file_path)
        self._symbol_id = None
        self._svg_content = None
        self._viewbox = None

    @property
    def symbol_id(self) -> str:
        """Generate a unique symbol ID based on the SVG file name (without extension)"""
        if self._symbol_id is None:
            # Use the file name without extension as the symbol id
            file_stem = self.svg_file_path.stem
            self._symbol_id = f"svg_symbol_{file_stem}"
        return self._symbol_id

    def read_svg_content(self) -> str:
        """Read and process SVG file content for symbol definition"""
        if self._svg_content is not None:
            return self._svg_content

        if not self.svg_file_path.exists():
            raise FileNotFoundError(f"SVG file not found: {self.svg_file_path}")

        with open(self.svg_file_path, "r", encoding="utf-8") as f:
            svg_content = f.read()

        # Parse SVG and extract content between <svg> tags
        try:
            # Remove namespace declarations to avoid conflicts
            root = ET.fromstring(svg_content)

            # Extract viewBox from original SVG if it exists
            viewbox = root.get("viewBox")
            if not viewbox:
                # If no viewBox, create one from width and height
                width = root.get("width", "100")
                height = root.get("height", "100")
                # Remove units like 'px', 'pt', etc.
                import re

                width = re.sub(r"[^0-9.]", "", str(width))
                height = re.sub(r"[^0-9.]", "", str(height))
                viewbox = f"0 0 {width} {height}"

            self._viewbox = viewbox

            # Remove the outer <svg> tag and keep the inner content
            inner_content = []
            for child in root:
                # Convert to string and clean up namespaces
                element_str = ET.tostring(child, encoding="unicode")
                # Remove namespace prefixes and declarations
                element_str = self._clean_namespaces(element_str)
                inner_content.append(element_str)
            self._svg_content = "\n".join(inner_content)
        except ET.ParseError:
            # Fallback: use regex to extract content between <svg> tags
            import re

            svg_match = re.search(r"<svg([^>]*)>(.*?)</svg>", svg_content, re.DOTALL)
            if svg_match:
                svg_attrs = svg_match.group(1)
                content = svg_match.group(2).strip()

                # Extract viewBox from SVG attributes
                viewbox_match = re.search(r'viewBox\s*=\s*["\']([^"\']*)["\']', svg_attrs)
                if viewbox_match:
                    self._viewbox = viewbox_match.group(1)
                else:
                    # Extract width and height
                    width_match = re.search(r'width\s*=\s*["\']?([^"\'>\s]*)["\']?', svg_attrs)
                    height_match = re.search(r'height\s*=\s*["\']?([^"\'>\s]*)["\']?', svg_attrs)
                    width = width_match.group(1) if width_match else "100"
                    height = height_match.group(1) if height_match else "100"
                    # Remove units
                    width = re.sub(r"[^0-9.]", "", str(width))
                    height = re.sub(r"[^0-9.]", "", str(height))
                    self._viewbox = f"0 0 {width} {height}"

                self._svg_content = self._clean_namespaces(content)
            else:
                raise ValueError(f"Invalid SVG content in file: {self.svg_file_path}")

        return self._svg_content

    def _clean_namespaces(self, svg_string: str) -> str:
        """Clean namespace prefixes and declarations from SVG string"""
        import re

        # Remove xmlns declarations
        svg_string = re.sub(r'\s+xmlns:[^=]*="[^"]*"', "", svg_string)
        svg_string = re.sub(r'\s+xmlns="[^"]*"', "", svg_string)

        # Remove namespace prefixes (like ns0:, ns1:, etc.)
        # Handle opening tags: <ns0: -> <
        svg_string = re.sub(r"<ns\d+:", "<", svg_string)
        # Handle closing tags: </ns0: -> </
        svg_string = re.sub(r"</ns\d+:", "</", svg_string)

        # Clean up any extra whitespace
        svg_string = re.sub(r"\s+", " ", svg_string)
        svg_string = svg_string.strip()

        return svg_string

    def get_symbol_definition(self) -> str:
        """Generate symbol definition for this SVG"""
        content = self.read_svg_content()
        # Include viewBox in symbol to ensure proper scaling
        return f'<symbol id="{self.symbol_id}" viewBox="{self._viewbox}">\n{content}\n</symbol>'

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        center_x = self.config.x + self.config.width / 2
        center_y = self.config.y + self.config.height / 2
        return (center_x, center_y)

    @override
    def get_bounding_box(self) -> BBox:
        return BBox(
            x=self.transform.translate[0] + self.config.x,
            y=self.transform.translate[1] + self.config.y,
            width=self.config.width,
            height=self.config.height,
        )

    @override
    def restrict_size(
        self, width: float, height: float, mode: Literal["fit", "force"] = "fit"
    ) -> "SVGContent":
        ratio = min(width / self.config.width, height / self.config.height)
        if mode == "fit" and ratio >= 1.0:
            return self
        self.config.width = self.config.width * ratio
        self.config.height = self.config.height * ratio
        return self

    @override
    def to_svg_element(self) -> str:
        """Generate use element that references the symbol"""
        attrs = self.get_attr_dict()
        attrs["href"] = f"#{self.symbol_id}"
        attrs_ls = [f'{k}="{v}"' for k, v in attrs.items()]
        return f"<use {' '.join(attrs_ls)} />"
