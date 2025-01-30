from tbl2pic.generator import TableImageGenerator
from tbl2pic.settings import TableSettings
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    settings = TableSettings(
        font_size=50,
        cell_width=800,
        cell_height=100,
        # header_color=(0, 0, 0, 0),
        cell_color=(255, 255, 255, 128),
    )
    t2p = TableImageGenerator(settings)
    t2p._read_from_json("example/data/data.json")

    t2p.generate_table_image("example/output/table.png")
