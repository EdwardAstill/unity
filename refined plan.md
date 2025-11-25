# Refined Plan: Unit Conversion System

Based on the backbone analysis, this project will implement a unit conversion system using a **Canonical Form** approach. This ensures robustness by reducing all units to a common base representation (Scale + Dimensions) before comparing or converting.

## 1. Core Concepts

### The Canonical Form
Every unit string (simple like `"mg"` or compound like `"kg m s-2"`) will be parsed into a **Canonical Unit** object containing:
1.  **`scale`** (`float`): The multiplier relative to the base SI system (e.g., relative to kg, m, s).
2.  **`dims`** (`dict`): A map of base dimensions to their exponents (e.g., `{"M": 1, "L": 1, "T": -2}`).

### Conversion Logic
To convert a value from `Unit A` to `Unit B`:
1.  Parse `Unit A` → `Canonical A` (scale_a, dims_a)
2.  Parse `Unit B` → `Canonical B` (scale_b, dims_b)
3.  **Validate**: Ensure `dims_a == dims_b` (Dimensionally equivalent).
4.  **Calculate**: `Conversion Factor = scale_a / scale_b`.
5.  **Result**: `New Value = Old Value * Conversion Factor`.

---

## 2. Implementation Steps

### Step 1: The Unit Database (`UNIT_DB`)
Create a central dictionary mapping atomic unit strings to their base definition.
*   **Dimensions**: M (Mass), L (Length), T (Time).
*   **Base Units**: kg (Mass), m (Length), s (Time).

```python
UNIT_DB = {
    # Mass (Base: kg)
    "kg": {"scale": 1.0,    "dims": {"M": 1}},
    "g":  {"scale": 1e-3,   "dims": {"M": 1}},
    "mg": {"scale": 1e-6,   "dims": {"M": 1}},
    
    # Length (Base: m)
    "m":  {"scale": 1.0,    "dims": {"L": 1}},
    "mm": {"scale": 1e-3,   "dims": {"L": 1}},
    
    # Time (Base: s)
    "s":  {"scale": 1.0,    "dims": {"T": 1}},
    
    # Derived
    "N":  {"scale": 1.0,    "dims": {"M": 1, "L": 1, "T": -2}},
    "kPa":{"scale": 1e3,    "dims": {"M": 1, "L": -1, "T": -2}},
}
```

### Step 2: The Parser (`parse_unit`)
Implement a function to turn string inputs into the Canonical Form.
*   **Input**: `"kg m2 s-2 mm-1"`
*   **Process**:
    1.  Tokenize by space.
    2.  For each token, split into unit name and exponent (handle implied `1`).
    3.  Lookup unit in `UNIT_DB`.
    4.  Accumulate `scale` and `dims`.
        *   `current_scale *= (db_scale ** exponent)`
        *   `current_dims[d] += (db_dims[d] * exponent)`

### Step 3: Functional API (`conv`)
Implement the pure function for conversion.
```python
def conv(value: float, from_unit: str, to_unit: str) -> float:
    # ... logic ...
```

### Step 4: Object-Oriented API (`Quantity`)
Implement the `Quantity` class for better ergonomics.
```python
q = Quantity(7834.2, "N")
result = q.to("kPa m2")
```

---

## 3. Verification Cases

1.  **Simple Mass**: `mg` -> `kg`
    *   Expected Factor: $10^{-6}$
2.  **Complex Derived**: `kg m s-2` (N) -> `kg m2 s-2 mm-1`
    *   This tests the handling of multiple length units canceling out or combining.
    *   Expected Factor: $10^{-3}$ (since `mm-1` is $10^3 m^{-1}$, effectively adding a factor of 1000 to the denominator, wait—`mm` is $10^{-3}m$, so `mm^{-1}` is $10^3 m^{-1}$. $N = kg \cdot m \cdot s^{-2}$. Target = $kg \cdot m^2 \cdot s^{-2} \cdot (10^3 m^{-1}) = 10^3 \cdot kg \cdot m \cdot s^{-2}$. So Target is 1000x larger unit. 1 N = 0.001 Target).

## 4. Next Actions
- [x] Create `main.py` structure.
- [x] Define `UNIT_DB`.
- [x] Implement `CanonicalUnit` and parser.
- [x] Implement `Quantity` class.

