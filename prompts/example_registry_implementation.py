"""
Example implementation of FieldRegistry for field-framework package.
Demonstrates centralized field management and lookup.
"""

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from example_field_implementation import Field, ureg


class FieldRegistry:
    """
    Central registry for field definitions with multiple lookup methods.
    
    Supports:
    - Lookup by name (primary key)
    - Lookup by symbol
    - Lookup by alias
    - Category filtering
    - Custom predicates
    
    Example:
        >>> registry = FieldRegistry()
        >>> registry.register(Field("MagneticField", "B", "tesla"))
        >>> field = registry.get("MagneticField")  # By name
        >>> field = registry.get("B")              # By symbol
    """
    
    def __init__(self):
        # Primary storage
        self._fields: Dict[str, Field] = {}
        
        # Secondary indices for fast lookup
        self._by_symbol: Dict[str, Field] = {}
        self._by_alias: Dict[str, List[Field]] = {}
        self._by_category: Dict[str, List[Field]] = {}
    
    def register(self, field: Field) -> None:
        """
        Register a field in the registry.
        
        Args:
            field: Field to register
        
        Raises:
            ValueError: If a field with the same name already exists
        
        Example:
            >>> registry = FieldRegistry()
            >>> field = Field("Temperature", "T", "degC")
            >>> registry.register(field)
        """
        # Check for duplicate names
        if field.name in self._fields:
            raise ValueError(f"Field '{field.name}' already registered")
        
        # Store in primary dict
        self._fields[field.name] = field
        
        # Index by symbol
        if field.symbol in self._by_symbol:
            # Warning: symbol collision
            print(f"Warning: Symbol '{field.symbol}' used by multiple fields")
        self._by_symbol[field.symbol] = field
        
        # Index by aliases
        for alias in field.aliases:
            if alias not in self._by_alias:
                self._by_alias[alias] = []
            self._by_alias[alias].append(field)
        
        # Index by category (if present in metadata)
        category = field.metadata.get('category')
        if category:
            if category not in self._by_category:
                self._by_category[category] = []
            self._by_category[category].append(field)
    
    def get(self, identifier: str) -> Optional[Field]:
        """
        Get a field by name, symbol, or alias.
        
        Lookup priority:
        1. Name (exact match)
        2. Symbol (exact match)
        3. Alias (if unambiguous)
        
        Args:
            identifier: Field name, symbol, or alias
        
        Returns:
            Field if found, None otherwise
        
        Example:
            >>> registry.get("MagneticField")      # By name
            >>> registry.get("B")                  # By symbol
            >>> registry.get("magnetic_field")     # By alias
        """
        # Try name lookup (highest priority)
        if identifier in self._fields:
            return self._fields[identifier]
        
        # Try symbol lookup
        if identifier in self._by_symbol:
            return self._by_symbol[identifier]
        
        # Try alias lookup
        if identifier in self._by_alias:
            matches = self._by_alias[identifier]
            if len(matches) == 1:
                return matches[0]
            elif len(matches) > 1:
                # Ambiguous alias
                field_names = [f.name for f in matches]
                print(f"Warning: Alias '{identifier}' matches multiple fields: "
                      f"{field_names}")
                return None
        
        return None
    
    def get_or_raise(self, identifier: str) -> Field:
        """
        Get a field or raise an exception if not found.
        
        Args:
            identifier: Field name, symbol, or alias
        
        Returns:
            Field object
        
        Raises:
            KeyError: If field not found
        """
        field = self.get(identifier)
        if field is None:
            raise KeyError(f"Field '{identifier}' not found in registry")
        return field
    
    def list_fields(self, 
                   category: Optional[str] = None,
                   predicate: Optional[Callable[[Field], bool]] = None) -> List[Field]:
        """
        List all fields, optionally filtered.
        
        Args:
            category: Filter by category (from metadata)
            predicate: Custom filter function
        
        Returns:
            List of matching fields
        
        Example:
            >>> # All fields
            >>> registry.list_fields()
            >>> # Electromagnetic fields only
            >>> registry.list_fields(category="electromagnetic")
            >>> # Fields with units in tesla
            >>> registry.list_fields(
            ...     predicate=lambda f: str(f.unit) == "tesla"
            ... )
        """
        fields = list(self._fields.values())
        
        # Filter by category
        if category:
            if category in self._by_category:
                fields = self._by_category[category]
            else:
                fields = []
        
        # Apply custom predicate
        if predicate:
            fields = [f for f in fields if predicate(f)]
        
        return fields
    
    def list_categories(self) -> List[str]:
        """
        Get list of all categories.
        
        Returns:
            List of category names
        """
        return list(self._by_category.keys())
    
    def bulk_register(self, fields: List[Field]) -> None:
        """
        Register multiple fields at once.
        
        Args:
            fields: List of fields to register
        
        Example:
            >>> fields = [
            ...     Field("B", "B", "tesla"),
            ...     Field("E", "E", "V/m"),
            ...     Field("J", "J", "A/m^2")
            ... ]
            >>> registry.bulk_register(fields)
        """
        for field in fields:
            try:
                self.register(field)
            except ValueError as e:
                print(f"Skipping: {e}")
    
    def unregister(self, name: str) -> bool:
        """
        Remove a field from the registry.
        
        Args:
            name: Name of field to remove
        
        Returns:
            True if field was removed, False if not found
        """
        if name not in self._fields:
            return False
        
        field = self._fields[name]
        
        # Remove from all indices
        del self._fields[name]
        
        if field.symbol in self._by_symbol:
            del self._by_symbol[field.symbol]
        
        for alias in field.aliases:
            if alias in self._by_alias:
                self._by_alias[alias].remove(field)
                if not self._by_alias[alias]:
                    del self._by_alias[alias]
        
        category = field.metadata.get('category')
        if category and category in self._by_category:
            self._by_category[category].remove(field)
            if not self._by_category[category]:
                del self._by_category[category]
        
        return True
    
    def clear(self) -> None:
        """Remove all fields from the registry."""
        self._fields.clear()
        self._by_symbol.clear()
        self._by_alias.clear()
        self._by_category.clear()
    
    def __len__(self) -> int:
        """Return number of registered fields."""
        return len(self._fields)
    
    def __contains__(self, identifier: str) -> bool:
        """Check if a field exists (by name, symbol, or alias)."""
        return self.get(identifier) is not None
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"FieldRegistry({len(self)} fields)"
    
    def summary(self) -> str:
        """
        Get a human-readable summary of the registry.
        
        Returns:
            Multi-line string with registry statistics
        """
        lines = [
            f"FieldRegistry Summary:",
            f"  Total fields: {len(self._fields)}",
            f"  Categories: {len(self._by_category)}",
        ]
        
        if self._by_category:
            lines.append("  Fields by category:")
            for cat, fields in sorted(self._by_category.items()):
                lines.append(f"    {cat}: {len(fields)}")
        
        return "\n".join(lines)


