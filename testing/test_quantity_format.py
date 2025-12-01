import unittest
import sys
import os

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from unity.quantity import Quantity

class TestQuantityFormat(unittest.TestCase):
    def test_format_magnitude(self):
        cases = [
            (0.0, '$ 0 \\u{22C5} m $'),
            (0.05, '$ 5.00E-02 \\u{22C5} m $'),
            (0.1, '$ 0.100 \\u{22C5} m $'),
            (5.0, '$ 5.000 \\u{22C5} m $'),
            (9.999, '$ 9.999 \\u{22C5} m $'),
            (10.0, '$ 10.00 \\u{22C5} m $'),
            (99.99, '$ 99.99 \\u{22C5} m $'),
            (100.0, '$ 100.0 \\u{22C5} m $'),
            (999.9, '$ 999.9 \\u{22C5} m $'),
            (1000.0, '$ 1000 \\u{22C5} m $'),
            (9999.9, '$ 10000 \\u{22C5} m $'),
            (10000.0, '$ 1.00E+04 \\u{22C5} m $'),
            (-0.05, '$ -5.00E-02 \\u{22C5} m $'),
            (-5.0, '$ -5.000 \\u{22C5} m $'),
        ]

        for val, expected in cases:
            q = Quantity(val, "m")
            result = q.format()
            self.assertEqual(result, expected, f"Failed for {val}")

    def test_format_units(self):
        # Test unit formatting logic
        cases = [
            (5.0, "kg", '$ 5.000 \\u{22C5} kg $'),
            (5.0, "m2", '$ 5.000 \\u{22C5} m#super[2] $'),
            (5.0, "m-1", '$ 5.000 \\u{22C5} m#super[-1] $'),
            (5.0, "kg m s-2", '$ 5.000 \\u{22C5} kg \\u{22C5} m \\u{22C5} s#super[-2] $'),
            (5.0, "kg mm-2", '$ 5.000 \\u{22C5} kg \\u{22C5} mm#super[-2] $'),
        ]
        
        for val, unit, expected in cases:
            q = Quantity(val, unit)
            result = q.format()
            self.assertEqual(result, expected, f"Failed for {val} {unit}")

if __name__ == "__main__":
    unittest.main()

