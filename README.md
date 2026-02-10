# field-framework

Generic field and unit management for scientific computing with Python.

## Features

- ✨ Type-safe field definitions with pint units
- 🔍 Field registry with name/symbol/alias lookup
- 🔄 Automatic unit conversion
- 📊 Plot label generation
- 🎯 Region/domain exclusions
- 🔌 Extensible standard field library
- 🔙 Backwards compatibility with dict-based formats

## Quick Start

\`\`\`python
from field_framework import Field, FieldRegistry, ureg

# Define a field
B_field = Field(
    name="MagneticField",
    symbol="B",
    unit=ureg.tesla,
    latex_symbol=r"$B$"
)

# Use it
value_in_gauss = B_field.convert(1.5, "gauss")  # 15000.0
label = B_field.format_label("gauss", use_latex=True)  # "$B$ [G]"

# Registry
registry = FieldRegistry()
registry.register(B_field)
field = registry.get("MagneticField")  # or "B" or any alias
\`\`\`

## Installation

\`\`\`bash
pip install field-framework
\`\`\`

## Documentation

Full documentation: https://field-framework.readthedocs.io

## License

MIT License
