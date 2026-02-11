"""
Tests for the formats module.
"""

import json
import tempfile
from pathlib import Path

import pytest
from python_magnetunits import FieldType, ureg
from python_magnetunits.formats import (
    FieldDefinition,
    FormatDefinition,
    FormatMetadata,
    get_field_type,
    normalize_unit,
)


class TestNormalizeUnit:
    """Test unit normalization."""

    def test_normalize_celsius(self) -> None:
        """Test normalizing celsius to degC."""
        assert normalize_unit("celsius") == "degC"

    def test_normalize_bar(self) -> None:
        """Test bar remains bar."""
        assert normalize_unit("bar") == "bar"

    def test_normalize_unknown_passes_through(self) -> None:
        """Test that unknown units pass through unchanged."""
        assert normalize_unit("some_unknown_unit") == "some_unknown_unit"

    def test_normalize_ampere(self) -> None:
        """Test ampere normalization."""
        assert normalize_unit("ampere") == "ampere"
        assert normalize_unit("A") == "ampere"

    def test_normalize_percent(self) -> None:
        """Test percent normalization."""
        assert normalize_unit("percent") == "percent"
        assert normalize_unit("%") == "percent"


class TestGetFieldType:
    """Test FieldType lookup from string."""

    def test_get_magnetic_field_type(self) -> None:
        """Test getting MAGNETIC_FIELD type."""
        assert get_field_type("magnetic_field") == FieldType.MAGNETIC_FIELD

    def test_get_temperature_type(self) -> None:
        """Test getting TEMPERATURE type."""
        assert get_field_type("temperature") == FieldType.TEMPERATURE

    def test_get_unknown_returns_none(self) -> None:
        """Test that unknown types return None."""
        assert get_field_type("unknown_type") is None
        assert get_field_type("") is None


class TestFieldDefinition:
    """Test FieldDefinition class."""

    def test_create_basic_field_definition(self) -> None:
        """Test creating a basic FieldDefinition."""
        defn = FieldDefinition(
            name="Temperature",
            field_type="temperature",
            unit="celsius",
            symbol="T",
        )
        assert defn.name == "Temperature"
        assert defn.field_type == "temperature"
        assert defn.unit == "celsius"
        assert defn.symbol == "T"

    def test_field_definition_from_dict(self) -> None:
        """Test creating FieldDefinition from dict."""
        data = {
            "name": "Pressure",
            "field_type": "pressure",
            "unit": "bar",
            "symbol": "P",
            "description": "Static pressure",
        }
        defn = FieldDefinition.from_dict(data)
        assert defn.name == "Pressure"
        assert defn.field_type == "pressure"
        assert defn.description == "Static pressure"

    def test_to_field_creates_valid_field(self) -> None:
        """Test converting FieldDefinition to Field."""
        defn = FieldDefinition(
            name="MagneticField",
            field_type="magnetic_field",
            unit="tesla",
            symbol="B",
            description="Magnetic flux density",
        )
        field = defn.to_field()
        assert field.name == "MagneticField"
        assert field.symbol == "B"
        assert field.field_type == FieldType.MAGNETIC_FIELD
        assert field.unit == ureg.tesla

    def test_to_field_with_celsius(self) -> None:
        """Test that celsius is converted to degC."""
        defn = FieldDefinition(
            name="Temp",
            field_type="temperature",
            unit="celsius",
            symbol="T",
        )
        field = defn.to_field()
        # Should be able to convert to kelvin
        result = field.convert(0, "kelvin")
        assert abs(result - 273.15) < 0.01

    def test_to_field_without_field_type(self) -> None:
        """Test creating field without field_type."""
        defn = FieldDefinition(
            name="CustomField",
            unit="meter",
            symbol="X",
        )
        field = defn.to_field()
        assert field.field_type is None

    def test_to_field_incompatible_type_creates_untyped(self) -> None:
        """Test that incompatible type/unit creates untyped field."""
        import warnings
        
        defn = FieldDefinition(
            name="BadField",
            field_type="temperature",  # expects kelvin-compatible
            unit="meter",  # but we give length
            symbol="X",
        )
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            field = defn.to_field()
            # Should have warned
            assert len(w) == 1
            assert "incompatible" in str(w[0].message).lower()
        
        # Field should be created but without field_type
        assert field.name == "BadField"
        assert field.field_type is None


class TestFormatMetadata:
    """Test FormatMetadata class."""

    def test_default_metadata(self) -> None:
        """Test default metadata values."""
        meta = FormatMetadata()
        assert meta.delimiter == "\t"
        assert meta.file_extension == ".txt"
        assert meta.header_row is True

    def test_metadata_from_dict(self) -> None:
        """Test creating metadata from dict."""
        data = {
            "description": "Test format",
            "file_extension": ".csv",
            "delimiter": ",",
            "header_row": True,
        }
        meta = FormatMetadata.from_dict(data)
        assert meta.description == "Test format"
        assert meta.file_extension == ".csv"
        assert meta.delimiter == ","


