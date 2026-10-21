# Unity

Unit conversion and dimensional analysis for scalars and NumPy arrays.
Requires Python 3.13+ and NumPy; install from the repository with `pip install -e .`.

## Unit strings

Use space-separated unit names with optional integer exponents: `"kg m s-2"`,
`"mm2"`, `"m s-1"`. Names are case-sensitive; `/`, `^`, and `**` are not conversion
syntax. Use `""` for dimensionless values (`"-"`, `"dimensionless"`, `"ratio"`, and
`"none"` are also accepted by `Unit.from_string`). Supported names and scales are in
[`src/unity/db.py`](src/unity/db.py). Temperature conversion supports Kelvin
units only, not Celsius or Fahrenheit offsets.

## Functions

| Function | Result |
| --- | --- |
| `conv(value, from_unit, to_unit)` | Convert a number or NumPy array. Returns the converted value, not a `Quantity`. Raises `ValueError` for malformed, unknown, or incompatible units. Use `Quantity` for list inputs. |
| `is_compatible(from_unit, to_unit)` | Return `True` when the units have matching dimensions; `False` for incompatible, malformed, or unknown units. |
| `invert_unit(unit_str)` | Negate each token's exponent: `"m s-2"` becomes `"m-1 s2"`. Checks token syntax, not whether unit names exist. |

## Unit object

`Unit.from_string(unit_str)` is a classmethod that parses a unit string and returns
a `Unit` with `.scale` relative to SI and `.dims`, a dictionary of dimension
exponents. Malformed or unknown units raise `ValueError`.

`Unit(scale, dims)` constructs directly from a scale and dimension dictionary,
omitting zero exponents. Dimension keys are `M` (mass), `L` (length), `T` (time),
`A` (angle), `I` (current), and `Theta` (temperature).

## Quantity object

`Quantity(value, unit)` accepts an `int`, `float`, list, or NumPy array.
`.value` holds a float for scalars or an ndarray for arrays; lists become arrays,
and existing arrays are stored without copying. `.unit` holds the unit string.
Construction stores the unit without validating it.

### Methods

| Method | Result |
| --- | --- |
| `q.to(target_unit)` | Return a new `Quantity` in the target units; leave `q` unchanged. Raises `ValueError` for malformed, unknown, or incompatible units. |
| `q.to_si()` | Return a new `Quantity` scaled to SI base units. **Currently only mass, length, and time dimensions are preserved; angle, current, and temperature dimensions are dropped.** Use `.to(...)` for units involving those dimensions. |
| `q.format(num_format="", style="typst")` | Return formatted text for a scalar or an array of any dimension. `num_format` is a Python number format such as `".2f"`; when empty, precision depends on magnitude. `"typst"` and `"typst-math"` produce Typst math syntax; `"typst-markup"` produces content markup. Other styles raise `ValueError`. |
| `str(q)` | Return the value followed by the unit. |
| `repr(q)` | Return a representation such as `Quantity(5.0, 'm')`. |
| `q[key]` | Return an indexed or sliced `Quantity` with the same unit, using NumPy indexing. Scalar quantities raise `TypeError`. |

### Operators

| Operation | Behavior |
| --- | --- |
| `q + other`, `q - other` | Require another compatible `Quantity`; convert it to `q.unit` before operating. Incompatible units raise `ValueError`. |
| `q * other`, `q / other` | Accept another `Quantity` or an `int`/`float`. Quantity multiplication concatenates units; division negates the divisor's exponents. Unit strings are not simplified. |
| `number * q`, `number / q` | Scale the value; division also inverts the units. |
| `q == other`, `q != other`, `q < other`, `q <= other`, `q > other`, `q >= other` | Convert another compatible `Quantity` to `q.unit`, then compare. Return a boolean for scalars or a boolean array for array comparisons. Incompatible units raise `ValueError`; bare numbers raise `TypeError`. |

Array arithmetic and comparisons are element-wise and follow NumPy broadcasting.

## Module helpers

These functions are available from their modules, not the top-level package:

