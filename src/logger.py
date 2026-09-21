import logging
from logging.handlers import RotatingFileHandler
import os

LOG_FILE_NAME = "project.log"

def get_logger(name: str, log_dir: str = "logs"):
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return logger
    log_path = os.path.join(log_dir, LOG_FILE_NAME)
    handler = RotatingFileHandler(
        log_path,
        maxBytes=5_000_000,
        backupCount=5
    )
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
