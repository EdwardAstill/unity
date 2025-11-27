import unittest
import sys
import os

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from unity.main import Quantity

class TestQuantityOps(unittest.TestCase):

    def test_add(self):
        q1 = Quantity(10, "m")
        q2 = Quantity(0.001, "km") # 1 m
        q3 = q1 + q2
        self.assertAlmostEqual(q3.value, 11.0)
        self.assertEqual(q3.unit, "m")
        
    def test_add_incompatible(self):
        q1 = Quantity(10, "m")
        q2 = Quantity(10, "s")
        with self.assertRaises(ValueError):
            _ = q1 + q2

    def test_sub(self):
        q1 = Quantity(10, "m")
        q2 = Quantity(500, "cm") # 5 m
        q3 = q1 - q2
        self.assertAlmostEqual(q3.value, 5.0)
        self.assertEqual(q3.unit, "m")

    def test_mul_scalar(self):
        q1 = Quantity(10, "m")
        q2 = q1 * 2
        self.assertEqual(q2.value, 20)
        self.assertEqual(q2.unit, "m")
        
        q3 = 3 * q1
        self.assertEqual(q3.value, 30)
        self.assertEqual(q3.unit, "m")

    def test_mul_quantity(self):
        q1 = Quantity(10, "N")
        q2 = Quantity(2, "m")
        q3 = q1 * q2
        self.assertEqual(q3.value, 20)
        self.assertEqual(q3.unit, "N m") # Basic string concatenation

    def test_div_scalar(self):
        q1 = Quantity(10, "m")
        q2 = q1 / 2
        self.assertEqual(q2.value, 5)
        self.assertEqual(q2.unit, "m")

    def test_div_quantity(self):
        q1 = Quantity(10, "m")
        q2 = Quantity(2, "s")
        q3 = q1 / q2
        self.assertEqual(q3.value, 5)
        # s -> s-1
        self.assertEqual(q3.unit, "m s-1")

    def test_div_quantity_complex(self):
        q1 = Quantity(10, "kg m")
        q2 = Quantity(2, "s2")
        q3 = q1 / q2
        self.assertEqual(q3.value, 5)
        # s2 -> s-2
        self.assertEqual(q3.unit, "kg m s-2")

    def test_rdiv_scalar(self):
        q1 = Quantity(2, "s")
        q2 = 1 / q1
        self.assertEqual(q2.value, 0.5)
        self.assertEqual(q2.unit, "s-1")

if __name__ == '__main__':
    unittest.main()
