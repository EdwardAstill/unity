"""Scalar and array quantities with unit-aware arithmetic and Typst formatting."""

from __future__ import annotations

import re

import numpy as np

from .core import Unit, conv, dims_to_si_unit, invert_unit

# Display accepts exponent markers that the conversion grammar does not.
_DISPLAY_UNIT_TOKEN = re.compile(r"([a-zA-Z]+)(?:\^|\*\*)?([-+]?\d+)?")


def _parse_unit_tokens(unit: str) -> list[tuple[str, str | None]]:
    """Split display tokens, leaving unrecognized text as a literal unit name."""
    tokens = []
    for part in unit.split():
        match = _DISPLAY_UNIT_TOKEN.fullmatch(part)
        tokens.append((match[1], match[2]) if match else (part, None))
    return tokens


def format_unit_typst(unit: str) -> str:
    """Format units for Typst math, e.g. ``mm2`` becomes ``"mm"^(2)``."""
    return "".join(
        f'"{base}"^({exponent})' if exponent else f'"{base}"'
        for base, exponent in _parse_unit_tokens(unit)
    )


def format_unit_typst_markup(unit: str) -> str:
    """Format units for Typst markup, e.g. ``mm2`` becomes ``mm#super[2]``."""
    return "".join(
        f"{base}#super[{exponent}]" if exponent else base
        for base, exponent in _parse_unit_tokens(unit)
    )


def _format_number(value: float, num_format: str) -> str:
    if not num_format:
        magnitude = abs(value)
        if magnitude == 0:
            num_format = ".0f"
        elif magnitude < 0.1 or magnitude > 9999.9:
            num_format = ".2E"
        elif magnitude < 10:
            num_format = ".3f"
        elif magnitude < 100:
            num_format = ".2f"
        elif magnitude < 1000:
            num_format = ".1f"
        else:
            num_format = ".0f"
    return format(value, num_format)


def _format_value(value: float | np.ndarray, num_format: str) -> str:
    if not isinstance(value, np.ndarray):
        return _format_number(value, num_format)

    numbers = (_format_number(item, num_format) for item in value.flat)

    def format_shape(shape: tuple[int, ...]) -> str:
        if not shape:
            return next(numbers)
        elements = (format_shape(shape[1:]) for _ in range(shape[0]))
        return "[" + ", ".join(elements) + "]"

    return format_shape(value.shape or (1,))


class Quantity:
    """A scalar or NumPy array paired with a unit string, validated on conversion."""

    def __init__(self, value: float | int | list | np.ndarray, unit: str):
        if isinstance(value, list):
            value = np.array(value)
        self.value = value if isinstance(value, np.ndarray) else float(value)
        self.unit = unit

    def to(self, target_unit: str) -> Quantity:
        """Return a new quantity expressed in the target units."""
        return Quantity(conv(self.value, self.unit, target_unit), target_unit)

    def to_si(self) -> Quantity:
        """Scale to SI, expressing only mass, length, and time dimensions."""
        unit = Unit.from_string(self.unit)
        return Quantity(self.value * unit.scale, dims_to_si_unit(unit.dims))

    def __repr__(self) -> str:
        value = self.value
        if isinstance(value, np.ndarray):
            value = value.tolist()
        return f"Quantity({value}, '{self.unit}')"

    def __str__(self) -> str:
        value = self.value
        if isinstance(value, np.ndarray):
            value = value.tolist()
        return f"{value} {self.unit}"

    def __getitem__(self, key) -> Quantity:
        """Index or slice an array quantity, retaining its unit."""
        if not isinstance(self.value, np.ndarray):
            raise TypeError("Indexing is only supported for array quantities")
        value = self.value[key]
        return Quantity(float(value) if np.ndim(value) == 0 else value, self.unit)

    def _converted_value(self, other: Quantity, operation: str) -> float | np.ndarray:
        """Convert the other operand, with an operation-specific error message."""
        try:
            return conv(other.value, other.unit, self.unit)
        except ValueError:
            raise ValueError(
                f"Incompatible units for {operation}: '{self.unit}' and '{other.unit}'"
            ) from None

    def _comparison_value(self, other: object) -> float | np.ndarray:
        if not isinstance(other, Quantity):
            raise TypeError(
                "Quantity comparisons require another Quantity, "
                f"got {type(other).__name__}"
            )
        return self._converted_value(other, "comparison")

    def __eq__(self, other: object) -> bool | np.ndarray:
        return self.value == self._comparison_value(other)

    def __ne__(self, other: object) -> bool | np.ndarray:
        return self.value != self._comparison_value(other)

    def __lt__(self, other: object) -> bool | np.ndarray:
        return self.value < self._comparison_value(other)

    def __le__(self, other: object) -> bool | np.ndarray:
        return self.value <= self._comparison_value(other)

    def __gt__(self, other: object) -> bool | np.ndarray:
        return self.value > self._comparison_value(other)

    def __ge__(self, other: object) -> bool | np.ndarray:
        return self.value >= self._comparison_value(other)

    def __add__(self, other: Quantity) -> Quantity:
        if not isinstance(other, Quantity):
            return NotImplemented
        value = self.value + self._converted_value(other, "addition")
        return Quantity(value, self.unit)

    def __sub__(self, other: Quantity) -> Quantity:
        if not isinstance(other, Quantity):
            return NotImplemented
        value = self.value - self._converted_value(other, "subtraction")
        return Quantity(value, self.unit)

    def __mul__(self, other: Quantity | float | int) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(self.value * other, self.unit)
        if isinstance(other, Quantity):
            return Quantity(
                self.value * other.value, f"{self.unit} {other.unit}".strip()
            )
        return NotImplemented

    def __rmul__(self, other: float | int) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(self.value * other, self.unit)
        return NotImplemented

    def __truediv__(self, other: Quantity | float | int) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(self.value / other, self.unit)
        if isinstance(other, Quantity):
            return Quantity(
                self.value / other.value,
                f"{self.unit} {invert_unit(other.unit)}".strip(),
            )
        return NotImplemented

    def __rtruediv__(self, other: float | int) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(other / self.value, invert_unit(self.unit))
        return NotImplemented

    def format(self, num_format: str = "", style: str = "typst") -> str:
        """Format a value and its unit, choosing precision by magnitude by default."""
        number = _format_value(self.value, num_format)
        if style in ("typst", "typst-math"):
            unit = format_unit_typst(self.unit)
            separator = " space "
        elif style == "typst-markup":
            unit = format_unit_typst_markup(self.unit)
            separator = " "
        else:
            raise ValueError(f"Unknown style: '{style}'")
        return f"{number}{separator}{unit}" if unit else number
