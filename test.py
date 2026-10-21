import operator
import sys
from pathlib import Path

import numpy as np
import pytest

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


@pytest.mark.parametrize(
    "alias", ["", " ", "-", "dimensionless", "ratio", "none", " NONE "]
)
def test_dimensionless_aliases(alias):
    unit = Unit.from_string(alias)
    assert (unit.scale, unit.dims) == (1.0, {})
    assert conv(2, alias, "") == 2


@pytest.mark.parametrize(
    ("text", "scale", "dims"),
    [
        (" kg  m\ts-2 ", 1, {"M": 1, "L": 1, "T": -2}),
        ("mm2", 1e-6, {"L": 2}),
        ("cm-2", 1e4, {"L": -2}),
        ("m+2 m-2 s0", 1, {}),
        ("N m", 1, {"M": 1, "L": 2, "T": -2}),
        ("mA mK deg", 1e-6 * np.pi / 180, {"I": 1, "Theta": 1, "A": 1}),
    ],
)
def test_unit_parsing(text, scale, dims):
    unit = Unit.from_string(text)
    assert unit.scale == pytest.approx(scale)
    assert unit.dims == dims


@pytest.mark.parametrize("token", ["m/s", "m^2", "m**2", "2m", "ft_lbf", "m-"])
def test_invalid_unit_syntax(token):
    for parse in (Unit.from_string, invert_unit):
        with pytest.raises(ValueError) as error:
            parse(token)
        assert str(error.value) == f"Invalid unit token: '{token}'"
    assert not is_compatible(token, "m")
    assert not is_compatible("m", token)


@pytest.mark.parametrize(
    ("token", "message"),
    [
        ("xyz", "Unknown unit: 'xyz'"),
        ("n", "Unknown unit: 'n'"),
        ("kNm", "Unknown unit: 'kNm'"),
        ("Nmm+02", "Unknown unit: 'Nmm'"),
    ],
)
def test_unknown_unit_errors(token, message):
    with pytest.raises(ValueError) as error:
        Unit.from_string(token)
    assert str(error.value) == message
    assert not is_compatible(token, "m")


def test_conversion_errors_and_array_values():
    values = np.array([[100, 200], [300, 400]])
    converted = conv(values, "cm", "m")
    np.testing.assert_array_equal(converted, [[1, 2], [3, 4]])
    np.testing.assert_array_equal(values, [[100, 200], [300, 400]])
    with pytest.raises(ValueError) as error:
        conv(1, "m", "s")
    assert str(error.value) == "Incompatible units: 'm' {'L': 1} vs 's' {'T': 1}"
    assert not is_compatible("rad", "")


@pytest.mark.parametrize(
    ("unit", "inverse"),
    [("m s-2", "m-1 s2"), ("m+2 s0", "m-2 s0"), ("xyz-1", "xyz"), ("", "")],
)
def test_unit_inversion(unit, inverse):
    assert invert_unit(unit) == inverse


def test_quantity_storage_and_indexing():
    values = np.array([[1, 2], [3, 4]])
    quantity = Quantity(values, "m")
    assert quantity.value is values
    assert isinstance(Quantity(1, "m").value, float)
    assert repr(quantity) == "Quantity([[1, 2], [3, 4]], 'm')"
    assert str(quantity) == "[[1, 2], [3, 4]] m"
    assert (quantity[1, 0].value, quantity[1, 0].unit) == (3, "m")
    np.testing.assert_array_equal(quantity[:, 1].value, [2, 4])
    np.testing.assert_array_equal(quantity[values > 2].value, [3, 4])
    assert np.shares_memory(quantity[1:].value, values)
    with pytest.raises(
        TypeError, match="Indexing is only supported for array quantities"
    ):
        Quantity(1, "m")[0]
    invalid = Quantity(1, "xyz")
    assert invalid.unit == "xyz"
    with pytest.raises(ValueError, match="Unknown unit"):
        invalid.to("m")


@pytest.mark.parametrize(
    ("value", "unit", "si_value", "si_unit"),
    [(2, "kPa", 2000, "m-1 kg s-2"), (2, "min", 120, "s"), (2, "ratio", 2, "")],
)
def test_si_conversion(value, unit, si_value, si_unit):
    original = Quantity(value, unit)
    converted = original.to_si()
    assert (converted.value, converted.unit) == (si_value, si_unit)
    assert (original.value, original.unit) == (value, unit)


@pytest.mark.parametrize(
    "operation",
    [operator.eq, operator.ne, operator.lt, operator.le, operator.gt, operator.ge],
)
def test_comparisons(operation):
    assert operation(Quantity(1, "m"), Quantity(100, "cm")) == operation(1, 1)
    compared = operation(Quantity([[1], [2]], "m"), Quantity([100, 200], "cm"))
    expected = operation(np.array([[1], [2]]), np.array([1, 2]))
    np.testing.assert_array_equal(compared, expected)
    with pytest.raises(
        TypeError, match="Quantity comparisons require another Quantity, got int"
    ):
        operation(Quantity(1, "m"), 1)
    with pytest.raises(ValueError) as error:
        operation(Quantity(1, "m"), Quantity(1, "s"))
    assert str(error.value) == "Incompatible units for comparison: 'm' and 's'"


