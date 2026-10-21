import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from unity import Quantity, Unit, conv, invert_unit, is_compatible
from unity.core import dims_to_si_unit
from unity.quantity import format_unit_typst, format_unit_typst_markup


def test_functions():
    assert conv(100, "cm", "m") == 1.0
    assert is_compatible("N", "kg m s-2")
    assert not is_compatible("m", "s")
    parsed = Unit.from_string("mm2")
    assert parsed.scale == 1e-6
    assert parsed.dims == {"L": 2}
    assert invert_unit("s-1") == "s"
    assert Unit(1, {"L": 1, "T": 0}).dims == {"L": 1}


def test_quantity():
    q = Quantity([1, 2, 3], "km")
    converted = q.to("m")
    np.testing.assert_array_equal(converted.value, [1000.0, 2000.0, 3000.0])
    assert converted.unit == "m"
    assert (q[0].value, q[0].unit) == (1.0, "km")
    np.testing.assert_array_equal(q[1:].value, [2, 3])
    si = Quantity(1, "km").to_si()
    assert (si.value, si.unit) == (1000.0, "m")
    assert str(Quantity(5, "m")) == "5.0 m"
    assert repr(Quantity(5, "m")) == "Quantity(5.0, 'm')"


def test_formatting():
    area = Quantity(5, "m2")
    assert area.format() == '5.000 space "m"^(2)'
    assert area.format(".2f") == '5.00 space "m"^(2)'
    assert area.format(".2f", "typst-markup") == "5.00 m#super[2]"
    assert Quantity([[1, 2], [3, 4]], "m").format(".1f") == (
        '[[1.0, 2.0], [3.0, 4.0]] space "m"'
    )


def test_operators():
    distance = Quantity(10, "m")
    added = distance + Quantity(500, "cm")
    assert (added.value, added.unit) == (15.0, "m")
    subtracted = distance - Quantity(500, "cm")
    assert (subtracted.value, subtracted.unit) == (5.0, "m")
    work = Quantity(100, "N") * distance
    assert (work.value, work.unit) == (1000.0, "N m")
    speed = distance / Quantity(2, "s")
    assert (speed.value, speed.unit) == (5.0, "m s-1")
    assert (distance * 2).value == 20.0
    assert (2 * distance).value == 20.0
    assert (distance / 2).value == 5.0
    inverse = 1 / Quantity(2, "s")
    assert (inverse.value, inverse.unit) == (0.5, "s-1")
    assert Quantity(1, "kN") == Quantity(1000, "N")
    q = Quantity([1, 2, 3], "km")
    np.testing.assert_array_equal((q + Quantity(500, "m")).value, [1.5, 2.5, 3.5])
    np.testing.assert_array_equal(q > Quantity(1500, "m"), [False, True, True])


def test_module_helpers():
    assert dims_to_si_unit({"M": 1, "L": 1, "T": -2}) == "m kg s-2"
    assert format_unit_typst("m2") == '"m"^(2)'
    assert format_unit_typst_markup("m2") == "m#super[2]"


if __name__ == "__main__":
    test_functions()
    test_quantity()
    test_formatting()
    test_operators()
    test_module_helpers()
    print("All README example tests passed.")
