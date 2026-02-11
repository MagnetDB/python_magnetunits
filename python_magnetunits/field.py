"""
Core Field class for representing physical fields with units and metadata.
"""

from __future__ import annotations

from dataclasses import dataclass, field as dc_field
from typing import TYPE_CHECKING, Any, List, Optional, Union

from pint import UnitRegistry

if TYPE_CHECKING:
    from .field_types import FieldType

# Module-level singleton instance
_global_ureg: Optional[UnitRegistry] = None


def get_global_ureg() -> UnitRegistry:
    """Get the global UnitRegistry instance (singleton pattern)."""
    global _global_ureg
    if _global_ureg is None:
        _global_ureg = UnitRegistry(system="SI")
        _global_ureg.define("percent = 0.01 = %")
        _global_ureg.define("ppm = 1e-6")
        _global_ureg.define("var = volt * ampere")  # For reactive power (VAr)
        # SI-compatible Gauss (pint's lowercase 'gauss' is CGS with different dimensionality)
        _global_ureg.define("Gauss = 1e-4 tesla = G")
    return _global_ureg


# Initialize the global ureg instance at module load time
ureg = get_global_ureg()


@dataclass
class Field:
    """
    Represents a physical field with units, symbols, and metadata.

    A Field encapsulates all information needed to work with a physical quantity:
    its name, symbols (plain and LaTeX), units, descriptions, and domain-specific
    exclusions. This provides type-safe field definitions with integrated unit conversion
    and formatting for scientific computing applications.

    Attributes:
        name: Unique identifier for the field (e.g., "MagneticField")
        symbol: Short symbol for display (e.g., "B")
        unit: Pint unit or unit string (e.g., "tesla", ureg.tesla)
        field_type: Optional FieldType enum value for categorization and validation
        description: Optional human-readable description of the field
        latex_symbol: Optional LaTeX representation (e.g., r"$B$")
        aliases: Alternative names for this field (for registry lookup)
        exclude_regions: Regions/domains where this field doesn't apply
        default_value: Optional default value in the field's unit
        metadata: Custom metadata dict for application-specific data

    Example:
        >>> from python_magnetunits import Field, FieldType, ureg
        >>> B_field = Field(
        ...     name="MagneticField",
        ...     symbol="B",
        ...     unit=ureg.tesla,
        ...     field_type=FieldType.MAGNETIC_FIELD,
        ...     description="Magnetic flux density",
        ...     latex_symbol=r"$B$",
        ... )
        >>> B_field.convert(1.5, "millitesla")
        1500.0
    """

    name: str
    symbol: str
    unit: Union[str, Any]  # pint.Unit or str
    field_type: Optional["FieldType"] = None
    description: Optional[str] = None
    latex_symbol: Optional[str] = None
    aliases: List[str] = dc_field(default_factory=list)
    exclude_regions: List[str] = dc_field(default_factory=list)
    default_value: Optional[float] = None
    metadata: dict[str, Any] = dc_field(default_factory=dict)

    def __post_init__(self) -> None:
        """Convert string units to pint Units and validate field_type compatibility."""
        # Convert string units to pint Units
        if isinstance(self.unit, str):
            self.unit = ureg.Unit(self.unit)
        
        # Default latex_symbol to symbol if not provided
        if self.latex_symbol is None:
            self.latex_symbol = self.symbol
        
        # Validate unit compatibility with field_type if provided
        if self.field_type is not None:
            if not self.field_type.is_compatible(self.unit):
                raise ValueError(
                    f"Unit '{self.unit}' is not compatible with field_type "
                    f"'{self.field_type.name}' (expected dimensionality of "
                    f"'{self.field_type.default_unit}')"
                )

    @classmethod
    def from_field_type(
        cls,
        field_type: "FieldType",
        name: Optional[str] = None,
        symbol: Optional[str] = None,
        unit: Optional[Union[str, Any]] = None,
        latex_symbol: Optional[str] = None,
        **kwargs: Any,
    ) -> "Field":
        """
        Create a Field from a FieldType with default values.

        This factory method creates a Field using the FieldType's default unit,
        symbol, and LaTeX symbol, while allowing overrides for customization.

        Args:
            field_type: The FieldType to base this field on
            name: Override the default name (defaults to FieldType name)
            symbol: Override the default symbol
            unit: Override the default unit (must be compatible)
            latex_symbol: Override the default LaTeX symbol
            **kwargs: Additional Field attributes (description, aliases, etc.)

        Returns:
            A new Field instance

        Raises:
            ValueError: If provided unit is not compatible with field_type

        Example:
            >>> from python_magnetunits import Field, FieldType
            >>> # Create with all defaults
            >>> B = Field.from_field_type(FieldType.MAGNETIC_FIELD)
            >>> B.symbol
            'B'
            >>> # Create with custom name and unit
            >>> B_res = Field.from_field_type(
            ...     FieldType.MAGNETIC_FIELD,
            ...     name="ResistiveMagneticField",
            ...     symbol="B_res",
            ...     unit="millitesla",
            ... )
        """
        return cls(
            name=name or field_type.name,
            symbol=symbol or field_type.default_symbol,
            unit=unit or field_type.default_unit,
            field_type=field_type,
            latex_symbol=latex_symbol or field_type.latex_symbol,
            **kwargs,
        )

    def convert(self, value: float, to_unit: Union[str, Any]) -> float:
        """
        Convert a value from this field's unit to a target unit.

        Args:
            value: The value to convert (in this field's unit)
            to_unit: Target unit (string or pint Unit)

        Returns:
            Converted value in the target unit

        Raises:
            pint.DimensionalityError: If units are incompatible
            pint.UndefinedUnitError: If unit string is not recognized

        Example:
            >>> field = Field("B", "B", "tesla")
            >>> field.convert(1.0, "gauss")
            10000.0
        """
        quantity = ureg.Quantity(value, self.unit)
        return quantity.to(to_unit).magnitude

    def convert_array(self, values: List[float], to_unit: Union[str, Any]) -> List[float]:
        """
        Convert an array of values from this field's unit to a target unit.

        Args:
            values: List of values to convert (in this field's unit)
            to_unit: Target unit (string or pint Unit)

        Returns:
            List of converted values in the target unit

        Example:
            >>> field = Field("B", "B", "tesla")
            >>> field.convert_array([1.0, 2.0, 3.0], "millitesla")
            [1000.0, 2000.0, 3000.0]
        """
        return [self.convert(v, to_unit) for v in values]

    def validate_value(self, value: Any) -> bool:
        """
        Check if a value is compatible with this field's unit.

        Args:
            value: Value to validate

        Returns:
            True if value is dimensionally compatible, False otherwise

        Example:
            >>> field = Field("B", "B", "tesla")
            >>> field.validate_value(1.5)
            True
            >>> field.validate_value("invalid")
            False
        """
        try:
            ureg.Quantity(value, self.unit)
            return True
        except (TypeError, ValueError):
            return False

    def format_label(
        self,
        target_unit: Optional[Union[str, Any]] = None,
        use_latex: bool = False,
    ) -> str:
        """
        Generate a formatted label suitable for plot axes.

        Args:
            target_unit: Optional target unit to include in label
            use_latex: If True, use LaTeX symbol; otherwise use plain symbol

        Returns:
            Formatted label string

        Example:
            >>> field = Field("B", "B", "tesla", latex_symbol=r"$B$")
            >>> field.format_label("tesla", use_latex=True)
            '$B$ [T]'
            >>> field.format_label(use_latex=False)
            'B'
        """
        sym = self.latex_symbol if use_latex else self.symbol

        if target_unit:
            # Format unit using pint's pretty formatting
            unit_obj = ureg.Unit(target_unit) if isinstance(target_unit, str) else target_unit
            unit_str = f"{unit_obj:~P}"  # Pretty format
            return f"{sym} [{unit_str}]"
        return sym

    def applies_to_region(self, region: str) -> bool:
        """
        Check if this field is valid in a given region/domain.

        Args:
            region: Region/domain name to check

        Returns:
            True if field applies to region, False if excluded

        Example:
            >>> field = Field("T", "T", "kelvin", exclude_regions=["vacuum"])
            >>> field.applies_to_region("air")
            True
            >>> field.applies_to_region("vacuum")
            False
        """
        return region not in self.exclude_regions

    def __repr__(self) -> str:
        """String representation of the Field."""
        field_type_str = f", field_type={self.field_type.name}" if self.field_type else ""
        return (
            f"Field(name={self.name!r}, symbol={self.symbol!r}, "
            f"unit={self.unit!r}{field_type_str})"
        )
