from typing import Literal, Tuple

from pysvg.constants import INDENT
from pysvg.components.content import TextContent
from pysvg.schema import AppearanceConfig, TransformConfig, BBox
from pysvg.components.base import BaseSVGComponent
from pysvg.components.rectangle import Rectangle, RectangleConfig
from pysvg.logger import get_logger
from pydantic import Field
from typing_extensions import override

_logger = get_logger(__name__)


class CellConfig(RectangleConfig):
    """Configuration for Cell components, extends Rectangle config."""

    model_config = {"arbitrary_types_allowed": True}

    embed_component: BaseSVGComponent = Field(
        default=TextContent(""),
        description="Component to embed inside the cell",
    )
    padding: float = Field(default=5, ge=0, description="Padding around the embedded component")

    @override
    def to_svg_dict(self) -> dict[str, str]:
        return {}


class Cell(BaseSVGComponent):
    """
    Cell Component - A rectangle that contains another SVG component

    The cell will automatically:
    1. Scale the embedded component to fit within the cell (considering padding)
    2. Center the embedded component within the cell
    3. Render both the cell background and the embedded component
    """

    def __init__(
        self,
        config: CellConfig,
        appearance: AppearanceConfig | None = None,
        transform: TransformConfig | None = None,
    ):
        super().__init__(
            config=config,
            transform=transform or TransformConfig(),
        )

        # Create the background rectangle
        self._rectangle = Rectangle(
            config=RectangleConfig(
                x=self.config.x,
                y=self.config.y,
                width=self.config.width,
                height=self.config.height,
                rx=self.config.rx,
                ry=self.config.ry,
            ),
            appearance=appearance,
        )

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        """Get the central point of the cell (same as rectangle)."""
        cpx = self.config.x + self.config.width / 2
        cpy = self.config.y + self.config.height / 2
        return (cpx, cpy)

    @override
    def get_bounding_box(self) -> BBox:
        """Get the bounding box of the cell (same as rectangle)."""
        if isinstance(self.config.embed_component, TextContent):
            _logger.warning("TextContent may exceed the cell's bounding box")
        return BBox(
            x=self.transform.translate[0] + self.config.x,
            y=self.transform.translate[1] + self.config.y,
            width=self.config.width,
            height=self.config.height,
        )

    @override
    def restrict_size(
        self, width: float, height: float, mode: Literal["fit", "force"] = "fit"
    ) -> "Cell":
        self._rectangle.restrict_size(width, height, mode)

        self.config.width = self._rectangle.config.width
        self.config.height = self._rectangle.config.height
        if self.config.rx is not None:
            self.config.rx = self._rectangle.config.rx
        if self.config.ry is not None:
            self.config.ry = self._rectangle.config.ry

        try:
            self.config.embed_component.restrict_size(width, height, mode)
        except (NotImplementedError, RuntimeWarning):
            _logger.warning(
                f"Can't restrict the size of the embedded component {self.config.embed_component.__class__.__name__}, "
                "will keep the original size",
            )
        return self

    @override
    def to_svg_element(self) -> str:
        """
        Generate the SVG element for the cell.

        Returns a group element containing the rectangle background
        and the embedded component.
        """
        elements = []

        # Add the rectangle background
        elements.append(self._rectangle.to_svg_element())

        # Add the embedded component if it exists
        if self.has_embedded_component():
            self.set_embed_component()
            elements.append(self.config.embed_component.to_svg_element())

        attr = self.get_attr_str()
        svg_code = "\n".join(elements)
        # If no transform or single element, return joined elements
        return f"<g {attr}>\n{svg_code}".replace("\n", "\n" + INDENT) + "\n</g>"

    def has_embedded_component(self) -> bool:
        """Check if cell has an embedded component."""
        return self.config.embed_component is not None

    def get_embedded_component(self) -> BaseSVGComponent | None:
        """Get the embedded component."""
        return self.config.embed_component

    def set_embed_component(self) -> None:
        """
        Process the embedded component by scaling it to fit within the cell
        and centering it within the cell boundaries.
        """
        self.config: CellConfig

        if not self.has_embedded_component():
            return

        # Calculate available space (cell size minus padding)
        available_width = self.config.width - 2 * self.config.padding
        available_height = self.config.height - 2 * self.config.padding

        # Ensure available space is positive
        if available_width <= 0 or available_height <= 0:
            raise ValueError("Available space should be positive")

        # Restrict the embedded component's size to fit within available space
        try:
            self.config.embed_component.restrict_size(available_width, available_height)
        except (NotImplementedError, RuntimeWarning):
            _logger.warning(
                f"Can't restrict the size of the embedded component {self.config.embed_component.__class__.__name__} since we can't get the get_bounding_box method"
            )

        # Calculate the center position of the cell
        # Note: Do not use self.central_point, otherwise when using cell.move,
        #       embed_component will be moved twice (once in cell.move, once in embed_component.move)
        cell_center_x_relative, cell_center_y_relative = self.central_point_relative

        # Get the embedded component's bounding box after scaling
        try:
            self.config.embed_component.move(cell_center_x_relative, cell_center_y_relative)
        except (NotImplementedError, RuntimeWarning) as e:
            raise RuntimeError(
                f"Can't embed component {self.config.embed_component.__class__.__name__} since we can't determine the central point of the component"
            ) from e


class CellCenterLocate(Cell):
    pass


class CellLeftTopLocate(Cell):
    """NOTE: Hacking implementation, used for matrix"""

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        cpx = self.config.x
        cpy = self.config.y
        return (cpx, cpy)

    @override
    def set_cpoint_to_lefttop(self) -> "Cell":
        self = super().set_cpoint_to_lefttop()
        return self.move_by(-self.config.width / 2, -self.config.height / 2)


class CellLeftBottomLocate(Cell):
    """NOTE: Hacking implementation, used for matrix"""

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        cpx = self.config.x
        cpy = self.config.y + self.config.height
        return (cpx, cpy)

    @override
    def set_cpoint_to_lefttop(self) -> "Cell":
        self = super().set_cpoint_to_lefttop()
        return self.move_by(-self.config.width / 2, self.config.height / 2)


class CellRightTopLocate(Cell):
    """NOTE: Hacking implementation, used for matrix"""

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        cpx = self.config.x + self.config.width
        cpy = self.config.y
        return (cpx, cpy)

    @override
    def set_cpoint_to_lefttop(self) -> "Cell":
        self = super().set_cpoint_to_lefttop()
        return self.move_by(self.config.width / 2, -self.config.height / 2)


class CellRightBottomLocate(Cell):
    """NOTE: Hacking implementation, used for matrix"""

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        cpx = self.config.x + self.config.width
        cpy = self.config.y + self.config.height
        return (cpx, cpy)

    @override
    def set_cpoint_to_lefttop(self) -> "Cell":
        self = super().set_cpoint_to_lefttop()
        return self.move_by(self.config.width / 2, self.config.height / 2)
