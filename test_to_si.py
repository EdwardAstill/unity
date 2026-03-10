#!/usr/bin/env python
"""Test script for the to_si() method"""

from src.unity.quantity import Quantity
import numpy as np

print("=" * 60)
print("Testing to_si() Method")
print("=" * 60)

# Test 1: Simple length conversion
print("\nTest 1: Simple length conversion")
q1 = Quantity(1, "km")
si1 = q1.to_si()
print(f"  Quantity(1, 'km').to_si() = {si1}")

# Test 2: Millimeters to meters
print("\nTest 2: Millimeters to meters")
q2 = Quantity(1000, "mm")
si2 = q2.to_si()
print(f"  Quantity(1000, 'mm').to_si() = {si2}")

# Test 3: Force to kg m s-2
print("\nTest 3: Force to kg m s-2")
q3 = Quantity(100, "N")
si3 = q3.to_si()
print(f"  Quantity(100, 'N').to_si() = {si3}")

# Test 4: Time conversion
print("\nTest 4: Time conversion")
q4 = Quantity(60, "min")
si4 = q4.to_si()
print(f"  Quantity(60, 'min').to_si() = {si4}")

# Test 5: Array conversion
print("\nTest 5: Array conversion")
q5 = Quantity([1, 2, 3], "km")
si5 = q5.to_si()
print(f"  Quantity([1, 2, 3], 'km').to_si() = {si5}")

# Test 6: Comparing values after to_si()
print("\nTest 6: Comparing values after to_si()")
q6a = Quantity(1, "km")
q6b = Quantity(1000, "m")
si6a = q6a.to_si()
si6b = q6b.to_si()
print(f"  Quantity(1, 'km').to_si().value = {si6a.value}")
print(f"  Quantity(1000, 'm').to_si().value = {si6b.value}")
print(f"  Values equal: {si6a.value == si6b.value}")

# Test 7: Scalar quantities
print("\nTest 7: Scalar quantity")
q7 = Quantity(5.5, "cm")
si7 = q7.to_si()
print(f"  Quantity(5.5, 'cm').to_si() = {si7}")
print(f"  Value type: {type(si7.value)}")

# Test 8: Compound units
print("\nTest 8: Compound units (velocity)")
q8 = Quantity(100, "km h-1")
si8 = q8.to_si()
print(f"  Quantity(100, 'km h-1').to_si() = {si8}")

print("\n" + "=" * 60)
print("All tests completed successfully!")
print("=" * 60)
