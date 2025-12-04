# Unity Reference Documentation

This document provides a comprehensive reference for the `unity` library, including API usage, supported units, and syntax for compound units.

## Core API

### `conv(value, from_unit, to_unit)`

Converts a numeric value from one unit to another. Supports both scalar values and numpy arrays.

- **Parameters**:
  - `value` (float | np.ndarray): The magnitude to convert. Can be a scalar or array.
  - `from_unit` (str): The string representation of the source unit (e.g., `"kg"`, `"m s-1"`).
  - `to_unit` (str): The string representation of the target unit.
- **Returns**: `float | np.ndarray` - The converted value with same shape as input.
- **Raises**: `ValueError` if units are dimensionally incompatible or unknown.

**Examples**:
```python
from unity.core import conv

# Scalar conversion
speed = conv(100, "km h-1", "m s-1")  # Returns: 27.777...

# Array conversion
distances = np.array([1, 2, 3])
meters = conv(distances, "km", "m")  # Returns: [1000, 2000, 3000]
```

### `valid(from_unit, to_unit)`

Checks if a conversion between two units is dimensionally valid.

- **Parameters**:
  - `from_unit` (str): Source unit string.
  - `to_unit` (str): Target unit string.
- **Returns**: `bool` - `True` if valid, `False` if incompatible or unknown.

**Example**:
```python
from unity.core import valid
if valid("N", "kg m s-2"):
    print("Compatible!")
```

### `Quantity` Class

An object-oriented wrapper for handling values with units. Supports scalar values, lists, and numpy arrays with a unified interface.

#### `__init__(value: Union[float, int, list, np.ndarray], unit: str)`
Creates a new Quantity. Automatically converts lists to numpy arrays.

**Examples**:
```python
# Scalar
q1 = Quantity(500, "mg")

# From list (automatically converts to array)
q2 = Quantity([1, 2, 3], "m")

# From numpy array
q3 = Quantity(np.array([10, 20]), "kg")

# Works with int too
q4 = Quantity(100, "m")
```

#### `to(target_unit: str) -> Quantity`
Returns a new `Quantity` converted to the target unit. Works with both scalars and arrays.

**Examples**:
```python
# Scalar conversion
q_kg = Quantity(500, "mg").to("kg")
print(q_kg)  # 0.0005 kg

# Array conversion
distances = Quantity([1, 2, 3], "km")
meters = distances.to("m")
print(meters)  # [1000.0, 2000.0, 3000.0] m
```

#### `format(num_format: str = "", style: str = "typst") -> str`
Formats the quantity with smart magnitude handling.

- **Parameters**:
  - `num_format` (str): Optional format string (e.g., `".2f"`). If empty, uses magnitude-based formatting.
  - `style` (str): Output style (currently supports `"typst"`).
- **Returns**: `str` - Formatted string representation.

**Behavior**:
- **Scalars**: Applies magnitude-based formatting rules
- **Arrays**: Displays as `[val1, val2, ...] unit` with each element formatted individually

**Format Rules** (when `num_format` is empty):
- Value = 0: `0`
- 0 < |value| < 0.1 or |value| > 9999.9: Scientific notation (`.2E`)
- 0.1 ≤ |value| < 10: `.3f`
- 10 ≤ |value| < 100: `.2f`
- 100 ≤ |value| < 1000: `.1f`
- 1000 ≤ |value| ≤ 9999.9: `.0f`

**Examples**:
```python
# Scalar formatting
Quantity(5.0, "m").format()              # "5.000 m"
Quantity(0.001, "m").format()            # "1.00E-03 m"
Quantity(1234, "m").format()             # "1234 m"

# Array formatting
Quantity([1.5, 25.0, 1234], "m").format()  # "[1.500, 25.00, 1234] m"

# Custom format
Quantity(5.12345, "m").format(".1f")     # "5.1 m"
```

#### Arithmetic Operations

All arithmetic operations (`+`, `-`, `*`, `/`) support:
- Scalar ± Scalar → Scalar
- Array ± Array → Array (element-wise)
- Scalar ± Array → Array (broadcasting)
- Scalar * Scalar → Scalar
- Array * Array → Array (element-wise)
- Scalar * Array → Array (broadcasting)
- (same for division)

