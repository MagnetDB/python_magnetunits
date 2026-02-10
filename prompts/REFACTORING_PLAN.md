# Field Framework Extraction - Refactoring Plan

## Executive Summary

Extract field and unit management logic from `magnetrun` into a standalone Python package `field-framework` (or `sci-fields`, `physics-fields`, etc.) to enable reuse across multiple projects including `python_hifimagnetparaview`.

---

## Current Architecture Analysis

### Current State in magnetrun

**Files to Extract:**
- `magnetrun/core/fields/utils.py` - Field utilities
- `magnetrun/core/fields/field.py` - Core Field class
- Uses `pint` for unit management

**Files to Keep:**
- `magnetrun/formats/format_definition.py` - Format-specific mappings

### Current Usage Pattern (from python_hifimagnetparaview)

The uploaded files show how fields are currently used:

```python
# From method3D.py
fieldunits = {
    "MagneticField": {
        "Symbol": "B",
        "mSymbol": r"$B$",  # matplotlib/LaTeX
        "Units": [ureg.tesla, ureg.tesla],  # [input_unit, output_unit]
        "Exclude": [],  # domains to exclude
        "Val": value  # optional actual value
    },
    # ... many more fields
}

# From plot.py - Usage pattern
symbol = fieldunits[fieldname]["Symbol"]
[in_unit, out_unit] = fieldunits[fieldname]["Units"]
out_values = convert_data(units, values, fieldname)
```

**Key Requirements Identified:**
1. Field definition with symbol, units, optional LaTeX symbol
2. Unit conversion using pint
3. Domain/region exclusions
4. Easy lookup by field name
5. Support for vector components (x, y, z, r, θ)
6. Extensibility for domain-specific fields

---

## Phase 1: Design the Standalone Package

### 1.1 Package Structure

```
field-framework/
├── pyproject.toml
├── README.md
├── LICENSE
├── docs/
│   ├── index.md
│   ├── quickstart.md
│   ├── api_reference.md
│   └── examples.md
├── field_framework/
│   ├── __init__.py
│   ├── field.py           # Core Field class
│   ├── registry.py        # FieldRegistry for lookups
│   ├── utils.py           # Utility functions
│   ├── validators.py      # Validation logic
│   ├── converters.py      # Unit conversion helpers
│   └── standard_fields/
│       ├── __init__.py
│       ├── electromagnetic.py
│       ├── thermal.py
│       ├── mechanical.py
│       └── flow.py
├── tests/
│   ├── __init__.py
│   ├── test_field.py
│   ├── test_registry.py
│   ├── test_converters.py
│   └── test_integration.py
└── examples/
    ├── basic_usage.py
    ├── custom_fields.py
    └── integration_example.py
```

### 1.2 Core API Design

```python
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


# field_framework/registry.py
from typing import Dict, List, Optional
from .field import Field

class FieldRegistry:
    """
    Central registry for field definitions.
    Supports lookup by name, symbol, or alias.
    """
    def __init__(self):
        self._fields: Dict[str, Field] = {}
        self._by_symbol: Dict[str, Field] = {}
        self._by_alias: Dict[str, List[Field]] = {}
    
    def register(self, field: Field):
        """Register a field"""
        self._fields[field.name] = field
        self._by_symbol[field.symbol] = field
        for alias in field.aliases:
            if alias not in self._by_alias:
                self._by_alias[alias] = []
            self._by_alias[alias].append(field)
    
    def get(self, identifier: str) -> Optional[Field]:
        """Get field by name, symbol, or alias"""
        # Try direct name lookup
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
            # Ambiguous - return None and let caller handle
        return None
    
    def list_fields(self, category: Optional[str] = None) -> List[Field]:
        """List all registered fields, optionally filtered by category"""
        fields = list(self._fields.values())
        if category:
            fields = [f for f in fields if f.metadata.get('category') == category]
        return fields
    
    def bulk_register(self, fields: List[Field]):
        """Register multiple fields at once"""
        for field in fields:
            self.register(field)

# Global registry instance
default_registry = FieldRegistry()


# field_framework/converters.py
from typing import Dict, List, Union, Any
from .field import Field, ureg

def convert_data(field_units: Dict[str, List], values: Union[List, Any], 
                 fieldname: str) -> Union[List, Any]:
    """
    Convert values from input unit to output unit.
    
    Compatible with existing magnetrun usage pattern:
    field_units = {"fieldname": [input_unit, output_unit]}
    
    Args:
        field_units: Dict mapping field names to [input_unit, output_unit]
        values: Single value or list of values to convert
        fieldname: Name of the field
    
    Returns:
        Converted value(s) in output unit
    """
    if fieldname not in field_units:
        return values
    
    input_unit, output_unit = field_units[fieldname]
    
    is_list = isinstance(values, list)
    vals = values if is_list else [values]
    
    converted = []
    for val in vals:
        quantity = ureg.Quantity(val, input_unit)
        converted.append(quantity.to(output_unit).magnitude)
    
    return converted if is_list else converted[0]


# field_framework/standard_fields/electromagnetic.py
from ..field import Field, ureg
from ..registry import default_registry

# Define standard electromagnetic fields
ELECTROMAGNETIC_FIELDS = [
    Field(
        name="MagneticField",
        symbol="B",
        unit=ureg.tesla,
        description="Magnetic flux density",
        latex_symbol=r"$B$",
        aliases=["magnetic_field", "B"],
        metadata={"category": "electromagnetic"}
    ),
    Field(
        name="MagneticField_x",
        symbol="Bx",
        unit=ureg.tesla,
        description="Magnetic field x-component",
        latex_symbol=r"$B_x$",
        aliases=["Bx"],
        metadata={"category": "electromagnetic", "component": "x"}
    ),
    # ... more fields
]

def register_electromagnetic_fields():
    """Register all electromagnetic fields with default registry"""
    default_registry.bulk_register(ELECTROMAGNETIC_FIELDS)
```

