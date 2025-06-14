from typing import Tuple, Literal
from pathlib import Path

from pysvg.schema import AppearanceConfig, TransformConfig, Color, SVGCode
from pysvg.components.base import BaseSVGComponent
from pysvg.components.cell import Cell, CellConfig
from pysvg.components.content import TextConfig, ImageConfig, SVGConfig, TextContent
from pydantic import BaseModel, Field


# Define matrix element data type
MatElemType = str | int | float | Path | SVGCode

# Define border position type
BorderPosition = Literal["upperleft", "upperright", "lowerleft", "lowerright"]


class MatrixConfig(BaseModel):
    """Matrix component configuration"""

    x: float = Field(default=0, description="Matrix x position")
    y: float = Field(default=0, description="Matrix y position")
    cell_size: float = Field(default=50, ge=1, description="Size of each cell")
    cell_padding: float = Field(default=5, ge=0, description="Padding inside each cell")


class Matrix(BaseSVGComponent):
    """
    Matrix Component - Matrix visualization component, implemented based on Cell component
    """

    def __init__(
        self,
        data: list[list[MatElemType]],
        element_map: dict[MatElemType, MatElemType] | None = None,
        appearance_matrix: list[list[AppearanceConfig]] | None = None,
        element_appearance_map: dict[MatElemType, AppearanceConfig] | None = None,
        caption: TextContent | None = None,
        caption_location: Literal["top", "down", "left", "right"] | None = None,
        border_as_number: BorderPosition | None = None,
        coord_font_size: float | None = None,
        coord_font_family: str | None = None,
        coord_color: Color | None = None,
        config: MatrixConfig | None = None,
        transform: TransformConfig | None = None,
    ):
        """
        Initialize Matrix component

        Args:
            data: 2D list, each element is one of Path/str/SVGCode
            element_map: Element mapping, replaces corresponding elements in data
            appearance_matrix: 2D list of AppearanceConfig, sets appearance for each cell
            element_appearance_map: Element appearance mapping, sets appearance based on element content
            caption: Text description
            caption_location: Description position
            border_as_number: Border position, specifies which corner's rows and columns are used for coordinate labeling
            coord_font_size: Font size for coordinate labels
            coord_font_family: Font family for coordinate labels
            coord_color: Color for coordinate labels
            config: Matrix configuration
            transform: Transform configuration
        """
        super().__init__(
            config=config if config is not None else MatrixConfig(),
            transform=transform if transform is not None else TransformConfig(),
        )

        # Validate data validity
        if not data or not all(data):
            raise ValueError("Matrix data cannot be empty")

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

        # Validate appearance_matrix shape
        if appearance_matrix is not None:
            if len(appearance_matrix) != rows or not all(
                len(row) == cols for row in appearance_matrix
            ):
                raise ValueError("appearance_matrix must have the same shape as data")

        # Store data and configuration
        self._data = data
        self._element_map = element_map or {}
        self._appearance_matrix = appearance_matrix
        self._element_appearance_map = element_appearance_map or {}
        self._caption = caption
        self._caption_location = caption_location

        # Matrix properties
        self._rows = rows
        self._cols = cols

        # Font settings
        self._font_family: str = "Arial"
        self._font_size: float = 12
        self._font_color: Color = Color("black")

        # Global appearance settings
        self._global_appearance: AppearanceConfig | None = None

        # border_as_number related settings
        self._border_position: BorderPosition | None = border_as_number
        self._coord_font_size: float = coord_font_size if coord_font_size is not None else 16
        self._coord_font_family: str = (
            coord_font_family if coord_font_family is not None else "Arial"
        )
        self._coord_color: Color = coord_color if coord_color is not None else Color("black")

        # Validate border elements (if border_as_number is set)
        if self._border_position is not None:
            self._validate_border_elements(self._border_position)

        # Create cells
        self._create_cells()

    def _create_cells(self):
        """Create all Cell components"""
        self._cells: list[list[Cell]] = []

        for i in range(self._rows):
            row_cells = []
            for j in range(self._cols):
                # Get actual element (considering mapping)
                original_elem = self._data[i][j]
                actual_elem = self._element_map.get(original_elem, original_elem)

                # Calculate position (considering border adjustment)
                cell_x, cell_y = self._get_border_cell_position(i, j)

                # Create cell configuration
                cell_config = self._create_cell_config(cell_x, cell_y, actual_elem, i, j)

                # Get appearance configuration
                appearance = self._get_cell_appearance(i, j, original_elem, actual_elem)

                # Create cell
                cell = Cell(config=cell_config, rectangle_appearance=appearance)
                row_cells.append(cell)

            self._cells.append(row_cells)

    def _create_cell_config(
        self, x: float, y: float, elem: MatElemType, row: int, col: int
    ) -> CellConfig:
        """Create configuration for a single cell"""
        cell_config = CellConfig(
            x=x,
            y=y,
            width=self.config.cell_size,
            height=self.config.cell_size,
            content_padding=self.config.cell_padding,
        )

        # Check if it's a border cell
        is_border = self._is_border_cell(row, col)

        # Set content based on element type
        if isinstance(elem, (str, int, float)):
            # Text content
            if is_border:
                # Border elements use special font settings
                cell_config.text_content = TextConfig(
                    text=str(elem),
                    font_family=self._coord_font_family,
                    font_size=self._coord_font_size,
                    color=self._coord_color,
                    text_anchor="middle",
                    dominant_baseline="central",
                )
            else:
                # Regular elements use default font settings
                cell_config.text_content = TextConfig(
                    text=str(elem),
                    font_family=self._font_family,
                    font_size=self._font_size,
                    color=self._font_color,
                    text_anchor="middle",
                    dominant_baseline="central",
                )
        elif isinstance(elem, Path):
            # Image content
            cell_config.image_content = ImageConfig(
                href=str(elem), preserveAspectRatio="xMidYMid meet"
            )
        elif isinstance(elem, SVGCode):
            # SVG content
            cell_config.svg_content = SVGConfig(svg_content=elem)

        return cell_config

    def _get_cell_appearance(
        self, row: int, col: int, original_elem: MatElemType, actual_elem: MatElemType
    ) -> AppearanceConfig | None:
        """Get appearance configuration for a single cell"""
        # Priority: Border appearance (highest) > Global appearance > Element appearance mapping > Appearance matrix > Default

        # 1. Border element appearance (highest priority)
        if self._is_border_cell(row, col):
            return AppearanceConfig(
                fill=Color("none"),  # No fill
                stroke=Color("none"),  # No border
                stroke_width=0,
            )

        # 2. If global appearance is set, use it
        if self._global_appearance is not None:
            return self._global_appearance

        # 3. Check element appearance mapping
        if original_elem in self._element_appearance_map:
            return self._element_appearance_map[original_elem]

        # 4. Check appearance matrix
        if self._appearance_matrix is not None:
            return self._appearance_matrix[row][col]

        # 5. For images and SVG content, reset to default appearance
        if isinstance(actual_elem, (Path, SVGCode)):
            return AppearanceConfig()  # Default appearance

        return None

    @property
    def central_point(self) -> Tuple[float, float]:
        """Get matrix center point (considering border labeling effect)"""
        if self._border_position is None:
            # No border labeling, use center of entire matrix
            center_x = self.config.x + (self._cols * self.config.cell_size) / 2
            center_y = self.config.y + (self._rows * self.config.cell_size) / 2
        else:
            # With border labeling, need to calculate center of actual content area
            if self._border_position == "upperleft":
                # Actual content area: excluding row 0 and column 0
                content_cols = self._cols - 1
                content_rows = self._rows - 1
                content_start_x = self.config.x + self.config.cell_size  # Start from column 1
                content_start_y = self.config.y + self.config.cell_size  # Start from row 1
                center_x = content_start_x + (content_cols * self.config.cell_size) / 2
                center_y = content_start_y + (content_rows * self.config.cell_size) / 2
            elif self._border_position == "upperright":
                # Actual content area: excluding row 0 and last column
                content_cols = self._cols - 1
                content_rows = self._rows - 1
                content_start_x = self.config.x  # Start from column 0
                content_start_y = self.config.y + self.config.cell_size  # Start from row 1
                center_x = content_start_x + (content_cols * self.config.cell_size) / 2
                center_y = content_start_y + (content_rows * self.config.cell_size) / 2
            elif self._border_position == "lowerleft":
                # Actual content area: excluding last row and column 0
                content_cols = self._cols - 1
                content_rows = self._rows - 1
                content_start_x = self.config.x + self.config.cell_size  # Start from column 1
                content_start_y = self.config.y  # Start from row 0
                center_x = content_start_x + (content_cols * self.config.cell_size) / 2
                center_y = content_start_y + (content_rows * self.config.cell_size) / 2
            elif self._border_position == "lowerright":
                # Actual content area: excluding last row and last column
                content_cols = self._cols - 1
                content_rows = self._rows - 1
                content_start_x = self.config.x  # Start from column 0
                content_start_y = self.config.y  # Start from row 0
                center_x = content_start_x + (content_cols * self.config.cell_size) / 2
                center_y = content_start_y + (content_rows * self.config.cell_size) / 2

        return (center_x, center_y)

    def to_svg_element(self) -> str:
        """Generate complete SVG element string"""
        elements = []

        # Add all cells
        for row_cells in self._cells:
            for cell in row_cells:
                elements.append(cell.to_svg_element())

        # Add caption
        if self._caption is not None:
            elements.append(self._render_caption())

        # Apply transform
        if self.has_transform():
            transform_dict = self.transform.to_svg_dict()
            if "transform" in transform_dict and transform_dict["transform"] != "none":
                return f'<g transform="{transform_dict["transform"]}">{"".join(elements)}</g>'

        return f"<g>{''.join(elements)}</g>"

    def _render_caption(self) -> str:
        """Render caption"""
        if self._caption is None or self._caption_location is None:
            return ""

        # Get matrix center point (considering border labeling effect)
        center_x, center_y = self.central_point

        # Get caption configuration, copy to avoid modifying original object
        caption_config = TextConfig(
            text=self._caption.config.text,
            font_size=self._caption.config.font_size,
            font_family=self._caption.config.font_family,
            color=self._caption.config.color,
            text_anchor="middle",
            dominant_baseline="central",
        )

        # Calculate matrix boundaries (for determining caption offset)
        matrix_width = self._cols * self.config.cell_size
        matrix_height = self._rows * self.config.cell_size

        # Adjust coordinates based on position, using center point as reference
        if self._caption_location == "top":
            caption_config.x = center_x
            caption_config.y = self.config.y - 20  # Offset upward from matrix top
        elif self._caption_location == "down":
            caption_config.x = center_x
            caption_config.y = (
                self.config.y + matrix_height + 20
            )  # Offset downward from matrix bottom
        elif self._caption_location == "left":
            caption_config.x = self.config.x - 20  # Offset leftward from matrix left
            caption_config.y = center_y
        elif self._caption_location == "right":
            caption_config.x = (
                self.config.x + matrix_width + 20
            )  # Offset rightward from matrix right
            caption_config.y = center_y

        # Create new TextContent object
        positioned_caption = TextContent(config=caption_config)
        return positioned_caption.to_svg_element()

    def set_cell_size(self, size: float) -> "Matrix":
        """Set size for all cells (will automatically adjust border element positions)"""
        self.config.cell_size = size
        self._create_cells()  # Recreate cells (including border element position adjustment)
        return self

    def set_pad(self, padding: float) -> "Matrix":
        """Set padding between cell elements and borders"""
        self.config.cell_padding = padding
        self._create_cells()  # Recreate cells
        return self

    def set_global_appearance(self, appearance: AppearanceConfig) -> "Matrix":
        """Set appearance for all cells (except border elements)"""
        self._global_appearance = appearance
        self._create_cells()  # Recreate cells
        return self

    def set_font_family(self, font_family: str) -> "Matrix":
        """Set font family for all matrix elements that are str (except border elements)"""
        self._font_family = font_family
        self._create_cells()  # Recreate cells
        return self

    def set_font_size(self, font_size: float) -> "Matrix":
        """Set font size for all matrix elements that are str (except border elements)"""
        self._font_size = font_size
        self._create_cells()  # Recreate cells
        return self

    def set_font_color(self, font_color: Color) -> "Matrix":
        """Set font color for all matrix elements that are str (except border elements)"""
        self._font_color = font_color
        self._create_cells()  # Recreate cells
        return self

    def get_bounding_box(self) -> Tuple[float, float, float, float]:
        """Get matrix bounding box"""
        matrix_width = self._cols * self.config.cell_size
        matrix_height = self._rows * self.config.cell_size

        min_x = self.config.x
        min_y = self.config.y
        max_x = self.config.x + matrix_width
        max_y = self.config.y + matrix_height

        # Consider caption position
        if self._caption is not None and self._caption_location is not None:
            if self._caption_location == "top":
                min_y -= 40  # Leave space for caption
            elif self._caption_location == "down":
                max_y += 40
            elif self._caption_location == "left":
                min_x -= 40
            elif self._caption_location == "right":
                max_x += 40

        return (min_x, min_y, max_x, max_y)

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

    def _validate_border_elements(self, border_position: BorderPosition) -> None:
        """Validate that border elements are all text content"""
        border_cells = []

        if border_position == "upperleft":
            # First row and first column
            border_cells.extend([(0, j) for j in range(self._cols)])  # First row
            border_cells.extend(
                [(i, 0) for i in range(1, self._rows)]
            )  # First column (excluding duplicate (0,0))
        elif border_position == "upperright":
            # First row and last column
            border_cells.extend([(0, j) for j in range(self._cols)])  # First row
            border_cells.extend([(i, self._cols - 1) for i in range(1, self._rows)])  # Last column
        elif border_position == "lowerleft":
            # Last row and first column
            border_cells.extend([(self._rows - 1, j) for j in range(self._cols)])  # Last row
            border_cells.extend([(i, 0) for i in range(self._rows - 1)])  # First column
        elif border_position == "lowerright":
            # Last row and last column
            border_cells.extend([(self._rows - 1, j) for j in range(self._cols)])  # Last row
            border_cells.extend([(i, self._cols - 1) for i in range(self._rows - 1)])  # Last column

        # Check that all border elements are text content
        for row, col in border_cells:
            original_elem = self._data[row][col]
            actual_elem = self._element_map.get(original_elem, original_elem)
            if not isinstance(actual_elem, (str, int, float)):
                raise ValueError(
                    f"Border element at ({row}, {col}) must be text content, got {type(actual_elem)}"
                )

    def _get_border_cell_position(self, row: int, col: int) -> Tuple[float, float]:
        """Get adjusted position for border cells to make them closer to matrix borders"""
        if not self._is_border_cell(row, col):
            # Regular cell position
            cell_x = self.config.x + col * self.config.cell_size
            cell_y = self.config.y + row * self.config.cell_size
            return (cell_x, cell_y)

        # Border cell needs position adjustment
        base_x = self.config.x + col * self.config.cell_size
        base_y = self.config.y + row * self.config.cell_size

        # Adjustment amount to make border elements closer to actual matrix
        offset = self.config.cell_size * 0.1  # 10% of cell_size as offset

        if self._border_position == "upperleft":
            if row == 0 and col > 0:  # First row (except (0,0))
                base_y += offset
            elif col == 0 and row > 0:  # First column (except (0,0))
                base_x += offset
        elif self._border_position == "upperright":
            if row == 0 and col < self._cols - 1:  # First row (except upper right corner)
                base_y += offset
            elif col == self._cols - 1 and row > 0:  # Last column (except upper right corner)
                base_x -= offset
        elif self._border_position == "lowerleft":
            if row == self._rows - 1 and col > 0:  # Last row (except lower left corner)
                base_y -= offset
            elif col == 0 and row < self._rows - 1:  # First column (except lower left corner)
                base_x += offset
        elif self._border_position == "lowerright":
            if (
                row == self._rows - 1 and col < self._cols - 1
            ):  # Last row (except lower right corner)
                base_y -= offset
            elif (
                col == self._cols - 1 and row < self._rows - 1
            ):  # Last column (except lower right corner)
                base_x -= offset

        return (base_x, base_y)
