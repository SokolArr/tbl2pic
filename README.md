# Table Image Generator

This project provides a Python-based solution for generating table images from JSON data. It uses the Python Imaging Library (PIL) to create customizable tables with headers, rows, and columns. The project consists of two main classes:

1. **`TableSettings`**: Manages configuration settings for the table, such as fonts, colors, dimensions, and alignment.
2. **`TableImageGenerator`**: Generates the table image based on the provided settings and data.

---

## **Features**

- **Customizable Table Settings**:
  - Header and cell colors, padding, and text alignment.
  - Adaptive or fixed cell widths.
  - Custom fonts and font sizes.
  - Background images or solid colors.
  - Table margins, border colors, and thickness.

- **Data Loading**:
  - Load table data (headers and rows) from a JSON file.
  - Supports column and row limits.

- **Dynamic Image Generation**:
  - Generates a table image with headers and rows.
  - Supports text alignment and padding within cells.
  - Combines background and table images for a polished look.

- **Error Handling**:
  - Gracefully handles missing files, invalid JSON, and font loading errors.

---

## **Classes Overview**

### **1. `TableSettings`**

This class manages all configuration settings for the table. It can be initialized directly or loaded from a JSON file.

#### **Key Attributes**:
- **Header**: `header_color`, `header_cell_padding`, `header_cell_text_align`.
- **Cell**: `cell_width`, `cell_height`, `cell_color`, `cell_padding`, `cell_text_align`.
- **Font**: `font_size`, `font`.
- **Background**: `background_image`, `background_color`.
- **Table**: `table_margin`, `table_border_color`, `table_border_thickness`.
- **Limits**: `col_limit`, `row_limit`.
- **Columns**: `cols_settings` (list of column-specific settings like `maxWidth` and `minWidth`).

#### **Methods**:
- **`from_json(fp: str) -> TableSettings`**:
  - Loads settings from a JSON file.
  - Returns a `TableSettings` object with the loaded configuration.

---

### **2. `TableImageGenerator`**

This class generates a table image based on the provided settings and data.

#### **Key Attributes**:
- **Data**: `table_name`, `cols`, `rows`.
- **Image**: `image`, `draw`, `background`, `table_image`.
- **Technical**: `cells_content_width`, `font`, `letter_size`.

#### **Methods**:
- **`read_data_from_json(fp: str)`**:
  - Loads table data (headers and rows) from a JSON file.
- **`create_image()`**:
  - Creates a blank image with the specified background.
- **`_draw_rectangle(...)`**:
  - Draws a rectangle representing a cell.
- **`_draw_cell_content(...)`**:
  - Draws text inside a cell with proper alignment and padding.
- **`draw_headers()`**:
  - Draws the table headers.
- **`draw_rows()`**:
  - Draws the table rows.
- **`_composite_images()`**:
  - Combines the background and table images.
- **`save_image(output_path="table.png")`**:
  - Saves the final image to a file.
- **`generate_table_image(output_path="table.png")`**:
  - Generates and saves the table image.

---

## **Usage Example**

### **1. Initialize Settings**
```python
from table_settings import TableSettings

# Direct initialization
settings = TableSettings(
    header_color=(200, 200, 200, 255),
    cell_width=None,
    cell_height=50,
    font_size=20,
    background_image="example/img/bg.jpg",
    table_margin=40,
    cols_settings=[{"maxWidth": 150, "minWidth": 50}]
)

# Or load from JSON
settings = TableSettings.from_json("config/settings.json")
```

### **2. Generate Table Image**
```python
from table_image_generator import TableImageGenerator

# Initialize the generator
generator = TableImageGenerator(settings)

# Load data from JSON
generator.read_data_from_json("data.json")

# Generate and save the table image
generator.generate_table_image("output_table.png")
```

---

## **JSON Configuration**

### **Settings JSON Example**
```json
{
  "settings": {
    "header": {
      "header_color": [255, 255, 255, 255],
      "header_cell_padding": [10, 10, 10, 10],
      "header_cell_text_align": "center"
    },
    "cell": {
      "cell_width": null,
      "cell_height": 50,
      "cell_color": [255, 255, 255, 255],
      "cell_padding": [10, 0, 10, 0],
      "cell_text_align": "left"
    },
    "font": {
      "font_size": 20,
      "font": "example/font/shrift.ttf"
    },
    "background": {
      "background_image": "example/img/bg.jpg",
      "background_color": [255, 255, 255, 255]
    },
    "table": {
      "table_margin": 40,
      "table_border_color": [0, 0, 0, 255],
      "table_border_thickness": 2
    },
    "limits": {
      "col_limit": 100,
      "row_limit": 20
    },
    "cols": [
      {"maxWidth": 150, "minWidth": 50},
      {"maxWidth": 200, "minWidth": 100}
    ]
  }
}
```

### **Data JSON Example**
```json
{
  "tableName": "Sample Table",
  "header": ["Column 1", "Column 2", "Column 3"],
  "data": [
    ["Row 1, Cell 1", "Row 1, Cell 2", "Row 1, Cell 3"],
    ["Row 2, Cell 1", "Row 2, Cell 2", "Row 2, Cell 3"]
  ]
}
```

---

## **Dependencies**

- **Pillow**: Python Imaging Library (PIL) for image manipulation.
  ```bash
  pip install pillow
  ```

---

## **Error Handling**

- **File Not Found**: Logs a warning and uses default settings or skips missing files.
- **JSON Decode Error**: Logs an error and uses default settings.
- **Font Loading Error**: Logs a warning and falls back to the default font.

---

## **License**

This project is open-source and available under the Apache License.