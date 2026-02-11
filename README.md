# python_magnetunits

**Shared field and unit management for scientific computing with Python**

A robust, type-safe Python package for managing physical fields and units across scientific computing applications. Provides centralized field definitions, flexible lookup registries, and seamless unit conversion using the industry-standard `pint` library.

## Features

✨ **Type-Safe Field Definitions**
- Strongly-typed `Field` class with integrated unit management
- LaTeX symbol support for publication-quality plots
- Comprehensive field metadata and domain-specific extensions

🔍 **Flexible Field Registry**
- Lookup fields by name, symbol, or custom aliases
- Support for hierarchical field organization
- List and filter fields by category

🔄 **Unit Conversion & Validation**
- Seamless unit conversion using pint
- Single values and array conversion
- Unit compatibility checking
- Value validation against field definitions

📊 **Plot Integration**
- Automatic formatted label generation
- LaTeX symbol support
- Integration with matplotlib and scientific visualization

🎯 **Domain Exclusions**
- Mark fields as invalid in specific regions/domains
- Essential for multi-domain simulations

🔌 **Extensible Standard Library**
- Pre-defined electromagnetic fields
- Easy to add custom field definitions
- Namespace organization by physical domain

🔙 **Backwards Compatible**
- Compatibility helpers for dict-based field definitions
- Gradual migration path from legacy systems
- Works with existing magnetrun infrastructure

## Installation

```bash
pip install python_magnetunits
```

### Requirements

- Python 3.9+
- pint >= 0.20

## Quick Start

### Basic Usage with Standard Fields

```python
from python_magnetunits import FieldRegistry
from python_magnetunits.physics import electromagnetic

# Create a registry and register standard electromagnetic fields
registry = FieldRegistry()
electromagnetic.register_electromagnetic_fields(registry)

# Get a field by name, symbol, or alias
B_field = registry.get("MagneticField")  # or "B" or "magnetic_field"

# Convert values
value_in_gauss = B_field.convert(1.5, "gauss")  # 15000.0

# Generate formatted labels for plots
label = B_field.format_label("gauss", use_latex=True)  # "$B$ [G]"
```

### Custom Field Definitions

```python
from python_magnetunits import Field, FieldRegistry, ureg

# Define a custom field
temperature = Field(
    name="Temperature",
    symbol="T",
    unit=ureg.kelvin,
    description="Absolute temperature",
    latex_symbol=r"$T$",
    aliases=["temp", "T_absolute"],
    metadata={"category": "thermal"},
)

# Register it
registry = FieldRegistry()
registry.register(temperature)

# Use it
temp_celsius = temperature.convert(273.15, "degC")  # 0.0
label = temperature.format_label("degC")  # "T [°C]"
```

### Working with Field Arrays

```python
from python_magnetunits import Field, ureg

field = Field(name="B", symbol="B", unit="tesla")

# Convert arrays of values
values_tesla = [1.0, 2.0, 3.0]
values_gauss = field.convert_array(values_tesla, "gauss")
# [10000.0, 20000.0, 30000.0]
```

### Backwards Compatibility

```python
from python_magnetunits import convert_data, ureg

# Works with magnetrun-style field_units dict
field_units = {
    "MagneticField": [ureg.tesla, ureg.gauss],
    "Temperature": [ureg.kelvin, ureg.degC],
}

# Single value
B_gauss = convert_data(field_units, 1.5, "MagneticField")  # 15000.0

# Arrays
values_gauss = convert_data(field_units, [1.0, 2.0], "MagneticField")
# [10000.0, 20000.0]
```

## Core Components

### Field Class

Represents a physical field with units, symbols, and metadata.

```python
Field(
    name: str,                    # Unique identifier
    symbol: str,                  # Display symbol
    unit: Union[str, Unit],       # pint unit
    description: Optional[str],   # Human-readable description
    latex_symbol: Optional[str],  # LaTeX representation
    aliases: List[str],           # Alternative names
    exclude_regions: List[str],   # Regions where field doesn't apply
    default_value: Optional[float],
    metadata: Dict[str, Any],     # Custom metadata
)
```

**Key Methods:**
- `convert(value, to_unit)` - Convert value to different unit
- `convert_array(values, to_unit)` - Convert array of values
- `validate_value(value)` - Check if value is compatible
- `format_label(target_unit, use_latex)` - Generate plot label
- `applies_to_region(region)` - Check if field applies to region

### FieldRegistry

Central registry for field definitions with flexible lookup.

```python
registry = FieldRegistry()

# Registration
registry.register(field)                          # Single field
registry.bulk_register(fields_list)               # Multiple fields

# Lookup (supports name, symbol, or alias)
field = registry.get("identifier")                # Returns Field or None

# Listing
all_fields = registry.list_fields()               # All fields
em_fields = registry.list_fields(category="electromagnetic")  # Filtered

# Utility
has_field = registry.has_field("identifier")      # Boolean check
removed = registry.remove("field_name")           # Remove field
count = len(registry)                             # Number of fields
contains = "B" in registry                        # Containment check
```