class TestFormatDefinition:
    """Test FormatDefinition class."""

    def test_create_empty_format(self) -> None:
        """Test creating an empty format definition."""
        fmt = FormatDefinition("test_format")
        assert fmt.format_name == "test_format"
        assert len(fmt) == 0

    def test_create_format_with_fields(self) -> None:
        """Test creating format with field definitions."""
        field_defs = [
            FieldDefinition(name="Col1", unit="tesla", symbol="B"),
            FieldDefinition(name="Col2", unit="kelvin", symbol="T"),
        ]
        fmt = FormatDefinition("test", field_definitions=field_defs)
        assert len(fmt) == 2

    def test_get_field_by_column_name(self) -> None:
        """Test getting field by column name."""
        field_defs = [
            FieldDefinition(name="Temperature", unit="celsius", symbol="T",
                          field_type="temperature"),
        ]
        fmt = FormatDefinition("test", field_definitions=field_defs)
        
        field = fmt.get_field("Temperature")
        assert field is not None
        assert field.symbol == "T"

    def test_get_field_by_symbol(self) -> None:
        """Test getting field by symbol through registry."""
        field_defs = [
            FieldDefinition(name="MagField", unit="tesla", symbol="B_res",
                          field_type="magnetic_field"),
        ]
        fmt = FormatDefinition("test", field_definitions=field_defs)
        
        # Lookup by symbol
        field = fmt.get_field_by_symbol("B_res")
        assert field is not None
        assert field.name == "MagField"

    def test_has_column(self) -> None:
        """Test checking if column exists."""
        field_defs = [
            FieldDefinition(name="Col1", unit="meter", symbol="X"),
        ]
        fmt = FormatDefinition("test", field_definitions=field_defs)
        
        assert fmt.has_column("Col1") is True
        assert fmt.has_column("NonExistent") is False

    def test_column_names(self) -> None:
        """Test getting list of column names."""
        field_defs = [
            FieldDefinition(name="A", unit="meter", symbol="a"),
            FieldDefinition(name="B", unit="meter", symbol="b"),
            FieldDefinition(name="C", unit="meter", symbol="c"),
        ]
        fmt = FormatDefinition("test", field_definitions=field_defs)
        
        assert set(fmt.column_names) == {"A", "B", "C"}

    def test_list_fields_by_type(self) -> None:
        """Test listing fields by FieldType."""
        field_defs = [
            FieldDefinition(name="T1", unit="kelvin", symbol="T1",
                          field_type="temperature"),
            FieldDefinition(name="T2", unit="celsius", symbol="T2",
                          field_type="temperature"),
            FieldDefinition(name="P", unit="pascal", symbol="P",
                          field_type="pressure"),
        ]
        fmt = FormatDefinition("test", field_definitions=field_defs)
        
        temp_fields = fmt.list_fields_by_type(FieldType.TEMPERATURE)
        assert len(temp_fields) == 2
        
        pressure_fields = fmt.list_fields_by_type(FieldType.PRESSURE)
        assert len(pressure_fields) == 1

    def test_registry_property(self) -> None:
        """Test accessing the internal registry."""
        field_defs = [
            FieldDefinition(name="Field1", unit="tesla", symbol="B",
                          field_type="magnetic_field"),
        ]
        fmt = FormatDefinition("test", field_definitions=field_defs)
        
        # Access registry
        registry = fmt.registry
        assert "B" in registry

    def test_to_dict(self) -> None:
        """Test converting format back to dict."""
        field_defs = [
            FieldDefinition(name="Col1", unit="meter", symbol="X",
                          field_type="length", description="Test column"),
        ]
        fmt = FormatDefinition("test", field_definitions=field_defs)
        
        result = fmt.to_dict()
        assert result["format_name"] == "test"
        assert len(result["fields"]) == 1
        assert result["fields"][0]["name"] == "Col1"


