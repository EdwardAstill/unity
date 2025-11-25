# Unity - Unit Conversion System

A robust unit conversion tool using a canonical form approach.

## Features

- **Canonical Representation**: Internally converts all units to a base scale and dimension map (Mass, Length, Time).
- **Compound Units**: Supports complex unit strings like `kg m s-2` or `kPa m2`.
- **Dimensional Analysis**: Validates that source and target units are dimensionally equivalent before converting.
- **Quantity Object**: Ergonomic API for unit conversions.

## Usage

### Simple Function Call

```python
from main import conv

# Convert 100 mg to kg
result = conv(100, "mg", "kg")
print(result)  # 0.0001
```

### Quantity Object

```python
from main import Quantity

q = Quantity(5000, "N")
new_q = q.to("kN")
print(new_q)  # 5.0 kN
```

## Supported Units

The current database supports:
- **Mass**: kg, g, mg, t
- **Length**: m, mm, cm, km
- **Time**: s, min, h
- **Derived**: N, Pa, kPa

## Running Verification

Run the script directly to see verification cases:

```bash
python main.py
```