@pytest.mark.parametrize(
    ("operation", "name"),
    [(operator.add, "addition"), (operator.sub, "subtraction")],
)
def test_addition_and_subtraction(operation, name):
    left = Quantity([[1], [2]], "m")
    right = Quantity([100, 200], "cm")
    result = operation(left, right)
    expected = operation(np.array([[1], [2]]), np.array([1, 2]))
    np.testing.assert_array_equal(result.value, expected)
    assert result.unit == "m"
    np.testing.assert_array_equal(left.value, [[1], [2]])
    for unit in ("s", "xyz", "m/s"):
        with pytest.raises(ValueError) as error:
            operation(left, Quantity(1, unit))
        assert str(error.value) == f"Incompatible units for {name}: 'm' and '{unit}'"
    with pytest.raises(TypeError):
        operation(left, 1)


def test_array_multiplication_and_division():
    distances = Quantity([[2], [4]], "m")
    times = Quantity([1, 2], "s")
    product = distances * times
    quotient = distances / times
    assert product.unit == "m s"
    assert quotient.unit == "m s-1"
    np.testing.assert_array_equal(product.value, [[2, 4], [4, 8]])
    np.testing.assert_array_equal(quotient.value, [[2, 1], [4, 2]])
    np.testing.assert_array_equal((2 / distances).value, [[1], [0.5]])
    assert (2 / distances).unit == "m-1"
    cancelled = distances / distances
    assert cancelled.unit == "m m-1"
    assert cancelled.to_si().unit == ""


@pytest.mark.parametrize(
    ("value", "formatted"),
    [
        (0, "0"),
        (-0.0, "-0"),
        (0.01, "1.00E-02"),
        (0.1, "0.100"),
        (9.999, "9.999"),
        (10, "10.00"),
        (99.99, "99.99"),
        (100, "100.0"),
        (999.9, "999.9"),
        (1000, "1000"),
        (9999.9, "10000"),
        (10000, "1.00E+04"),
        (-0.01, "-1.00E-02"),
        (float("nan"), "nan"),
        (float("inf"), "INF"),
    ],
)
def test_default_number_format(value, formatted):
    assert Quantity(value, "").format() == formatted


@pytest.mark.parametrize(
    ("value", "formatted"),
    [
        (np.array(2), "[2.00]"),
        ([], "[]"),
        ([[], []], "[[], []]"),
        ([1, 2], "[1.00, 2.00]"),
        ([[1, 2], [3, 4]], "[[1.00, 2.00], [3.00, 4.00]]"),
        (
            [[[1, 2], [3, 4]], [[5, 6], [7, 8]]],
            "[[[1.00, 2.00], [3.00, 4.00]], [[5.00, 6.00], [7.00, 8.00]]]",
        ),
        ([[[], []]], "[[[], []]]"),
    ],
)
def test_array_formatting(value, formatted):
    assert Quantity(value, "").format(".2f") == formatted


@pytest.mark.filterwarnings("ignore:the matrix subclass:PendingDeprecationWarning")
def test_matrix_formatting():
    values = np.matrix([[1, 2], [3, 4]])
    assert Quantity(values, "m").format(".1f") == (
        '[[1.0, 2.0], [3.0, 4.0]] space "m"'
    )


@pytest.mark.filterwarnings("ignore:Format strings passed to MaskedConstant:FutureWarning")
def test_masked_array_formatting():
    values = np.ma.array([1, 2], mask=[False, True])
    assert Quantity(values, "m").format(".1f") == '[1.0, --] space "m"'


@pytest.mark.parametrize("unit", ["m2", "m^2", "m**2"])
def test_display_exponent_syntax(unit):
    assert format_unit_typst(unit) == '"m"^(2)'
    assert format_unit_typst_markup(unit) == "m#super[2]"


def test_format_styles_and_literal_units():
    quantity = Quantity(1, "kg m s-2")
    assert quantity.format(".1f", "typst-math") == '1.0 space "kg""m""s"^(-2)'
    assert quantity.format(".1f", "typst-markup") == "1.0 kgms#super[-2]"
    assert format_unit_typst("m/s") == '"m/s"'
    assert format_unit_typst_markup("m/s") == "m/s"
    with pytest.raises(ValueError, match="Unknown style: 'plain'"):
        quantity.format(style="plain")


if __name__ == "__main__":
    test_functions()
    test_quantity()
    test_formatting()
    test_operators()
    test_module_helpers()
    print("All README example tests passed.")
