import unittest
import sys
import os
import numpy as np

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from unity.quantity import Quantity


class TestQuantityArrays(unittest.TestCase):
    
    def test_create_from_list(self):
        """Test creating quantity from list."""
        q = Quantity([1, 2, 3], "m")
        self.assertIsInstance(q.value, np.ndarray)
        np.testing.assert_array_equal(q.value, np.array([1, 2, 3]))
        self.assertEqual(q.unit, "m")
    
    def test_create_from_numpy_array(self):
        """Test creating quantity from numpy array."""
        arr = np.array([4.5, 5.5, 6.5])
        q = Quantity(arr, "kg")
        self.assertIsInstance(q.value, np.ndarray)
        np.testing.assert_array_equal(q.value, arr)
        self.assertEqual(q.unit, "kg")
    
    def test_create_scalar(self):
        """Test that scalar quantities still work."""
        q = Quantity(5.0, "m")
        self.assertIsInstance(q.value, float)
        self.assertEqual(q.value, 5.0)
        self.assertEqual(q.unit, "m")
    
    def test_array_add_array_elementwise(self):
        """Test element-wise addition of two array quantities."""
        q1 = Quantity([1, 2, 3], "m")
        q2 = Quantity([4, 5, 6], "m")
        q3 = q1 + q2
        np.testing.assert_array_equal(q3.value, np.array([5, 7, 9]))
        self.assertEqual(q3.unit, "m")
    
    def test_array_add_scalar_broadcast(self):
        """Test broadcasting addition: array + scalar."""
        q1 = Quantity([1, 2, 3], "m")
        q2 = Quantity(10, "m")
        q3 = q1 + q2
        np.testing.assert_array_equal(q3.value, np.array([11, 12, 13]))
        self.assertEqual(q3.unit, "m")
    
    def test_scalar_add_array_broadcast(self):
        """Test broadcasting addition: scalar + array."""
        q1 = Quantity(10, "m")
        q2 = Quantity([1, 2, 3], "m")
        q3 = q1 + q2
        np.testing.assert_array_equal(q3.value, np.array([11, 12, 13]))
        self.assertEqual(q3.unit, "m")
    
    def test_array_sub_array_elementwise(self):
        """Test element-wise subtraction of two array quantities."""
        q1 = Quantity([10, 20, 30], "m")
        q2 = Quantity([1, 2, 3], "m")
        q3 = q1 - q2
        np.testing.assert_array_equal(q3.value, np.array([9, 18, 27]))
        self.assertEqual(q3.unit, "m")
    
    def test_array_sub_scalar_broadcast(self):
        """Test broadcasting subtraction: array - scalar."""
        q1 = Quantity([10, 20, 30], "m")
        q2 = Quantity(5, "m")
        q3 = q1 - q2
        np.testing.assert_array_equal(q3.value, np.array([5, 15, 25]))
        self.assertEqual(q3.unit, "m")
    
    def test_array_mul_scalar(self):
        """Test multiplying array quantity by scalar number."""
        q1 = Quantity([1, 2, 3], "m")
        q2 = q1 * 2
        np.testing.assert_array_equal(q2.value, np.array([2, 4, 6]))
        self.assertEqual(q2.unit, "m")
        
        # Test reverse multiplication
        q3 = 3 * q1
        np.testing.assert_array_equal(q3.value, np.array([3, 6, 9]))
        self.assertEqual(q3.unit, "m")
    
    def test_array_mul_array_elementwise(self):
        """Test element-wise multiplication of two array quantities."""
        q1 = Quantity([1, 2, 3], "N")
        q2 = Quantity([4, 5, 6], "m")
        q3 = q1 * q2
        np.testing.assert_array_equal(q3.value, np.array([4, 10, 18]))
        self.assertEqual(q3.unit, "N m")
    
    def test_array_mul_scalar_quantity(self):
        """Test broadcasting multiplication: array * scalar quantity."""
        q1 = Quantity([1, 2, 3], "m")
        q2 = Quantity(2, "s")
        q3 = q1 * q2
        np.testing.assert_array_equal(q3.value, np.array([2, 4, 6]))
        self.assertEqual(q3.unit, "m s")
    
    def test_array_div_scalar(self):
        """Test dividing array quantity by scalar number."""
        q1 = Quantity([10, 20, 30], "m")
        q2 = q1 / 2
        np.testing.assert_array_equal(q2.value, np.array([5, 10, 15]))
        self.assertEqual(q2.unit, "m")
    
    def test_array_div_array_elementwise(self):
        """Test element-wise division of two array quantities."""
        q1 = Quantity([10, 20, 30], "m")
        q2 = Quantity([2, 4, 5], "s")
        q3 = q1 / q2
        np.testing.assert_array_equal(q3.value, np.array([5, 5, 6]))
        self.assertEqual(q3.unit, "m s-1")
    
    def test_array_div_scalar_quantity(self):
        """Test broadcasting division: array / scalar quantity."""
        q1 = Quantity([10, 20, 30], "m")
        q2 = Quantity(2, "s")
        q3 = q1 / q2
        np.testing.assert_array_equal(q3.value, np.array([5, 10, 15]))
        self.assertEqual(q3.unit, "m s-1")
    
    def test_scalar_div_array(self):
        """Test reverse division: scalar / array."""
        q1 = Quantity([1, 2, 4], "s")
        q2 = 1 / q1
        np.testing.assert_array_equal(q2.value, np.array([1, 0.5, 0.25]))
        self.assertEqual(q2.unit, "s-1")
    
    def test_indexing_single_element(self):
        """Test indexing to get a single element (returns scalar quantity)."""
        q = Quantity([10, 20, 30], "m")
        q0 = q[0]
        self.assertIsInstance(q0, Quantity)
        self.assertEqual(q0.value, 10.0)
        self.assertIsInstance(q0.value, float)
        self.assertEqual(q0.unit, "m")
        
        q2 = q[2]
        self.assertEqual(q2.value, 30.0)
    
    def test_indexing_negative(self):
        """Test negative indexing."""
        q = Quantity([10, 20, 30], "m")
        q_last = q[-1]
        self.assertEqual(q_last.value, 30.0)
    
    def test_slicing(self):
        """Test slicing to get a subset (returns array quantity)."""
        q = Quantity([10, 20, 30, 40, 50], "m")
        q_slice = q[1:4]
        self.assertIsInstance(q_slice, Quantity)
        self.assertIsInstance(q_slice.value, np.ndarray)
        np.testing.assert_array_equal(q_slice.value, np.array([20, 30, 40]))
        self.assertEqual(q_slice.unit, "m")
    
    def test_slicing_with_step(self):
        """Test slicing with step."""
        q = Quantity([1, 2, 3, 4, 5, 6], "m")
        q_slice = q[::2]
        np.testing.assert_array_equal(q_slice.value, np.array([1, 3, 5]))
        self.assertEqual(q_slice.unit, "m")
    
    def test_indexing_scalar_raises_error(self):
        """Test that indexing a scalar quantity raises TypeError."""
        q = Quantity(10, "m")
        with self.assertRaises(TypeError):
            _ = q[0]
    
    def test_unit_conversion_array(self):
        """Test unit conversion with arrays."""
        q1 = Quantity([1, 2, 3], "km")
        q2 = q1.to("m")
        np.testing.assert_array_equal(q2.value, np.array([1000, 2000, 3000]))
        self.assertEqual(q2.unit, "m")
    
    def test_unit_conversion_array_complex(self):
        """Test unit conversion with arrays and complex units."""
        q1 = Quantity([100, 200, 300], "cm")
        q2 = q1.to("m")
        np.testing.assert_array_equal(q2.value, np.array([1, 2, 3]))
        self.assertEqual(q2.unit, "m")
    
    def test_add_with_conversion_array(self):
        """Test addition with unit conversion on arrays."""
        q1 = Quantity([1, 2, 3], "m")
        q2 = Quantity([100, 200, 300], "cm")
        q3 = q1 + q2
        np.testing.assert_array_equal(q3.value, np.array([2, 4, 6]))
        self.assertEqual(q3.unit, "m")
    
    def test_format_array_1d(self):
        """Test formatting of 1D array quantity."""
        q = Quantity([1.5, 25.0, 1234.0], "m")
        result = q.format()
        # Expected: [1.500, 25.00, 1234] m
        self.assertIn("[", result)
        self.assertIn("]", result)
        self.assertIn("m", result)
        self.assertIn("1.500", result)
        self.assertIn("25.00", result)
        self.assertIn("1234", result)
    
    def test_format_array_scientific(self):
        """Test formatting with scientific notation for arrays."""
        q = Quantity([0.001, 0.05, 10000], "m")
        result = q.format()
        # Small and large values should be in scientific notation
        self.assertIn("E", result)  # Scientific notation
    
    def test_format_scalar_unchanged(self):
        """Test that scalar formatting still works as before."""
        q = Quantity(5.0, "m")
        result = q.format()
        self.assertEqual(result, "5.000 m")
    
    def test_repr_array(self):
        """Test __repr__ for array quantity."""
        q = Quantity([1, 2, 3], "m")
        result = repr(q)
        self.assertIn("Quantity", result)
        self.assertIn("[1, 2, 3]", result)
        self.assertIn("'m'", result)
    
    def test_str_array(self):
        """Test __str__ for array quantity."""
        q = Quantity([1, 2, 3], "m")
        result = str(q)
        self.assertIn("[1, 2, 3]", result)
        self.assertIn("m", result)
    
    def test_empty_array(self):
        """Test creating quantity with empty array."""
        q = Quantity([], "m")
        self.assertIsInstance(q.value, np.ndarray)
        self.assertEqual(len(q.value), 0)
    
    def test_single_element_array(self):
        """Test array with single element."""
        q = Quantity([5], "m")
        self.assertIsInstance(q.value, np.ndarray)
        np.testing.assert_array_equal(q.value, np.array([5]))
        
        # Indexing should return scalar
        q0 = q[0]
        self.assertIsInstance(q0.value, float)
        self.assertEqual(q0.value, 5.0)
    
    def test_multidimensional_array(self):
        """Test 2D array support."""
        arr = np.array([[1, 2], [3, 4]])
        q = Quantity(arr, "m")
        self.assertEqual(q.value.shape, (2, 2))
        np.testing.assert_array_equal(q.value, arr)
    
    def test_multidimensional_operations(self):
        """Test operations on 2D arrays."""
        arr1 = np.array([[1, 2], [3, 4]])
        arr2 = np.array([[5, 6], [7, 8]])
        q1 = Quantity(arr1, "m")
        q2 = Quantity(arr2, "m")
        q3 = q1 + q2
        np.testing.assert_array_equal(q3.value, np.array([[6, 8], [10, 12]]))
    
    def test_incompatible_units_array(self):
        """Test that incompatible units raise error with arrays."""
        q1 = Quantity([1, 2, 3], "m")
        q2 = Quantity([1, 2, 3], "s")
        with self.assertRaises(ValueError):
            _ = q1 + q2
    
    def test_mixed_operations_preserve_types(self):
        """Test that mixed operations properly preserve scalar vs array."""
        # Scalar + Scalar = Scalar
        q1 = Quantity(5, "m")
        q2 = Quantity(3, "m")
        q3 = q1 + q2
        self.assertIsInstance(q3.value, float)
        
        # Array + Array = Array
        q4 = Quantity([5, 6], "m")
        q5 = Quantity([3, 4], "m")
        q6 = q4 + q5
        self.assertIsInstance(q6.value, np.ndarray)
        
        # Scalar + Array = Array (broadcasting)
        q7 = q1 + q4
        self.assertIsInstance(q7.value, np.ndarray)
        np.testing.assert_array_equal(q7.value, np.array([10, 11]))


if __name__ == "__main__":
    unittest.main()

