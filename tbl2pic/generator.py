import json
from PIL import Image, ImageDraw, ImageFont
from typing import Optional
import logging

from .settings import TableSettings

logger = logging.getLogger(__name__)

class TableImageGenerator:
    def __init__(self, settings: TableSettings, data: Optional[dict] = None):
        self.data = data if data else {}
        self.settings = settings
        self.image = None
        self.draw = None
        
    def _read_from_json(self, fp: str):
        """Читает данные из JSON-файла."""
        try:
            with open(fp, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            logger.warning(f"Файл {fp} не найден.")
        except json.JSONDecodeError:
            logger.error(f"Ошибка декодирования JSON в файле {fp}.")

    def create_image(self):
        """Создает пустое изображение для таблицы с фоном."""
        rows = len(self.data.get("data", [])) + 1  # Заголовок + данные
        cols = len(self.data.get("headers", []))   # Количество столбцов
        image_width = self.settings.cell_width * cols
        image_height = self.settings.cell_height * rows

        # Создаем изображение с фоном
        if self.settings.background_image:
            try:
                logger.debug(f"Попытка загрузить фоновое изображение: {self.settings.background_image}")
                background = Image.open(self.settings.background_image).resize((image_width, image_height))
                self.image = background.convert("RGBA")
                logger.info(f"Фоновое изображение загружено: {self.settings.background_image}.")
            except IOError:
                logger.warning(f"Фоновое изображение {self.settings.background_image} не найдено. Использую белый фон.")
                self.image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 255))
        else:
            logger.info("Фоновое изображение не указано. Использую белый фон.")
            self.image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 255))

        self.draw = ImageDraw.Draw(self.image)

        # Загружаем шрифт
        try:
            self.font = ImageFont.truetype(self.settings.font_path, self.settings.font_size)
            logger.info(f"Шрифт загружен: {self.settings.font_path}.")
        except IOError:
            logger.warning(f"Шрифт {self.settings.font_path} не найден. Использую стандартный.")
            self.font = ImageFont.load_default()


    def _draw_rectangle(self, x: int, y: int, fill_color=(255, 255, 255, 0)):
        """Рисует прямоугольник для ячейки таблицы с заданным цветом фона."""
        self.draw.rectangle(
            [x, y, x + self.settings.cell_width, y + self.settings.cell_height],
            fill=fill_color,
            outline=self.settings.border_color,
            width=self.settings.border_thickness
        )

    def draw_headers(self):
        """Рисует заголовки таблицы."""
        for col, header in enumerate(self.data.get("headers", [])):
            x = col * self.settings.cell_width
            y = 0
            
            # Рисуем прямоугольник для заголовка
            self._draw_rectangle(x, y, fill_color=self.settings.header_color)
            
            # Получаем размеры текста с использованием textbbox
            bbox = self.draw.textbbox((x, y), header.upper(), font=self.font)
            text_width = bbox[2] - bbox[0]  # right - left
            text_height = bbox[3] - bbox[1]  # bottom - top
            
            # Вычисляем координаты для центрирования текста
            match self.settings.header_cell_text_align:
                case 'center':
                    text_x = x + (self.settings.cell_width - text_width) / 2
                    text_y = y + (self.settings.cell_height - text_height) / 2
                
                case 'left':
                    text_x = x + self.settings.header_cell_padding[0]
                    text_y = text_y = y + (self.settings.cell_height - text_height) / 2
            
            # Рисуем текст
            self.draw.text((text_x, text_y), header.upper(), fill="black", font=self.font)

    def draw_data(self):
        """Рисует данные таблицы."""
        for row, row_data in enumerate(self.data.get("data", [])):
            for col, cell_data in enumerate(row_data):
                x = col * self.settings.cell_width
                y = (row + 1) * self.settings.cell_height      
                         
                self._draw_rectangle(x, y, fill_color=self.settings.cell_color)
                
                
                # Получаем размеры текста с использованием textbbox
                bbox = self.draw.textbbox((x, y), cell_data.upper(), font=self.font)
                text_width = bbox[2] - bbox[0]  # right - left
                text_height = bbox[3] - bbox[1]  # bottom - top
                
                # Вычисляем координаты для центрирования текста
                match self.settings.cell_text_align:
                    case 'center':
                        text_x = x + (self.settings.cell_width - text_width) / 2
                        text_y = y + (self.settings.cell_height - text_height) / 2
                    
                    case 'left':
                        text_x = x + self.settings.cell_padding[0]
                        text_y = text_y = y + (self.settings.cell_height - text_height) / 2
                
                self.draw.text((text_x, text_y), str(cell_data), fill="black", font=self.font)

    def save_image(self, output_path="table.png"):
        """Сохраняет изображение в указанный путь."""
        if self.image is not None:
            self.image.save(output_path)
            logger.info(f"Таблица сохранена в файл: {output_path}")
        else:
            logger.warning("Сначала создайте изображение.")

    def generate_table_image(self, output_path="table.png"):
        """Основной метод для генерации изображения таблицы."""
        self.create_image()
        self.draw_headers()
        self.draw_data()
        self.save_image(output_path)
        
    def _get_max_cell_len(self) -> dict:
        header_row: list = self.data.get("headers", [])
        rows: list[list] = self.data.get("data", [])
        rows.append(header_row)
    
        max_lengths = {i: 0 for i in range(len(self.data.get("headers", [])))}
        for row in rows:
            for col_index, cell_data in enumerate(row):
                cell_length = len(str(cell_data))
                if cell_length > max_lengths[col_index]:
                    max_lengths[col_index] = cell_length

        return max_lengths

