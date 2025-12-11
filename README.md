# Unity - Unit Conversion System

A robust and flexible unit conversion library with support for scalar values, lists, and numpy arrays. Designed for scientific and engineering calculations with automatic dimensional analysis.

## Features

- **Canonical Representation**: Internally converts all units to a base scale and dimension map (Mass, Length, Time).
- **Compound Units**: Supports complex unit strings like `kg m s-2` or `kPa m2`.
- **Dimensional Analysis**: Validates that source and target units are dimensionally equivalent before converting.
- **Quantity Object**: Ergonomic API for unit conversions and arithmetic.
- **Array Support**: Handle scalar values, lists, and numpy arrays with the same intuitive interface.
- **Broadcasting**: Seamless operations between array and scalar quantities.
- **Indexing & Slicing**: Full numpy-style indexing and slicing support for array quantities.
- **Element-wise Operations**: Automatic element-wise arithmetic operations on arrays.

## Quick Start

### Basic Conversion

```python
from unity.quantity import Quantity

# Create a scalar quantity
distance = Quantity(5000, "m")

# Convert to another unit
distance_km = distance.to("km")
print(distance_km)  # 5.0 km
```

### Scalar Arithmetic

```python
# Basic arithmetic with automatic unit handling
distance = Quantity(10, "m")
time = Quantity(2, "s")
velocity = distance / time
print(velocity)  # 5.0 m s-1

force = Quantity(100, "N")
work = force * distance
print(work)  # 1000 N m
```

### Array Support

```python
import numpy as np

# Create array quantities from lists or numpy arrays
distances = Quantity([100, 200, 300], "m")
times = Quantity([10, 20, 15], "s")

# Element-wise operations
velocities = distances / times
print(velocities)  # [10.0, 10.0, 20.0] m s-1

# Broadcasting (array + scalar)
adjusted = distances + Quantity(50, "m")
print(adjusted)  # [150, 250, 350] m
```

### Indexing and Slicing

```python
speeds = Quantity([5, 10, 15, 20, 25], "m s-1")

# Get single element
first_speed = speeds[0]
print(first_speed)  # 5.0 m s-1

# Slice array
subset = speeds[1:4]
print(subset)  # [10, 15, 20] m s-1

# Stride
every_other = speeds[::2]
print(every_other)  # [5, 15, 25] m s-1
```

### Unit Validation

```python
from unity.core import valid

# Check if conversion is possible
print(valid("mg", "kg"))  # True
print(valid("m", "s"))    # False
```

## Supported Units

The current database supports a wide range of units including:
- **Mass**: kg, g, mg, t, lb, oz, tn...
- **Length**: m, mm, cm, km, in, ft, yd, mi...
- **Time**: s, min, h, d, y...
- **Derived**: N, Pa, kPa, psi, J, W, Hz...
- **Compound**: Any combination of the above (e.g., `kg m s-2`, `m s-1`)

## Installation

```bash
pip install -e .
```

This will install `unity` with numpy as a dependency.

## Examples

### Scalar-Only Calculation

```python
from unity.quantity import Quantity

# Convert 100 mg to kg
q = Quantity(100, "mg")
q_kg = q.to("kg")
print(q_kg)  # 0.0001 kg
```

### Array-Based Physics

```python
import numpy as np
from unity.quantity import Quantity

# Calculate work done by varying forces
forces = Quantity([50, 100, 150, 200], "N")
distance = Quantity(10, "m")
work = forces * distance
print(work)  # [500.0, 1000.0, 1500.0, 2000.0] N m
```

### Mixed Unit Operations

```python
# Addition with automatic conversion
distance1 = Quantity([1, 2, 3], "km")
distance2 = Quantity([500, 750, 1000], "m")
total = distance1 + distance2
print(total)  # [1.5, 2.75, 4.0] km
```

### Formatted Output

```python
# Beautiful formatted output
temperatures = Quantity([0.001, 5.5, 150, 10000], "m")
print(temperatures.format())
# [1.00E-03, 5.500, 150.0, 1.00E+04] m
```

## Testing

Run the included test suites:

```bash
python testing/test_quantity_ops.py       # Scalar operations
python testing/test_quantity_format.py    # Formatting
python testing/test_quantity_arrays.py    # Array functionality
```

Run the demo scripts:

```bash
python examples/demo.py              # Basic examples
python examples/array_demo.py        # Array examples
```

