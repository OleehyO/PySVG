from pathlib import Path
from typing import Literal

from pysvg.logger import get_logger


def resolve_path(path: str | Path, as_path: bool = False) -> str | Path:
    if isinstance(path, str):
        path = Path(path)
    ret = path.expanduser().resolve()
    ret = ret if as_path else str(ret)
    return ret


def touch(path: str | Path) -> None:
    if isinstance(path, str):
        path = Path(path)
    path.touch(exist_ok=True)


def mkdir(path: str | Path) -> None:
    if isinstance(path, str):
        path = Path(path)
    path.mkdir(parents=True, exist_ok=True)


def rmfile(path: str | Path) -> None:
    if isinstance(path, str):
        path = Path(path)
    path.unlink(missing_ok=False)


def rmdir(path: str | Path, mode: Literal["empty", "recursive"] = "empty") -> None:
    """Remove a directory.

    Args:
        path: Path to directory to remove
        mode: "empty" to only remove empty directories, "all" to recursively remove all contents
    """
    _logger = get_logger(__name__)
    if isinstance(path, str):
        path = Path(path)

    if mode == "empty":
        path.rmdir()
        _logger.info(f"Removed empty directory: {path}")
    elif mode == "recursive":
        import shutil

        shutil.rmtree(path)
        _logger.info(f"Recursively removed directory and all contents: {path}")
    else:
        raise ValueError(f"Invalid mode: {mode}. Must be 'empty' or 'all'")
