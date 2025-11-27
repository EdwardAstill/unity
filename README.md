# Unity - Unit Conversion System

A robust unit conversion tool using a canonical form approach.

## Features

- **Canonical Representation**: Internally converts all units to a base scale and dimension map (Mass, Length, Time).
- **Compound Units**: Supports complex unit strings like `kg m s-2` or `kPa m2`.
- **Dimensional Analysis**: Validates that source and target units are dimensionally equivalent before converting.
- **Quantity Object**: Ergonomic API for unit conversions and arithmetic.

## Usage

### Simple Function Call

```python
from unity.main import conv

# Convert 100 mg to kg
result = conv(100, "mg", "kg")
print(result)  # 0.0001
```

### Validation

```python
from unity.main import valid

# Check if conversion is possible (dimensionally equivalent)
print(valid("mg", "kg"))  # True
print(valid("m", "s"))    # False
```

### Quantity Object

The `Quantity` object allows for object-oriented usage and supports arithmetic operations that handle units automatically.

```python
from unity.main import Quantity

# Basic conversion
q = Quantity(5000, "N")
new_q = q.to("kN")
print(new_q)  # 5.0 kN

# Arithmetic
d = Quantity(10, "m")
t = Quantity(2, "s")

# Division (Length / Time -> Speed)
v = d / t
print(v)  # 5.0 m s-1

# Multiplication (Force * Distance -> Work)
f = Quantity(100, "N")
w = f * d
print(w)  # 1000 N m
print(w.to("kJ")) # 1.0 kJ

# Addition (Auto-conversion)
l1 = Quantity(1, "km")
l2 = Quantity(500, "m")
total = l1 + l2
print(total) # 1.5 km
```

## Supported Units

The current database supports a wide range of units including:
- **Mass**: kg, g, mg, t, lb, oz, tn...
- **Length**: m, mm, cm, km, in, ft, yd, mi...
- **Time**: s, min, h, d, y...
- **Derived**: N, Pa, kPa, psi, J, W, Hz...
- **Compound**: Any combination of the above (e.g., `kg m s-2`, `m s-1`)

## Running Verification

Run the included tests to verify functionality:

```bash
python testing/test.py
python testing/test_quantity_ops.py
```

Run the demo script for examples:

```bash
python examples/demo.py
```
