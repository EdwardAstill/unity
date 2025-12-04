# Working with Array Quantities

This document provides comprehensive guidance on using the array functionality in the Unity library.

## Overview

The `Quantity` class supports three types of values:

1. **Scalar Quantities**: Single numeric values (float or int)
2. **Array Quantities**: Multiple values in numpy arrays
3. **Multidimensional Arrays**: 2D, 3D, or higher dimensional arrays

All three types use the same `Quantity` interface, making it easy to scale from single values to bulk operations.

## Creating Array Quantities

### From Python Lists

```python
from unity.quantity import Quantity

# 1D array from list
speeds = Quantity([10, 20, 30, 40], "m s-1")

# 2D array from nested list
matrix = Quantity([[1, 2, 3], [4, 5, 6]], "kg")

# Lists are automatically converted to numpy arrays internally
print(type(speeds.value))  # <class 'numpy.ndarray'>
```

### From Numpy Arrays

```python
import numpy as np
from unity.quantity import Quantity

# Direct numpy array
arr = np.array([100, 200, 300])
distances = Quantity(arr, "m")

# From numpy functions
linspace_values = np.linspace(0, 100, 10)
temps = Quantity(linspace_values, "°C")

# Random arrays
random_masses = Quantity(np.random.rand(5) * 100, "kg")

# Arrays with specific dtype
float32_arr = np.array([1.0, 2.0, 3.0], dtype=np.float32)
q = Quantity(float32_arr, "m")
```

### From Scalar to Array

```python
# A scalar quantity can be converted through operations
scalar = Quantity(10, "m")

# Many operations return arrays if appropriate
array = scalar * np.array([1, 2, 3])  # Returns array quantity
```

## Accessing Array Values

### Direct Access

```python
speeds = Quantity([10, 20, 30], "m s-1")

# Access the underlying numpy array
print(speeds.value)        # [10 20 30]
print(speeds.value.shape)  # (3,)
print(speeds.value.dtype)  # dtype('int64')

# Array properties
print(len(speeds.value))   # 3
print(speeds.value.ndim)   # 1
```

### Indexing

Single element access returns a **scalar** Quantity:

```python
speeds = Quantity([10, 20, 30, 40, 50], "m s-1")

# Positive indexing
first = speeds[0]    # Quantity(10.0, "m s-1")
second = speeds[1]   # Quantity(20.0, "m s-1")

# Negative indexing
last = speeds[-1]    # Quantity(50.0, "m s-1")
second_last = speeds[-2]  # Quantity(40.0, "m s-1")

# All indices return scalar quantities
print(type(first.value))   # <class 'float'>
print(first.unit)           # "m s-1"
```

### Slicing

Slicing returns an **array** Quantity:

```python
speeds = Quantity([10, 20, 30, 40, 50], "m s-1")

# Basic slicing
first_three = speeds[0:3]    # [10, 20, 30] m s-1
last_two = speeds[-2:]       # [40, 50] m s-1

# Step slicing
every_other = speeds[::2]    # [10, 30, 50] m s-1
reversed_arr = speeds[::-1]  # [50, 40, 30, 20, 10] m s-1

# Complex slices
middle = speeds[1:4:2]       # [20, 40] m s-1

# All slices return array quantities
print(type(first_three.value))   # <class 'numpy.ndarray'>
print(first_three.unit)           # "m s-1"
```

### Multidimensional Indexing

```python
matrix = Quantity(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), "kg")

# 2D indexing
element = matrix.value[0, 0]      # 1
row = matrix[0]                   # [1, 2, 3] kg
# Note: Direct fancy indexing on Quantity uses [index], 
# for raw array use matrix.value[row, col]

# Extract row as quantity
first_row = Quantity(matrix.value[0, :], "kg")
```

## Array Arithmetic Operations

### Addition and Subtraction

#### Same-Shape Arrays

