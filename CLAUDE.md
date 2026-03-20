# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Unity is a Python unit conversion and dimensional analysis library supporting scalars, lists, and numpy arrays. It uses a canonical scale+dimensions approach: every unit is stored as a scale factor relative to SI base units plus a dimension exponent map (M, L, T, A, I, Theta).

## Build & Run

```bash
pip install -e .           # Install in editable mode (requires Python >=3.13, numpy>=1.24)
```

## Testing

Tests use `unittest` and live in `testing/`. Run all tests:
```bash
python -m pytest testing/  # or run individually:
python testing/test.py                  # Core conversion tests
python testing/test_quantity_ops.py     # Arithmetic operations
python testing/test_quantity_format.py  # Formatting
python testing/test_quantity_arrays.py  # Array/broadcasting
python testing/test_angles.py          # Angle unit tests
```

There is also a standalone `test_to_si.py` in the project root (not unittest-based, just print assertions).

## Architecture

All source is under `src/unity/`:

- **`db.py`** — `UNIT_DB` dictionary: the single source of truth for all supported units. Each entry maps a unit string to `{"scale": float, "dims": {"M": int, "L": int, ...}}`. To add a new unit, add an entry here.
- **`core.py`** — Parsing and conversion engine. `parse_unit()` tokenizes a unit string (space-separated tokens like `"kg m s-2"`), looks up each token in `UNIT_DB`, and returns a `CanonicalUnit(scale, dims)`. `conv()` converts values between units by comparing canonical forms. `invert_unit()` negates exponents for division.
- **`quantity.py`** — `Quantity` class wrapping a value (float or ndarray) + unit string. Supports arithmetic (`+`, `-`, `*`, `/`), unit conversion (`.to()`, `.to_si()`), indexing/slicing for arrays, and Typst-formatted output (`.format()`).
- **`main.py`** — Legacy re-export module (imports from core and quantity).

## Key Design Decisions

- **Unit strings are space-separated tokens** with optional integer exponents: `"kg m s-2"`, `"mm2"`. No `/` or `^` syntax in internal representation.
- **Multiplication concatenates unit strings** (`"N" * "m"` → `"N m"`); **division inverts exponents** (`"m" / "s"` → `"m s-1"`). These are string operations, not simplified.
- **Dimensional compatibility** is checked by comparing dimension dicts. Addition/subtraction require matching dims; multiplication/division do not.
- **Temperature** only supports Kelvin (no offset-based °C/°F conversions).
- **`.format()`** outputs Typst markup (e.g., `m#super[2]`, `\u{22C5}` for dot separator).
