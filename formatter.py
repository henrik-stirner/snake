import logging


COLORS = {
    "black": "\033[30m",
    "bright black": "\x1b[90m",  # some humans also call it grey... no standard "color"
    "white": "\x1b[37m",
    "yellow": "\x1b[33m",
    "green": "\x1b[32m",
    "cyan": "\x1b[36m",
    "blue": "\x1b[34m",
    "magenta": "\x1b[35m",
    "red": "\x1b[31m",
    "bold_red": "\x1b[31;1m",
    "reset": "\x1b[0m"
}


class ColoredFormatter(logging.Formatter):
    # ANSI escape sequences for colored output
    color_mapping = {
        logging.DEBUG: COLORS["white"],
        logging.INFO: COLORS["blue"],
        logging.WARNING: COLORS["yellow"],
        logging.ERROR: COLORS["red"],
        logging.CRITICAL: COLORS["bold_red"]
    }

    def format(self, record):
        return f"{self.color_mapping[record.levelno]}{super().format(record)}{COLORS['reset']}"
