from loguru import logger
from loguru._logger import Logger
import sys
from pathlib import Path

from pysvg.globals import Globals


def get_logger() -> Logger:
    return logger


def configure_logging(
    console_level: str | int | None = None,
    file_level: str | int | None = None,
    use_file_handler: bool = False,
) -> None:
    """
    Configures the global Loguru logger with console and optional file handlers.
    This function should be called ONLY ONCE at application startup.
    """
    logger.remove()  # Always start with a clean slate to ensure previous handlers are gone

    # Use Globals().logging_level as default if not explicitly provided
    effective_console_level = (
        console_level if console_level is not None else Globals().logging_level
    )
    effective_file_level = file_level if file_level is not None else Globals().logging_level

    # Add console handler
    logger.add(
        sys.stderr,
        level=effective_console_level,
        colorize=True,
    )

    # Add file handler if requested
    if use_file_handler:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"{Path().cwd().name}.log"

        logger.add(
            log_file,
            level=effective_file_level,
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            enqueue=True,  # Recommended for file logging, especially with multiple processes
            diagnose=True,  # Set to False in production
        )


def set_global_logging_level(level: int | str, use_file_handler: bool = False) -> None:
    """
    Updates the global logging level and reconfigures all active handlers.
    This is the way to dynamically change log levels at runtime.
    """
    Globals().logging_level = level

    configure_logging(console_level=level, file_level=level, use_file_handler=use_file_handler)
