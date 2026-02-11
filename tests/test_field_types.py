"""
Tests for the FieldType enum.
"""

import pytest
from python_magnetunits import ureg
from python_magnetunits.field_types import FieldType


class TestFieldTypeBasics:
    """Test FieldType enum basic functionality."""

    def test_all_field_types_have_units(self) -> None:
        """Verify all FieldType members have a default unit."""
        for ftype in FieldType:
            assert ftype.default_unit is not None, f"{ftype} missing default_unit"

    def test_all_field_types_have_symbols(self) -> None:
        """Verify all FieldType members have a default symbol."""
        for ftype in FieldType:
            assert ftype.default_symbol is not None, f"{ftype} missing default_symbol"
            assert len(ftype.default_symbol) > 0, f"{ftype} has empty symbol"

    def test_all_field_types_have_latex(self) -> None:
        """Verify all FieldType members have a LaTeX symbol."""
        for ftype in FieldType:
            assert ftype.latex_symbol is not None, f"{ftype} missing latex_symbol"
            assert "$" in ftype.latex_symbol, f"{ftype} latex_symbol not in LaTeX format"

    def test_field_type_from_string(self) -> None:
        """Test creating FieldType from string value."""
        ftype = FieldType("magnetic_field")
        assert ftype == FieldType.MAGNETIC_FIELD

    def test_field_type_value(self) -> None:
        """Test FieldType value attribute."""
        assert FieldType.MAGNETIC_FIELD.value == "magnetic_field"
        assert FieldType.TEMPERATURE.value == "temperature"


class TestFieldTypeUnits:
    """Test FieldType default units."""

    def test_magnetic_field_unit(self) -> None:
        """Test magnetic field has tesla as default unit."""
        assert FieldType.MAGNETIC_FIELD.default_unit == ureg.tesla

    def test_temperature_unit(self) -> None:
        """Test temperature has kelvin as default unit."""
        assert FieldType.TEMPERATURE.default_unit == ureg.kelvin

    def test_pressure_unit(self) -> None:
        """Test pressure has pascal as default unit."""
        assert FieldType.PRESSURE.default_unit == ureg.pascal

    def test_current_unit(self) -> None:
        """Test current has ampere as default unit."""
        assert FieldType.CURRENT.default_unit == ureg.ampere

    def test_power_unit(self) -> None:
        """Test power has watt as default unit."""
        assert FieldType.POWER.default_unit == ureg.watt


class TestFieldTypeSymbols:
    """Test FieldType default symbols."""

    def test_magnetic_field_symbol(self) -> None:
        """Test magnetic field symbol."""
        assert FieldType.MAGNETIC_FIELD.default_symbol == "B"

    def test_temperature_symbol(self) -> None:
        """Test temperature symbol."""
        assert FieldType.TEMPERATURE.default_symbol == "T"

    def test_current_symbol(self) -> None:
        """Test current symbol."""
        assert FieldType.CURRENT.default_symbol == "I"

    def test_magnetic_field_latex(self) -> None:
        """Test magnetic field LaTeX symbol."""
        assert FieldType.MAGNETIC_FIELD.latex_symbol == r"$B$"

    def test_density_latex(self) -> None:
        """Test density LaTeX symbol."""
        assert FieldType.DENSITY.latex_symbol == r"$\rho$"


