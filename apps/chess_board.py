from pysvg.components import Matrix, Circle, TextContent, Canvas
from pysvg.schema import AppearanceConfig, Color


# Create chess board data, first row and column as coordinate labels
chess_data = [
    ["", "A", "B", "C", "D", "E", "F", "G", "H", "I"],
    ["9", "X", ".", ".", ".", "X", ".", ".", ".", "."],
    ["8", ".", ".", ".", ".", ".", ".", ".", ".", "."],
    ["7", ".", "O", ".", "O", ".", ".", "X", ".", "."],
    ["6", ".", ".", ".", "X", ".", ".", ".", ".", "O"],
    ["5", "O", ".", "X", "O", "X", ".", ".", ".", "."],
    ["4", ".", "X", "O", "O", ".", "O", ".", ".", "."],
    ["3", ".", ".", "X", "O", "X", ".", ".", ".", "."],
    ["2", ".", ".", ".", "X", ".", ".", ".", ".", "."],
    ["1", ".", "O", ".", "O", ".", ".", "X", ".", "."],
]

black_stone = Circle(appearance=AppearanceConfig(fill=Color("black"), stroke=Color("#333333")))
white_stone = Circle(appearance=AppearanceConfig(fill=Color("white"), stroke=Color("#333333")))

# Set appearance for pieces and empty spaces
bg_appearance = AppearanceConfig(
    fill=Color("#DEB887"),
    stroke=Color("#8B4513"),
    fill_opacity=0.85,
    stroke_width=1.4,
    stroke_opacity=0.85,
)
bgmap = {
    "X": bg_appearance,
    "O": bg_appearance,
    ".": bg_appearance,
}
elemap = {
    "X": black_stone,
    "O": white_stone,
    ".": TextContent(""),
}

matrix = Matrix(
    data=chess_data,
    element_map=elemap,
    background_map=bgmap,
    border_as_coord="upperleft",
    coord_font_size=20,
    coord_font_family="Times New Roman",
    coord_font_color=Color("black"),
    elem_locate_on_line=True,
)

canvas = Canvas(width=530, height=530)
canvas.add(matrix.move_by(30, 30))

canvas.save("chess_board.svg")