class TestFormatDefinitionFromJSON:
    """Test loading FormatDefinition from JSON files."""

    def test_from_dict(self) -> None:
        """Test loading from dictionary."""
        data = {
            "format_name": "test_format",
            "metadata": {
                "description": "Test format",
                "file_extension": ".csv",
                "delimiter": ",",
            },
            "fields": [
                {
                    "name": "Temperature",
                    "field_type": "temperature",
                    "unit": "celsius",
                    "symbol": "T",
                    "description": "Measured temperature",
                },
                {
                    "name": "Pressure",
                    "field_type": "pressure",
                    "unit": "bar",
                    "symbol": "P",
                },
            ],
        }
        
        fmt = FormatDefinition.from_dict(data)
        
        assert fmt.format_name == "test_format"
        assert fmt.metadata.description == "Test format"
        assert fmt.metadata.delimiter == ","
        assert len(fmt) == 2
        
        # Check fields
        temp = fmt.get_field("Temperature")
        assert temp.symbol == "T"
        assert temp.field_type == FieldType.TEMPERATURE

    def test_from_json_file(self) -> None:
        """Test loading from JSON file."""
        data = {
            "format_name": "json_test",
            "metadata": {"description": "From JSON file"},
            "fields": [
                {"name": "Col1", "unit": "meter", "symbol": "X"},
            ],
        }
        
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            temp_path = f.name
        
        try:
            fmt = FormatDefinition.from_json(temp_path)
            assert fmt.format_name == "json_test"
            assert len(fmt) == 1
        finally:
            Path(temp_path).unlink()

    def test_from_json_with_path_object(self) -> None:
        """Test loading from JSON using Path object."""
        data = {
            "format_name": "path_test",
            "fields": [],
        }
        
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            temp_path = Path(f.name)
        
        try:
            fmt = FormatDefinition.from_json(temp_path)
            assert fmt.format_name == "path_test"
        finally:
            temp_path.unlink()


class TestFormatDefinitionRepr:
    """Test string representation methods."""

    def test_repr(self) -> None:
        """Test __repr__ output."""
        fmt = FormatDefinition("test_format")
        repr_str = repr(fmt)
        assert "FormatDefinition" in repr_str
        assert "test_format" in repr_str

    def test_summary(self) -> None:
        """Test summary output."""
        field_defs = [
            FieldDefinition(name="T1", unit="kelvin", symbol="T1",
                          field_type="temperature"),
            FieldDefinition(name="P1", unit="pascal", symbol="P1",
                          field_type="pressure"),
        ]
        meta = FormatMetadata(description="Test format", file_extension=".dat")
        fmt = FormatDefinition("test", metadata=meta, field_definitions=field_defs)
        
        summary = fmt.summary()
        assert "test" in summary
        assert "Test format" in summary
        assert ".dat" in summary
        assert "TEMPERATURE" in summary
        assert "PRESSURE" in summary


class TestPupitreFormat:
    """Integration tests with actual pupitre.json format."""

    @pytest.fixture
    def pupitre_path(self) -> Path:
        """Get path to pupitre.json."""
        return Path("/mnt/project/pupitre.json")

    def test_load_pupitre_json(self, pupitre_path: Path) -> None:
        """Test loading the actual pupitre.json file."""
        if not pupitre_path.exists():
            pytest.skip("pupitre.json not found")
        
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fmt = FormatDefinition.from_json(pupitre_path)
        
        assert fmt.format_name == "pupitre"
        assert len(fmt) == 90  # Total fields in pupitre.json

    def test_pupitre_magnetic_fields(self, pupitre_path: Path) -> None:
        """Test magnetic field definitions in pupitre."""
        if not pupitre_path.exists():
            pytest.skip("pupitre.json not found")
        
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fmt = FormatDefinition.from_json(pupitre_path)
        
        # Check resistive field
        field = fmt.get_field("Field")
        assert field is not None
        assert field.symbol == "B_res"
        assert field.field_type == FieldType.MAGNETIC_FIELD
        
        # Test conversion
        gauss_value = field.convert(1.0, "Gauss")
        assert abs(gauss_value - 10000.0) < 0.1

    def test_pupitre_temperature_fields(self, pupitre_path: Path) -> None:
        """Test temperature field definitions in pupitre."""
        if not pupitre_path.exists():
            pytest.skip("pupitre.json not found")
        
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fmt = FormatDefinition.from_json(pupitre_path)
        
        # Check inlet temperature
        tin1 = fmt.get_field("Tin1")
        assert tin1 is not None
        assert tin1.symbol == "T_in1"
        assert tin1.field_type == FieldType.TEMPERATURE
        
        # Test conversion (20°C to K)
        kelvin_value = tin1.convert(20, "kelvin")
        assert abs(kelvin_value - 293.15) < 0.01

    def test_pupitre_list_by_type(self, pupitre_path: Path) -> None:
        """Test listing pupitre fields by type."""
        if not pupitre_path.exists():
            pytest.skip("pupitre.json not found")
        
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fmt = FormatDefinition.from_json(pupitre_path)
        
        # Count temperature fields
        temp_fields = fmt.list_fields_by_type(FieldType.TEMPERATURE)
        assert len(temp_fields) == 22  # Based on pupitre.json

        # Count current fields
        current_fields = fmt.list_fields_by_type(FieldType.CURRENT)
        assert len(current_fields) == 20  # Icoil1-16 + Idcct1-4