```python
forces1 = Quantity([10, 20, 30], "N")
forces2 = Quantity([5, 10, 15], "N")

total_force = forces1 + forces2  # [15, 30, 45] N
net_force = forces1 - forces2    # [5, 10, 15] N
```

#### Broadcasting (Array + Scalar)

```python
# Add scalar to each element
baseline = Quantity(100, "m")
offsets = Quantity([0, 10, 20, 30], "m")
adjusted = baseline + offsets    # [100, 110, 120, 130] m

# Subtract scalar from array
target = Quantity(50, "s")
times = Quantity([10, 20, 30, 40], "s")
deviations = times - target      # [-40, -30, -20, -10] s
```

#### Incompatible Units

```python
distances = Quantity([1, 2, 3], "m")
times = Quantity([10, 20, 30], "s")

# This raises ValueError
try:
    result = distances + times
except ValueError as e:
    print(f"Error: {e}")  # Incompatible units for addition
```

### Multiplication

#### Array × Scalar Number

```python
speeds = Quantity([10, 20, 30], "m s-1")

doubled = speeds * 2            # [20, 40, 60] m s-1
tripled = 3 * speeds            # [30, 60, 90] m s-1
halved = speeds / 2             # [5, 10, 15] m s-1
```

#### Array × Array (Element-wise)

```python
masses = Quantity([1, 2, 3], "kg")
accelerations = Quantity([5, 10, 15], "m s-2")

forces = masses * accelerations  # [5, 20, 45] kg m s-2
```

#### Broadcasting (Array × Scalar Quantity)

```python
distances = Quantity([100, 200, 300], "m")
time_unit = Quantity(1, "s")

# Creates rates
speeds = distances / time_unit   # [100, 200, 300] m s-1

# Multiply by another array
times = Quantity([2, 3, 4], "s")
works = distances * times         # [200, 600, 1200] m s
```

### Division

#### Array ÷ Scalar Number

```python
distances = Quantity([100, 200, 300], "m")
segments = distances / 5         # [20, 40, 60] m
```

#### Array ÷ Array (Element-wise)

```python
work = Quantity([100, 200, 300], "J")
time = Quantity([10, 10, 15], "s")

power = work / time              # [10, 20, 20] J s-1
```

#### Broadcasting (Array ÷ Scalar Quantity)

```python
total_distances = Quantity([100, 200, 300], "m")
time_per_segment = Quantity(10, "s")

speeds = total_distances / time_per_segment  # [10, 20, 30] m s-1
```

## Unit Conversions

### Array Conversion

```python
distances_km = Quantity([1, 2, 5, 10], "km")

# Convert all elements at once
distances_m = distances_km.to("m")
print(distances_m)  # [1000, 2000, 5000, 10000] m

distances_cm = distances_km.to("cm")
print(distances_cm)  # [100000, 200000, 500000, 1000000] cm
```

### Complex Unit Conversions

```python
accelerations = Quantity([9.8, 9.81], "m s-2")

# Convert to other acceleration units
converted = accelerations.to("m s-2")  # Same unit, returns copy

# Must be dimensionally compatible
try:
    wrong_convert = accelerations.to("kg")  # Raises error
except ValueError as e:
    print(f"Error: {e}")  # Incompatible units
```

## Formatting Array Quantities

### Default Formatting

```python
from unity.quantity import Quantity

# Magnitude-based formatting applied to each element
small_values = Quantity([0.001, 0.05, 0.1], "m")
print(small_values.format())
# [1.00E-03, 5.00E-02, 0.100] m

medium_values = Quantity([1.5, 25, 150], "m")
print(medium_values.format())
# [1.500, 25.00, 150.0] m

large_values = Quantity([1000, 5000, 100000], "m")
print(large_values.format())
# [1000, 5.000E+03, 1.00E+05] m
```

### Custom Format Strings

```python
speeds = Quantity([10.123, 20.456, 30.789], "m s-1")

# Apply custom format to all elements
formatted = speeds.format(".1f")
print(formatted)  # [10.1, 20.5, 30.8] m s-1
```

