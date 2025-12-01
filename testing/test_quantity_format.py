import unittest
import sys
import os

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from unity.quantity import Quantity

class TestQuantityFormat(unittest.TestCase):
    def test_format_magnitude(self):
        cases = [
            (0.0, '$ 0 space "m" $'),
            (0.05, '$ 5.00E-02 space "m" $'),
            (0.1, '$ 0.100 space "m" $'),
            (5.0, '$ 5.000 space "m" $'),
            (9.999, '$ 9.999 space "m" $'),
            (10.0, '$ 10.00 space "m" $'),
            (99.99, '$ 99.99 space "m" $'),
            (100.0, '$ 100.0 space "m" $'),
            (999.9, '$ 999.9 space "m" $'),
            (1000.0, '$ 1000 space "m" $'),
            (9999.9, '$ 10000 space "m" $'),
            (10000.0, '$ 1.00E+04 space "m" $'),
            (-0.05, '$ -5.00E-02 space "m" $'),
            (-5.0, '$ -5.000 space "m" $'),
        ]

        for val, expected in cases:
            q = Quantity(val, "m")
            result = q.format("typst")
            self.assertEqual(result, expected, f"Failed for {val}")

    def test_format_units(self):
        # Test unit formatting logic
        cases = [
            (5.0, "kg", '$ 5.000 space "kg" $'),
            (5.0, "m2", '$ 5.000 space "m"^(2) $'),
            (5.0, "m-1", '$ 5.000 space "m"^(-1) $'),
            (5.0, "kg m s-2", '$ 5.000 space "kg" "m" "s"^(-2) $'),
            (5.0, "kg mm-2", '$ 5.000 space "kg" "mm"^(-2) $'),
        ]
        
        for val, unit, expected in cases:
            q = Quantity(val, unit)
            result = q.format("typst")
            self.assertEqual(result, expected, f"Failed for {val} {unit}")

if __name__ == "__main__":
    unittest.main()

