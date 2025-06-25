"""
Terminal animation and progress bar utilities.
"""
import sys
import time
import math
import shutil
import logging

log = logging.getLogger(__name__)

COLORS = {
    "pink": "\033[38;5;219m",
    "purple": "\033[38;5;183m",
    "cyan": "\033[38;5;123m",
    "yellow": "\033[38;5;228m",
    "blue": "\033[38;5;111m",
    "orange": "\033[38;5;216m",
    "green": "\033[38;5;156m",
    "red": "\033[38;5;210m",
    "magenta": "\033[38;5;201m",
    "light_blue": "\033[38;5;159m",
    "lavender": "\033[38;5;147m",
    "peach": "\033[38;5;223m",
    "mint": "\033[38;5;121m",
    "reset": "\033[0m",
    "bold": "\033[1m",
    "italic": "\033[3m",
    "underline": "\033[4m",
}

def _get_terminal_size():
    """Get terminal size."""
    return shutil.get_terminal_size()

def _hide_cursor():
    """Hide the terminal cursor."""
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def _show_cursor():
    """Show the terminal cursor."""
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

class ProgressBar:
    """
    A class to display a progress bar in the terminal.
    """
    def __init__(self, total, text="Processing", width=40, fill_char="•", empty_char="·", bar_color="cyan", text_color="yellow", pulse=True):
        self.total = total
        self.text = text
        self.width = width
        self.fill_char = fill_char
        self.empty_char = empty_char
        self.bar_color = bar_color
        self.text_color = text_color
        self.pulse = pulse
        self.current = 0
        _hide_cursor()

    def update(self, amount=1):
        """Update the progress bar."""
        try:
            self.current += amount
            progress = self.current / self.total if self.total > 0 else 0
            
            if self.pulse:
                pulse_factor = abs(math.sin(time.time() * 5))
                filled_width = int(self.width * progress * (0.8 + 0.2 * pulse_factor))
            else:
                filled_width = int(self.width * progress)
            
            filled = self.fill_char * filled_width
            empty = self.empty_char * (self.width - filled_width)
            
            bar = f"{COLORS[self.bar_color]}{filled}{COLORS['reset']}{empty}"
            
            percent = int(progress * 100)
            display_text = f"{COLORS[self.text_color]}{self.text}{COLORS['reset']}"
            
            sys.stdout.write(f"\r {display_text} [{bar}] {percent}% ({self.current}/{self.total})")
            sys.stdout.flush()
        except Exception as e:
            log.error(f"Error updating progress bar: {e}")
            _show_cursor()

    def finish(self):
        """Finalize the progress bar."""
        try:
            # Ensure the final state is 100%
            self.current = self.total
            self.update(0)
            sys.stdout.write("\n")
        except Exception as e:
            log.error(f"Error finishing progress bar: {e}")
        finally:
            _show_cursor()

def typing_effect(text, speed=0.001, variance=0.001):
    """Simulates typing with realistic timing variations."""
    import random
    _hide_cursor()
    for char in text:
        delay = speed + random.uniform(-variance, variance)
        if delay < 0.001:
            delay = 0.001
        
        if char in ".!?,:;":
            delay *= 3
            
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    _show_cursor()
    sys.stdout.write("\n")