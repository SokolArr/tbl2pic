class TableSettings:
    def __init__(
        self,
        # header
        header_color=(255, 255, 255, 255),
        header_cell_padding=(10, 10, 10, 10),
        header_cell_text_align="center",
        # cell
        cell_width=200,
        cell_height=50,
        cell_color=(255, 255, 255, 255),
        cell_padding=(10, 0, 10, 0),
        cell_text_align="left",
        # font
        font_size=20,
        font="example/font/shrift.ttf",
        # background
        background_image="example/img/bg.jpg",
        background_color=(255, 255, 255, 255),
        # table
        table_margin=40,
        table_border_color=(0, 0, 0, 255),
        table_border_thickness=2,
        # limits
        col_limit=100,
        row_limit=20,
        # filters
        col_filter=None,
        row_filter=None,
    ):
        # header
        self.header_color = header_color
        self.header_cell_padding = header_cell_padding
        self.header_cell_text_align = header_cell_text_align

        # cell
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.cell_color = cell_color
        self.cell_padding = cell_padding
        self.cell_text_align = cell_text_align

        # font
        self.font_size = font_size
        self.font = font

        # background
        self.background_image = background_image
        self.background_color = background_color

        # table
        self.table_margin = table_margin
        self.table_border_color = table_border_color
        self.table_border_thickness = table_border_thickness

        # limits
        self.col_limit = col_limit
        self.row_limit = row_limit

        # filters
        self.col_filter = col_filter
        self.row_filter = row_filter
