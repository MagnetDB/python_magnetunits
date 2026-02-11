"""
Format definition classes for loading field definitions from JSON/YAML files.

This module provides the FormatDefinition class which represents a data file format
(like pupitre.json) and manages the mapping between file columns and Field objects.
"""

from __future__ import annotations

from dataclasses import dataclass, field as dc_field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ..field import Field, ureg
from ..field_types import FieldType
from ..registry import FieldRegistry


# Mapping of common unit names to pint-compatible strings
UNIT_ALIASES: Dict[str, str] = {
    # Temperature
    "celsius": "degC",
    "fahrenheit": "degF",
    "kelvin": "kelvin",
    # Pressure
    "bar": "bar",
    "pascal": "pascal",
    "Pa": "pascal",
    "MPa": "megapascal",
    "psi": "psi",
    # Flow rate
    "liter/minute": "liter/minute",
    "l/min": "liter/minute",
    "m3/h": "meter**3/hour",
    "meter**3/hour": "meter**3/hour",
    # Power
    "megawatt": "megawatt",
    "MW": "megawatt",
    "watt": "watt",
    "W": "watt",
    "megavar": "megavar",
    "Mvar": "megavar",
    # Current
    "ampere": "ampere",
    "A": "ampere",
    # Voltage
    "volt": "volt",
    "V": "volt",
    # Magnetic field
    "tesla": "tesla",
    "T": "tesla",
    # Rotation
    "rpm": "revolution/minute",
    # Dimensionless
    "dimensionless": "dimensionless",
    "percent": "percent",
    "%": "percent",
}


def normalize_unit(unit_str: str) -> str:
    """
    Normalize a unit string to pint-compatible format.

    Args:
        unit_str: Unit string from JSON (e.g., "celsius", "bar")

    Returns:
        Pint-compatible unit string (e.g., "degC", "bar")
    """
    return UNIT_ALIASES.get(unit_str, unit_str)


def get_field_type(field_type_str: str) -> Optional[FieldType]:
    """
    Convert a field_type string to FieldType enum.

    Args:
        field_type_str: Field type string from JSON (e.g., "magnetic_field", "temperature")

    Returns:
        FieldType enum value, or None if not found
    """
    try:
        return FieldType(field_type_str)
    except ValueError:
        return None


