"""
Unity - Unit Conversion and Dimensional Analysis Library

A robust Python library for unit conversion and dimensional analysis,
supporting scalar values, lists, and numpy arrays.

Features:
    - Unit conversion with dimensional analysis
    - Arithmetic operations with automatic unit handling
    - Scalar and array quantity support
    - Broadcasting for array operations
    - Indexing and slicing for arrays
    - Smart formatting with magnitude-based rules

Quick Start:
    >>> from unity import Quantity
    >>> distance = Quantity(5, "km")
    >>> distance.to("m")
    Quantity(5000.0, 'm')
    
    >>> velocity = distance / Quantity(10, "s")
    >>> print(velocity)
    500.0 m s-1

Examples:
    Scalar quantities:
        q = Quantity(100, "m")
        q.to("km")
    
    Array quantities:
        temperatures = Quantity([20, 25, 30], "°C")
        doubled = temperatures * 2
    
    Calculations:
        distance = Quantity(100, "m")
        time = Quantity(10, "s")
        speed = distance / time

For more information, see:
    - README.md - Overview and features
    - GUIDE.md - Getting started guide
    - API_REFERENCE.md - Complete API reference
    - ARRAYS.md - Array operations guide
"""

from .core import (
    CanonicalUnit,
    parse_unit,
    conv,
    valid,
    invert_unit,
)
from .quantity import Quantity

__version__ = "0.1.0"
__author__ = "Unity Contributors"
__license__ = "MIT"

__all__ = [
    # Core functions
    'CanonicalUnit',
    'parse_unit',
    'conv',
    'valid',
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
        'Unit': 'Use Quantity instead: from unity import Quantity',
        'convert': 'Use conv function or Quantity.to() method',
        'Converter': 'Use Quantity class: from unity import Quantity',
        'parse': 'Use parse_unit function: from unity import parse_unit',
    }
    
    if name in suggestions:
        raise AttributeError(
            f"'{name}' is not defined in unity. "
            f"Did you mean: {suggestions[name]}"
        )
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

