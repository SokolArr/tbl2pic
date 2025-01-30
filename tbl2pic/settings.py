import json
import logging
from typing import Optional, Dict, List, Tuple

logger = logging.getLogger(__name__)


class TableSettings:
    def __init__(
        self,
        # header
        header_color: Tuple[int, int, int, int] = (255, 255, 255, 255),
        header_cell_padding: Tuple[int, int, int, int] = (10, 10, 10, 10),
        header_cell_text_align: str = "center",
        # cell
        cell_width: Optional[int] = None,
        cell_height: int = 50,
        cell_color: Tuple[int, int, int, int] = (255, 255, 255, 255),
        cell_padding: Tuple[int, int, int, int] = (10, 0, 10, 0),
        cell_text_align: str = "left",
        # font
        font_size: int = 20,
        font: str = "example/font/shrift.ttf",
        # background
        background_image: str = "example/img/bg.jpg",
        background_color: Tuple[int, int, int, int] = (255, 255, 255, 255),
        # table
        table_margin: int = 40,
        table_border_color: Tuple[int, int, int, int] = (0, 0, 0, 255),
        table_border_thickness: int = 2,
        # limits
        col_limit: int = 100,
        row_limit: int = 20,
        # cols
        cols_settings: Optional[List[Dict]] = None,
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

        # cols
        self.cols_settings = cols_settings if cols_settings else []

    @classmethod
    def from_json(cls, fp: str) -> "TableSettings":
        try:
            with open(fp, "r") as file:
                json_data: dict = json.load(file)

            settings_data: dict = json_data.get("settings", {})

            header_settings: dict = settings_data.get("header", {})
            cell_settings: dict = settings_data.get("cell", {})
            font_settings: dict = settings_data.get("font", {})
            background_settings: dict = settings_data.get("background", {})
            table_settings: dict = settings_data.get("table", {})
            limits_settings: dict = settings_data.get("limits", {})
            cols_settings: dict = settings_data.get("cols", [])

            return cls(
                # header
                header_color=tuple(
                    header_settings.get("header_color", (255, 255, 255, 255))
                ),
                header_cell_padding=tuple(
                    header_settings.get("header_cell_padding", (10, 10, 10, 10))
                ),
                header_cell_text_align=header_settings.get(
                    "header_cell_text_align", "center"
                ),
                # cell
                cell_width=cell_settings.get("cell_width", None),
                cell_height=cell_settings.get("cell_height", 50),
                cell_color=tuple(cell_settings.get("cell_color", (255, 255, 255, 255))),
                cell_padding=tuple(cell_settings.get("cell_padding", (10, 0, 10, 0))),
                cell_text_align=cell_settings.get("cell_text_align", "left"),
                # font
                font_size=font_settings.get("font_size", 20),
                font=font_settings.get("font", "example/font/shrift.ttf"),
                # background
                background_image=background_settings.get(
                    "background_image", "example/img/bg.jpg"
                ),
                background_color=tuple(
                    background_settings.get("background_color", (255, 255, 255, 255))
                ),
                # table
                table_margin=table_settings.get("table_margin", 40),
                table_border_color=tuple(
                    table_settings.get("table_border_color", (0, 0, 0, 255))
                ),
                table_border_thickness=table_settings.get("table_border_thickness", 2),
                # limits
                col_limit=limits_settings.get("col_limit", 100),
                row_limit=limits_settings.get("row_limit", 20),
                # cols
                cols_settings=cols_settings,
            )

        except FileNotFoundError:
            logger.warning(f"Файл {fp} не найден.")
            return cls()
        except json.JSONDecodeError:
            logger.error(f"Ошибка декодирования JSON в файле {fp}.")
            return cls()
