from tbl2pic.generator import TableImageGenerator
from tbl2pic.settings import TableSettings
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    settings = TableSettings().from_json("example/data/data.json")
    t2p = TableImageGenerator(settings)
    t2p.read_data_from_json("example/data/data.json")
    t2p.generate_table_image("example/output/table.png")
