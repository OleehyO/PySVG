import inspect
import logging
import os
from datetime import datetime
from logging import Logger

import colorama
from colorama import Fore, Style

from pysvg.globals import Globals

# Initialize colorama for colored console output
colorama.init(autoreset=True)


TEMPLATE = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors based on log level."""

    FORMATS = {  # noqa: E501
        logging.DEBUG: Fore.LIGHTBLACK_EX + TEMPLATE + Style.RESET_ALL,
        logging.INFO: Fore.WHITE + TEMPLATE + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW + TEMPLATE + Style.RESET_ALL,
        logging.ERROR: Fore.RED + TEMPLATE + Style.RESET_ALL,
        logging.CRITICAL: Fore.RED + Style.BRIGHT + TEMPLATE + Style.RESET_ALL,
    }  # noqa: E501

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS[logging.INFO])
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def get_logger(name: str | None = None, use_file_handler: bool = False) -> Logger:
    """
    Creates and configures a logger with the caller's module name (if provided) or the first two modules.
    If the module name is too long, it takes the first two modules.

    Args:
        name (str, optional): Custom logger name. If None, derives from caller's module.
        use_file_handler (bool, optional): Whether to use a file handler. Defaults to False.

    Returns:
        Logger: Configured logger with colored console output and file handler.
    """
    # If name is not provided, derive it from the caller's module
    if name is None:
        # Get the caller's stack frame
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        if module and module.__name__:
            module_name = module.__name__
            # Split module name and take first two components if too long
            parts = module_name.split(".")
            if len(parts) > 2:
                name = ".".join(parts[:2])
            else:
                name = module_name
        else:
            name = "root"

    # Create or get logger
    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Set logger level
    logger.setLevel(Globals().logging_level)

    # Create console handler with colored formatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(Globals().logging_level)
    console_formatter = ColoredFormatter()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create file handler
    if use_file_handler:
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(Globals().logging_level)
        # File formatter (no colors)
        file_formatter = logging.Formatter(TEMPLATE, datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Prevent logger from propagating to root logger
    logger.propagate = False

    return logger
