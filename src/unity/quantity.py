from typing import Union
import re
from .core import conv, valid, invert_unit

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

    def __add__(self, other: 'Quantity') -> 'Quantity':
        if not isinstance(other, Quantity):
            return NotImplemented
        
        # Check compatibility
        if not valid(self.unit, other.unit):
             raise ValueError(f"Incompatible units for addition: '{self.unit}' and '{other.unit}'")
             
        # Convert other to self's unit
        other_converted_val = conv(other.value, other.unit, self.unit)
        return Quantity(self.value + other_converted_val, self.unit)
        
    def __sub__(self, other: 'Quantity') -> 'Quantity':
        if not isinstance(other, Quantity):
            return NotImplemented
            
        if not valid(self.unit, other.unit):
             raise ValueError(f"Incompatible units for subtraction: '{self.unit}' and '{other.unit}'")
             
        other_converted_val = conv(other.value, other.unit, self.unit)
        return Quantity(self.value - other_converted_val, self.unit)

    def __mul__(self, other: Union['Quantity', float, int]) -> 'Quantity':
        if isinstance(other, (int, float)):
            return Quantity(self.value * other, self.unit)
        elif isinstance(other, Quantity):
            new_value = self.value * other.value
            new_unit = f"{self.unit} {other.unit}".strip()
            return Quantity(new_value, new_unit)
        else:
            return NotImplemented

    def __rmul__(self, other: Union[float, int]) -> 'Quantity':
        if isinstance(other, (int, float)):
            return Quantity(self.value * other, self.unit)
        return NotImplemented

    def __truediv__(self, other: Union['Quantity', float, int]) -> 'Quantity':
        if isinstance(other, (int, float)):
            return Quantity(self.value / other, self.unit)
        elif isinstance(other, Quantity):
            new_value = self.value / other.value
            inverted_other_unit = invert_unit(other.unit)
            new_unit = f"{self.unit} {inverted_other_unit}".strip()
            return Quantity(new_value, new_unit)
        else:
            return NotImplemented

    def __rtruediv__(self, other: Union[float, int]) -> 'Quantity':
        if isinstance(other, (int, float)):
            new_value = other / self.value
            inverted_unit = invert_unit(self.unit)
            return Quantity(new_value, inverted_unit)
        return NotImplemented

    def format(self,num_format: str = "", style: str = "typst") -> str:
        """
        Format the quantity according to specific magnitude rules.
        """
        if num_format == "":
            abs_val = abs(self.value)
            if abs_val == 0.0:
                fmt = "{:.0f}"
            elif abs_val < 0.1 or abs_val > 9999.9:
                fmt = "{:.2E}"
            elif abs_val < 10:
                fmt = "{:.3f}"
            elif abs_val < 100:
                fmt = "{:.2f}"
            elif abs_val < 1000:
                fmt = "{:.1f}"
            else:
                # Covers 1000 <= abs_val <= 9999.9
                fmt = "{:.0f}"
        else:
            fmt = f"{{:{num_format}}}"
            
        
            
        formatted_num = fmt.format(self.value)
        
        # Unit formatting logic for typst
        parts = self.unit.split()
        formatted_parts = []
        for part in parts:
            match = re.match(r"^([a-zA-Z]+)([-+]?\d+)?$", part)
            if match:
                base = match.group(1)
                exp = match.group(2)
                if exp:
                    formatted_parts.append(f'{base}#super[{exp}]')
                else:
                    formatted_parts.append(f'{base}')
            else:
                formatted_parts.append(f'{part}')
                
        format_unit = " \\u{22C5} ".join(formatted_parts)
        
        if format_unit:
            return f"{formatted_num} \\u{{22C5}} {format_unit}"
        else:
            return f"{formatted_num}"