| Function | Result |
| --- | --- |
| `dims_to_si_unit(dims)` | Build a unit string from `M`, `L`, and `T` exponents in sorted-key order; other dimension keys are ignored. Returns `""` for no dimensions. |
| `format_unit_typst(unit)` | Format units for Typst math: `"m2"` becomes `'"m"^(2)'`. |
| `format_unit_typst_markup(unit)` | Format units for Typst markup: `"m2"` becomes `"m#super[2]"`. |

## Examples

### Convert a value

```python
from unity import conv

print(conv(100, "cm", "m"))  # 1.0
print(conv(1, "kN", "N"))  # 1000.0
```

### Check unit compatibility

```python
from unity import is_compatible

print(is_compatible("N", "kg m s-2"))  # True
print(is_compatible("m", "s"))  # False
```

### Inspect a unit

```python
from unity import Unit

unit = Unit.from_string("mm2")
print(unit.scale)  # 1e-06
print(unit.dims)  # {'L': 2}
print(Unit(1, {"L": 1, "T": 0}).dims)  # {'L': 1}
```

### Invert a unit

```python
from unity import invert_unit

print(invert_unit("s-1"))  # s
print(invert_unit("m s-2"))  # m-1 s2
```

### Convert a quantity

```python
from unity import Quantity

distance = Quantity(2.5, "km")
print(distance.to("m"))  # 2500.0 m
```

### Convert to SI base units

```python
from unity import Quantity

print(Quantity(1, "km").to_si())  # 1000.0 m
print(Quantity(100, "N").to_si())  # 100.0 m kg s-2
```

### Convert an array

```python
from unity import Quantity

distances = Quantity([1, 2, 3], "km")
print(distances.to("m"))  # [1000.0, 2000.0, 3000.0] m
```

### Index and slice an array

```python
from unity import Quantity

distances = Quantity([1, 2, 3], "km")
print(distances[0])  # 1.0 km
print(distances[1:])  # [2, 3] km
```

### Add and subtract quantities

```python
from unity import Quantity

distance = Quantity(10, "m")
print(distance + Quantity(500, "cm"))  # 15.0 m
print(distance - Quantity(500, "cm"))  # 5.0 m
```

### Multiply and divide quantities

```python
from unity import Quantity

distance = Quantity(10, "m")
work = Quantity(100, "N") * distance
print(work.to("J"))  # 1000.0 J
print(distance / Quantity(2, "s"))  # 5.0 m s-1
print(2 * distance)  # 20.0 m
```

### Compare quantities

```python
from unity import Quantity

print(Quantity(1, "kN") == Quantity(1000, "N"))  # True
print(Quantity(2, "m") > Quantity(150, "cm"))  # True
```

### Broadcast arrays

```python
from unity import Quantity

distances = Quantity([[1], [2]], "m")
offsets = Quantity([100, 200], "cm")
print(distances + offsets)  # [[2.0, 3.0], [3.0, 4.0]] m
print((distances > offsets).tolist())  # [[False, False], [True, False]]
```

### Format a quantity for Typst

```python
from unity import Quantity

area = Quantity(5, "m2")
print(area.format())  # 5.000 space "m"^(2)
print(area.format(".2f"))  # 5.00 space "m"^(2)
print(area.format(".2f", "typst-markup"))  # 5.00 m#super[2]
```

### Format a multidimensional array

```python
from unity import Quantity

values = Quantity([[[1, 2]], [[3, 4]]], "m")
print(values.format(".1f"))  # [[[1.0, 2.0]], [[3.0, 4.0]]] space "m"
```

### Use angles with NumPy

Convert angles to radians before passing their values to NumPy.

```python
import numpy as np
from unity import Quantity

angles = Quantity([0, 30, 90], "deg").to("rad")
print(np.sin(angles.value).round(3).tolist())  # [0.0, 0.5, 1.0]
```

### Build an SI unit string

```python
from unity.core import dims_to_si_unit

print(dims_to_si_unit({"M": 1, "L": 1, "T": -2}))  # m kg s-2
```

### Format a unit for Typst

```python
from unity.quantity import format_unit_typst, format_unit_typst_markup

print(format_unit_typst("m2"))  # "m"^(2)
print(format_unit_typst_markup("m2"))  # m#super[2]
```

## Testing

Run the examples with `python test.py`.
