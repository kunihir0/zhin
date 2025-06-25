"""
Logging configuration.
"""
import logging
from config import config

from color_logger import ColorFormatter

def get_logger(name):
    """
    Returns a configured logger.
    """
    log_level = config.get("logging", {}).get("level", "INFO")
    
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Prevent duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = ColorFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger