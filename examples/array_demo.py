"""
Demonstration of array support in Quantity class.
Shows how to use scalars, lists, and numpy arrays with the same Quantity object.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import numpy as np
from unity.quantity import Quantity

print("=" * 60)
print("ARRAY QUANTITY DEMONSTRATION")
print("=" * 60)

# 1. Creating quantities from different sources
print("\n1. Creating Quantities:")
print("-" * 40)

scalar_q = Quantity(10, "m")
print(f"Scalar:      {scalar_q}")

list_q = Quantity([1, 2, 3, 4, 5], "m")
print(f"From list:   {list_q}")

array_q = Quantity(np.array([10.0, 20.0, 30.0]), "kg")
print(f"From array:  {array_q}")

# 2. Element-wise operations on arrays
print("\n2. Element-wise Operations:")
print("-" * 40)

q1 = Quantity([1, 2, 3], "m")
q2 = Quantity([4, 5, 6], "m")
print(f"q1 = {q1}")
print(f"q2 = {q2}")
print(f"q1 + q2 = {q1 + q2}")
print(f"q1 * 2  = {q1 * 2}")
print(f"q2 / 2  = {q2 / 2}")

# 3. Broadcasting operations
print("\n3. Broadcasting (Array + Scalar):")
print("-" * 40)

array_q = Quantity([10, 20, 30], "m")
scalar_q = Quantity(5, "m")
print(f"Array:   {array_q}")
print(f"Scalar:  {scalar_q}")
print(f"Array + Scalar = {array_q + scalar_q}")

# 4. Indexing and slicing
print("\n4. Indexing and Slicing:")
print("-" * 40)

q = Quantity([100, 200, 300, 400, 500], "m")
print(f"Original: {q}")
print(f"q[0]    = {q[0]}")
print(f"q[-1]   = {q[-1]}")
print(f"q[1:4]  = {q[1:4]}")
print(f"q[::2]  = {q[::2]}")

# 5. Unit conversions with arrays
print("\n5. Unit Conversions with Arrays:")
print("-" * 40)

km_q = Quantity([1, 2, 3], "km")
print(f"Original (km): {km_q}")
m_q = km_q.to("m")
print(f"Converted (m): {m_q}")

# 6. Mixed operations with conversion
print("\n6. Mixed Operations with Unit Conversion:")
print("-" * 40)

q1 = Quantity([1, 2, 3], "m")
q2 = Quantity([100, 200, 300], "cm")
print(f"q1 (m):  {q1}")
print(f"q2 (cm): {q2}")
print(f"q1 + q2 = {q1 + q2}")

# 7. Formatting arrays
print("\n7. Formatted Output:")
print("-" * 40)

q_small = Quantity([0.001, 0.05, 0.5], "m")
print(f"Small values: {q_small.format()}")

q_mixed = Quantity([1.5, 25.0, 150.0, 1234.0], "m")
print(f"Mixed values: {q_mixed.format()}")

q_large = Quantity([10000, 50000, 100000], "m")
print(f"Large values: {q_large.format()}")

# 8. Multidimensional arrays
print("\n8. Multidimensional Arrays:")
print("-" * 40)

matrix_q = Quantity(np.array([[1, 2], [3, 4]]), "kg")
print(f"2D array:\n{matrix_q}")
print(f"Shape: {matrix_q.value.shape}")

doubled = matrix_q * 2
print(f"Doubled:\n{doubled}")

# 9. Physical calculations with arrays
print("\n9. Physical Calculation Example:")
print("-" * 40)

# Calculate velocity from distance and time arrays
distances = Quantity([100, 200, 300], "m")
times = Quantity([10, 20, 15], "s")
velocities = distances / times

print(f"Distances: {distances}")
print(f"Times:     {times}")
print(f"Velocities = {velocities}")
print(f"Formatted: {velocities.format()}")

# 10. Broadcasting with different shapes
print("\n10. Array-Scalar Quantity Operations:")
print("-" * 40)

forces = Quantity([10, 20, 30], "N")
distance = Quantity(5, "m")
work = forces * distance

print(f"Forces (N):   {forces}")
print(f"Distance (m): {distance}")
print(f"Work (N m):   {work}")

print("\n" + "=" * 60)
print("Demo complete! All operations maintain type safety and units.")
print("=" * 60)

