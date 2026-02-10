# field_framework/field.py
from pint import UnitRegistry
from typing import Optional, List, Any
from dataclasses import dataclass, field as dc_field

ureg = UnitRegistry()

@dataclass
class Field:
    """
    Represents a physical field with units, symbols, and metadata.
    
    Attributes:
        name: Unique identifier for the field (e.g., "MagneticField")
        symbol: Short symbol for display (e.g., "B")
        unit: Pint unit or unit string
        description: Optional human-readable description
        latex_symbol: Optional LaTeX representation (e.g., r"$B$")
        aliases: Alternative names for this field
        exclude_regions: Regions where this field doesn't apply
        default_value: Optional default value
        metadata: Additional custom metadata
    """
    name: str
    symbol: str
    unit: Any  # pint.Unit or str
    description: Optional[str] = None
    latex_symbol: Optional[str] = None
    aliases: List[str] = dc_field(default_factory=list)
    exclude_regions: List[str] = dc_field(default_factory=list)
    default_value: Optional[Any] = None
    metadata: dict = dc_field(default_factory=dict)
    
    def __post_init__(self):
        """Convert string units to pint Units"""
        if isinstance(self.unit, str):
            self.unit = ureg(self.unit)
        if self.latex_symbol is None:
            self.latex_symbol = self.symbol
    
    def convert(self, value, to_unit):
        """Convert value from this field's unit to target unit"""
        quantity = ureg.Quantity(value, self.unit)
        return quantity.to(to_unit).magnitude
    
    def convert_array(self, values, to_unit):
        """Convert array of values"""
        return [self.convert(v, to_unit) for v in values]
    
    def validate_value(self, value) -> bool:
        """Check if value is compatible with field's unit"""
        try:
            ureg.Quantity(value, self.unit)
            return True
        except:
            return False
    
    def format_label(self, target_unit=None, use_latex=False) -> str:
        """Generate formatted label for plotting"""
        sym = self.latex_symbol if use_latex else self.symbol
        if target_unit:
            unit_str = f"{target_unit:~P}"  # Pint pretty format
            return f"{sym} [{unit_str}]"
        return sym
    
    def applies_to_region(self, region: str) -> bool:
        """Check if field is valid in given region"""
        return region not in self.exclude_regions


