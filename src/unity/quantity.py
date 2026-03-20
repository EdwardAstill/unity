from typing import Union
import re
import numpy as np
from .core import conv, valid, invert_unit, parse_unit, dims_to_si_unit

def format_unit_typst(unit: str) -> str:
    """
    Convert a unit string into Typst-friendly output.

    Examples:
    - "mm2"  -> '"mm"^(2)'
    - "mm^2" -> '"mm"^(2)'
    - "mm**2" -> '"mm"^(2)'
    - "N m"  -> '"N""m"'

    Notes:
    - This is token-based (splits on whitespace). Tokens that don't match the supported
      patterns are passed through unchanged.
    """
    parts = unit.split()
    formatted_parts: list[str] = []
    for part in parts:
        # Accept both "mm2" and caret/pythonic styles like "mm^2" / "mm**2".
        # If the token doesn't match, we leave it unchanged (e.g. "kN/m^2" or already-formatted).
        match = re.match(r"^([a-zA-Z]+)(?:(?:\^)|(?:\*\*))?([-+]?\d+)?$", part)
        if match:
            base = match.group(1)
            exp = match.group(2)
            if exp:
                formatted_parts.append(f'"{base}"^({exp})')
            else:
                formatted_parts.append(f'"{base}"')
        else:
            formatted_parts.append(f"{part}")

    return "".join(formatted_parts)

