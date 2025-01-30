from tbl2pic.generator import TableImageGenerator  # Импортируем класс из пакета
from tbl2pic.settings import TableSettings  # Импортируем настройки
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)  # Устанавливаем уровень логирования на DEBUG
logger = logging.getLogger(__name__)

# Пример использования класса
if __name__ == "__main__":
    settings = TableSettings(
        font_size=50,
        cell_width=800,
        cell_height=100
    )
    t2p = TableImageGenerator(settings)
    t2p._read_from_json('example/data/data.json')  # Укажите путь к вашему JSON-файлу
    
    # print(t2p._get_max_cell_len())
    t2p.generate_table_image("example/output/table.png")   # Укажите путь для сохранения изображения
    
