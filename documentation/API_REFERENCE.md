# API Reference

Quick reference for Unity library functions and classes.

## Imports

```python
# Core functions
from unity.core import conv, valid, parse_unit, invert_unit, CanonicalUnit

# Quantity class
from unity.quantity import Quantity
```

## Core Functions

### `conv(value, from_unit, to_unit) -> Union[float, np.ndarray]`

Convert a value from one unit to another.

| Parameter | Type | Description |
|-----------|------|-------------|
| `value` | `float \| np.ndarray` | Value(s) to convert |
| `from_unit` | `str` | Source unit string |
| `to_unit` | `str` | Target unit string |

**Returns**: Converted value with same type/shape as input

**Raises**: `ValueError` if units are incompatible

**Examples**:
```python
conv(100, "cm", "m")                    # 1.0
conv(np.array([1000, 2000]), "m", "km")  # [1.0, 2.0]
```

---

### `valid(from_unit, to_unit) -> bool`

Check if two units are dimensionally compatible.

| Parameter | Type | Description |
|-----------|------|-------------|
| `from_unit` | `str` | Source unit string |
| `to_unit` | `str` | Target unit string |

**Returns**: `True` if compatible, `False` otherwise

**Examples**:
```python
valid("m", "km")                    # True
valid("m", "s")                     # False
valid("N", "kg m s-2")             # True
```

---

### `parse_unit(unit_str) -> CanonicalUnit`

Parse a unit string into canonical form.

| Parameter | Type | Description |
|-----------|------|-------------|
| `unit_str` | `str` | Unit string (e.g., "kg m s-2") |

**Returns**: `CanonicalUnit` object with scale and dimensions

**Raises**: `ValueError` if unit is malformed

**Examples**:
```python
canonical = parse_unit("km")
print(canonical.scale)   # 1000.0
print(canonical.dims)    # {'L': 1}
```

---

### `invert_unit(unit_str) -> str`

Invert a unit (useful for division).

| Parameter | Type | Description |
|-----------|------|-------------|
| `unit_str` | `str` | Unit to invert |

**Returns**: Inverted unit string

**Examples**:
```python
invert_unit("s")            # "s-1"
invert_unit("m2")           # "m-2"
invert_unit("kg m s-2")     # "kg-1 m-1 s2"
```

---

## Quantity Class

### Constructor

```python
Quantity(value: Union[float, int, list, np.ndarray], unit: str)
```

Create a new Quantity.

| Parameter | Type | Description |
|-----------|------|-------------|
| `value` | `float \| int \| list \| np.ndarray` | The numeric value(s) |
| `unit` | `str` | Unit string |

**Notes**:
- Lists are automatically converted to numpy arrays
- Type is preserved: scalars stay scalars, arrays stay arrays

**Examples**:
```python
Quantity(5.0, "m")                  # Scalar
Quantity([1, 2, 3], "m")           # Array (list converted)
Quantity(np.array([1, 2, 3]), "m")  # Array (numpy)
```

---

### `to(target_unit) -> Quantity`

Convert to a different unit.

| Parameter | Type | Description |
|-----------|------|-------------|
| `target_unit` | `str` | Target unit string |

**Returns**: New `Quantity` with converted value and unit

**Raises**: `ValueError` if units are incompatible

**Examples**:
```python
q = Quantity(5, "km")
q_m = q.to("m")          # Quantity(5000, "m")

q_arr = Quantity([1, 2], "km")
q_cm = q_arr.to("cm")    # Quantity([100000, 200000], "cm")
```

---

### `format(num_format="", style="typst") -> str`

Format as a formatted string.

| Parameter | Type | Description |
|-----------|------|-------------|
| `num_format` | `str` | Format spec (e.g., ".2f"). Empty uses magnitude-based formatting |
| `style` | `str` | Output style (default: "typst") |

**Returns**: Formatted string

**Format Rules** (when `num_format=""`):
- Value = 0: `"0"`
- 0 < \|value\| < 0.1 or \|value\| > 9999.9: Scientific (`.2E`)
- 0.1 ≤ \|value\| < 10: `.3f`
- 10 ≤ \|value\| < 100: `.2f`
- 100 ≤ \|value\| < 1000: `.1f`
- 1000 ≤ \|value\| ≤ 9999.9: `.0f`

**Examples**:
```python
Quantity(5.0, "m").format()              # "5.000 m"
Quantity(0.001, "m").format()            # "1.00E-03 m"
Quantity([1.5, 25, 1234], "m").format()  # "[1.500, 25.00, 1234] m"
Quantity(5.123, "m").format(".1f")       # "5.1 m"
```

---

### Arithmetic Operators

#### Addition (`+`)

```python
q1 + q2 -> Quantity
```

Adds quantities with the same units.

- Scalar ± Scalar → Scalar
- Array ± Array → Array (element-wise)
- Scalar ± Array → Array (broadcasting)

**Examples**:
```python
Quantity(10, "m") + Quantity(5, "m")  # 15.0 m
Quantity([1, 2], "m") + Quantity([3, 4], "m")  # [4, 6] m
Quantity(10, "m") + Quantity([1, 2], "m")      # [11, 12] m
```

---

#### Subtraction (`-`)

```python
q1 - q2 -> Quantity
```

Same behavior as addition.

**Examples**:
```python
Quantity(10, "m") - Quantity(3, "m")  # 7.0 m
Quantity([10, 20], "m") - Quantity([1, 2], "m")  # [9, 18] m
```

---

#### Multiplication (`*`)

```python
q1 * q2 -> Quantity
q * scalar -> Quantity
scalar * q -> Quantity
```

Element-wise multiplication with unit combination.