**Examples**:
```python
# Scalar arithmetic
q1 = Quantity(10, "m")
q2 = Quantity(3, "m")
print(q1 + q2)    # 13.0 m
print(q1 / q2)    # 3.333... m m-1

# Array element-wise
arr1 = Quantity([1, 2, 3], "m")
arr2 = Quantity([4, 5, 6], "m")
print(arr1 + arr2)  # [5.0, 7.0, 9.0] m

# Broadcasting
scalar = Quantity(10, "m")
array = Quantity([1, 2, 3], "m")
print(scalar + array)  # [11.0, 12.0, 13.0] m
print(array * 2)       # [2, 4, 6] m
```

#### `__getitem__(key: Union[int, slice]) -> Quantity`
Supports indexing and slicing for array quantities.

- **Parameters**:
  - `key` (int | slice): Index or slice object.
- **Returns**: `Quantity` - For single index, returns scalar Quantity. For slice, returns array Quantity.
- **Raises**: `TypeError` if called on a scalar quantity.

**Examples**:
```python
q = Quantity([10, 20, 30, 40, 50], "m")

# Single element (returns scalar)
q[0]        # Quantity(10.0, "m")
q[-1]       # Quantity(50.0, "m")

# Slicing (returns array)
q[1:4]      # Quantity([20, 30, 40], "m")
q[::2]      # Quantity([10, 30, 50], "m")
q[::-1]     # Quantity([50, 40, 30, 20, 10], "m")

# Negative indexing
q[-2]       # Quantity(40.0, "m")
```

#### String Representations

##### `__str__()` 
Returns human-readable string.
```python
str(Quantity(5.0, "m"))              # "5.0 m"
str(Quantity([1, 2, 3], "m"))        # "[1, 2, 3] m"
```

##### `__repr__()`
Returns detailed representation.
```python
repr(Quantity(5.0, "m"))              # "Quantity(5.0, 'm')"
repr(Quantity([1, 2, 3], "m"))        # "Quantity([1, 2, 3], 'm')"
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

---

## Usage Guides

### Working with Scalar Quantities

Scalar quantities are for single values with units. They maintain full compatibility with all existing code.

```python
from unity.quantity import Quantity

# Create scalar quantities
mass = Quantity(1000, "g")
distance = Quantity(100, "m")
time = Quantity(10, "s")

# Convert between units
mass_kg = mass.to("kg")          # 1.0 kg
distance_km = distance.to("km")  # 0.1 km

# Perform calculations
speed = distance / time          # 10.0 m s-1
```

### Working with Array Quantities

Array quantities let you perform bulk calculations efficiently.

#### Creating Array Quantities

```python
import numpy as np
from unity.quantity import Quantity

# From Python list
speeds = Quantity([10, 20, 30], "m s-1")

# From numpy array
distances = Quantity(np.array([100, 200, 300]), "m")

# From nested list (2D array)
matrix = Quantity([[1, 2], [3, 4]], "kg")
print(matrix.value.shape)  # (2, 2)
```

#### Element-wise Operations

```python
# Two arrays of same shape
forces = Quantity([10, 20, 30], "N")
distances = Quantity([2, 3, 5], "m")
work = forces * distances
print(work)  # [20.0, 60.0, 150.0] N m

# Element-wise division
total_work = Quantity([100, 150, 200], "J")
time_spent = Quantity([10, 15, 20], "s")
power = total_work / time_spent
print(power)  # [10.0, 10.0, 10.0] J s-1 (watts)
```

#### Broadcasting

Broadcasting allows operations between arrays and scalars, automatically extending the scalar to match the array shape.

```python
# Array + Scalar
temperatures = Quantity([20, 25, 30], "°C")
increase = Quantity(5, "°C")
new_temps = temperatures + increase
print(new_temps)  # [25, 30, 35] °C

# Scalar * Array
base_price = Quantity(100, "USD")
quantities = Quantity([1, 2, 5, 10], "")
total_prices = base_price * quantities
print(total_prices)  # [100, 200, 500, 1000] USD

