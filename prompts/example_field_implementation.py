"""
Example implementation of the new Field class for field-framework package.
This shows how the refactored code would look.
"""

from pint import UnitRegistry
from typing import Optional, List, Any, Union
from dataclasses import dataclass, field as dc_field

# Initialize unit registry
ureg = UnitRegistry()


@dataclass
class Field:
    """
    Represents a physical field with units, symbols, and metadata.
    
    This replaces the dict-based field definitions used in magnetrun and
    python_hifimagnetparaview with a type-safe, object-oriented approach.
    
    Example:
        >>> B_field = Field(
        ...     name="MagneticField",
        ...     symbol="B",
        ...     unit="tesla",
        ...     latex_symbol=r"$B$"
        ... )
        >>> B_field.convert(1.0, "gauss")
        10000.0
        >>> B_field.format_label("gauss", use_latex=True)
        '$B$ [G]'
    """
    
    # Core attributes
    name: str
    symbol: str
    unit: Union[Any, str]  # pint.Unit or string
    
    # Optional attributes
    description: Optional[str] = None
    latex_symbol: Optional[str] = None
    aliases: List[str] = dc_field(default_factory=list)
    exclude_regions: List[str] = dc_field(default_factory=list)
    default_value: Optional[Any] = None
    metadata: dict = dc_field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize and validate the field after creation."""
        # Convert string units to pint Units
        if isinstance(self.unit, str):
            self.unit = ureg(self.unit)
        
        # Use symbol as latex_symbol if not provided
        if self.latex_symbol is None:
            self.latex_symbol = self.symbol
    
    def convert(self, value: float, to_unit: Union[str, Any]) -> float:
        """
        Convert a value from this field's unit to a target unit.
        
        Args:
            value: The value to convert
            to_unit: Target unit (pint.Unit or string)
        
        Returns:
            Converted value as float
        
        Example:
            >>> field = Field("B", "B", "tesla")
            >>> field.convert(1.5, "gauss")
            15000.0
        """
        if isinstance(to_unit, str):
            to_unit = ureg(to_unit)
        
        quantity = ureg.Quantity(value, self.unit)
        return quantity.to(to_unit).magnitude
    
    def convert_array(self, values: List[float], 
                     to_unit: Union[str, Any]) -> List[float]:
        """
        Convert an array of values to a target unit.
        
        Args:
            values: List of values to convert
            to_unit: Target unit
        
        Returns:
            List of converted values
        """
        return [self.convert(v, to_unit) for v in values]
    
    def validate_value(self, value: Any) -> bool:
        """
        Check if a value is compatible with this field's unit.
        
        Args:
            value: Value to validate
        
        Returns:
            True if value can be represented in this field's unit
        """
        try:
            ureg.Quantity(value, self.unit)
            return True
        except (ValueError, TypeError):
            return False
    
    def format_label(self, target_unit: Optional[Union[str, Any]] = None, 
                    use_latex: bool = False) -> str:
        """
        Generate a formatted label for plotting.
        
        Args:
            target_unit: Unit to display in label (default: field's unit)
            use_latex: Use LaTeX symbol instead of plain symbol
        
        Returns:
            Formatted string like "B [T]" or "$B$ [G]"
        
        Example:
            >>> field = Field("B", "B", "tesla", latex_symbol=r"$B$")
            >>> field.format_label()
            'B [T]'
            >>> field.format_label("gauss", use_latex=True)
            '$B$ [G]'
        """
        sym = self.latex_symbol if use_latex else self.symbol
        
        if target_unit:
            if isinstance(target_unit, str):
                target_unit = ureg(target_unit)
            unit_str = f"{target_unit:~P}"  # Pint pretty print format
            return f"{sym} [{unit_str}]"
        
        return sym
    
    def applies_to_region(self, region: str) -> bool:
        """
        Check if this field is valid in a given region/domain.
        
        Args:
            region: Name of the region (e.g., "Air", "Isolant")
        
        Returns:
            False if region is in exclude_regions, True otherwise
        
        Example:
            >>> field = Field("T", "T", "degC", exclude_regions=["Air"])
            >>> field.applies_to_region("Conductor")
            True
            >>> field.applies_to_region("Air")
            False
        """
        return region not in self.exclude_regions
    
    def to_dict(self, input_unit=None, output_unit=None) -> dict:
        """
        Convert to magnetrun-compatible dictionary format.
        
        This provides backwards compatibility with the old dict-based format:
        {
            "Symbol": str,
            "mSymbol": str,
            "Units": [input_unit, output_unit],
            "Exclude": List[str],
            "Val": Any
        }
        
        Args:
            input_unit: Input unit for conversion (default: field's unit)
            output_unit: Output unit for conversion (default: field's unit)
        
        Returns:
            Dictionary in magnetrun format
        """
        result = {
            "Symbol": self.symbol,
            "Units": [
                input_unit or self.unit,
                output_unit or self.unit
            ],
            "Exclude": self.exclude_regions
        }
        
        # Add LaTeX symbol if different from regular symbol
        if self.latex_symbol != self.symbol:
            result["mSymbol"] = self.latex_symbol
        
        # Add default value if present
        if self.default_value is not None:
            result["Val"] = self.default_value
        
        return result
    
    @classmethod
    def from_dict(cls, name: str, field_dict: dict) -> 'Field':
        """
        Create a Field from magnetrun dictionary format.
        
        Args:
            name: Field name
            field_dict: Dictionary in magnetrun format
        
        Returns:
            Field object
        
        Example:
            >>> field_dict = {
            ...     "Symbol": "B",
            ...     "mSymbol": r"$B$",
            ...     "Units": [ureg.tesla, ureg.tesla],
            ...     "Exclude": []
            ... }
            >>> field = Field.from_dict("MagneticField", field_dict)
        """
        return cls(
            name=name,
            symbol=field_dict["Symbol"],
            unit=field_dict["Units"][0],
            latex_symbol=field_dict.get("mSymbol"),
            exclude_regions=field_dict.get("Exclude", []),
            default_value=field_dict.get("Val")
        )
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return (f"Field(name={self.name!r}, symbol={self.symbol!r}, "
                f"unit={self.unit})")
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.name} ({self.symbol}): {self.unit}"


# Example usage demonstrating the new approach
if __name__ == "__main__":
    # Create a magnetic field
    B_field = Field(
        name="MagneticField",
        symbol="B",
        unit="tesla",
        description="Magnetic flux density",
        latex_symbol=r"$B$",
        aliases=["magnetic_field", "B_field"],
        exclude_regions=[]
    )
    
    print("Field:", B_field)
    print()
    
    # Convert values
    value_tesla = 1.5
    value_gauss = B_field.convert(value_tesla, "gauss")
    print(f"{value_tesla} T = {value_gauss} G")
    print()
    
    # Convert array
    values_tesla = [1.0, 1.5, 2.0]
    values_gauss = B_field.convert_array(values_tesla, "gauss")
    print(f"{values_tesla} T = {values_gauss} G")
    print()
    
    # Format labels for plotting
    print("Plain label:", B_field.format_label("tesla"))
    print("LaTeX label:", B_field.format_label("gauss", use_latex=True))
    print()
    
    # Check region applicability
    temp_field = Field(
        name="Temperature",
        symbol="T",
        unit="degC",
        exclude_regions=["Air", "Vacuum"]
    )
    print(f"Temperature in Conductor: {temp_field.applies_to_region('Conductor')}")
    print(f"Temperature in Air: {temp_field.applies_to_region('Air')}")
    print()
    
    # Backwards compatibility - convert to dict
    field_dict = B_field.to_dict()
    print("As dict:", field_dict)
    print()
    
    # Reconstruct from dict
    B_field_reconstructed = Field.from_dict("MagneticField", field_dict)
    print("Reconstructed:", B_field_reconstructed)
