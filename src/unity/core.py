import re
from collections import defaultdict
from typing import Dict, Union
import numpy as np
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

def _suggest_unit_split(token: str) -> str | None:
    """
    Try to split an unknown unit token into known units by greedy longest-prefix match.
    Returns a space-separated suggestion string, or None if no valid split found.
    e.g. "kNm" -> "kN m", "Nmm" -> "N mm"
    """
    def _split(s: str) -> list[str] | None:
        if not s:
            return []
        for i in range(len(s), 0, -1):
            prefix = s[:i]
            if prefix in UNIT_DB:
                rest = _split(s[i:])
                if rest is not None:
                    return [prefix] + rest
        return None

    parts = _split(token)
    if parts and len(parts) > 1:
        return " ".join(parts)
    return None


_DIMENSIONLESS_ALIASES = {"-", "dimensionless", "ratio", "none", ""}

def parse_unit(unit_str: str) -> CanonicalUnit:
    """
    Parses a unit string (e.g., "kg m s-2") into a CanonicalUnit.
    """
    if unit_str.strip().lower() in _DIMENSIONLESS_ALIASES:
        return CanonicalUnit(1.0, {})

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
            suggestion = _suggest_unit_split(unit_name)
            if suggestion:
                exponent_str_hint = match.group(2) or ""
                # Attach the exponent to the last token of the suggestion
                suggested_tokens = suggestion.split()
                suggested_tokens[-1] += exponent_str_hint
                hint = f" — did you mean '{' '.join(suggested_tokens)}'?"
            else:
                hint = ""
            raise ValueError(f"Unknown unit: '{unit_name}'{hint}")
        
        unit_def = UNIT_DB[unit_name]
        
        # Apply exponent to the base scale
        # e.g. if unit is "mm" (scale 1e-3) and token is "mm2", scale factor is (1e-3)^2
        total_scale *= (unit_def["scale"] ** exponent)
        
        # Add dimensions
        for dim, dim_exp in unit_def["dims"].items():
            total_dims[dim] += dim_exp * exponent
            
    return CanonicalUnit(total_scale, dict(total_dims))

def conv(value: Union[float, np.ndarray], from_unit: str, to_unit: str) -> Union[float, np.ndarray]:
    """
    Converts a value from one unit to another.
    Supports both scalar values and numpy arrays.
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

def dims_to_si_unit(dims: Dict[str, int]) -> str:
    """
    Converts a dimensions dictionary to an SI base unit string.
    
    Examples:
    - {L: 1} -> "m"
    - {M: 1} -> "kg"
    - {T: 1} -> "s"
    - {M: 1, L: 1, T: -2} -> "kg m s-2"
    
    Args:
        dims: Dictionary mapping dimension names to exponents
        
    Returns:
        SI base unit string (space-separated tokens)
    """
    # Map dimension abbreviations to SI base unit names
    dim_to_unit = {
        'M': 'kg',  # Mass -> kilogram
        'L': 'm',   # Length -> meter
        'T': 's',   # Time -> second
    }
    
    tokens = []
    
    # Sort for consistent output
    for dim in sorted(dims.keys()):
        exp = dims[dim]
        if dim not in dim_to_unit:
            # Unknown dimension, skip (shouldn't happen in normal use)
            continue
        
        unit = dim_to_unit[dim]
        
        if exp == 1:
            tokens.append(unit)
        else:
            tokens.append(f"{unit}{exp}")
    
    # Return space-separated or empty string for dimensionless
    return " ".join(tokens) if tokens else ""

