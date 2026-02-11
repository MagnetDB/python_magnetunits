"""
Basic usage example for python_magnetunits.

This example demonstrates:
1. Creating and using standard fields
2. Custom field definitions
3. Unit conversions
4. Field registry operations
5. Label formatting for plots
"""

from python_magnetunits import Field, FieldRegistry, ureg
from python_magnetunits.physics import electromagnetic


def example_standard_fields():
    """Example: Using standard electromagnetic fields."""
    print("=" * 60)
    print("Example 1: Standard Electromagnetic Fields")
    print("=" * 60)

    # Create a registry and register standard fields
    registry = FieldRegistry()
    electromagnetic.register_electromagnetic_fields(registry)

    # Access fields by different identifiers
    B = registry.get("MagneticField")  # By name
    if B is None:
        print("ERROR: MagneticField not found!")
        return

    B_symbol = registry.get("B")  # By symbol
    B_alias = registry.get("magnetic_field")  # By alias

    print(f"\nLooked up field multiple ways:")
    print(f"  By name: {B}")
    print(f"  By symbol: {B_symbol}")
    print(f"  By alias: {B_alias}")

    # Convert values
    print(f"\nUnit conversions:")
    print(f"  1.5 Tesla = {B.convert(1.5, 'millitesla')} mT")
    print(f"  1.5 Tesla = {B.convert(1.5, 'microtesla')} µT")

    # Format labels for plots
    print(f"\nFormatted labels for plots:")
    print(f"  Plain: {B.format_label('millitesla', use_latex=False)}")
    print(f"  LaTeX: {B.format_label('millitesla', use_latex=True)}")

    # Get field components
    print(f"\nField components:")
    for axis in ["x", "y", "z"]:
        field_name = f"MagneticField_{axis}"
        component = registry.get(field_name)
        if component:
            print(f"  {component.symbol}: {component.latex_symbol}")


def example_custom_fields():
    """Example: Defining custom fields."""
    print("\n" + "=" * 60)
    print("Example 2: Custom Field Definitions")
    print("=" * 60)

    # Define custom fields
    temperature = Field(
        name="Temperature",
        symbol="T",
        unit=ureg.kelvin,
        description="Absolute temperature",
        latex_symbol=r"$T$",
        aliases=["temp", "T_abs"],
        metadata={"category": "thermal"},
    )

    pressure = Field(
        name="Pressure",
        symbol="P",
        unit=ureg.pascal,
        description="Pressure",
        latex_symbol=r"$P$",
        aliases=["press"],
        # FIXED: Changed category from "mechanical" to "hydraulics"
        metadata={"category": "hydraulics"},
    )

    # Register custom fields
    registry = FieldRegistry()
    registry.register(temperature)
    registry.register(pressure)

    print(f"\nRegistered {len(registry)} custom fields")

    # Use custom fields
    T = registry.get("Temperature")
    if T is None:
        print("ERROR: Temperature not found!")
        return

    print(f"\nTemperature conversions:")
    print(f"  273.15 K = {T.convert(273.15, 'degC')} °C")
    print(f"  300 K = {T.convert(300, 'degF'):.1f} °F")

    # List fields
    print(f"\nAll registered fields:")
    for field in registry.list_fields():
        print(f"  - {field.name} ({field.symbol}): {field.unit}")


def example_array_operations():
    """Example: Working with arrays of values."""
    print("\n" + "=" * 60)
    print("Example 3: Array Conversions")
    print("=" * 60)

    B = Field(name="B", symbol="B", unit="tesla")

    # Convert array of values
    values_tesla = [0.5, 1.0, 1.5, 2.0]
    values_millitesla = B.convert_array(values_tesla, "millitesla")

    print(f"\nMagnetic field values:")
    print(f"  Tesla:       {values_tesla}")
    print(f"  millitesla:  {[f'{v:.0f}' for v in values_millitesla]}")

    # Validate values
    print(f"\nValue validation:")
    test_values = [1.5, "invalid", None, 0.0]
    for val in test_values:
        is_valid = B.validate_value(val)
        print(f"  {str(val):20} -> valid: {is_valid}")