### String Representations

```python
speeds = Quantity([10, 20, 30], "m s-1")

# str() - human readable
print(str(speeds))   # [10, 20, 30] m s-1

# repr() - detailed
print(repr(speeds))  # Quantity([10, 20, 30], 'm s-1')
```

## Advanced Array Operations

### Using Numpy Functions

Since array quantities store numpy arrays, you can use numpy functions on the underlying data:

```python
import numpy as np
from unity.quantity import Quantity

measurements = Quantity([100, 150, 120, 180, 160], "m")

# Statistics
mean = np.mean(measurements.value)          # 142.0
std = np.std(measurements.value)            # 29.66...
max_val = np.max(measurements.value)        # 180
min_val = np.min(measurements.value)        # 100

print(f"Mean: {mean} m")
print(f"Std: {std} m")

# Filtering
above_average = measurements.value > mean
filtered = Quantity(measurements.value[above_average], "m")
print(f"Above average: {filtered}")  # [150, 180, 160] m

# Cumulative operations
cumsum = Quantity(np.cumsum(measurements.value), "m")
print(f"Cumulative: {cumsum}")
```

### Mathematical Operations

```python
import numpy as np
from unity.quantity import Quantity

angles = Quantity([0, 30, 45, 60, 90], "deg")

# Note: conversion to radians would be needed for trig functions
# This is just a demonstration
magnitudes = Quantity([1, 2, 3, 4, 5], "")

# Sqrt (if physically meaningful)
intensities = magnitudes ** 0.5
print(intensities)
```

### Reshaping Arrays

```python
import numpy as np
from unity.quantity import Quantity

values = Quantity(np.arange(12), "m")

# Reshape using value property, create new Quantity
reshaped_data = values.value.reshape(3, 4)
reshaped = Quantity(reshaped_data, "m")
print(reshaped.value.shape)  # (3, 4)

# Flatten
flattened = Quantity(reshaped.value.flatten(), "m")
print(flattened)  # [0, 1, 2, ..., 11] m
```

## Broadcasting Rules

NumPy broadcasting follows specific rules for arrays of different shapes:

```python
# Compatible shapes
a = Quantity(np.ones((3, 1)), "m")    # Shape (3, 1)
b = Quantity(np.ones((1, 4)), "m")    # Shape (1, 4)
result = a + b                        # Shape (3, 4) - broadcasts!

# Scalar quantity with array
scalar = Quantity(10, "m")            # Shape ()
array = Quantity([1, 2, 3], "m")      # Shape (3,)
result = scalar + array               # Shape (3,) - broadcasts!

# Different shapes - may fail
try:
    x = Quantity(np.ones((3,)), "m")        # Shape (3,)
    y = Quantity(np.ones((4,)), "m")        # Shape (4,)
    result = x + y                          # Raises ValueError
except ValueError:
    print("Incompatible shapes for broadcasting")
```

## Common Patterns

### Pattern: Batch Conversion

```python
# Convert multiple measurements with different original units
measurements_km = [1, 2, 5]
measurements_m = [100, 200, 500]
measurements_cm = [10000, 20000, 50000]

# Combine and normalize to meters
all_measurements = Quantity(measurements_km, "km").to("m")
# Then extend with other measurements converted to m
```

### Pattern: Calculate Statistics

```python
import numpy as np
from unity.quantity import Quantity

speeds = Quantity([10, 15, 20, 18, 22, 19], "m s-1")

# Calculate statistics
mean_speed = np.mean(speeds.value)
median_speed = np.median(speeds.value)
std_speed = np.std(speeds.value)

print(f"Mean: {mean_speed} m s-1")
print(f"Median: {median_speed} m s-1")
print(f"Std Dev: {std_speed} m s-1")
```

### Pattern: Conditional Operations

```python
from unity.quantity import Quantity
import numpy as np

temperatures = Quantity([15, 20, 25, 30, 35], "°C")
threshold = Quantity(25, "°C")

# Find which temperatures exceed threshold
exceeds = temperatures.value > threshold.value
high_temps = Quantity(temperatures.value[exceeds], "°C")

print(high_temps)  # [30, 35] °C
```

