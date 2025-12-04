# Getting Started with Unity

A comprehensive guide to get you up and running with the Unity unit conversion library.

## What is Unity?

Unity is a Python library for **unit conversion and dimensional analysis**. It helps you:

- Convert between different units (meters to kilometers, etc.)
- Perform arithmetic with units (e.g., divide distance by time to get speed)
- Validate dimensional compatibility before operations
- Work with scalar values, lists, or numpy arrays seamlessly

## Installation

Unity requires Python 3.13+ and numpy.

```bash
# Clone the repository
git clone <repository-url>
cd unity

# Install the package
pip install -e .
```

This installs Unity and its numpy dependency in editable mode.

## Basic Concepts

### Units

A unit is a label for a physical quantity:
- `"m"` → meters (length)
- `"s"` → seconds (time)
- `"kg"` → kilograms (mass)

### Compound Units

Combine units with spaces and exponents:
- `"m s-1"` → meters per second (velocity)
- `"kg m s-2"` → kilograms meter per second squared (force, equivalent to Newton)
- `"kg m2 s-2"` → energy (Joule)

### The Quantity

A `Quantity` is a value with a unit:

```python
from unity.quantity import Quantity

distance = Quantity(100, "m")     # 100 meters
time = Quantity(10, "s")          # 10 seconds
```

## Your First Conversion

Convert a single value from one unit to another:

```python
from unity.quantity import Quantity

# Create a quantity
distance = Quantity(5, "km")

# Convert to meters
distance_meters = distance.to("m")
print(distance_meters)  # 5000.0 m
```

## Your First Calculation

Perform arithmetic that automatically handles units:

```python
from unity.quantity import Quantity

distance = Quantity(100, "m")
time = Quantity(10, "s")

# Calculate velocity (distance / time)
velocity = distance / time
print(velocity)  # 10.0 m s-1
```

Velocity has the correct unit! The `s` from time is inverted to `s-1`.

## Scalar vs Array

### Scalar Quantities (Single Values)

```python
from unity.quantity import Quantity

# A single value
distance = Quantity(100, "m")
print(distance)  # 100.0 m
```

### Array Quantities (Multiple Values)

```python
from unity.quantity import Quantity

# Multiple values from a list
distances = Quantity([100, 200, 300], "m")
print(distances)  # [100, 200, 300] m

# Operations work on all elements
doubled = distances * 2
print(doubled)  # [200, 400, 600] m
```

## Working with Scalars

### Creating Scalar Quantities

```python
from unity.quantity import Quantity

q1 = Quantity(10, "m")        # float
q2 = Quantity(10, "m")        # int (converted to float)
```

### Converting Units

```python
q = Quantity(1, "km")
q_m = q.to("m")     # 1000 m
q_cm = q.to("cm")   # 100000 cm
```

### Arithmetic with Scalars

```python
d = Quantity(10, "m")
t = Quantity(2, "s")

v = d / t              # 5.0 m s-1
w = d + Quantity(5, "m")  # 15.0 m
f = d * Quantity(100, "N")  # 1000 N m
```

### Formatting Scalars

```python
q = Quantity(5.123, "m")
print(q.format())       # "5.123 m" (auto-format)
print(q.format(".1f"))  # "5.1 m" (custom format)
```

## Working with Arrays

### Creating Array Quantities

```python
from unity.quantity import Quantity
import numpy as np

# From list
arr1 = Quantity([1, 2, 3], "m")

# From numpy array
arr2 = Quantity(np.array([10, 20, 30]), "m")

# Lists are automatically converted to arrays internally
print(type(arr1.value))  # <class 'numpy.ndarray'>
```

### Element-wise Operations

When operating on two arrays, operations apply to each element:

```python
speeds = Quantity([10, 20, 30], "m s-1")
times = Quantity([2, 2, 2], "s")

distances = speeds * times
print(distances)  # [20, 40, 60] m
```