# Create global default registry (similar to pint's UnitRegistry)
default_registry = FieldRegistry()


def create_electromagnetic_fields() -> List[Field]:
    """
    Create standard electromagnetic fields.
    
    Returns:
        List of electromagnetic Field objects
    """
    return [
        Field(
            name="MagneticField",
            symbol="B",
            unit=ureg.tesla,
            description="Magnetic flux density",
            latex_symbol=r"$B$",
            aliases=["magnetic_field", "B_field"],
            metadata={"category": "electromagnetic", "physics": "magnetism"}
        ),
        Field(
            name="MagneticField_x",
            symbol="Bx",
            unit=ureg.tesla,
            description="Magnetic field x-component",
            latex_symbol=r"$B_x$",
            aliases=["Bx", "B_x"],
            metadata={"category": "electromagnetic", "component": "x"}
        ),
        Field(
            name="MagneticField_y",
            symbol="By",
            unit=ureg.tesla,
            description="Magnetic field y-component",
            latex_symbol=r"$B_y$",
            aliases=["By", "B_y"],
            metadata={"category": "electromagnetic", "component": "y"}
        ),
        Field(
            name="MagneticField_z",
            symbol="Bz",
            unit=ureg.tesla,
            description="Magnetic field z-component",
            latex_symbol=r"$B_z$",
            aliases=["Bz", "B_z"],
            metadata={"category": "electromagnetic", "component": "z"}
        ),
        Field(
            name="ElectricField",
            symbol="E",
            unit=ureg.volt / ureg.meter,
            description="Electric field intensity",
            latex_symbol=r"$E$",
            aliases=["electric_field", "E_field"],
            exclude_regions=["Air", "Isolant"],
            metadata={"category": "electromagnetic", "physics": "electricity"}
        ),
        Field(
            name="CurrentDensity",
            symbol="J",
            unit=ureg.ampere / ureg.meter**2,
            description="Current density",
            latex_symbol=r"$J$",
            aliases=["current_density", "J_current"],
            exclude_regions=["Air", "Isolant"],
            metadata={"category": "electromagnetic", "physics": "electricity"}
        ),
    ]


def create_thermal_fields() -> List[Field]:
    """Create standard thermal fields."""
    return [
        Field(
            name="Temperature",
            symbol="T",
            unit=ureg.kelvin,
            description="Temperature",
            latex_symbol=r"$T$",
            aliases=["temperature", "temp"],
            exclude_regions=["Air"],
            metadata={"category": "thermal"}
        ),
        Field(
            name="ThermalConductivity",
            symbol="k",
            unit=ureg.watt / ureg.meter / ureg.kelvin,
            description="Thermal conductivity",
            latex_symbol=r"$k$",
            aliases=["thermal_conductivity", "k_thermal"],
            exclude_regions=["Air"],
            metadata={"category": "thermal"}
        ),
    ]


# Example usage
if __name__ == "__main__":
    # Create registry
    registry = FieldRegistry()
    
    # Register electromagnetic fields
    em_fields = create_electromagnetic_fields()
    registry.bulk_register(em_fields)
    
    # Register thermal fields
    thermal_fields = create_thermal_fields()
    registry.bulk_register(thermal_fields)
    
    print(registry.summary())
    print()
    
    # Lookup examples
    print("=== Lookup Examples ===")
    
    # By name
    field = registry.get("MagneticField")
    print(f"By name: {field}")
    
    # By symbol
    field = registry.get("B")
    print(f"By symbol: {field}")
    
    # By alias
    field = registry.get("magnetic_field")
    print(f"By alias: {field}")
    
    print()
    
    # List by category
    print("=== Electromagnetic Fields ===")
    em_fields = registry.list_fields(category="electromagnetic")
    for field in em_fields:
        print(f"  - {field.name} ({field.symbol}): {field.unit}")
    
    print()
    
    # Custom filtering
    print("=== Fields excluding 'Air' ===")
    air_excluded = registry.list_fields(
        predicate=lambda f: "Air" in f.exclude_regions
    )
    for field in air_excluded:
        print(f"  - {field.name}")
    
    print()
    
    # Demonstrate field usage
    print("=== Field Usage ===")
    B_field = registry.get("MagneticField")
    value = 1.5  # Tesla
    converted = B_field.convert(value, "gauss")
    print(f"{value} {B_field.unit} = {converted} G")
    
    label = B_field.format_label("gauss", use_latex=True)
    print(f"Plot label: {label}")
