import pytest
from tbl2pic.settings import TableSettings
from tbl2pic.generator import TableImageGenerator
import json
import os

@pytest.fixture(scope="module")
def setup_generator():
    """Фикстура для настройки генератора таблиц."""
    settings = TableSettings()
    generator = TableImageGenerator(settings)

    # Загрузка тестовых данных из JSON
    with open('example/data/data.json', 'r') as file:
        generator.data = json.load(file)

    return generator

def test_create_image(setup_generator):
    """Тестирование создания изображения."""
    generator = setup_generator
    generator.create_image()
    assert generator.image is not None, "Изображение не должно быть None"

def test_draw_headers(setup_generator):
    """Тестирование рисования заголовков."""
    generator = setup_generator
    generator.create_image()
    
    # Проверяем, что заголовки нарисованы (например, можно проверить цвет или координаты)
    try:
        generator.draw_headers()
    except Exception as e:
        pytest.fail(f"Метод draw_headers вызвал ошибку: {e}")

def test_draw_data(setup_generator):
    """Тестирование рисования данных."""
    generator = setup_generator
    generator.create_image()
    
    try:
        generator.draw_data()
    except Exception as e:
        pytest.fail(f"Метод draw_data вызвал ошибку: {e}")

def test_save_image(setup_generator):
    """Тестирование сохранения изображения."""
    generator = setup_generator
    output_path = 'output/test_table.png'
    
    # Удаляем файл, если он существует
    if os.path.exists(output_path):
        os.remove(output_path)
    
    generator.generate_table_image(output_path)
    
    assert os.path.exists(output_path), "Файл изображения не был создан"
