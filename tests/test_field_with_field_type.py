"""
Tests for the Field class with FieldType integration.
"""

import pytest
from python_magnetunits import Field, FieldType, ureg


class TestFieldWithFieldType:
    """Test Field creation with FieldType."""

    def test_field_with_compatible_field_type(self) -> None:
        """Test creating a Field with compatible FieldType."""
        field = Field(
            name="MagneticField",
            symbol="B",
            unit=ureg.tesla,
            field_type=FieldType.MAGNETIC_FIELD,
        )
        assert field.field_type == FieldType.MAGNETIC_FIELD
        assert field.unit == ureg.tesla

    def test_field_with_compatible_unit_variant(self) -> None:
        """Test creating a Field with compatible but different unit."""
        field = Field(
            name="MagneticField",
            symbol="B",
            unit="millitesla",
            field_type=FieldType.MAGNETIC_FIELD,
        )
        assert field.field_type == FieldType.MAGNETIC_FIELD

    def test_field_with_incompatible_field_type_raises(self) -> None:
        """Test that incompatible unit raises ValueError."""
        with pytest.raises(ValueError, match="not compatible"):
            Field(
                name="WrongField",
                symbol="X",
                unit=ureg.meter,  # length unit
                field_type=FieldType.MAGNETIC_FIELD,  # expects tesla
            )

    def test_field_without_field_type(self) -> None:
        """Test creating a Field without FieldType (no validation)."""
        field = Field(
            name="CustomField",
            symbol="X",
            unit=ureg.meter,
        )
        assert field.field_type is None

    def test_field_type_temperature_with_celsius(self) -> None:
        """Test temperature field type with Celsius."""
        field = Field(
            name="Temperature",
            symbol="T",
            unit="degC",
            field_type=FieldType.TEMPERATURE,
        )
        assert field.field_type == FieldType.TEMPERATURE

    def test_field_type_pressure_with_bar(self) -> None:
        """Test pressure field type with bar."""
        field = Field(
            name="Pressure",
            symbol="P",
            unit="bar",
            field_type=FieldType.PRESSURE,
        )
        assert field.field_type == FieldType.PRESSURE

    def test_field_type_flow_rate_with_liter_per_minute(self) -> None:
        """Test flow rate field type with liter/minute."""
        field = Field(
            name="FlowRate",
            symbol="Q",
            unit=ureg.liter / ureg.minute,
            field_type=FieldType.FLOW_RATE,
        )
        assert field.field_type == FieldType.FLOW_RATE

    def test_field_type_dimensionless(self) -> None:
        """Test dimensionless field types."""
        field = Field(
            name="Strain",
            symbol="ε",
            unit=ureg.dimensionless,
            field_type=FieldType.STRAIN,
        )
        assert field.field_type == FieldType.STRAIN


