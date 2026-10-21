"""Parse, compare, and convert space-separated unit expressions."""

from __future__ import annotations

import re
from collections import defaultdict

import numpy as np

from .db import UNIT_DB

_UNIT_TOKEN = re.compile(r"([a-zA-Z]+)([-+]?\d+)?")
_DIMENSIONLESS_ALIASES = {"", "-", "dimensionless", "ratio", "none"}
_SI_UNITS = {"M": "kg", "L": "m", "T": "s"}


class Unit:
    """A scale relative to SI and a mapping of base dimension exponents."""

    def __init__(self, scale: float, dims: dict[str, int]):
        self.scale = scale
        self.dims = {
            dimension: exponent
            for dimension, exponent in dims.items()
            if exponent != 0
        }

    @classmethod
    def from_string(cls, unit_str: str) -> Unit:
        """Parse an expression such as ``kg m s-2`` or a dimensionless alias."""
        if unit_str.strip().lower() in _DIMENSIONLESS_ALIASES:
            return cls(1.0, {})

        scale = 1.0
        dims: defaultdict[str, int] = defaultdict(int)
        for token in unit_str.split():
            name, exponent = _parse_unit_token(token)
            if name not in UNIT_DB:
                raise ValueError(f"Unknown unit: '{name}'")

            definition = UNIT_DB[name]
            scale *= definition["scale"] ** exponent
            for dimension, power in definition["dims"].items():
                dims[dimension] += power * exponent

        return cls(scale, dims)

    def __repr__(self) -> str:
        return f"Unit(scale={self.scale}, dims={self.dims})"


def _parse_unit_token(token: str) -> tuple[str, int]:
    """Return a unit name and its exponent, defaulting to one."""
    match = _UNIT_TOKEN.fullmatch(token)
    if match is None:
        raise ValueError(f"Invalid unit token: '{token}'")
    return match[1], int(match[2] or 1)


def _format_unit_token(name: str, exponent: int) -> str:
    return name if exponent == 1 else f"{name}{exponent}"


def conv(value: float | np.ndarray, from_unit: str, to_unit: str) -> float | np.ndarray:
    """Convert a scalar or NumPy array between dimensionally compatible units."""
    source = Unit.from_string(from_unit)
    target = Unit.from_string(to_unit)
    if source.dims != target.dims:
        raise ValueError(
            f"Incompatible units: '{from_unit}' {source.dims} "
            f"vs '{to_unit}' {target.dims}"
        )
    return value * (source.scale / target.scale)


def is_compatible(from_unit: str, to_unit: str) -> bool:
    """Return whether dimensions match; malformed or unknown units return False."""
    try:
        return Unit.from_string(from_unit).dims == Unit.from_string(to_unit).dims
    except ValueError:
        return False


def invert_unit(unit_str: str) -> str:
    """Negate each token's exponent, checking syntax but not unit names."""
    tokens = []
    for token in unit_str.split():
        name, exponent = _parse_unit_token(token)
        tokens.append(_format_unit_token(name, -exponent))
    return " ".join(tokens)


def dims_to_si_unit(dims: dict[str, int]) -> str:
    """Format mass, length, and time dimensions in sorted-key order; ignore others."""
    return " ".join(
        _format_unit_token(_SI_UNITS[dimension], exponent)
        for dimension, exponent in sorted(dims.items())
        if dimension in _SI_UNITS
    )