### Pattern: Element Mapping

```python
from unity.quantity import Quantity

# Map each element to a computed value
distances = Quantity([10, 20, 30], "m")
times_constant = Quantity(2, "s")

# Calculate speeds for each distance
speeds = distances / times_constant
print(speeds)  # [5, 10, 15] m s-1
```

## Performance Tips

1. **Use Arrays for Bulk Operations**: Array operations are significantly faster than scalar operations in loops.

   ```python
   # Slow - loop approach
   speeds = [Quantity(v, "m s-1") for v in range(1000)]
   doubled = [s * 2 for s in speeds]
   
   # Fast - array approach
   speeds = Quantity(list(range(1000)), "m s-1")
   doubled = speeds * 2
   ```

2. **Avoid Repeated Conversions**: Convert once, then operate.

   ```python
   # Less efficient
   result = [v.to("m") for v in large_array]
   
   # More efficient
   large_array_m = large_array.to("m")
   ```

3. **Use NumPy Functions on Values**: Direct numpy operations are faster than creating new Quantity objects repeatedly.

   ```python
   measurements = Quantity([1, 2, 3, 4, 5], "m")
   
   # For statistics, use numpy directly
   mean = np.mean(measurements.value)
   ```

## Error Handling

```python
from unity.quantity import Quantity

# Indexing scalar raises error
scalar = Quantity(10, "m")
try:
    val = scalar[0]
except TypeError as e:
    print(f"Cannot index scalar: {e}")

# Incompatible unit operations
q1 = Quantity([1, 2], "m")
q2 = Quantity([3, 4], "s")
try:
    result = q1 + q2
except ValueError as e:
    print(f"Unit mismatch: {e}")

# Shape mismatch in numpy
q1 = Quantity([1, 2, 3], "m")
q2 = Quantity([1, 2], "m")
try:
    result = q1 + q2
except (ValueError, TypeError) as e:
    print(f"Shape mismatch: {e}")
```

## Examples

### Physics: Projectile Motion

```python
import numpy as np
from unity.quantity import Quantity

# Simulate multiple projectiles with different launch angles
launch_velocity = Quantity(50, "m s-1")
time_steps = Quantity(np.linspace(0, 10, 100), "s")

# Vertical position: y = v*sin(θ)*t - 0.5*g*t²
g = Quantity(9.81, "m s-2")
angle = 45  # degrees
sin_45 = 0.707

vertical_displacement = (launch_velocity * sin_45 * time_steps) - (0.5 * g * time_steps**2)
```

### Engineering: Stress-Strain

```python
from unity.quantity import Quantity
import numpy as np

# Multiple material samples
strains = Quantity([0.001, 0.002, 0.003, 0.004, 0.005], "")  # unitless
stresses = Quantity([200, 400, 600, 800, 1000], "Pa")

# Calculate young's modulus for each sample
youngs_modulus = stresses / strains
print(youngs_modulus.format())
```

### Data Science: Array Operations

```python
from unity.quantity import Quantity
import numpy as np

# Time series of measurements
measurements = Quantity([100, 102, 98, 105, 103, 99], "m")

# Calculate moving average
window_size = 3
moving_avg = Quantity(
    np.convolve(measurements.value, np.ones(window_size)/window_size, mode='valid'),
    "m"
)
print(moving_avg)
```

## Limitations

- Indexing with boolean arrays directly on Quantity objects is not supported; use `quantity.value[boolean_array]` instead.
- Complex operations should extract `.value`, perform the operation, and wrap result back in Quantity.
- Multidimensional array operations work, but advanced numpy operations need direct `.value` access.

## See Also

- [reference.md](reference.md) - Complete API reference
- [README.md](README.md) - Quick start guide
- [examples/array_demo.py](examples/array_demo.py) - Working examples