def example_registry_operations():
    """Example: Registry operations."""
    print("\n" + "=" * 60)
    print("Example 4: Registry Operations")
    print("=" * 60)

    registry = FieldRegistry()

    # Create fields
    fields = [
        Field(
            name="MagneticField",
            symbol="B",
            unit="tesla",
            aliases=["B_field"],
            metadata={"category": "electromagnetic"},
        ),
        Field(
            name="ElectricField",
            symbol="E",
            unit="volt/meter",
            aliases=["E_field"],
            metadata={"category": "electromagnetic"},
        ),
        Field(
            name="Temperature",
            symbol="T",
            unit="kelvin",
            aliases=["temp"],
            metadata={"category": "thermal"},
        ),
    ]

    # Bulk register
    registry.bulk_register(fields)
    print(f"Registered {len(registry)} fields")

    # List all fields
    print(f"\nAll fields: {[f.name for f in registry.list_fields()]}")

    # List by category
    em_fields = registry.list_fields(category="electromagnetic")
    thermal_fields = registry.list_fields(category="thermal")
    print(f"Electromagnetic fields: {[f.name for f in em_fields]}")
    print(f"Thermal fields: {[f.name for f in thermal_fields]}")

    # Check containment
    print(f"\nContainment checks:")
    print(f"  'B' in registry: {'B' in registry}")
    print(f"  'B_field' in registry: {'B_field' in registry}")
    print(f"  'NonExistent' in registry: {'NonExistent' in registry}")

    # Remove field
    print(f"\nRemoving 'Temperature'...")
    registry.remove("Temperature")
    print(f"Registry now has {len(registry)} fields")


def example_region_exclusion():
    """Example: Region exclusion logic."""
    print("\n" + "=" * 60)
    print("Example 5: Region Exclusion")
    print("=" * 60)

    # Field valid everywhere except in vacuum
    B = Field(
        name="MagneticField",
        symbol="B",
        unit="tesla",
        exclude_regions=["vacuum", "space"],
    )

    test_regions = ["air", "water", "conductor", "vacuum", "space"]
    print(f"\nField applies to regions:")
    for region in test_regions:
        applies = B.applies_to_region(region)
        status = "✓" if applies else "✗"
        print(f"  {status} {region}")


def example_advanced_formatting():
    """Example: Advanced label formatting."""
    print("\n" + "=" * 60)
    print("Example 6: Advanced Label Formatting")
    print("=" * 60)

    fields = [
        Field(
            name="MagneticField",
            symbol="B",
            unit=ureg.tesla,
            latex_symbol=r"$\vec{B}$",
        ),
        Field(
            name="ElectricField",
            symbol="E",
            unit=ureg.volt / ureg.meter,
            latex_symbol=r"$\vec{E}$",
        ),
        Field(
            name="CurrentDensity",
            symbol="J",
            unit=ureg.ampere / ureg.meter**2,
            latex_symbol=r"$\vec{J}$",
        ),
    ]

    print(f"\nLabel formatting for matplotlib/LaTeX:")
    for field in fields:
        units = ["tesla" if "tesla" in str(field.unit) else str(field.unit)]
        unit = units[0]

        # Different formatting options
        label_plain = field.format_label(use_latex=False)
        label_unit = field.format_label(unit, use_latex=False)
        label_latex = field.format_label(unit, use_latex=True)

        print(f"\n  {field.name}:")
        print(f"    Plain:     {label_plain}")
        print(f"    With unit: {label_unit}")
        print(f"    LaTeX:     {label_latex}")


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  python_magnetunits - Usage Examples".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")

    example_standard_fields()
    example_custom_fields()
    example_array_operations()
    example_registry_operations()
    example_region_exclusion()
    example_advanced_formatting()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
