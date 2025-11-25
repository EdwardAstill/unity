# Unity Reference Documentation

This document provides a comprehensive reference for the `unity` library, including API usage, supported units, and syntax for compound units.

## Core API

### `conv(value, from_unit, to_unit)`

Converts a numeric value from one unit to another.

- **Parameters**:
  - `value` (float): The magnitude to convert.
  - `from_unit` (str): The string representation of the source unit (e.g., `"kg"`, `"m s-1"`).
  - `to_unit` (str): The string representation of the target unit.
- **Returns**: `float` - The converted value.
- **Raises**: `ValueError` if units are dimensionally incompatible or unknown.

**Example**:
```python
from unity.main import conv
speed = conv(100, "km h-1", "m s-1")
```

### `valid(from_unit, to_unit)`

Checks if a conversion between two units is dimensionally valid.

- **Parameters**:
  - `from_unit` (str): Source unit string.
  - `to_unit` (str): Target unit string.
- **Returns**: `bool` - `True` if valid, `False` if incompatible or unknown.

**Example**:
```python
from unity.main import valid
if valid("N", "kg m s-2"):
    print("Compatible!")
```

### `Quantity` Class

An object-oriented wrapper for handling values with units.

#### `__init__(value, unit)`
Creates a new Quantity.
```python
q = Quantity(500, "mg")
```

#### `to(target_unit)`
Returns a new `Quantity` converted to the target unit.
```python
q_kg = q.to("kg")
print(q_kg) # "0.0005 kg"
```

---

## Supported Units

The following atomic units are defined in the database. You can combine these to form compound units.

### Mass (Base: kg)
| Unit | Scale (kg) | Description |
|------|------------|-------------|
| `kg` | 1.0        | Kilogram    |
| `g`  | 0.001      | Gram        |
| `mg` | 1e-6       | Milligram   |
| `t`  | 1000       | Tonne       |

### Length (Base: m)
| Unit | Scale (m) | Description |
|------|-----------|-------------|
| `m`  | 1.0       | Meter       |
| `mm` | 0.001     | Millimeter  |
| `cm` | 0.01      | Centimeter  |
| `km` | 1000      | Kilometer   |

### Time (Base: s)
| Unit | Scale (s) | Description |
|------|-----------|-------------|
| `s`  | 1.0       | Second      |
| `min`| 60.0      | Minute      |
| `h`  | 3600.0    | Hour        |

### Derived Units
| Unit  | Definition | Dimensions |
|-------|------------|------------|
| `N`   | Newton     | Mass * Length * Time⁻² |
| `Pa`  | Pascal     | Mass * Length⁻¹ * Time⁻² |
| `kPa` | Kilopascal | 1000 * Pa |

---

## Compound Unit Syntax

You can create complex units by separating atomic units with spaces. Exponents are appended directly to the unit name (integer only).

**Syntax**: `[unit][exponent] [unit][exponent] ...`

- **Multiplication**: Implicit with space.
- **Division**: Use negative exponents.
- **Exponents**: Optional integers (default is 1).

### Examples
| Concept | Notation | Interpretation |
|---------|----------|----------------|
| Area | `m2` | meters squared |
| Volume | `mm3` | millimeters cubed |
| Velocity | `m s-1` | meters per second |
| Acceleration | `m s-2` | meters per second squared |
| Force | `kg m s-2` | Equivalent to `N` |
| Pressure | `N m-2` | Equivalent to `Pa` |

### Comparison Example
A force of 1 Newton is defined as $1 \text{ kg} \cdot \text{m} \cdot \text{s}^{-2}$.
Using the library, `valid("N", "kg m s-2")` returns `True`.

