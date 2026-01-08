import unittest
from unity.quantity import Quantity
import math

class TestAngles(unittest.TestCase):
    def test_angle_conversions(self):
        # Degrees to Radians
        q_deg = Quantity(180, "deg")
        q_rad = q_deg.to("rad")
        self.assertAlmostEqual(q_rad.value, math.pi, places=5)
        
        # Radians to Degrees
        q_rad2 = Quantity(math.pi / 2, "rad")
        q_deg2 = q_rad2.to("deg")
        self.assertAlmostEqual(q_deg2.value, 90.0, places=5)
        
        # Revolutions to Degrees
        q_rev = Quantity(1, "rev")
        q_deg3 = q_rev.to("deg")
        self.assertAlmostEqual(q_deg3.value, 360.0, places=5)
        
        # Revolutions to Radians
        q_rev2 = Quantity(0.5, "rev")
        q_rad3 = q_rev2.to("rad")
        self.assertAlmostEqual(q_rad3.value, math.pi, places=5)

    def test_angle_arithmetic(self):
        q1 = Quantity(90, "deg")
        q2 = Quantity(math.pi/2, "rad")
        
        # Addition (result in first operand's unit)
        sum_q = q1 + q2
        self.assertAlmostEqual(sum_q.value, 180.0, places=5)
        self.assertEqual(sum_q.unit, "deg")
        
        # Subtraction
        diff_q = q1 - q2
        self.assertAlmostEqual(diff_q.value, 0.0, places=5)

    def test_incompatibility(self):
        # Angles should not be compatible with dimensionless or other units
        q_angle = Quantity(1, "rad")
        q_len = Quantity(1, "m")
        
        with self.assertRaises(ValueError):
             q_angle + q_len

if __name__ == '__main__':
    unittest.main()

