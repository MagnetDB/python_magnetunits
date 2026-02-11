"""
Core Field class for representing physical fields with units and metadata.
"""

from __future__ import annotations

from dataclasses import dataclass, field as dc_field
from typing import Any, List, Optional, Union

from pint import UnitRegistry

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
        field_type: Optional FieldType enum value for categorization
        description: Optional human-readable description of the field
        latex_symbol: Optional LaTeX representation (e.g., r"$B$")
        aliases: Alternative names for this field (for registry lookup)
        exclude_regions: Regions/domains where this field doesn't apply
        default_value: Optional default value in the field's unit
        metadata: Custom metadata dict for application-specific data

    Example:
        >>> B_field = Field(
        ...     name="MagneticField",
        ...     symbol="B",
        ...     unit=ureg.tesla,
        ...     description="Magnetic flux density",
        ...     latex_symbol=r"$B$",
        ...     aliases=["B_field", "magnetic_field"]
        ... )
        >>> B_field.convert(1.5, "gauss")
        15000.0
        >>> B_field.format_label("tesla", use_latex=True)
        '$B$ [T]'
    """

    name: str
    symbol: str
    unit: Union[str, Any]  # pint.Unit or str
    field_type: Optional[Any] = None  # Optional[FieldType] - avoiding circular import
    description: Optional[str] = None
    latex_symbol: Optional[str] = None
    aliases: List[str] = dc_field(default_factory=list)
    exclude_regions: List[str] = dc_field(default_factory=list)
    default_value: Optional[float] = None
    metadata: dict[str, Any] = dc_field(default_factory=dict)

    def __post_init__(self) -> None:
        """Convert string units to pint Units after initialization."""
        if isinstance(self.unit, str):
            self.unit = ureg(self.unit)
        if self.latex_symbol is None:
            self.latex_symbol = self.symbol

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
            unit_obj = ureg(target_unit) if isinstance(target_unit, str) else target_unit
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
        return (
            f"Field(name={self.name!r}, symbol={self.symbol!r}, "
            f"unit={self.unit!r}, aliases={self.aliases})"
        )
