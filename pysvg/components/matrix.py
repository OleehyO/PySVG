from typing import Literal, Tuple
from typing_extensions import override

from pydantic import Field

from pysvg.components.base import BaseSVGComponent, ComponentConfig
from pysvg.components.cell import Cell, CellConfig
from pysvg.components.content import TextConfig, TextContent
from pysvg.schema import AppearanceConfig, Color, TransformConfig, BBox

# Define matrix element data type
MatElemType = str | int | float

# Define border position type
BorderPosition = Literal["upperleft", "upperright", "lowerleft", "lowerright"]


class MatrixConfig(ComponentConfig):
    """Matrix component configuration"""

    x: float = Field(default=0, description="Matrix x position")
    y: float = Field(default=0, description="Matrix y position")
    cell_size: float = Field(default=50, ge=1, description="Size of each cell")
    cell_padding: float = Field(default=5, ge=0, description="Padding inside each cell")

    @override
    def to_svg_dict(self) -> dict[str, str]:
        raise NotImplementedError("MatrixConfig is not implemented")


class Matrix(BaseSVGComponent):
    """
    Matrix Component - Matrix visualization component, implemented based on Cell component
    """

    def __init__(
        self,
        data: list[list[MatElemType]],
        config: MatrixConfig | None = None,
        transform: TransformConfig | None = None,
        element_map: dict[MatElemType, BaseSVGComponent] = {},
        background_map: dict[MatElemType, AppearanceConfig] = {},
        caption: str | None = None,
        caption_location: Literal["top", "down", "left", "right"] | None = None,
        caption_margin: float = 20,
        caption_font_size: float = 16,
        caption_font_family: str = "Arial",
        caption_font_color: Color = Color("black"),
        border_as_number: BorderPosition | None = None,
        coord_font_size: float = 16,
        coord_font_family: str = "Arial",
        coord_font_color: Color = Color("black"),
    ):
        """Creates a Matrix component for visualizing 2D data in SVG format.

        This component allows you to create a matrix visualization where each element can be
        customized with different content and appearance. It supports features like captions
        and border numbering for better data representation.

        Args:
            data (list[list[MatElemType]]): 2D list containing the matrix data. Must be rectangular
                (all rows must have the same length). Elements can be strings, integers, or floats.
            config (MatrixConfig | None, optional): Configuration for the matrix component.
                Defaults to MatrixConfig().
            transform (TransformConfig | None, optional): Transform configuration for the matrix.
                Defaults to TransformConfig().
            element_map (dict[MatElemType, BaseSVGComponent] | None, optional): Maps matrix elements
                to their visual representations. If None, elements are displayed as text.
            background_map (dict[MatElemType, AppearanceConfig] | None, optional): Maps matrix elements
                to their cell background appearances. If None, cells have transparent background.
            caption (str | None, optional): Caption text for the matrix. Must be provided if
                caption_location is set.
            caption_location (Literal["top", "down", "left", "right"] | None, optional): Position of
                the caption relative to the matrix. Must be provided if caption is set.
            caption_margin (float, optional): Space between caption and matrix. Defaults to 20.
            caption_font_size (float, optional): Font size for caption text. Defaults to 16.
            caption_font_family (str, optional): Font family for caption text. Defaults to "Arial".
            caption_font_color (Color, optional): Color for caption text. Defaults to black.
            border_as_number (BorderPosition | None, optional): Position for displaying row/column
                numbers. Can be "upperleft", "upperright", "lowerleft", or "lowerright".
            coord_font_size (float, optional): Font size for border numbers. Defaults to 16.
            coord_font_family (str, optional): Font family for border numbers. Defaults to "Arial".
            coord_font_color (Color, optional): Color for border numbers. Defaults to black.

        Raises:
            ValueError: If the matrix data is not rectangular, or if caption and caption_location
                are not properly paired (both must be either set or None).
        """
        super().__init__(
            config=config or MatrixConfig(),
            transform=transform or TransformConfig(),
        )

        # Verify matrix is rectangular
        rows = len(data)
        cols = len(data[0])
        if not all(len(row) == cols for row in data):
            raise ValueError("Matrix data must be rectangular")

        # Validate caption and caption_location pairing
        if caption is not None and caption_location is None:
            raise ValueError("caption_location must be provided when caption is specified")
        if caption_location is not None and caption is None:
            raise ValueError("caption must be provided when caption_location is specified")

        # Matrix properties
        self._rows = rows
        self._cols = cols
        self._data = data

        # Store element and background maps
        self._element_map = element_map
        self._background_map = background_map

        # Caption related settings
        self._caption = (
            TextContent(
                text=caption,
                config=TextConfig(
                    font_size=caption_font_size,
                    font_family=caption_font_family,
                    color=caption_font_color,
                    text_anchor="middle",
                    dominant_baseline="central",
                ),
            )
            if caption
            else None
        )
        self._caption_location = caption_location
        self._caption_margin = caption_margin

        # border_as_number related settings
        self._border_position: BorderPosition | None = border_as_number
        self._coord_font_size: float = coord_font_size
        self._coord_font_family: str = coord_font_family
        self._coord_color: Color = coord_font_color

    @override
    @property
    def central_point_relative(self) -> Tuple[float, float]:
        if self._border_position is None:
            # No border labeling, use center of entire matrix
            center_x = self.config.x + (self._cols * self.config.cell_size) / 2
            center_y = self.config.y + (self._rows * self.config.cell_size) / 2
        else:
            # With border labeling, need to calculate center of actual content area
            content_cols = self._cols - 1
            content_rows = self._rows - 1
            if self._border_position == "upperleft":
                # Actual content area: excluding row 0 and column 0
                content_start_x = self.config.x + self.config.cell_size  # Start from column 1
                content_start_y = self.config.y + self.config.cell_size  # Start from row 1
            elif self._border_position == "upperright":
                # Actual content area: excluding row 0 and last column
                content_start_x = self.config.x  # Start from column 0
                content_start_y = self.config.y + self.config.cell_size  # Start from row 1
            elif self._border_position == "lowerleft":
                # Actual content area: excluding last row and column 0
                content_start_x = self.config.x + self.config.cell_size  # Start from column 1
                content_start_y = self.config.y  # Start from row 0
            elif self._border_position == "lowerright":
                # Actual content area: excluding last row and last column
                content_start_x = self.config.x  # Start from column 0
                content_start_y = self.config.y  # Start from row 0
            else:
                raise ValueError(f"Invalid border position: {self._border_position}")
            center_x = content_start_x + (content_cols * self.config.cell_size) / 2
            center_y = content_start_y + (content_rows * self.config.cell_size) / 2

        return (center_x, center_y)

    @override
    def get_bounding_box(self) -> BBox:
        matrix_width = self._cols * self.config.cell_size
        matrix_height = self._rows * self.config.cell_size

        min_x = self.config.x
        min_y = self.config.y
        max_x = self.config.x + matrix_width
        max_y = self.config.y + matrix_height

        # Consider caption position
        if self._caption is not None:
            max_y += self.config.caption_margin
            max_x += self.config.caption_margin

        return BBox(
            x=self.transform.translate[0] + min_x,
            y=self.transform.translate[1] + min_y,
            width=max_x - min_x,
            height=max_y - min_y,
        )

    @override
    def to_svg_element(self) -> str:
        elements = []

        self._create_cells()

        # Add all cells
        for row_cells in self._cells:
            for cell in row_cells:
                elements.append(cell.to_svg_element())

        # Add caption
        if self._caption is not None:
            elements.append(self._render_caption())

        # Apply transform
        transform_dict = self.transform.to_svg_dict()
        if "transform" in transform_dict and transform_dict["transform"] != "none":
            return f'<g transform="{transform_dict["transform"]}">{"".join(elements)}</g>'

        return f"<g>{''.join(elements)}</g>"

    def _create_cells(self):
        """Create all Cell components"""
        self._cells: list[list[Cell]] = []

        for i in range(self._rows):
            row_cells = []
            for j in range(self._cols):
                # Get actual element (considering mapping)
                original_elem = self._data[i][j]
                actual_elem: BaseSVGComponent = self._element_map.get(
                    original_elem, TextContent(str(original_elem))
                )
                bg_appearance = self._background_map.get(
                    original_elem, AppearanceConfig(fill=Color("none"), stroke=Color("black"))
                )

                if self._is_border_cell(i, j):
                    bg_appearance = AppearanceConfig(
                        fill=Color("none"), stroke=Color("none"), stroke_width=0
                    )
                    if isinstance(actual_elem, TextContent):
                        actual_elem.config.color = self._coord_color
                        actual_elem.config.font_size = self._coord_font_size
                        actual_elem.config.font_family = self._coord_font_family

                cell = Cell(
                    config=CellConfig(
                        embed_component=actual_elem,
                        padding=self.config.cell_padding,
                        width=self.config.cell_size,
                        height=self.config.cell_size,
                    ),
                    appearance=bg_appearance,
                )
                cell.move(
                    self.config.x + i * self.config.cell_size + self.config.cell_size / 2,
                    self.config.y + j * self.config.cell_size + self.config.cell_size / 2,
                )

                row_cells.append(cell)

            self._cells.append(row_cells)

    def _render_caption(self) -> str:
        """Convert caption to svg code"""
        if self._caption is None or self._caption_location is None:
            raise ValueError(
                "Caption is not set or caption_location is not set, but using _render_caption()"
            )

        self._caption.set_cpoint_to_lefttop()

        # Get matrix center point (considering border labeling effect)
        center_x_relative, center_y_relative = self.central_point_relative

        # Calculate matrix boundaries (for determining caption offset)
        matrix_width = self._cols * self.config.cell_size
        matrix_height = self._rows * self.config.cell_size

        # Adjust coordinates based on position, using center point as reference
        if self._caption_location == "top":
            self._caption.move(center_x_relative, self.config.y - self._caption_margin)
        elif self._caption_location == "down":
            self._caption.move(
                center_x_relative, self.config.y + matrix_height + self._caption_margin
            )
        elif self._caption_location == "left":
            self._caption.config.text_anchor = "end"
            self._caption.move(self.config.x - self._caption_margin, center_y_relative)
        elif self._caption_location == "right":
            self._caption.config.text_anchor = "start"
            self._caption.move(
                self.config.x + matrix_width + self._caption_margin, center_y_relative
            )

        return self._caption.to_svg_element()

    def _is_border_cell(self, row: int, col: int) -> bool:
        """Check if the cell at specified position is a border label cell"""
        if self._border_position is None:
            return False

        if self._border_position == "upperleft":
            return row == 0 or col == 0
        elif self._border_position == "upperright":
            return row == 0 or col == self._cols - 1
        elif self._border_position == "lowerleft":
            return row == self._rows - 1 or col == 0
        elif self._border_position == "lowerright":
            return row == self._rows - 1 or col == self._cols - 1

        return False
