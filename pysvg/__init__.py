"""
pysvg - A Python library for creating SVG graphics
"""

from importlib.metadata import version

__version__ = version("svg-python")

from pysvg.components import *
from pysvg.schema import *
from pysvg.utils import *

__all__ = (
    components.__all__  # type: ignore
    + schema.__all__  # type: ignore
    + utils.__all__  # type: ignore
)