### Conversion Functions

```python
from python_magnetunits import (
    convert_data,          # Dict-based conversion (backwards compatible)
    convert_value,         # Single value conversion
    convert_array,         # Array conversion
    get_unit_string,       # Format unit as string
    are_compatible,        # Check unit compatibility
)
```

## Standard Fields

### Electromagnetic Fields

Pre-defined fields for electromagnetic simulations:

- `MagneticField` (B, Tesla)
  - Components: `MagneticField_x`, `MagneticField_y`, `MagneticField_z`
- `ElectricField` (E, Volt/meter)
  - Components: `ElectricField_x`, `ElectricField_y`, `ElectricField_z`
- `CurrentDensity` (J, Ampere/meter²)
  - Components: `CurrentDensity_x`, `CurrentDensity_y`, `CurrentDensity_z`
- `Potential` (V, Volt)
- `Conductivity` (σ, Siemens/meter)
- `Permeability` (μ, Henry/meter)
- `RelativePermeability` (μ_r, dimensionless)
- `RelativePermittivity` (ε_r, dimensionless)

```python
from python_magnetunits import FieldRegistry
from python_magnetunits.physics import electromagnetic

registry = FieldRegistry()
electromagnetic.register_electromagnetic_fields(registry)

# Access predefined fields
B = registry.get("MagneticField")
B_x = registry.get("MagneticField_x")
E = registry.get("ElectricField")
```

## Integration Examples

### With magnetrun

```python
from field_framework import FieldRegistry
from field_framework.physics import electromagnetic

# Setup fields
registry = FieldRegistry()
electromagnetic.register_electromagnetic_fields(registry)

# Use in your code
field = registry.get("MagneticField")
converted = field.convert(data, output_unit)
```

### With python_hifimagnetparaview

```python
from python_magnetunits import FieldRegistry
from python_magnetunits.physics import electromagnetic

# Setup
registry = FieldRegistry()
electromagnetic.register_electromagnetic_fields(registry)

# In plotting functions
def plot_field(data, field_name, output_unit):
    field = registry.get(field_name)
    converted = field.convert_array(data, output_unit)
    label = field.format_label(output_unit, use_latex=True)
    
    plt.plot(converted)
    plt.ylabel(label)
```

## Architecture

```
python_magnetunits/
├── field.py              # Core Field class
├── registry.py           # FieldRegistry for management
├── converters.py         # Unit conversion utilities
└── physics/
    ├── electromagnetic.py # EM field definitions
    └── ...               # More domains
```

## Design Philosophy

- **Type Safety**: Leverage Python's type system for better IDE support and error catching
- **Flexibility**: Support multiple lookup methods (name, symbol, alias)
- **Simplicity**: Clean API without unnecessary complexity
- **Extensibility**: Easy to add custom fields and domains
- **Compatibility**: Maintain backwards compatibility with existing dict-based systems
- **Maintainability**: Single source of truth for field definitions

## Testing

Run the comprehensive test suite:

```bash
# With pytest
pytest tests/

# With coverage
pytest tests/ --cov=python_magnetunits

# Specific test file
pytest tests/test_field.py -v
```

Tests cover:
- Field creation and initialization
- Unit conversion (single values and arrays)
- Value validation
- Label formatting with LaTeX support
- Registry registration and lookup
- Filter and list operations
- Backwards compatibility
- Error handling

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Add tests for new functionality
4. Ensure all tests pass (`pytest`)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/python_magnetunits.git
cd python_magnetunits

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .

# Type checking
mypy python_magnetunits
```

## Roadmap

### v0.2.0 (Planned)
- [ ] Additional standard field domains (thermal, mechanical, flow)
- [ ] JSON/YAML field definition import/export
- [ ] Field templates for common domain configurations
- [ ] Enhanced documentation with Sphinx

### v0.3.0 (Planned)
- [ ] Field derived calculations
- [ ] Field interpolation utilities
- [ ] Integration with xarray/pandas
- [ ] GUI for field management

### v1.0.0 (Planned)
- [ ] Stable API
- [ ] Comprehensive documentation
- [ ] Production-ready error handling
- [ ] Performance optimizations

## License

MIT License - See LICENSE file for details

## Citation

If you use python_magnetunits in your research, please cite:

```bibtex
@software{python_magnetunits_2024,
  title = {python_magnetunits: Shared field and unit management for scientific computing},
  author = {Christophe},
  year = {2024},
  url = {https://github.com/yourusername/python_magnetunits},
  version = {0.1.0},
}
```

## Support

- 📚 **Documentation**: [Read the Docs](https://python-magnetunits.readthedocs.io)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/python_magnetunits/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/python_magnetunits/discussions)

## Related Projects

- [pint](https://github.com/hgrecco/pint) - Units and quantities library
- [magnetrun](https://github.com/yourusername/magnetrun) - Magnetic field simulation
- [python_hifimagnetparaview](https://github.com/yourusername/python_hifimagnetparaview) - Visualization

---

**Made with ❤️ for scientific computing**
