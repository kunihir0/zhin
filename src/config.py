"""
Configuration management.
"""
import toml

def load_config():
    """
    Loads the config.toml file.
    """
    try:
        with open("config.toml", "r") as f:
            return toml.load(f)
    except FileNotFoundError:
        return {}

config = load_config()