### 1.3 Compatibility Layer

```python
# field_framework/compat/magnetrun.py
"""
Backwards compatibility layer for magnetrun's fieldunits dict format.
"""
from typing import Dict, List
from ..field import Field, ureg

def field_to_dict(field: Field, input_unit=None, output_unit=None) -> Dict:
    """
    Convert Field object to magnetrun's dict format.
    
    Returns:
        {
            "Symbol": str,
            "mSymbol": str,  # optional
            "Units": [input_unit, output_unit],
            "Exclude": List[str],
            "Val": Any  # optional
        }
    """
    result = {
        "Symbol": field.symbol,
        "Units": [
            input_unit or field.unit,
            output_unit or field.unit
        ],
        "Exclude": field.exclude_regions
    }
    
    if field.latex_symbol and field.latex_symbol != field.symbol:
        result["mSymbol"] = field.latex_symbol
    
    if field.default_value is not None:
        result["Val"] = field.default_value
    
    return result


def create_fieldunits_dict(fields: List[Field], 
                           distance_unit: str = "meter") -> Dict:
    """
    Create magnetrun-compatible fieldunits dictionary from Field list.
    
    This function mimics the behavior of dictTypeUnits() from method3D.py
    """
    ureg_local = ureg
    du = ureg_local.Unit(distance_unit)
    
    fieldunits = {}
    for field in fields:
        # Determine appropriate units based on field type
        # This logic would need to be customized per field
        fieldunits[field.name] = field_to_dict(field)
    
    return fieldunits
```

---

## Phase 2: Extraction Steps

### 2.1 Step-by-Step Migration

**Step 1: Create New Package Structure**
```bash
# Create new repository
mkdir field-framework
cd field-framework
git init
poetry init  # or setup.py

# Create structure
mkdir -p field_framework/standard_fields
mkdir -p tests
mkdir -p examples
mkdir -p docs
```

**Step 2: Extract Core Classes from magnetrun**

1. Copy `magnetrun/core/fields/field.py` → `field_framework/field.py`
2. Copy `magnetrun/core/fields/utils.py` → `field_framework/utils.py`
3. Refactor to remove magnetrun-specific dependencies
4. Add dataclass-based Field implementation (shown above)
5. Create FieldRegistry class

**Step 3: Create Standard Field Definitions**

Extract field definitions from:
- `method3D.py` dictTypeUnits function
- Create organized modules:
  - `electromagnetic.py` - B, E, J, etc.
  - `thermal.py` - T, k, etc.
  - `mechanical.py` - stress, displacement, etc.
  - `flow.py` - velocity, pressure, etc.

**Step 4: Add Compatibility Layers**

Create `field_framework/compat/magnetrun.py` to provide:
- `field_to_dict()` - Convert Field → old dict format
- `dict_to_field()` - Convert old dict → Field
- `create_fieldunits_dict()` - Generate full magnetrun dict

**Step 5: Write Tests**

```python
# tests/test_field.py
def test_field_creation():
    field = Field(
        name="MagneticField",
        symbol="B",
        unit="tesla"
    )
    assert field.name == "MagneticField"
    assert field.symbol == "B"

def test_field_conversion():
    field = Field(name="B", symbol="B", unit="tesla")
    result = field.convert(1.0, "gauss")
    assert abs(result - 10000.0) < 0.01

def test_field_label_formatting():
    field = Field(
        name="B",
        symbol="B",
        unit="tesla",
        latex_symbol=r"$B$"
    )
    assert field.format_label("gauss", use_latex=True) == r"$B$ [G]"
```