class TestFieldFromFieldType:
    """Test Field.from_field_type() factory method."""

    def test_from_field_type_with_defaults(self) -> None:
        """Test creating Field from FieldType with all defaults."""
        field = Field.from_field_type(FieldType.MAGNETIC_FIELD)
        
        assert field.name == "MAGNETIC_FIELD"
        assert field.symbol == "B"
        assert field.unit == ureg.tesla
        assert field.field_type == FieldType.MAGNETIC_FIELD
        assert field.latex_symbol == r"$B$"

    def test_from_field_type_with_custom_name(self) -> None:
        """Test creating Field with custom name."""
        field = Field.from_field_type(
            FieldType.MAGNETIC_FIELD,
            name="ResistiveMagneticField",
        )
        assert field.name == "ResistiveMagneticField"
        assert field.symbol == "B"  # default
        assert field.field_type == FieldType.MAGNETIC_FIELD

    def test_from_field_type_with_custom_symbol(self) -> None:
        """Test creating Field with custom symbol."""
        field = Field.from_field_type(
            FieldType.MAGNETIC_FIELD,
            name="B_res",
            symbol="B_res",
        )
        assert field.symbol == "B_res"

    def test_from_field_type_with_custom_unit(self) -> None:
        """Test creating Field with custom compatible unit."""
        field = Field.from_field_type(
            FieldType.MAGNETIC_FIELD,
            name="B_mT",
            unit="millitesla",
        )
        assert field.unit == ureg.millitesla

    def test_from_field_type_with_incompatible_unit_raises(self) -> None:
        """Test that incompatible custom unit raises ValueError."""
        with pytest.raises(ValueError, match="not compatible"):
            Field.from_field_type(
                FieldType.MAGNETIC_FIELD,
                name="WrongField",
                unit="meter",
            )

    def test_from_field_type_with_description(self) -> None:
        """Test creating Field with description."""
        field = Field.from_field_type(
            FieldType.TEMPERATURE,
            name="InletTemperature",
            description="Coolant inlet temperature",
        )
        assert field.description == "Coolant inlet temperature"

    def test_from_field_type_with_aliases(self) -> None:
        """Test creating Field with aliases."""
        field = Field.from_field_type(
            FieldType.TEMPERATURE,
            name="Temperature",
            aliases=["temp", "T_inlet"],
        )
        assert "temp" in field.aliases
        assert "T_inlet" in field.aliases

    def test_from_field_type_with_exclude_regions(self) -> None:
        """Test creating Field with exclude_regions."""
        field = Field.from_field_type(
            FieldType.TEMPERATURE,
            name="Temperature",
            exclude_regions=["vacuum", "air"],
        )
        assert "vacuum" in field.exclude_regions
        assert field.applies_to_region("water") is True
        assert field.applies_to_region("vacuum") is False

    def test_from_field_type_preserves_latex_symbol(self) -> None:
        """Test that LaTeX symbol is inherited from FieldType."""
        field = Field.from_field_type(FieldType.DENSITY)
        assert field.latex_symbol == r"$\rho$"

    def test_from_field_type_custom_latex_symbol(self) -> None:
        """Test overriding LaTeX symbol."""
        field = Field.from_field_type(
            FieldType.MAGNETIC_FIELD,
            name="B_vec",
            latex_symbol=r"$\vec{B}$",
        )
        assert field.latex_symbol == r"$\vec{B}$"

    def test_from_field_type_all_types(self) -> None:
        """Test that all FieldTypes can create Fields."""
        for ftype in FieldType:
            field = Field.from_field_type(ftype)
            assert field.field_type == ftype
            assert field.name == ftype.name
            assert field.symbol == ftype.default_symbol
            assert field.latex_symbol == ftype.latex_symbol


class TestFieldRepr:
    """Test Field string representation."""

    def test_repr_with_field_type(self) -> None:
        """Test repr includes field_type."""
        field = Field(
            name="B",
            symbol="B",
            unit="tesla",
            field_type=FieldType.MAGNETIC_FIELD,
        )
        repr_str = repr(field)
        assert "MAGNETIC_FIELD" in repr_str
        assert "B" in repr_str

    def test_repr_without_field_type(self) -> None:
        """Test repr without field_type."""
        field = Field(
            name="B",
            symbol="B",
            unit="tesla",
        )
        repr_str = repr(field)
        assert "field_type" not in repr_str


class TestFieldBasicFunctionality:
    """Test that basic Field functionality still works."""

    def test_convert_with_field_type(self) -> None:
        """Test unit conversion still works with field_type."""
        field = Field(
            name="B",
            symbol="B",
            unit="tesla",
            field_type=FieldType.MAGNETIC_FIELD,
        )
        result = field.convert(1.0, "millitesla")
        assert abs(result - 1000.0) < 0.1

    def test_format_label_with_field_type(self) -> None:
        """Test label formatting still works with field_type."""
        field = Field(
            name="B",
            symbol="B",
            unit="tesla",
            field_type=FieldType.MAGNETIC_FIELD,
            latex_symbol=r"$B$",
        )
        label = field.format_label("millitesla", use_latex=True)
        assert r"$B$" in label
        assert "mT" in label

    def test_validate_value_with_field_type(self) -> None:
        """Test value validation still works with field_type."""
        field = Field(
            name="B",
            symbol="B",
            unit="tesla",
            field_type=FieldType.MAGNETIC_FIELD,
        )
        assert field.validate_value(1.5) is True
        assert field.validate_value(None) is False