class TestFieldTypeCompatibility:
    """Test FieldType.is_compatible() method."""

    def test_magnetic_field_compatible_with_tesla(self) -> None:
        """Test magnetic field is compatible with tesla."""
        assert FieldType.MAGNETIC_FIELD.is_compatible(ureg.tesla) is True

    def test_magnetic_field_compatible_with_gauss(self) -> None:
        """Test magnetic field is compatible with Gauss (SI-compatible, capital G)."""
        # Note: pint's lowercase 'gauss' is CGS with different dimensionality
        # We define 'Gauss' (capital G) as SI-compatible in our ureg
        assert FieldType.MAGNETIC_FIELD.is_compatible("Gauss") is True

    def test_magnetic_field_compatible_with_millitesla(self) -> None:
        """Test magnetic field is compatible with millitesla."""
        assert FieldType.MAGNETIC_FIELD.is_compatible("millitesla") is True

    def test_magnetic_field_incompatible_with_meter(self) -> None:
        """Test magnetic field is not compatible with meter."""
        assert FieldType.MAGNETIC_FIELD.is_compatible(ureg.meter) is False

    def test_magnetic_field_incompatible_with_kelvin(self) -> None:
        """Test magnetic field is not compatible with kelvin."""
        assert FieldType.MAGNETIC_FIELD.is_compatible("kelvin") is False

    def test_temperature_compatible_with_celsius(self) -> None:
        """Test temperature is compatible with Celsius."""
        assert FieldType.TEMPERATURE.is_compatible("degC") is True

    def test_temperature_compatible_with_fahrenheit(self) -> None:
        """Test temperature is compatible with Fahrenheit."""
        assert FieldType.TEMPERATURE.is_compatible("degF") is True

    def test_pressure_compatible_with_bar(self) -> None:
        """Test pressure is compatible with bar."""
        assert FieldType.PRESSURE.is_compatible("bar") is True

    def test_pressure_compatible_with_psi(self) -> None:
        """Test pressure is compatible with psi."""
        assert FieldType.PRESSURE.is_compatible("psi") is True

    def test_flow_rate_compatible_with_liter_per_minute(self) -> None:
        """Test flow rate is compatible with liter/minute."""
        assert FieldType.FLOW_RATE.is_compatible(ureg.liter / ureg.minute) is True

    def test_dimensionless_types(self) -> None:
        """Test dimensionless field types."""
        assert FieldType.STRAIN.is_compatible(ureg.dimensionless) is True
        assert FieldType.POISSON_RATIO.is_compatible(ureg.dimensionless) is True
        assert FieldType.RELATIVE_PERMEABILITY.is_compatible(ureg.dimensionless) is True


class TestFieldTypeCount:
    """Test that all expected field types exist."""

    def test_total_field_type_count(self) -> None:
        """Verify we have exactly 40 field types."""
        assert len(FieldType) == 40

    def test_electromagnetic_field_types_exist(self) -> None:
        """Test electromagnetic field types exist."""
        em_types = [
            FieldType.MAGNETIC_FIELD,
            FieldType.ELECTRIC_FIELD,
            FieldType.CURRENT,
            FieldType.CURRENT_DENSITY,
            FieldType.VOLTAGE,
            FieldType.RESISTANCE,
            FieldType.INDUCTANCE,
        ]
        for ftype in em_types:
            assert ftype in FieldType

    def test_thermal_field_types_exist(self) -> None:
        """Test thermal field types exist."""
        thermal_types = [
            FieldType.TEMPERATURE,
            FieldType.HEAT_FLUX,
            FieldType.THERMAL_CONDUCTIVITY,
            FieldType.HEAT_TRANSFER_COEFFICIENT,
            FieldType.SPECIFIC_HEAT,
            FieldType.THERMAL_EXPANSION,
            FieldType.THERMAL_DIFFUSIVITY,
        ]
        for ftype in thermal_types:
            assert ftype in FieldType

    def test_hydraulics_field_types_exist(self) -> None:
        """Test hydraulics field types exist."""
        hydraulics_types = [
            FieldType.PRESSURE,
            FieldType.FLOW_RATE,
            FieldType.VELOCITY,
            FieldType.DYNAMIC_VISCOSITY,
            FieldType.KINEMATIC_VISCOSITY,
        ]
        for ftype in hydraulics_types:
            assert ftype in FieldType

    def test_mechanical_field_types_exist(self) -> None:
        """Test mechanical field types exist."""
        mechanical_types = [
            FieldType.FORCE,
            FieldType.STRESS,
            FieldType.STRAIN,
            FieldType.DENSITY,
            FieldType.YOUNG_MODULUS,
            FieldType.POISSON_RATIO,
        ]
        for ftype in mechanical_types:
            assert ftype in FieldType