**Step 6: Package and Publish**

```toml
# pyproject.toml
[tool.poetry]
name = "field-framework"
version = "0.1.0"
description = "Generic field and unit management for scientific computing"
authors = ["Your Name <email@example.com>"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.8"
pint = "^0.20"

[tool.poetry.dev-dependencies]
pytest = "^7.0"
pytest-cov = "^4.0"
black = "^23.0"
mypy = "^1.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

---

## Phase 3: Update Dependent Projects

### 3.1 Update magnetrun

**New Structure:**
```
magnetrun/
├── pyproject.toml  # Add field-framework dependency
├── magnetrun/
│   ├── core/
│   │   # Remove magnetrun/core/fields/ directory
│   ├── formats/
│   │   └── format_definition.py  # Update imports
│   └── ...
```

**Migration:**

```python
# magnetrun/formats/format_definition.py
# OLD:
from magnetrun.core.fields.field import Field
from magnetrun.core.fields.utils import convert_data

# NEW:
from field_framework import Field, FieldRegistry
from field_framework.converters import convert_data
from field_framework.compat.magnetrun import create_fieldunits_dict

class FormatDefinition:
    def __init__(self, format_name, registry=None):
        self.format_name = format_name
        self.registry = registry or FieldRegistry()
        self.field_map = {}
    
    def add_mapping(self, file_key: str, field_name: str):
        """Map file column to field"""
        field = self.registry.get(field_name)
        if field:
            self.field_map[file_key] = field
    
    def parse_data(self, raw_data: dict) -> dict:
        """Attach values to fields"""
        parsed = {}
        for key, value in raw_data.items():
            if key in self.field_map:
                field = self.field_map[key]
                parsed[field.name] = field.validate_value(value)
        return parsed
```

### 3.2 Update python_hifimagnetparaview

**New Structure:**
```
python_hifimagnetparaview/
├── pyproject.toml  # Add field-framework dependency
├── hifimagnetparaview/
│   ├── method3D.py  # Simplified
│   ├── plot.py      # Update to use Field objects
│   └── ...
```

**Migration:**

```python
# NEW method3D.py (simplified)
from field_framework import ureg
from field_framework.standard_fields import electromagnetic, thermal, mechanical
from field_framework.compat.magnetrun import create_fieldunits_dict
from field_framework.registry import FieldRegistry

def setup_fields(distance_unit: str = "meter"):
    """Setup field registry for 3D visualization"""
    registry = FieldRegistry()
    
    # Register standard fields
    electromagnetic.register_electromagnetic_fields()
    thermal.register_thermal_fields()
    mechanical.register_mechanical_fields()
    
    # For backwards compatibility, create dict format
    fields = registry.list_fields()
    fieldunits = create_fieldunits_dict(fields, distance_unit)
    
    # Ignored keys remain application-specific
    ignored_keys = [
        "elasticity.Lame1",
        "elasticity.Lame2",
        # ...
    ]
    
    return fieldunits, ignored_keys, registry


# NEW plot.py usage
from field_framework import Field
from field_framework.converters import convert_data

def plotOrField(file, key: str, theta: float, z: float, 
                fieldunits: dict, registry: FieldRegistry, basedir: str, ...):
    """Updated to use Field objects when available"""
    
    # Try to get Field object from registry
    field = registry.get(key)
    
    if field:
        # Use Field object methods
        symbol = field.symbol
        msymbol = field.latex_symbol
        # ... use field methods
    else:
        # Fallback to old dict format
        (toolbox, physic, fieldname) = keyinfo(key)
        symbol = fieldunits[fieldname]["Symbol"]
        msymbol = fieldunits[fieldname].get("mSymbol", symbol)
        # ...
```

---

## Phase 4: Testing and Validation

### 4.1 Integration Tests

```python
# tests/integration/test_magnetrun_integration.py
def test_magnetrun_format_definition():
    """Test that FormatDefinition works with new Field system"""
    from field_framework import Field, FieldRegistry
    from magnetrun.formats import FormatDefinition
    
    registry = FieldRegistry()
    registry.register(Field("Temperature", "T", "degC"))
    
    fmt = FormatDefinition("test_format", registry)
    fmt.add_mapping("temp_column", "Temperature")
    
    raw_data = {"temp_column": 25.0}
    parsed = fmt.parse_data(raw_data)
    
    assert "Temperature" in parsed
    assert parsed["Temperature"] == 25.0