@dataclass
class FieldDefinition:
    """
    Represents a single field definition from a format file.

    This is an intermediate representation between the JSON and the Field object.
    """

    name: str  # Column name in the data file
    field_type: Optional[str] = None  # FieldType string value
    unit: str = "dimensionless"
    symbol: Optional[str] = None
    description: Optional[str] = None
    latex_symbol: Optional[str] = None
    aliases: List[str] = dc_field(default_factory=list)
    exclude_regions: List[str] = dc_field(default_factory=list)

    def to_field(self) -> Field:
        """
        Convert this definition to a Field object.

        If field_type is specified but incompatible with the unit,
        the field is created without the field_type (with a warning).

        Returns:
            Field object with all attributes set
        """
        # Get FieldType if specified
        ftype = get_field_type(self.field_type) if self.field_type else None

        # Normalize unit
        unit = normalize_unit(self.unit)

        # Use name as symbol if not specified
        symbol = self.symbol or self.name

        # Validate field_type compatibility if both are specified
        if ftype is not None:
            if not ftype.is_compatible(unit):
                # Create field without field_type to avoid validation error
                import warnings
                warnings.warn(
                    f"Field '{self.name}': unit '{unit}' incompatible with "
                    f"field_type '{self.field_type}', creating without type validation"
                )
                ftype = None

        return Field(
            name=self.name,
            symbol=symbol,
            unit=unit,
            field_type=ftype,
            description=self.description,
            latex_symbol=self.latex_symbol,
            aliases=self.aliases,
            exclude_regions=self.exclude_regions,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FieldDefinition":
        """
        Create a FieldDefinition from a dictionary.

        Args:
            data: Dictionary with field definition data

        Returns:
            FieldDefinition object
        """
        return cls(
            name=data["name"],
            field_type=data.get("field_type"),
            unit=data.get("unit", "dimensionless"),
            symbol=data.get("symbol"),
            description=data.get("description"),
            latex_symbol=data.get("latex_symbol"),
            aliases=data.get("aliases", []),
            exclude_regions=data.get("exclude_regions", []),
        )


@dataclass
class FormatMetadata:
    """Metadata about the file format."""

    description: str = ""
    file_extension: str = ".txt"
    delimiter: str = "\t"
    header_row: bool = True
    encoding: str = "utf-8"
    skip_rows: int = 0
    comment_char: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FormatMetadata":
        """Create FormatMetadata from a dictionary."""
        return cls(
            description=data.get("description", ""),
            file_extension=data.get("file_extension", ".txt"),
            delimiter=data.get("delimiter", "\t"),
            header_row=data.get("header_row", True),
            encoding=data.get("encoding", "utf-8"),
            skip_rows=data.get("skip_rows", 0),
            comment_char=data.get("comment_char"),
        )


class FormatDefinition:
    """
    Represents a complete format definition loaded from JSON/YAML.

    A FormatDefinition contains:
    - Format name and metadata (delimiter, extension, etc.)
    - Field definitions mapping column names to Field objects
    - A FieldRegistry for looking up fields

    Example:
        >>> fmt = FormatDefinition.from_json("pupitre.json")
        >>> fmt.format_name
        'pupitre'
        >>> field = fmt.get_field("Field")  # Get field by column name
        >>> field.symbol
        'B_res'
        >>> field.convert(1.5, "Gauss")
        15000.0
    """

    def __init__(
        self,
        format_name: str,
        metadata: Optional[FormatMetadata] = None,
        field_definitions: Optional[List[FieldDefinition]] = None,
    ) -> None:
        """
        Initialize a FormatDefinition.

        Args:
            format_name: Name identifier for this format
            metadata: Optional format metadata
            field_definitions: List of field definitions
        """
        self.format_name = format_name
        self.metadata = metadata or FormatMetadata()
        self._field_definitions: List[FieldDefinition] = field_definitions or []

        # Internal storage
        self._fields: Dict[str, Field] = {}  # column_name -> Field
        self._registry: FieldRegistry = FieldRegistry()

        # Build fields from definitions
        self._build_fields()

    def _build_fields(self) -> None:
        """Convert field definitions to Field objects and register them."""
        import warnings
        
        for defn in self._field_definitions:
            try:
                field = defn.to_field()
                self._fields[defn.name] = field
                self._registry.register(field)
            except Exception as e:
                warnings.warn(f"Could not create field '{defn.name}': {e}")

    def get_field(self, column_name: str) -> Optional[Field]:
        """
        Get a Field by its column name in the data file.

        Args:
            column_name: Column name as it appears in the data file

        Returns:
            Field object if found, None otherwise
        """
        return self._fields.get(column_name)

    def get_field_by_symbol(self, symbol: str) -> Optional[Field]:
        """
        Get a Field by its symbol.

        Args:
            symbol: Field symbol (e.g., "B_res", "T_in1")

        Returns:
            Field object if found, None otherwise
        """
        return self._registry.get(symbol)

    @property
    def registry(self) -> FieldRegistry:
        """Get the internal FieldRegistry with all fields."""
        return self._registry

    @property
    def column_names(self) -> List[str]:
        """Get list of all column names defined in this format."""
        return list(self._fields.keys())

    @property
    def fields(self) -> List[Field]:
        """Get list of all Field objects."""
        return list(self._fields.values())

    def has_column(self, column_name: str) -> bool:
        """Check if a column name is defined in this format."""
        return column_name in self._fields

    def list_fields_by_type(self, field_type: FieldType) -> List[Field]:
        """
        List all fields of a specific FieldType.

        Args:
            field_type: FieldType to filter by

        Returns:
            List of fields matching the type
        """
        return [f for f in self._fields.values() if f.field_type == field_type]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the format definition back to a dictionary.

        Returns:
            Dictionary representation suitable for JSON serialization
        """
        return {
            "format_name": self.format_name,
            "metadata": {
                "description": self.metadata.description,
                "file_extension": self.metadata.file_extension,
                "delimiter": self.metadata.delimiter,
                "header_row": self.metadata.header_row,
                "encoding": self.metadata.encoding,
                "skip_rows": self.metadata.skip_rows,
                "comment_char": self.metadata.comment_char,
            },
            "fields": [
                {
                    "name": defn.name,
                    "field_type": defn.field_type,
                    "unit": defn.unit,
                    "symbol": defn.symbol,
                    "description": defn.description,
                }
                for defn in self._field_definitions
            ],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FormatDefinition":
        """
        Create a FormatDefinition from a dictionary.

        Args:
            data: Dictionary with format definition data

        Returns:
            FormatDefinition object
        """
        format_name = data.get("format_name", "unknown")

        # Parse metadata
        metadata_dict = data.get("metadata", {})
        metadata = FormatMetadata.from_dict(metadata_dict)

        # Parse field definitions
        fields_data = data.get("fields", [])
        field_definitions = [FieldDefinition.from_dict(f) for f in fields_data]

        return cls(
            format_name=format_name,
            metadata=metadata,
            field_definitions=field_definitions,
        )

    @classmethod
    def from_json(cls, path: Union[str, Path]) -> "FormatDefinition":
        """
        Load a FormatDefinition from a JSON file.

        Args:
            path: Path to JSON file

        Returns:
            FormatDefinition object

        Example:
            >>> fmt = FormatDefinition.from_json("pupitre.json")
            >>> fmt.format_name
            'pupitre'
        """
        import json

        path = Path(path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    @classmethod
    def from_yaml(cls, path: Union[str, Path]) -> "FormatDefinition":
        """
        Load a FormatDefinition from a YAML file.

        Args:
            path: Path to YAML file

        Returns:
            FormatDefinition object

        Raises:
            ImportError: If PyYAML is not installed
        """
        try:
            import yaml
        except ImportError:
            raise ImportError("PyYAML is required to load YAML files: pip install pyyaml")

        path = Path(path)
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    def __repr__(self) -> str:
        """String representation."""
        return f"FormatDefinition(name={self.format_name!r}, fields={len(self._fields)})"

    def __len__(self) -> int:
        """Number of fields in this format."""
        return len(self._fields)

    def summary(self) -> str:
        """
        Get a human-readable summary of this format definition.

        Returns:
            Multi-line string with format details
        """
        lines = [
            f"Format: {self.format_name}",
            f"Description: {self.metadata.description}",
            f"File extension: {self.metadata.file_extension}",
            f"Delimiter: {repr(self.metadata.delimiter)}",
            f"Fields: {len(self._fields)}",
            "",
            "Field list:",
        ]

        # Group by field_type
        by_type: Dict[str, List[Field]] = {}
        for field in self._fields.values():
            type_name = field.field_type.name if field.field_type else "untyped"
            if type_name not in by_type:
                by_type[type_name] = []
            by_type[type_name].append(field)

        for type_name, fields in sorted(by_type.items()):
            lines.append(f"  {type_name}:")
            for field in fields:
                lines.append(f"    - {field.name} ({field.symbol}): {field.unit}")

        return "\n".join(lines)
