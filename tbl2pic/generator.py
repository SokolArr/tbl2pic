import json
from PIL import Image, ImageDraw, ImageFont
import logging

from .settings import TableSettings

logger = logging.getLogger(__name__)


class TableImageGenerator:
    def __init__(self, settings: TableSettings):
        self.settings: TableSettings = settings
        self.is_adaptive_width = False if settings.cell_width else True

        # data
        self.table_name: str = None
        self.cols: list[str] = None
        self.rows: list[list] = None

        # draw
        self.image = None
        self.draw = None
        self.background = None
        self.table_image = None

        # tech data
        self.cells_content_width = None

        try:
            self.font = ImageFont.truetype(self.settings.font, self.settings.font_size)
            logger.info(f"Font loaded: {self.settings.font}.")
        except IOError:
            logger.warning(f"Font {self.settings.font} not found. Using default font.")
            self.font = ImageFont.load_default()

        self.letter_size = self._letter_size()
        self.letter_width = self.letter_size[2] - self.letter_size[0]
        self.letter_height = self.letter_size[3] - self.letter_size[1]

    def read_data_from_json(self, fp: str):
        try:
            json_data = {}
            with open(fp, "r") as file:
                json_data: dict = json.load(file)

            self.data = json_data
            self.table_name = json_data.get("tableName")
            self.cols = json_data.get("header")[: self.settings.col_limit]
            self.rows = json_data.get("data")[: self.settings.row_limit]

            self.cells_content_width = self._get_cells_content_width()

        except FileNotFoundError:
            logger.warning(f"File {fp} not found.")
        except json.JSONDecodeError:
            logger.error(f"JSON decoding error in file {fp}.")

    def create_image(self):
        rows_n = len(self.rows) + 1

        table_width = sum(
            self.cells_content_width[idx]
            for idx in range(len(self.cells_content_width))
        )
        table_height = self.settings.cell_height * rows_n

        image_width = table_width + 2 * self.settings.table_margin
        image_height = table_height + 2 * self.settings.table_margin

        if self.settings.background_image:
            try:
                logger.debug(
                    f"Attempting to load background image: {self.settings.background_image}"
                )
                self.background = Image.open(self.settings.background_image).convert(
                    "RGBA"
                )
                self.background = self.background.resize((image_width, image_height))
                logger.info(
                    f"Background image loaded: {self.settings.background_image}."
                )
            except IOError:
                logger.warning(
                    f"Background image {self.settings.background_image} not found."
                )
                self.background = Image.new(
                    "RGBA", (image_width, image_height), self.settings.background_color
                )
        else:
            logger.info("Background image not specified.")
            self.background = Image.new(
                "RGBA", (image_width, image_height), self.settings.background_color
            )

        self.table_image = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.table_image)

    def _draw_rectangle(
        self,
        x: int,
        y: int,
        cell_width: int,
        cell_height: int,
        fill_color: tuple,
    ):
        x += self.settings.table_margin
        y += self.settings.table_margin
        self.draw.rectangle(
            [x, y, x + cell_width, y + cell_height],
            fill=fill_color,
            outline=self.settings.table_border_color,
            width=self.settings.table_border_thickness,
        )

    def _letter_size(self):
        return ImageDraw.Draw(Image.new("RGBA", (1, 1), (255, 255, 255, 255))).textbbox(
            (0, 0), "A", font=self.font
        )

    def draw_headers(self):
        x = 0
        y = 0
        for col_id, cell_data in enumerate(self.cols):
            padding_left = self.settings.cell_padding[0]
            padding_top = self.settings.cell_padding[1]
            padding_right = self.settings.cell_padding[2]
            padding_bottom = self.settings.cell_padding[3]

            cell_width = self.cells_content_width[col_id]

            self._draw_rectangle(
                x,
                y,
                cell_width,
                self.settings.cell_height,
                fill_color=self.settings.header_color,
            )

            text_x = x + self.settings.table_margin + padding_left
            text_y = y + self.settings.table_margin + padding_top

            bbox = self.draw.textbbox(
                (text_x, text_y), str(cell_data).upper(), font=self.font
            )
            text_width = bbox[2] - bbox[0]  # right - left
            text_height = bbox[3] - bbox[1]  # bottom - top

            match self.settings.header_cell_text_align:
                case "center":
                    text_x += (
                        cell_width - text_width - padding_left - padding_right
                    ) / 2
                    text_y += (
                        self.settings.cell_height
                        - text_height
                        - padding_top
                        - padding_bottom
                    ) / 2

                case "left":
                    text_x += padding_left
                    text_y += (
                        self.settings.cell_height
                        - text_height
                        - padding_top
                        - padding_bottom
                    ) / 2

            self.draw.text(
                (text_x, text_y), str(cell_data).upper(), fill="black", font=self.font
            )
            x += cell_width

    def draw_rows(self):
        for row, row_data in enumerate(self.rows):
            x = 0
            for col_id, cell_data in enumerate(row_data):
                padding_left = self.settings.cell_padding[0]
                padding_top = self.settings.cell_padding[1]
                padding_right = self.settings.cell_padding[2]
                padding_bottom = self.settings.cell_padding[3]

                cell_width = self.cells_content_width[col_id]
                y = (row + 1) * self.settings.cell_height

                self._draw_rectangle(
                    x,
                    y,
                    cell_width,
                    self.settings.cell_height,
                    fill_color=self.settings.cell_color,
                )

                text_x = x + self.settings.table_margin + padding_left
                text_y = y + self.settings.table_margin + padding_top

                bbox = self.draw.textbbox(
                    (text_x, text_y), str(cell_data), font=self.font
                )
                text_width = bbox[2] - bbox[0]  # right - left
                text_height = bbox[3] - bbox[1]  # bottom - top

                match self.settings.cell_text_align:
                    case "center":
                        text_x += (
                            cell_width - text_width - padding_left - padding_right
                        ) / 2
                        text_y += (
                            self.settings.cell_height
                            - text_height
                            - padding_top
                            - padding_bottom
                        ) / 2

                    case "left":
                        text_x += padding_left
                        text_y += (
                            self.settings.cell_height
                            - text_height
                            - padding_top
                            - padding_bottom
                        ) / 2

                self.draw.text(
                    (text_x, text_y), str(cell_data), fill="black", font=self.font
                )
                x += cell_width

    def _composite_images(self):
        self.image = Image.alpha_composite(self.background, self.table_image)

    def save_image(self, output_path="table.png"):
        if self.image is not None:
            self.image.save(output_path)
            logger.info(f"Table saved to file: {output_path}")
        else:
            logger.warning("Create an image first.")

    def generate_table_image(self, output_path="table.png"):
        if self.data:
            self.create_image()
            self.draw_headers()
            self.draw_rows()
            self._composite_images()
            self.save_image(output_path)
        else:
            print("NO DATA")

    def _get_cells_content_width(self) -> dict:
        rows: list[list] = self.rows + [self.cols]

        if self.is_adaptive_width:
            cells_content_width = [0] * len(self.cols)

            for row in rows:
                for col_index, cell_data in enumerate(row):
                    cell_length = len(str(cell_data))
                    if cell_length > cells_content_width[col_index]:
                        cells_content_width[col_index] = cell_length

            for i in range(len(cells_content_width)):
                cell_width = cells_content_width[i] * self.letter_width
                max_cell_width = self.settings.cols_settings[i].get("maxWidth")
                min_cell_width = self.settings.cols_settings[i].get("minWidth")
                if max_cell_width and min_cell_width:
                    if cell_width >= max_cell_width:
                        cells_content_width[i] = max_cell_width
                    elif cell_width <= min_cell_width:
                        cells_content_width[i] = min_cell_width
                    else:
                        cells_content_width[i] *= self.letter_width
                else:
                    cells_content_width[i] *= self.letter_width
        else:
            cells_content_width = [self.settings.cell_width] * len(self.cols)

        return cells_content_width
