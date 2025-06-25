import logging

class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[38;5;159m",  # Light Blue
        "INFO": "\033[38;5;123m",   # Cyan
        "WARNING": "\033[38;5;228m", # Yellow
        "ERROR": "\033[38;5;210m",   # Red
        "CRITICAL": "\033[38;5;201m",# Magenta
        "RESET": "\033[0m",
    }

    def format(self, record):
        log_message = super().format(record)
        return f"{self.COLORS.get(record.levelname, self.COLORS['RESET'])}{log_message}{self.COLORS['RESET']}"