# Broadcast incompatible arrays (numpy handles this)
a = Quantity([[1, 2, 3]], "m")      # shape: (1, 3)
b = Quantity([[1], [2], [3]], "m")  # shape: (3, 1)
result = a + b                        # shape: (3, 3) - broadcast!
print(result.value)
# [[2, 3, 4],
#  [3, 4, 5],
#  [4, 5, 6]]
```

#### Indexing and Slicing

```python
speeds = Quantity([5, 10, 15, 20, 25, 30], "m s-1")

# Get first element as scalar quantity
first = speeds[0]
print(type(first.value))  # <class 'float'>

# Get range as array quantity
mid_range = speeds[2:5]
print(type(mid_range.value))  # <class 'numpy.ndarray'>
print(mid_range)  # [15, 20, 25] m s-1

# Advanced slicing
reversed_arr = speeds[::-1]
every_nth = speeds[::2]

# Use indexing in calculations
avg_of_first_three = (speeds[0] + speeds[1] + speeds[2]) / 3
```

#### Unit Conversions with Arrays

```python
# Convert entire array at once
distances_km = Quantity([1, 5, 10], "km")
distances_m = distances_km.to("m")
print(distances_m)  # [1000.0, 5000.0, 10000.0] m

# Convert complex units
accelerations = Quantity([9.8, 9.81], "m s-2")
other_units = accelerations.to("km h-2")
# Automatic dimensional analysis ensures compatibility
```

### Real-World Examples

#### Example 1: Kinematics Calculations

```python
from unity.quantity import Quantity
import numpy as np

# Multiple projectile trajectories
initial_velocities = Quantity([10, 15, 20, 25], "m s-1")
time = Quantity([2, 2, 2, 2], "s")
gravity = Quantity(9.81, "m s-2")

# Calculate distance fallen
distances = 0.5 * gravity * time**2
print(distances)
# [19.62, 19.62, 19.62, 19.62] m

# Calculate final velocities
final_velocities = initial_velocities + gravity * time
print(final_velocities)
# [29.62, 34.62, 39.62, 44.62] m s-1
```

#### Example 2: Energy Calculations

```python
# Masses of different objects
masses = Quantity([1, 2, 5, 10], "kg")

# Same velocity for all
velocity = Quantity(10, "m s-1")

# Calculate kinetic energies
kinetic_energies = 0.5 * masses * velocity**2
print(kinetic_energies.format())
# [50.0 J, 100.0 J, 250.0 J, 500.0 J]
```

#### Example 3: Pressure Distribution

```python
# Pressure readings from array of sensors
pressures = Quantity([101325, 101000, 100500, 99500], "Pa")

# Convert to atmospheres
pressures_atm = pressures.to("atm")
print(pressures_atm)

# Calculate pressure differences
baseline = pressures[0]
deviations = pressures - baseline
print(deviations)  # [0, -325, -825, -1825] Pa
```

### Performance Considerations

- **Numpy arrays are efficient**: Operations use vectorized numpy functions, making them fast for large arrays.
- **Memory**: Numpy arrays use less memory than Python lists for numeric data.
- **Type preservation**: Scalars remain scalars (float), arrays remain arrays (ndarray). This preserves type information.

### Common Patterns

**Pattern: Filtering Results**
```python
measurements = Quantity([100, 250, 150, 300, 175], "m")
threshold = Quantity(200, "m")

# Get measurements above threshold
above_threshold = measurements.value > threshold.value
filtered = Quantity(measurements.value[above_threshold], "m")
```

**Pattern: Statistical Analysis**
```python
import numpy as np
measurements = Quantity([10, 20, 15, 25, 30], "m")

mean = np.mean(measurements.value)
std = np.std(measurements.value)
print(f"Mean: {mean} m, Std: {std} m")
```

**Pattern: Batch Processing**
```python
# Process multiple measurements
measurements = Quantity([1, 2, 3, 4, 5], "km")

# Convert all to meters
in_meters = measurements.to("m")

# Apply scaling
doubled = in_meters * 2
```

