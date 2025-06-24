"""
Logging configuration.
"""
import logging
from config import config

def get_logger(name):
    """
    Returns a configured logger.
    """
    log_level = config.get("logging", {}).get("level", "INFO")
    
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    
    return logging.getLogger(name)