class Quantity:
    def __init__(self, value: Union[float, int, list, np.ndarray], unit: str):
        # Convert lists to numpy arrays for consistent handling
        if isinstance(value, list):
            self.value = np.array(value)
        elif isinstance(value, np.ndarray):
            self.value = value
        else:
            # Keep scalars as scalars (float or int)
            self.value = float(value)
        self.unit = unit
        
    def to(self, target_unit: str) -> 'Quantity':
        new_value = conv(self.value, self.unit, target_unit)
        return Quantity(new_value, target_unit)
    
    def to_si(self) -> 'Quantity':
        """
        Convert quantity to SI base units for standardized comparison.
        
        This converts the quantity to its SI base unit representation, allowing
        for easy comparison of values. The value is adjusted by the scale factor
        to maintain equivalence.
        
        Examples:
        - Quantity(1, "km").to_si() → Quantity(1000, "m")
        - Quantity(1000, "mm").to_si() → Quantity(1, "m")
        - Quantity(100, "N").to_si() → Quantity(100, "kg m s-2")
        - Quantity(60, "min").to_si() → Quantity(3600, "s")
        
        Returns:
            New Quantity with value converted to SI base units
            
        Notes:
            SI base units are:
            - Mass: kg
            - Length: m
            - Time: s
            - SI derived units are decomposed into these bases
        """
        # Parse the current unit to canonical form
        canonical = parse_unit(self.unit)
        
        # Generate SI base unit string from dimensions
        si_unit = dims_to_si_unit(canonical.dims)
        
        # Convert value: multiply by scale to get SI base value
        # (scale is relative to SI base, so multiplying by scale gives us the SI value)
        si_value = self.value * canonical.scale
        
        return Quantity(si_value, si_unit)
        
    def __repr__(self):
        if isinstance(self.value, np.ndarray):
            return f"Quantity({self.value.tolist()}, '{self.unit}')"
        return f"Quantity({self.value}, '{self.unit}')"

    def __str__(self):
        if isinstance(self.value, np.ndarray):
            return f"{self.value.tolist()} {self.unit}"
        return f"{self.value} {self.unit}"
    
    def __getitem__(self, key: Union[int, slice]) -> 'Quantity':
        """
        Support indexing and slicing for array quantities.
        Returns a new Quantity with the indexed/sliced values and same unit.
        """
        if not isinstance(self.value, np.ndarray):
            raise TypeError("Indexing is only supported for array quantities")
        
        indexed_value = self.value[key]
        # Convert scalar results back to float for consistency
        if np.ndim(indexed_value) == 0:
            indexed_value = float(indexed_value)
        return Quantity(indexed_value, self.unit)

    def __add__(self, other: 'Quantity') -> 'Quantity':
        if not isinstance(other, Quantity):
            return NotImplemented
        
        # Check compatibility
        if not valid(self.unit, other.unit):
             raise ValueError(f"Incompatible units for addition: '{self.unit}' and '{other.unit}'")
             
        # Convert other to self's unit (handles both scalars and arrays)
        other_converted_val = conv(other.value, other.unit, self.unit)
        # Numpy handles broadcasting automatically
        result = self.value + other_converted_val
        return Quantity(result, self.unit)
        
    def __sub__(self, other: 'Quantity') -> 'Quantity':
        if not isinstance(other, Quantity):
            return NotImplemented
            
        if not valid(self.unit, other.unit):
             raise ValueError(f"Incompatible units for subtraction: '{self.unit}' and '{other.unit}'")
             
        other_converted_val = conv(other.value, other.unit, self.unit)
        # Numpy handles broadcasting automatically
        result = self.value - other_converted_val
        return Quantity(result, self.unit)

    def __mul__(self, other: Union['Quantity', float, int]) -> 'Quantity':
        if isinstance(other, (int, float)):
            # Numpy handles scalar multiplication for both arrays and scalars
            result = self.value * other
            return Quantity(result, self.unit)
        elif isinstance(other, Quantity):
            # Element-wise multiplication with broadcasting
            new_value = self.value * other.value
            new_unit = f"{self.unit} {other.unit}".strip()
            return Quantity(new_value, new_unit)
        else:
            return NotImplemented

    def __rmul__(self, other: Union[float, int]) -> 'Quantity':
        if isinstance(other, (int, float)):
            result = self.value * other
            return Quantity(result, self.unit)
        return NotImplemented

    def __truediv__(self, other: Union['Quantity', float, int]) -> 'Quantity':
        if isinstance(other, (int, float)):
            result = self.value / other
            return Quantity(result, self.unit)
        elif isinstance(other, Quantity):
            # Element-wise division with broadcasting
            new_value = self.value / other.value
            inverted_other_unit = invert_unit(other.unit)
            new_unit = f"{self.unit} {inverted_other_unit}".strip()
            return Quantity(new_value, new_unit)
        else:
            return NotImplemented

    def __rtruediv__(self, other: Union[float, int]) -> 'Quantity':
        if isinstance(other, (int, float)):
            result = other / self.value
            inverted_unit = invert_unit(self.unit)
            return Quantity(result, inverted_unit)
        return NotImplemented

    def format(self, num_format: str = "", style: str = "typst") -> str:
        """
        Format the quantity according to specific magnitude rules.
        For arrays: displays as [val1, val2, ...] unit (compact format)
        """
        def get_format_string(val: float) -> str:
            """Helper to determine format string based on magnitude."""
            if num_format != "":
                return f"{{:{num_format}}}"
            
            abs_val = abs(val)
            if abs_val == 0.0:
                return "{:.0f}"
            elif abs_val < 0.1 or abs_val > 9999.9:
                return "{:.2E}"
            elif abs_val < 10:
                return "{:.3f}"
            elif abs_val < 100:
                return "{:.2f}"
            elif abs_val < 1000:
                return "{:.1f}"
            else:
                # Covers 1000 <= abs_val <= 9999.9
                return "{:.0f}"
        
        # Handle array formatting
        if isinstance(self.value, np.ndarray):
            # Format each element according to magnitude rules
            formatted_elements = []
            for val in self.value.flat:
                fmt = get_format_string(val)
                formatted_elements.append(fmt.format(val))
            
            # Reshape back if multidimensional (for proper display)
            if self.value.ndim > 1:
                # For multidimensional arrays, use numpy's array representation
                formatted_num = "["
                formatted_flat = formatted_elements
                idx = 0
                for i in range(self.value.shape[0]):
                    if i > 0:
                        formatted_num += ", "
                    formatted_num += "["
                    for j in range(self.value.shape[1] if self.value.ndim > 1 else 1):
                        if j > 0:
                            formatted_num += ", "
                        formatted_num += formatted_flat[idx]
                        idx += 1
                    formatted_num += "]"
                formatted_num += "]"
            else:
                # 1D array: simple list format
                formatted_num = "[" + ", ".join(formatted_elements) + "]"
        else:
            # Scalar formatting (original behavior)
            fmt = get_format_string(self.value)
            formatted_num = fmt.format(self.value)
        
        # Unit formatting logic for typst
        format_unit = format_unit_typst(self.unit)
        
        if format_unit:
            return f"{formatted_num} space {format_unit}"
        else:
            return f"{formatted_num}"
