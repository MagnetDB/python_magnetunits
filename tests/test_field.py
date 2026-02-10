"""
Tests for the Field class.
"""

import pytest
from python_magnetunits import Field, ureg


class TestFieldCreation:
    """Test Field object creation and initialization."""

    def test_basic_field_creation(self) -> None:
        """Test creating a basic field with required attributes."""
        field = Field(name="MagneticField", symbol="B", unit=ureg.tesla)
        assert field.name == "MagneticField"
        assert field.symbol == "B"
        assert field.unit == ureg.tesla

    def test_field_with_string_unit(self) -> None:
        """Test that string units are converted to pint Units."""
        field = Field(name="B", symbol="B", unit="meter")
        # Verify it was converted to a pint unit (can convert with it)
        assert field.convert(1.0, "centimeter") == 100.0

    def test_field_with_latex_symbol(self) -> None:
        """Test field with LaTeX symbol."""
        field = Field(
            name="B",
            symbol="B",
            unit="tesla",
            latex_symbol=r"$B$",
        )
        assert field.latex_symbol == r"$B$"

    def test_field_latex_symbol_defaults_to_symbol(self) -> None:
        """Test that latex_symbol defaults to symbol if not provided."""
        field = Field(name="B", symbol="B", unit="tesla")
        assert field.latex_symbol == "B"

    def test_field_with_aliases(self) -> None:
        """Test field with aliases."""
        field = Field(
            name="MagneticField",
            symbol="B",
            unit="tesla",
            aliases=["B_field", "magnetic_field"],
        )
        assert "B_field" in field.aliases
        assert "magnetic_field" in field.aliases

    def test_field_with_excluded_regions(self) -> None:
        """Test field with excluded regions."""
        field = Field(
            name="Temperature",
            symbol="T",
            unit="kelvin",
            exclude_regions=["vacuum", "space"],
        )
        assert "vacuum" in field.exclude_regions
        assert "space" in field.exclude_regions

    def test_field_with_metadata(self) -> None:
        """Test field with custom metadata."""
        field = Field(
            name="B",
            symbol="B",
            unit="tesla",
            metadata={"category": "electromagnetic", "component": "scalar"},
        )
        assert field.metadata["category"] == "electromagnetic"
        assert field.metadata["component"] == "scalar"


class TestFieldConversion:
    """Test unit conversion functionality."""

    def test_convert_single_value(self) -> None:
        """Test converting a single value."""
        field = Field(name="B", symbol="B", unit="tesla")
        result = field.convert(1.0, "millitesla")
        assert abs(result - 1000.0) < 0.01

    def test_convert_with_string_unit(self) -> None:
        """Test conversion with string unit specification."""
        field = Field(name="B", symbol="B", unit="tesla")
        result = field.convert(1.0, "millitesla")
        assert abs(result - 1000.0) < 0.01

    def test_convert_array(self) -> None:
        """Test converting an array of values."""
        field = Field(name="B", symbol="B", unit="tesla")
        values = [1.0, 2.0, 3.0]
        result = field.convert_array(values, "millitesla")
        expected = [1000.0, 2000.0, 3000.0]
        assert all(abs(r - e) < 0.1 for r, e in zip(result, expected))

    def test_convert_temperature(self) -> None:
        """Test converting temperature units."""
        field = Field(name="T", symbol="T", unit="kelvin")
        # 273.15 K = 0 °C
        result = field.convert(273.15, "degC")
        assert abs(result - 0.0) < 0.01

    def test_convert_incompatible_unit_conversion_raises_error(self) -> None:
        """Test that converting to incompatible unit raises error."""
        field = Field(name="B", symbol="B", unit="tesla")
        with pytest.raises(Exception):  # pint.DimensionalityError
            field.convert(1.0, "meter")


class TestFieldValidation:
    """Test field value validation."""

    def test_validate_compatible_value(self) -> None:
        """Test validating a compatible value."""
        field = Field(name="B", symbol="B", unit="tesla")
        assert field.validate_value(1.5) is True
        assert field.validate_value(0.0) is True
        assert field.validate_value(-2.5) is True

    def test_validate_incompatible_value(self) -> None:
        """Test validating an incompatible value."""
        field = Field(name="B", symbol="B", unit="tesla")
        # Note: pint.Quantity() accepts numeric strings, so we test with truly incompatible types
        assert field.validate_value(None) is False
        # Test with a dict which is incompatible
        assert field.validate_value({}) is False

    def test_validate_array(self) -> None:
        """Test that validate_value works with individual values."""
        field = Field(name="B", symbol="B", unit="tesla")
        values = [1.0, 2.0, 3.0]
        assert all(field.validate_value(v) for v in values)


class TestFieldFormatting:
    """Test label formatting for plotting."""

    def test_format_label_plain(self) -> None:
        """Test formatting label with plain symbol."""
        field = Field(name="B", symbol="B", unit="tesla")
        label = field.format_label(use_latex=False)
        assert label == "B"

    def test_format_label_latex(self) -> None:
        """Test formatting label with LaTeX symbol."""
        field = Field(
            name="B",
            symbol="B",
            unit="tesla",
            latex_symbol=r"$B$",
        )
        label = field.format_label(use_latex=True)
        assert label == r"$B$"

    def test_format_label_with_unit(self) -> None:
        """Test formatting label with unit."""
        field = Field(
            name="B",
            symbol="B",
            unit="tesla",
            latex_symbol=r"$B$",
        )
        label = field.format_label("millitesla", use_latex=True)
        assert r"$B$" in label
        assert "mT" in label or "millitesla" in label.lower()

    def test_format_label_with_unit_plain(self) -> None:
        """Test formatting label with unit and plain symbol."""
        field = Field(name="B", symbol="B", unit="tesla")
        label = field.format_label("millitesla", use_latex=False)
        assert "B" in label
        assert "mT" in label or "millitesla" in label.lower()


class TestFieldRegionExclusion:
    """Test region/domain exclusion logic."""

    def test_applies_to_region_included(self) -> None:
        """Test checking if field applies to included region."""
        field = Field(
            name="T",
            symbol="T",
            unit="kelvin",
            exclude_regions=["vacuum"],
        )
        assert field.applies_to_region("air") is True
        assert field.applies_to_region("water") is True

    def test_applies_to_region_excluded(self) -> None:
        """Test checking if field applies to excluded region."""
        field = Field(
            name="T",
            symbol="T",
            unit="kelvin",
            exclude_regions=["vacuum", "space"],
        )
        assert field.applies_to_region("vacuum") is False
        assert field.applies_to_region("space") is False

    def test_applies_to_region_no_exclusions(self) -> None:
        """Test field applies to all regions if no exclusions."""
        field = Field(name="B", symbol="B", unit="tesla")
        assert field.applies_to_region("any_region") is True


class TestFieldRepresentation:
    """Test field string representation."""

    def test_repr(self) -> None:
        """Test repr of field."""
        field = Field(name="B", symbol="B", unit="tesla")
        repr_str = repr(field)
        assert "Field" in repr_str
        assert "B" in repr_str
        assert "tesla" in repr_str
