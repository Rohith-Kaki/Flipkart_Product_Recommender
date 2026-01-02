import os
import logging
from datetime import datetime

LOG_DIR = os.makedirs("logs", exist_ok=True)
LOG_FILE_NAME = os.path.join(LOG_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(
    filename = LOG_FILE_NAME,
    level=logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
