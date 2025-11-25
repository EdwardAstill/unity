import re
from collections import defaultdict
from typing import Dict, Tuple

# --- 1. Unit Database ---
# Base Dimensions: M=Mass, L=Length, T=Time
UNIT_DB = {
    # Mass (Base: kg)
    "kg": {"scale": 1.0,    "dims": {"M": 1}},
    "g":  {"scale": 1e-3,   "dims": {"M": 1}},
    "mg": {"scale": 1e-6,   "dims": {"M": 1}},
    "t":  {"scale": 1e3,    "dims": {"M": 1}},
    
    # Length (Base: m)
    "m":  {"scale": 1.0,    "dims": {"L": 1}},
    "mm": {"scale": 1e-3,   "dims": {"L": 1}},
    "cm": {"scale": 1e-2,   "dims": {"L": 1}},
    "km": {"scale": 1e3,    "dims": {"L": 1}},
    
    # Time (Base: s)
    "s":  {"scale": 1.0,    "dims": {"T": 1}},
    "min":{"scale": 60.0,   "dims": {"T": 1}},
    "h":  {"scale": 3600.0, "dims": {"T": 1}},
    
    # Derived / Compound definitions
    # N = kg * m / s^2
    "N":   {"scale": 1.0,    "dims": {"M": 1, "L": 1, "T": -2}},
    # Pa = N / m^2 = kg / (m * s^2)
    "Pa":  {"scale": 1.0,    "dims": {"M": 1, "L": -1, "T": -2}},
    "kPa": {"scale": 1e3,    "dims": {"M": 1, "L": -1, "T": -2}},
}

class CanonicalUnit:
    """
    Represents a unit in its canonical form:
    - scale: multiplier relative to the base SI system
    - dims: dictionary of base dimension exponents
    """
    def __init__(self, scale: float, dims: Dict[str, int]):
        self.scale = scale
        # Remove dimensions with 0 exponent to keep it clean
        self.dims = {k: v for k, v in dims.items() if v != 0}

    def __repr__(self):
        return f"CanonicalUnit(scale={self.scale}, dims={self.dims})"

def parse_unit(unit_str: str) -> CanonicalUnit:
    """
    Parses a unit string (e.g., "kg m s-2") into a CanonicalUnit.
    """
    tokens = unit_str.strip().split()
    
    total_scale = 1.0
    total_dims = defaultdict(int)
    
    # Regex to separate unit name from exponent (e.g., "m2" -> "m", "2")
    # Matches alpha characters at start, optional integer at end
    pattern = re.compile(r"^([a-zA-Z]+)([-+]?\d+)?$")
    
    for token in tokens:
        match = pattern.match(token)
        if not match:
            raise ValueError(f"Invalid unit token: '{token}'")
        
        unit_name = match.group(1)
        exponent_str = match.group(2)
        exponent = int(exponent_str) if exponent_str else 1
        
        if unit_name not in UNIT_DB:
            raise ValueError(f"Unknown unit: '{unit_name}'")
        
        unit_def = UNIT_DB[unit_name]
        
        # Apply exponent to the base scale
        # e.g. if unit is "mm" (scale 1e-3) and token is "mm2", scale factor is (1e-3)^2
        total_scale *= (unit_def["scale"] ** exponent)
        
        # Add dimensions
        for dim, dim_exp in unit_def["dims"].items():
            total_dims[dim] += dim_exp * exponent
            
    return CanonicalUnit(total_scale, dict(total_dims))

def conv(value: float, from_unit: str, to_unit: str) -> float:
    """
    Converts a value from one unit to another.
    """
    # 1. Parse both to canonical form
    c_from = parse_unit(from_unit)
    c_to = parse_unit(to_unit)
    
    # 2. Validate dimensions match
    if c_from.dims != c_to.dims:
        raise ValueError(f"Incompatible units: '{from_unit}' {c_from.dims} vs '{to_unit}' {c_to.dims}")
        
    # 3. Calculate conversion
    # value_base = value * c_from.scale
    # value_target = value_base / c_to.scale
    factor = c_from.scale / c_to.scale
    return value * factor

class Quantity:
    def __init__(self, value: float, unit: str):
        self.value = value
        self.unit = unit
        
    def to(self, target_unit: str) -> 'Quantity':
        new_value = conv(self.value, self.unit, target_unit)
        return Quantity(new_value, target_unit)
        
    def __repr__(self):
        return f"Quantity({self.value}, '{self.unit}')"

    def __str__(self):
        return f"{self.value} {self.unit}"

def main():
    print("--- Unit Conversion Verification ---")
    
    # Case 1: Simple Mass
    # mg -> kg
    val = 1.0
    u1 = "mg"
    u2 = "kg"
    res = conv(val, u1, u2)
    print(f"\n1. {val} {u1} -> {u2}")
    print(f"   Result: {res}")
    print(f"   Expected: 1e-6")
    
    # Case 2: Complex Derived
    # N -> kPa m2 (which is effectively N, but let's test the components)
    # Actually the plan had a specific example: "kg m s-2" -> "kg m2 s-2 mm-1"
    # Let's try that exact one.
    
    val_complex = 1.0
    u_complex_1 = "kg m s-2"      # 1 N
    u_complex_2 = "kg m2 s-2 mm-1" 
    
    # Explanation of u_complex_2:
    # kg (M=1) * m^2 (L=2) * s^-2 (T=-2) * mm^-1 (L=-1 scale=(1e-3)^-1 = 1000)
    # Dimensions: M=1, L=2-1=1, T=-2 -> Matches N
    # Scale: 1 * 1 * 1 * 1000 = 1000 relative to base SI
    # N scale is 1.
    # Conversion factor = 1 / 1000 = 0.001
    
    res_complex = conv(val_complex, u_complex_1, u_complex_2)
    print(f"\n2. {val_complex} '{u_complex_1}' -> '{u_complex_2}'")
    print(f"   Result: {res_complex}")
    print(f"   Expected: 0.001")

    # Case 3: Quantity Object
    print(f"\n3. Quantity Object API")
    q = Quantity(7834.2, "N")
    print(f"   Original: {q}")
    
    # N -> kPa m2
    # N = kg m s-2
    # kPa = 1e3 kg m-1 s-2
    # m2 = m^2
    # kPa m2 = (1e3 kg m-1 s-2) * (m2) = 1e3 kg m s-2 = 1e3 N
    # So 1 N = 1e-3 kPa m2
    # 7834.2 N -> 7.8342 kPa m2
    target_u = "kPa m2"
    q_new = q.to(target_u)
    print(f"   Converted to '{target_u}': {q_new}")
    print(f"   Expected value: ~7.8342")

if __name__ == "__main__":
    main()
