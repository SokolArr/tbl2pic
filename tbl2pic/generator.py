import json
from PIL import Image, ImageDraw, ImageFont
import logging
from typing import List, Optional, Tuple

from .settings import TableSettings

logger = logging.getLogger(__name__)


class TableImageGenerator:
    def __init__(self, settings: TableSettings):
        self.settings: TableSettings = settings
        self.is_adaptive_width = not settings.cell_width

        # Data
        self.table_name: Optional[str] = None
        self.cols: List[str] = []
        self.rows: List[List[str]] = []

        # Draw
        self.image: Optional[Image.Image] = None
        self.draw: Optional[ImageDraw.Draw] = None
        self.background: Optional[Image.Image] = None
        self.table_image: Optional[Image.Image] = None

        # Tech data
        self.cells_content_width: List[int] = []

        # Load font
        try:
            self.font = ImageFont.truetype(self.settings.font, self.settings.font_size)
            logger.info(f"Font loaded: {self.settings.font}.")
        except IOError:
            logger.warning(f"Font {self.settings.font} not found. Using default font.")
            self.font = ImageFont.load_default()

        # Calculate letter size
        self.letter_size = self._letter_size()
        self.letter_width = self.letter_size[2] - self.letter_size[0]
        self.letter_height = self.letter_size[3] - self.letter_size[1]

    def read_data_from_json(self, fp: str):
        """Load table data from a JSON file."""
        try:
            with open(fp, "r") as file:
                json_data: dict = json.load(file)

            self.table_name = json_data.get("tableName")
            self.cols = json_data.get("header", [])[: self.settings.col_limit]
            self.rows = json_data.get("data", [])[: self.settings.row_limit]

            self.cells_content_width = self._get_cells_content_width()

        except FileNotFoundError:
            logger.warning(f"File {fp} not found.")
        except json.JSONDecodeError:
            logger.error(f"JSON decoding error in file {fp}.")

    def create_image(self):
        """Create a blank image with the specified background."""
        rows_n = len(self.rows) + 1

        table_width = sum(self.cells_content_width)
        table_height = self.settings.cell_height * rows_n

        image_width = table_width + 2 * self.settings.table_margin
        image_height = table_height + 2 * self.settings.table_margin

        # Load or create background
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

        # Create table image
        self.table_image = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.table_image)

    def _draw_rectangle(
        self,
        x: int,
        y: int,
        cell_width: int,
        cell_height: int,
        fill_color: Tuple[int, int, int, int],
    ):
        """Draw a rectangle representing a cell."""
        x += self.settings.table_margin
        y += self.settings.table_margin
        self.draw.rectangle(
            [x, y, x + cell_width, y + cell_height],
            fill=fill_color,
            outline=self.settings.table_border_color,
            width=self.settings.table_border_thickness,
        )

    def _letter_size(self):
        """Calculate the size of a single letter."""
        return ImageDraw.Draw(Image.new("RGBA", (1, 1), (255, 255, 255, 255))).textbbox(
            (0, 0), "A", font=self.font
        )

    def _draw_cell_content(
        self,
        x: int,
        y: int,
        cell_width: int,
        cell_height: int,
        text: str,
        padding: Tuple[int, int, int, int],
        text_align: str,
    ):
        """Draw text inside a cell with proper alignment and padding."""
        padding_left, padding_top, padding_right, padding_bottom = padding

        text_x = x + self.settings.table_margin + padding_left
        text_y = y + self.settings.table_margin + padding_top

        bbox = self.draw.textbbox((text_x, text_y), text, font=self.font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if text_align == "center":
            text_x += (cell_width - text_width - padding_left - padding_right) / 2
            text_y += (cell_height - text_height - padding_top - padding_bottom) / 2
        elif text_align == "left":
            text_x += padding_left
            text_y += (cell_height - text_height - padding_top - padding_bottom) / 2

        self.draw.text((text_x, text_y), text, fill="black", font=self.font)

    def draw_headers(self):
        """Draw table headers."""
        x = 0
        y = 0
        for col_id, cell_data in enumerate(self.cols):
            cell_width = self.cells_content_width[col_id]
            text_align = self.settings.cols_settings[col_id].get(
                "textAlign", self.settings.cell_text_align
            )
            self._draw_rectangle(
                x,
                y,
                cell_width,
                self.settings.cell_height,
                fill_color=self.settings.header_color,
            )

            self._draw_cell_content(
                x,
                y,
                cell_width,
                self.settings.cell_height,
                str(cell_data).upper(),
                self.settings.cell_padding,
                text_align,
            )
            x += cell_width

    def draw_rows(self):
        """Draw table rows."""
        for row, row_data in enumerate(self.rows):
            x = 0
            for col_id, cell_data in enumerate(row_data):
                cell_width = self.cells_content_width[col_id]
                y = (row + 1) * self.settings.cell_height
                text_align = self.settings.cols_settings[col_id].get(
                    "textAlign", self.settings.cell_text_align
                )
                self._draw_rectangle(
                    x,
                    y,
                    cell_width,
                    self.settings.cell_height,
                    fill_color=self.settings.cell_color,
                )

                self._draw_cell_content(
                    x,
                    y,
                    cell_width,
                    self.settings.cell_height,
                    str(cell_data),
                    self.settings.cell_padding,
                    text_align,
                )
                x += cell_width

    def _composite_images(self):
        """Combine background and table images."""
        self.image = Image.alpha_composite(self.background, self.table_image)

    def save_image(self, output_path="table.png"):
        """Save the final image to a file."""
        if self.image is not None:
            self.image.save(output_path)
            logger.info(f"Table saved to file: {output_path}")
        else:
            logger.warning("Create an image first.")

    def generate_table_image(self, output_path="table.png"):
        """Generate and save the table image."""
        if self.cols and self.rows:
            self.create_image()
            self.draw_headers()
            self.draw_rows()
            self._composite_images()
            self.save_image(output_path)
        else:
            logger.warning("No data to generate table.")

    def _get_cells_content_width(self) -> List[int]:
        """Calculate the width of each column based on content."""
        rows: List[List[str]] = self.rows + [self.cols]

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