# tests/integration/test_hifimagnetparaview_integration.py
def test_plot_with_new_fields():
    """Test that plotting functions work with Field objects"""
    from field_framework.standard_fields import electromagnetic
    from hifimagnetparaview.method3D import setup_fields
    
    fieldunits, ignored_keys, registry = setup_fields("millimeter")
    
    # Verify field is available
    field = registry.get("MagneticField")
    assert field is not None
    assert field.symbol == "B"
    
    # Verify backwards compatibility
    assert "MagneticField" in fieldunits
    assert "Symbol" in fieldunits["MagneticField"]
```

### 4.2 Compatibility Validation

Create validation script to ensure no breaking changes:

```python
# scripts/validate_compatibility.py
"""
Validate that all existing code still works with new field-framework.
"""
def validate_magnetrun():
    """Test magnetrun compatibility"""
    # Load old field definitions
    # Load new field definitions
    # Compare outputs
    pass

def validate_hifimagnetparaview():
    """Test python_hifimagnetparaview compatibility"""
    # Test that all plots still generate correctly
    # Verify field lookups work
    pass

if __name__ == "__main__":
    validate_magnetrun()
    validate_hifimagnetparaview()
    print("✓ All compatibility tests passed!")
```

---

## Phase 5: Documentation and Release

### 5.1 Documentation Structure

```
docs/
├── index.md              # Overview
├── installation.md       # pip install field-framework
├── quickstart.md         # Basic usage
├── migration_guide.md    # For existing magnetrun users
├── api/
│   ├── field.md
│   ├── registry.md
│   └── converters.md
├── examples/
│   ├── basic_field_definition.md
│   ├── custom_fields.md
│   ├── plotting_integration.md
│   └── format_readers.md
└── contributing.md
```

### 5.2 README.md

```markdown
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
```

---

## Timeline and Milestones

### Week 1-2: Setup and Core Development
- [ ] Create field-framework repository
- [ ] Implement core Field class
- [ ] Implement FieldRegistry
- [ ] Write unit tests (>80% coverage)
- [ ] Setup CI/CD pipeline

### Week 3-4: Standard Fields and Compatibility
- [ ] Create standard field definitions
- [ ] Implement compatibility layers
- [ ] Write integration tests
- [ ] Documentation (API reference)

### Week 5: magnetrun Integration
- [ ] Update magnetrun to use field-framework
- [ ] Remove old field code
- [ ] Test magnetrun functionality
- [ ] Update magnetrun documentation

### Week 6: python_hifimagnetparaview Integration
- [ ] Update python_hifimagnetparaview
- [ ] Test all plotting functions
- [ ] Validate output consistency
- [ ] Update examples

### Week 7-8: Polish and Release
- [ ] Complete documentation
- [ ] Write migration guides
- [ ] Package for PyPI
- [ ] Create example notebooks
- [ ] Release v0.1.0

---

## Success Criteria

✅ **Technical:**
- All tests pass (unit + integration)
- >80% code coverage
- Type hints throughout
- Documented API
- Backwards compatible

✅ **Usability:**
- Clear migration path
- Working examples
- Good documentation
- Easy to extend

✅ **Maintainability:**
- Clean architecture
- Minimal dependencies
- Versioned API
- CI/CD pipeline

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Breaking existing code | Maintain compatibility layer, extensive testing |
| Complex migration | Provide migration scripts and documentation |
| Adoption resistance | Demonstrate clear benefits, gradual rollout |
| Unit conversion bugs | Comprehensive test suite, use pint's validation |
| Performance concerns | Benchmark and optimize if needed |

---

## Future Enhancements (Post v1.0)

- [ ] Field validation rules (min/max values)
- [ ] Derived field calculations
- [ ] Field groups/categories
- [ ] Serialization (JSON/YAML export/import)
- [ ] Field interpolation utilities
- [ ] GUI for field management
- [ ] Integration with xarray/pandas
- [ ] Domain-specific field packs (CFD, EM, etc.)

---

## Questions to Resolve

1. **Package Name:** `field-framework`, `sci-fields`, `physics-fields`, or other?
2. **License:** MIT, BSD, Apache 2.0?
3. **Hosting:** GitHub? GitLab? 
4. **PyPI Name:** Same as package or different?
5. **Version Strategy:** Semantic versioning from 0.1.0?
6. **Standard Fields:** Which domains to include initially?
7. **Python Version:** Support 3.8+? Or 3.9+?
8. **Documentation Hosting:** Read the Docs? GitHub Pages?

---

## Contact and Next Steps

**Next Action Items:**
1. Review this plan and provide feedback
2. Decide on package name and hosting
3. Set up initial repository structure
4. Begin core Field implementation
5. Schedule weekly sync meetings

**Questions?**
- Which fields from method3D.py should be in the initial release?
- Are there other projects besides hifimagnetparaview that would use this?
- Any specific requirements for the magnetrun integration?
