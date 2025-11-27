import re
from collections import defaultdict
from typing import Dict
from .db import UNIT_DB

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
    factor = c_from.scale / c_to.scale
    return value * factor

def valid(from_unit: str, to_unit: str) -> bool:
    """
    Checks if a conversion between two units is valid (i.e., they are dimensionally equivalent).
    Returns True if valid, False otherwise.
    Also returns False if units are malformed or unknown.
    """
    try:
        c_from = parse_unit(from_unit)
        c_to = parse_unit(to_unit)
        return c_from.dims == c_to.dims
    except ValueError:
        return False

def invert_unit(unit_str: str) -> str:
    """
    Inverts a unit string (e.g., "s" -> "s-1", "m2" -> "m-2").
    Used for division.
    """
    tokens = unit_str.strip().split()
    inverted_tokens = []
    
    pattern = re.compile(r"^([a-zA-Z]+)([-+]?\d+)?$")
    
    for token in tokens:
        match = pattern.match(token)
        if not match:
             # Should be caught by parse_unit usually, but here just pass through or error
             raise ValueError(f"Invalid unit token: '{token}'")
             
        unit_name = match.group(1)
        exponent_str = match.group(2)
        exponent = int(exponent_str) if exponent_str else 1
        
        new_exponent = -exponent
        
        if new_exponent == 1:
            inverted_tokens.append(f"{unit_name}")
        else:
            inverted_tokens.append(f"{unit_name}{new_exponent}")
            
    return " ".join(inverted_tokens)