### Broadcasting

Operations between scalars and arrays broadcast automatically:

```python
baseline = Quantity(100, "m")
offsets = Quantity([0, 10, 20], "m")

results = baseline + offsets
print(results)  # [100, 110, 120] m
```

### Indexing Arrays

Access individual elements or slices:

```python
speeds = Quantity([10, 20, 30, 40, 50], "m s-1")

first = speeds[0]       # Quantity(10.0, "m s-1") - scalar
last = speeds[-1]       # Quantity(50.0, "m s-1") - scalar
middle = speeds[1:4]    # Quantity([20, 30, 40], "m s-1") - array
every_other = speeds[::2]  # Quantity([10, 30, 50], "m s-1") - array
```

### Converting Array Units

```python
distances_km = Quantity([1, 5, 10], "km")
distances_m = distances_km.to("m")
print(distances_m)  # [1000, 5000, 10000] m
```

### Formatting Arrays

```python
values = Quantity([0.001, 1.5, 25, 10000], "m")
print(values.format())
# [1.00E-03, 1.500, 25.00, 1.00E+04] m
```

## Real-World Examples

### Example 1: Speed Calculation

Calculate the speed of multiple objects:

```python
from unity.quantity import Quantity

# Multiple objects travel distances in known times
distances = Quantity([100, 250, 500, 1000], "m")
time = Quantity(10, "s")

speeds = distances / time
print(speeds)  # [10, 25, 50, 100] m s-1
print(speeds.format())  # Nicely formatted output
```

### Example 2: Unit Conversion Pipeline

Convert measurements from different sources to a standard unit:

```python
from unity.quantity import Quantity

# Measurements in different units
height_in = Quantity(72, "in")      # inches
height_cm = Quantity(180, "cm")     # centimeters

# Convert to meters
height_m_1 = height_in.to("m")
height_m_2 = height_cm.to("m")

print(f"Height 1: {height_m_1}")  # ~1.829 m
print(f"Height 2: {height_m_2}")  # 1.8 m
```

### Example 3: Physics Problem

Calculate kinetic energy for objects with different masses at the same speed:

```python
from unity.quantity import Quantity

# E_k = 0.5 * m * v²
masses = Quantity([1, 2, 5, 10], "kg")
velocity = Quantity(10, "m s-1")

kinetic_energy = 0.5 * masses * velocity**2
print(kinetic_energy)  # [50, 100, 250, 500] kg m2 s-2
print(kinetic_energy.format())  # Formatted with units
```

### Example 4: Data Processing

Calculate statistics on measurements with units:

```python
import numpy as np
from unity.quantity import Quantity

measurements = Quantity([100.5, 102.3, 99.8, 101.2, 98.5], "m")

# Get statistics
mean = np.mean(measurements.value)
std = np.std(measurements.value)
max_val = np.max(measurements.value)
min_val = np.min(measurements.value)

print(f"Mean: {mean} m")
print(f"Std: {std} m")
print(f"Range: {min_val} - {max_val} m")
```

## Common Workflows

### Workflow 1: Unit Validation

Before performing calculations, check if units are compatible:

```python
from unity.core import valid

if valid("m", "km"):
    result = q1 + q2
else:
    print("Cannot add these quantities")
```

### Workflow 2: Batch Conversion

Convert multiple measurements to standard units:

```python
from unity.quantity import Quantity

# Different measurements in different units
measurements = {
    "distance_km": Quantity([1, 2, 5], "km"),
    "distance_m": Quantity([100, 200, 500], "m"),
}

# Convert all to meters
standard = {
    k: v.to("m") for k, v in measurements.items()
}
```

### Workflow 3: Safe Operations

Catch errors for invalid operations:

```python
from unity.quantity import Quantity

try:
    distance = Quantity(100, "m")
    time = Quantity(10, "kg")  # Wrong unit!
    
    result = distance / time
except ValueError as e:
    print(f"Error: {e}")
```

