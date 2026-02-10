"""
Tests for the converters module.
"""

import pytest
from python_magnetunits import (
    convert_array,
    convert_data,
    convert_value,
    are_compatible,
    get_unit_string,
    ureg,
)


class TestConvertValue:
    """Test single value conversion."""

    def test_convert_magnetic_field(self) -> None:
        """Test converting magnetic field units."""
        result = convert_value(1.0, "tesla", "millitesla")
        assert abs(result - 1000.0) < 0.1

    def test_convert_with_pint_units(self) -> None:
        """Test converting with pint Unit objects."""
        result = convert_value(1.0, ureg.meter, ureg.centimeter)
        assert abs(result - 100.0) < 0.1

    def test_convert_temperature(self) -> None:
        """Test temperature conversion."""
        result = convert_value(273.15, "kelvin", "degC")
        assert abs(result - 0.0) < 0.01

    def test_convert_incompatible_units_raises_error(self) -> None:
        """Test that converting incompatible units raises error."""
        with pytest.raises(Exception):  # pint.DimensionalityError
            convert_value(1.0, "tesla", "meter")


class TestConvertArray:
    """Test array value conversion."""

    def test_convert_array_basic(self) -> None:
        """Test converting an array of values."""
        values = [1.0, 2.0, 3.0]
        result = convert_array(values, "tesla", "millitesla")
        expected = [1000.0, 2000.0, 3000.0]
        assert all(abs(r - e) < 0.1 for r, e in zip(result, expected))

    def test_convert_empty_array(self) -> None:
        """Test converting an empty array."""
        result = convert_array([], "meter", "centimeter")
        assert result == []

    def test_convert_array_with_floats(self) -> None:
        """Test converting array with decimal values."""
        values = [0.5, 1.5, 2.5]
        result = convert_array(values, "meter", "centimeter")
        expected = [50.0, 150.0, 250.0]
        assert all(abs(r - e) < 0.01 for r, e in zip(result, expected))


class TestConvertData:
    """Test the magnetrun-compatible convert_data function."""

    def test_convert_data_single_value(self) -> None:
        """Test converting a single value with dict format."""
        field_units = {"MagneticField": [ureg.tesla, ureg.millitesla]}
        result = convert_data(field_units, 1.5, "MagneticField")
        assert abs(result - 1500.0) < 0.1

    def test_convert_data_array(self) -> None:
        """Test converting an array with dict format."""
        field_units = {"MagneticField": [ureg.tesla, ureg.millitesla]}
        values = [1.0, 2.0, 3.0]
        result = convert_data(field_units, values, "MagneticField")
        expected = [1000.0, 2000.0, 3000.0]
        assert all(abs(r - e) < 0.1 for r, e in zip(result, expected))

    def test_convert_data_missing_field_returns_original(self) -> None:
        """Test that missing field returns original value."""
        field_units = {"MagneticField": [ureg.tesla, ureg.gauss]}
        result = convert_data(field_units, 1.5, "Temperature")
        assert result == 1.5

    def test_convert_data_multiple_fields(self) -> None:
        """Test converting with multiple fields defined."""
        field_units = {
            "MagneticField": [ureg.tesla, ureg.millitesla],
            "Temperature": [ureg.kelvin, ureg.degC],
        }
        # Convert magnetic field
        B_result = convert_data(field_units, 1.0, "MagneticField")
        assert abs(B_result - 1000.0) < 0.1
        
        # Convert temperature
        T_result = convert_data(field_units, 273.15, "Temperature")
        assert abs(T_result - 0.0) < 0.01

    def test_convert_data_with_string_units(self) -> None:
        """Test convert_data with string unit specifications."""
        field_units = {"B": ["tesla", "millitesla"]}
        result = convert_data(field_units, 1.0, "B")
        assert abs(result - 1000.0) < 0.1


class TestGetUnitString:
    """Test unit string formatting."""

    def test_get_unit_string_from_string(self) -> None:
        """Test getting unit string from string input."""
        result = get_unit_string("tesla")
        assert result == "tesla"

    def test_get_unit_string_pretty(self) -> None:
        """Test pretty formatting of unit."""
        unit = ureg.volt / ureg.meter
        result = get_unit_string(unit, pretty=True)
        # Can be either "V/m" or "volt / meter" depending on pint version
        assert ("v" in result.lower() or "volt" in result.lower()) and ("m" in result.lower() or "meter" in result.lower())

    def test_get_unit_string_compact(self) -> None:
        """Test compact formatting of unit."""
        unit = ureg.volt / ureg.meter
        result = get_unit_string(unit, pretty=False)
        assert "volt" in result or "V" in result

    def test_get_unit_string_simple_unit(self) -> None:
        """Test unit string for simple unit."""
        result = get_unit_string(ureg.tesla, pretty=True)
        assert "tesla" in result or "T" in result


class TestAreCompatible:
    """Test unit compatibility checking."""

    def test_compatible_length_units(self) -> None:
        """Test that compatible length units return True."""
        assert are_compatible("meter", "centimeter") is True
        assert are_compatible("meter", "kilometer") is True

    def test_compatible_magnetic_units(self) -> None:
        """Test that compatible magnetic units return True."""
        assert are_compatible("tesla", "millitesla") is True
        assert are_compatible("tesla", "microtesla") is True

    def test_incompatible_units(self) -> None:
        """Test that incompatible units return False."""
        assert are_compatible("tesla", "meter") is False
        assert are_compatible("kelvin", "volt") is False

    def test_compatible_with_pint_units(self) -> None:
        """Test compatibility checking with pint Unit objects."""
        assert are_compatible(ureg.meter, ureg.centimeter) is True
        assert are_compatible(ureg.tesla, ureg.millitesla) is True

    def test_compatible_same_unit(self) -> None:
        """Test that same unit is compatible with itself."""
        assert are_compatible("meter", "meter") is True
        assert are_compatible(ureg.tesla, ureg.tesla) is True

    def test_compatible_mixed_input_types(self) -> None:
        """Test compatibility checking with mixed input types."""
        assert are_compatible("meter", ureg.centimeter) is True
        assert are_compatible(ureg.tesla, "millitesla") is True
