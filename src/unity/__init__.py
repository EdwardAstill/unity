"""Unity unit conversion and dimensional analysis. See README.md for the API."""

from .core import (
    Unit,
    conv,
    is_compatible,
    invert_unit,
)
from .quantity import Quantity

__version__ = "0.1.0"
__author__ = "Unity Contributors"
__license__ = "MIT"

__all__ = [
    # Core functions
    'Unit',
    'conv',
    'is_compatible',
    'invert_unit',
    # Main class
    'Quantity',
    # Version info
    '__version__',
    '__author__',
    '__license__',
]


def __getattr__(name: str):
    """
    Provide helpful error messages for common typos or deprecated names.
    """
    suggestions = {
        'convert': 'Use conv function or Quantity.to() method',
        'Converter': 'Use Quantity class: from unity import Quantity',
        'parse': 'Use Unit.from_string(): from unity import Unit',
    }
    
    if name in suggestions:
        raise AttributeError(
            f"'{name}' is not defined in unity. "
            f"Did you mean: {suggestions[name]}"
        )
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