## Supported Units

### Common Units by Dimension

**Length**: m, mm, cm, km, in, ft, yd, mi  
**Mass**: kg, g, mg, t, lb, oz  
**Time**: s, min, h, d, y  
**Force**: N (Newton) = kg m s-2  
**Pressure**: Pa (Pascal) = N m-2  
**Energy**: J (Joule) = N m = kg m2 s-2  
**Power**: W (Watt) = J s-1 = kg m2 s-3  

For a complete list, see the database in `src/unity/db.py`.

## Tips & Tricks

### Tip 1: Type Hints

Use type hints with your quantities for better code:

```python
from typing import Union
import numpy as np
from unity.quantity import Quantity

def calculate_speed(
    distance: Quantity,
    time: Quantity
) -> Quantity:
    """Calculate speed from distance and time."""
    return distance / time
```

### Tip 2: Numpy Integration

Access the underlying numpy array for advanced operations:

```python
import numpy as np
from unity.quantity import Quantity

data = Quantity([1, 2, 3, 4, 5], "m")

# Use numpy functions directly
mean = np.mean(data.value)
filtered = data.value[data.value > 2]
```

### Tip 3: Preserve Types

Quantities preserve scalar vs array distinction:

```python
# Scalar stays scalar
scalar = Quantity(10, "m")
result_scalar = scalar * 2      # Still scalar

# Array stays array
array = Quantity([1, 2, 3], "m")
result_array = array * 2         # Still array
```

### Tip 4: Format for Display

Use `.format()` for readable output:

```python
speeds = Quantity([10.123, 20.456, 30.789], "m s-1")
print(speeds.format())          # Auto format
print(speeds.format(".1f"))     # Custom format
```

## Troubleshooting

### Issue: "Incompatible units for addition"

This means you're trying to add quantities with different dimensions:

```python
distance = Quantity(100, "m")
time = Quantity(10, "s")

result = distance + time  # Error! Can't add length and time
```

**Solution**: Make sure units are compatible.

### Issue: "Unknown unit"

The unit you're using isn't in the database:

```python
q = Quantity(100, "furlong")  # Error! Unknown unit
```

**Solution**: Use supported units. Check `ARRAYS.md` or `reference.md` for the complete list.

### Issue: "Indexing is only supported for array quantities"

You're trying to index a scalar:

```python
q = Quantity(10, "m")
first = q[0]  # Error! Can't index scalar
```

**Solution**: Only arrays support indexing. Check if your value is an array.

## Next Steps

1. **Read API Reference**: See [API_REFERENCE.md](API_REFERENCE.md) for complete API documentation
2. **Array Operations**: Check [ARRAYS.md](ARRAYS.md) for detailed array operations guide
3. **Run Examples**: Try the demo scripts:
   - `python examples/demo.py` - Basic examples
   - `python examples/array_demo.py` - Array examples
4. **Run Tests**: Verify everything works:
   - `python testing/test_quantity_ops.py`
   - `python testing/test_quantity_arrays.py`

## Quick Reference

| Task | Code |
|------|------|
| Create scalar | `Quantity(10, "m")` |
| Create array | `Quantity([1, 2, 3], "m")` |
| Convert units | `q.to("km")` |
| Perform calculation | `distance / time` |
| Format output | `q.format()` |
| Access array element | `q[0]` |
| Access array slice | `q[1:4]` |
| Check unit compatibility | `valid("m", "km")` |

## Resources

- **README.md** - Overview and features
- **reference.md** - Detailed documentation  
- **ARRAYS.md** - Array operations and advanced features
- **API_REFERENCE.md** - Quick API lookup
- **examples/** - Working code examples
- **testing/** - Test suite showing usage

## Contributing

Found a bug? Want to add a feature? See the repository's contribution guidelines.

## License

See LICENSE file in the repository.

