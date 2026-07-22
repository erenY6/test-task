import logging
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


logger = logging.getLogger("portfolio-api")
logger.setLevel(logging.INFO)


file_handler = logging.FileHandler(
    LOG_DIR / "requests.log",
    encoding="utf-8"
)

file_handler.setLevel(logging.INFO)


formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

file_handler.setFormatter(formatter)


if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(
        logging.StreamHandler()
    )