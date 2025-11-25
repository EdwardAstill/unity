import unittest
import sys
import os

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from unity.main import conv, Quantity, parse_unit, valid

class TestUnitConversion(unittest.TestCase):

    # --- 6. Valid Function Tests ---
    
    def test_valid_function(self):
        # Valid cases
        self.assertTrue(valid("kg", "mg"))
        self.assertTrue(valid("N", "kg m s-2"))
        self.assertTrue(valid("Pa", "N m-2"))
        
        # Invalid cases (Dimension mismatch)
        self.assertFalse(valid("kg", "m"))
        self.assertFalse(valid("N", "Pa"))
        
        # Invalid cases (Unknown unit)
        self.assertFalse(valid("foo", "bar"))
        self.assertFalse(valid("kg", "bar"))
        
        # Invalid cases (Malformed)
        self.assertFalse(valid("2m", "m"))

    # --- 1. Simple Unit Conversions ---
    
    def test_mass_simple(self):
        # mg -> kg: 1e-6
        self.assertAlmostEqual(conv(1, "mg", "kg"), 1e-6)
        # kg -> mg: 1e6
        self.assertAlmostEqual(conv(1, "kg", "mg"), 1e6)
        # g -> kg: 1e-3
        self.assertAlmostEqual(conv(1000, "g", "kg"), 1.0)

    def test_length_simple(self):
        # m -> mm: 1000
        self.assertAlmostEqual(conv(1, "m", "mm"), 1000)
        # km -> m: 1000
        self.assertAlmostEqual(conv(1, "km", "m"), 1000)
        # cm -> m: 0.01
        self.assertAlmostEqual(conv(100, "cm", "m"), 1.0)

    def test_time_simple(self):
        # min -> s: 60
        self.assertAlmostEqual(conv(1, "min", "s"), 60)
        # h -> min: 60
        self.assertAlmostEqual(conv(1, "h", "min"), 60)
        # h -> s: 3600
        self.assertAlmostEqual(conv(1, "h", "s"), 3600)

    # --- 2. Derived Unit Conversions ---

    def test_pressure(self):
        # Pa -> N m-2: Should be 1:1
        # Pa = N/m^2
        self.assertAlmostEqual(conv(1, "Pa", "N m-2"), 1.0)
        
        # kPa -> Pa: 1000
        self.assertAlmostEqual(conv(1, "kPa", "Pa"), 1000)
        
        # kPa -> N m-2: 1000
        self.assertAlmostEqual(conv(1, "kPa", "N m-2"), 1000)

    # --- 3. Compound Unit Conversions (Complex) ---

    def test_complex_compound(self):
        # The classic example: N vs kg m s-2
        # N = kg m s-2
        self.assertAlmostEqual(conv(1, "N", "kg m s-2"), 1.0)
        
        # Complex cancellation:
        # kg m s-2 -> kg m2 s-2 mm-1
        # mm-1 = 1000 m-1
        # m2 * mm-1 = m2 * 1000 m-1 = 1000 m
        # So target = 1000 * kg m s-2 = 1000 N
        # 1 N = 0.001 of target
        self.assertAlmostEqual(conv(1, "kg m s-2", "kg m2 s-2 mm-1"), 0.001)

    def test_exponents(self):
        # m2 -> cm2
        # 1 m = 100 cm
        # 1 m^2 = 100^2 cm^2 = 10000 cm^2
        self.assertAlmostEqual(conv(1, "m2", "cm2"), 10000)
        
        # m3 -> mm3
        # 1 m = 1000 mm
        # 1 m^3 = 10^9 mm^3
        # Floating point arithmetic can be tricky with large powers
        self.assertAlmostEqual(conv(1, "m3", "mm3"), 1e9, delta=0.001)

    # --- 4. Quantity Object API ---

    def test_quantity_object(self):
        q = Quantity(10, "km")
        q_new = q.to("m")
        
        self.assertEqual(q_new.value, 10000)
        self.assertEqual(q_new.unit, "m")
        # Floating point default format will include .0
        self.assertEqual(str(q_new), "10000.0 m")

    def test_quantity_complex(self):
        q = Quantity(7834.2, "N")
        # 1 N = 1e-3 kPa m2 (as established in previous analysis)
        q_new = q.to("kPa m2")
        self.assertAlmostEqual(q_new.value, 7.8342)

    # --- 5. Error Handling ---

    def test_incompatible_dimensions(self):
        # Mass vs Length
        with self.assertRaises(ValueError) as cm:
            conv(1, "kg", "m")
        self.assertIn("Incompatible units", str(cm.exception))

    def test_unknown_unit(self):
        with self.assertRaises(ValueError) as cm:
            conv(1, "flibble", "m")
        self.assertIn("Unknown unit", str(cm.exception))

    def test_malformed_string(self):
        # This regex accepts most things but let's try something weird
        # Actually our regex is permissive but expects units to exist.
        # "m2" splits to "m", "2". 
        # "2m" -> invalid token order based on regex ^([a-zA-Z]+)([-+]?\d+)?$
        with self.assertRaises(ValueError) as cm:
            conv(1, "2m", "m")
        self.assertIn("Invalid unit token", str(cm.exception))

if __name__ == '__main__':
    unittest.main()