**Examples**:
```python
Quantity(10, "m") * Quantity(2, "s")     # 20.0 m s
Quantity([1, 2, 3], "m") * 2             # [2, 4, 6] m
2 * Quantity([1, 2, 3], "m")             # [2, 4, 6] m
Quantity([2, 3], "N") * Quantity([5, 10], "m")  # [10, 30] N m
```

---

#### Division (`/`)

```python
q1 / q2 -> Quantity
q / scalar -> Quantity
scalar / q -> Quantity
```

Element-wise division with unit inversion for divisor.

**Examples**:
```python
Quantity(10, "m") / Quantity(2, "s")     # 5.0 m s-1
Quantity([10, 20, 30], "m") / 2          # [5, 10, 15] m
Quantity([100, 200], "m") / Quantity([10, 20], "s")  # [10, 10] m s-1
```

---

### Indexing & Slicing

#### `__getitem__(key) -> Quantity`

```python
q[index] -> Quantity
q[slice] -> Quantity
```

Access array elements or slices.

- Single index returns **scalar** Quantity
- Slice returns **array** Quantity

**Raises**: `TypeError` if called on scalar quantity

**Examples**:
```python
q = Quantity([10, 20, 30, 40, 50], "m")

q[0]        # Quantity(10.0, "m") - scalar
q[-1]       # Quantity(50.0, "m") - scalar
q[1:4]      # Quantity([20, 30, 40], "m") - array
q[::2]      # Quantity([10, 30, 50], "m") - array
q[::-1]     # Quantity([50, 40, 30, 20, 10], "m") - reversed
```

---

### String Representations

#### `__str__() -> str`

Human-readable string representation.

```python
str(Quantity(5.0, "m"))              # "5.0 m"
str(Quantity([1, 2, 3], "m"))        # "[1, 2, 3] m"
```

---

#### `__repr__() -> str`

Detailed representation.

```python
repr(Quantity(5.0, "m"))              # "Quantity(5.0, 'm')"
repr(Quantity([1, 2, 3], "m"))        # "Quantity([1, 2, 3], 'm')"
```

---

## Properties

### `value`

The underlying numeric value(s).

- For scalars: `float`
- For arrays: `np.ndarray`

```python
q1 = Quantity(5, "m")
print(q1.value)           # 5.0
print(type(q1.value))     # <class 'float'>

q2 = Quantity([1, 2, 3], "m")
print(q2.value)           # [1 2 3]
print(type(q2.value))     # <class 'numpy.ndarray'>
```

---

### `unit`

The unit string.

```python
q = Quantity(5, "m")
print(q.unit)  # "m"
```

---

## Common Unit Strings

### Base Units

| Dimension | Units |
|-----------|-------|
| **Mass** | kg, g, mg, t, lb, oz |
| **Length** | m, mm, cm, km, in, ft, yd, mi |
| **Time** | s, min, h, d, y |

### Derived Units

| Unit | Definition |
|------|------------|
| N (Newton) | kg m s-2 |
| Pa (Pascal) | N m-2 = kg m-1 s-2 |
| J (Joule) | N m = kg m2 s-2 |
| W (Watt) | J s-1 = kg m2 s-3 |
| Hz (Hertz) | s-1 |

### Compound Unit Syntax

```
[unit][exponent] [unit][exponent] ...
```

Examples:
- `m2` → square meters
- `m s-1` → meters per second
- `kg m s-2` → force (Newton)
- `kg m2 s-2` → energy (Joule)

---

## Exception Reference

### `ValueError`

Raised when:
- Units are dimensionally incompatible
- Unit strings are malformed
- Unknown units are used

```python
try:
    conv(100, "m", "s")
except ValueError as e:
    print(e)  # "Incompatible units: ..."
```

---

### `TypeError`

Raised when:
- Indexing is attempted on a scalar quantity
- Invalid operand types for operations

```python
try:
    q = Quantity(5, "m")
    val = q[0]
except TypeError as e:
    print(e)  # "Indexing is only supported for array quantities"
```

---

## Quick Examples

### Convert Multiple Values

```python
import numpy as np
from unity.quantity import Quantity

distances_km = Quantity([1, 5, 10, 50], "km")
distances_m = distances_km.to("m")
# Quantity([1000, 5000, 10000, 50000], "m")
```

### Physics Calculation

```python
from unity.quantity import Quantity

# F = ma
mass = Quantity([1, 2, 5], "kg")
acceleration = Quantity([10, 20, 15], "m s-2")
force = mass * acceleration
# Quantity([10, 40, 75], "kg m s-2")
```

### Broadcasting

```python
from unity.quantity import Quantity

speed = Quantity(10, "m s-1")          # Scalar
times = Quantity([1, 2, 3, 4], "s")    # Array
distances = speed * times
# Quantity([10, 20, 30, 40], "m")
```

### Statistics with Quantities

```python
import numpy as np
from unity.quantity import Quantity

measurements = Quantity([100, 150, 120, 180], "m")
mean = np.mean(measurements.value)
print(f"Mean: {mean} m")  # Mean: 137.5 m
```

---

## Type Hints

When writing code with Unity, use these type hints:

```python
from typing import Union
import numpy as np
from unity.quantity import Quantity

def process_distance(d: Quantity) -> Quantity:
    """Process a distance quantity."""
    return d * 2

def convert_multiple(values: Union[float, np.ndarray], unit: str) -> Quantity:
    """Convert multiple values."""
    return Quantity(values, unit).to("m")
```

---

## See Also

- [README.md](README.md) - Overview and quick start
- [reference.md](reference.md) - Detailed documentation
- [ARRAYS.md](ARRAYS.md) - Array operations guide
- [examples/](examples/) - Working examples

