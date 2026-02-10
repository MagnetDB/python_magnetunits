# Migration Guide: Before and After Comparison

This document shows concrete examples of how code changes when migrating from
the current dict-based field system to the new Field class framework.

## Table of Contents
1. [Field Definition](#field-definition)
2. [Field Lookup](#field-lookup)
3. [Unit Conversion](#unit-conversion)
4. [Plotting Integration](#plotting-integration)
5. [Format Definition](#format-definition)

---

## Field Definition

### BEFORE (method3D.py - Current)

```python
def dictTypeUnits(ureg, distance_unit: str):
    """create dict of units per Type for 3D"""
    
    TypeUnits = {
        "ThermalConductivity": {
            "Symbol": "k",
            "Units": [
                ureg.watt / ureg.meter / ureg.kelvin,
                ureg.watt / ureg.Unit(distance_unit) / ureg.kelvin,
            ],
            "Exclude": ["Air"],
        },
        "MagneticField": {
            "Symbol": "B",
            "mSymbol": r"$B$",
            "Units": [ureg.tesla, ureg.tesla],
            "Exclude": [],
        },
        "MagneticField_x": {
            "Symbol": "Bx",
            "Units": [ureg.tesla, ureg.tesla],
            "Exclude": [],
        },
        "Temperature": {
            "Symbol": "T",
            "Units": [ureg.degK, ureg.degC],
            "Exclude": ["Air"],
        },
        # ... 50+ more field definitions
    }
    
    return TypeUnits, ignored_keys
```

**Problems:**
- Lots of repetitive boilerplate
- Hard to validate
- No type safety
- Difficult to extend
- No encapsulation of behavior

### AFTER (field-framework)

```python
from field_framework import Field, FieldRegistry, ureg
from field_framework.standard_fields import electromagnetic, thermal

# Option 1: Use pre-defined standard fields
def setup_fields(distance_unit: str = "meter") -> FieldRegistry:
    """Setup field registry with standard fields"""
    registry = FieldRegistry()
    
    # Register standard field collections
    electromagnetic.register_all(registry)
    thermal.register_all(registry)
    
    return registry


# Option 2: Define custom fields
def create_custom_fields():
    """Create application-specific fields"""
    return [
        Field(
            name="ThermalConductivity",
            symbol="k",
            unit=ureg.watt / ureg.meter / ureg.kelvin,
            exclude_regions=["Air"],
            metadata={"category": "thermal"}
        ),
        Field(
            name="MagneticField",
            symbol="B",
            unit=ureg.tesla,
            latex_symbol=r"$B$",
            metadata={"category": "electromagnetic"}
        ),
        Field(
            name="MagneticField_x",
            symbol="Bx",
            unit=ureg.tesla,
            metadata={"category": "electromagnetic", "component": "x"}
        ),
        Field(
            name="Temperature",
            symbol="T",
            unit=ureg.kelvin,
            exclude_regions=["Air"],
            metadata={"category": "thermal"}
        ),
    ]
```

**Benefits:**
- Type-safe with dataclasses
- Reusable standard fields
- Clear structure
- Easy to validate
- Encapsulated behavior

---

## Field Lookup

### BEFORE

```python
# From plot.py
def plotOrField(file, key: str, theta: float, z: float, 
                fieldunits: dict, basedir: str, ...):
    
    # Complex key parsing
    (toolbox, physic, fieldname) = keyinfo(key)
    
    # Manual dict access with error-prone keys
    symbol = fieldunits[fieldname]["Symbol"]
    msymbol = symbol
    if "mSymbol" in fieldunits[fieldname]:
        msymbol = fieldunits[fieldname]["mSymbol"]
    [in_unit, out_unit] = fieldunits[fieldname]["Units"]
```

**Problems:**
- String-based lookups (typo-prone)
- KeyError if field doesn't exist
- Awkward nested dict access
- Inconsistent handling of optional fields

### AFTER

```python
from field_framework import FieldRegistry

def plotOrField(file, key: str, theta: float, z: float,
                registry: FieldRegistry, basedir: str, ...):
    
    # Simple, type-safe lookup
    field = registry.get(key)
    if field is None:
        raise ValueError(f"Unknown field: {key}")
    
    # Clean attribute access
    symbol = field.symbol
    msymbol = field.latex_symbol  # Always present
    in_unit = field.unit
    out_unit = field.unit  # Or specify target unit
```

**Benefits:**
- IDE autocomplete support
- Clearer error messages
- No KeyError surprises
- Type checking

---

## Unit Conversion

### BEFORE

```python
# From plot.py - Complex conversion logic
def plotOrField(...):
    # Get units from dict
    units = {fieldname: fieldunits[fieldname]["Units"]}
    values = keycsv[key].to_list()
    
    # Call separate conversion function
    out_values = convert_data(units, values, fieldname)
    ndf = {key: [val for val in out_values]}
    
    keycsv[key] = ndf[key]
```

**Problems:**
- Separate conversion function needed
- Complex data structure passing
- Not clear what units are being used

### AFTER

```python
def plotOrField(...):
    # Get field
    field = registry.get(key)
    
    # Direct, clear conversion
    values = keycsv[key].to_list()
    out_values = field.convert_array(values, target_unit="gauss")
    keycsv[key] = out_values
```

**Benefits:**
- Self-documenting
- No intermediate data structures
- Clear unit specification
- Method attached to field

---

## Plotting Integration

### BEFORE

```python
# From plot.py - Label generation
symbol = fieldunits[fieldname]["Symbol"]
msymbol = fieldunits[fieldname].get("mSymbol", symbol)
[in_unit, out_unit] = fieldunits[fieldname]["Units"]

# Manual label formatting
ax.set_ylabel(rf"{msymbol} [{out_unit:~P}]", fontsize=18)
```

**Problems:**
- Manual string formatting
- Repeated patterns
- Easy to make formatting mistakes

### AFTER

```python
# Clean, one-line label generation
field = registry.get(key)
label = field.format_label(target_unit="gauss", use_latex=True)
ax.set_ylabel(label, fontsize=18)

# Or even simpler with default unit
ax.set_ylabel(field.format_label(use_latex=True), fontsize=18)
```

**Benefits:**
- Consistent formatting
- Less code
- Harder to make mistakes
- Centralized formatting logic

---

## Format Definition

### BEFORE

```python
# magnetrun/formats/format_definition.py (conceptual)
class FormatDefinition:
    def __init__(self, format_name):
        self.format_name = format_name
        self.field_map = {}  # {file_column: field_name}
        self.fieldunits = None  # External dict
    
    def set_fieldunits(self, fieldunits: dict):
        """Must be called before parsing"""
        self.fieldunits = fieldunits
    
    def add_mapping(self, file_key: str, field_name: str):
        """Map file column to field name"""
        if field_name not in self.fieldunits:
            raise ValueError(f"Unknown field: {field_name}")
        self.field_map[file_key] = field_name
    
    def parse_data(self, raw_data: dict) -> dict:
        """Attach values to fields"""
        parsed = {}
        for key, value in raw_data.items():
            if key in self.field_map:
                field_name = self.field_map[key]
                field_info = self.fieldunits[field_name]
                # Manual validation...
                parsed[field_name] = value
        return parsed
```

**Problems:**
- Tight coupling to dict format
- External fieldunits dict required
- Manual validation
- No type safety

### AFTER

```python
from field_framework import Field, FieldRegistry

class FormatDefinition:
    def __init__(self, format_name: str, registry: FieldRegistry = None):
        self.format_name = format_name
        self.registry = registry or FieldRegistry()
        self.field_map: Dict[str, Field] = {}
    
    def add_mapping(self, file_key: str, field_identifier: str):
        """Map file column to field"""
        field = self.registry.get(field_identifier)
        if field is None:
            raise ValueError(f"Unknown field: {field_identifier}")
        self.field_map[file_key] = field
    
    def parse_data(self, raw_data: dict) -> dict:
        """Attach values to fields with automatic validation"""
        parsed = {}
        for key, value in raw_data.items():
            if key in self.field_map:
                field = self.field_map[key]
                if field.validate_value(value):
                    parsed[field.name] = value
                else:
                    print(f"Warning: Invalid value for {field.name}")
        return parsed
```

**Benefits:**
- Type-safe Field objects
- Automatic validation
- Self-contained
- Easier to test

---

## Complete Migration Example

### BEFORE: Full workflow

```python
# Setup
from magnetrun.method3D import dictTypeUnits
fieldunits, ignored_keys = dictTypeUnits(ureg, "millimeter")

# Use in plotting
def plot_function(data, field_name):
    # Get field info
    field_info = fieldunits[field_name]
    symbol = field_info["Symbol"]
    [in_unit, out_unit] = field_info["Units"]
    
    # Convert data
    units_dict = {field_name: field_info["Units"]}
    converted_data = convert_data(units_dict, data, field_name)
    
    # Plot
    plt.plot(converted_data)
    plt.ylabel(f"{symbol} [{out_unit:~P}]")
```

### AFTER: Full workflow

```python
# Setup
from field_framework import FieldRegistry
from field_framework.standard_fields import electromagnetic, thermal

registry = FieldRegistry()
electromagnetic.register_all(registry)
thermal.register_all(registry)

# Use in plotting
def plot_function(data, field_name):
    # Get field
    field = registry.get(field_name)
    
    # Convert and plot in one go
    converted_data = field.convert_array(data, "millimeter")
    
    plt.plot(converted_data)
    plt.ylabel(field.format_label("millimeter", use_latex=True))
```

**Lines of code:**
- Before: ~15 lines (not counting setup)
- After: ~5 lines
- **67% reduction in code!**

**Benefits:**
- Simpler
- More readable
- Type-safe
- Easier to maintain
- Better error messages

---

## Backwards Compatibility

For gradual migration, the field-framework provides compatibility helpers:

```python
from field_framework import Field, FieldRegistry
from field_framework.compat import create_fieldunits_dict

# Create new registry
registry = FieldRegistry()
# ... register fields ...

# Generate old-style dict for legacy code
fieldunits = create_fieldunits_dict(registry.list_fields(), "millimeter")

# Now legacy code still works!
old_function(fieldunits)  # Uses dict format

# But new code can use Field objects
new_function(registry)  # Uses Field objects
```

This allows you to:
1. Migrate core to field-framework
2. Keep using old dict format where needed
3. Gradually update functions to use Field objects
4. Remove compatibility layer once migration complete

---

## Summary of Improvements

| Aspect | Before | After |
|--------|--------|-------|
| **Type Safety** | ❌ Dict-based | ✅ Dataclass-based |
| **Validation** | ❌ Manual | ✅ Automatic |
| **IDE Support** | ❌ Limited | ✅ Full autocomplete |
| **Error Messages** | ❌ Generic KeyError | ✅ Specific errors |
| **Code Reuse** | ❌ Copy-paste | ✅ Import & use |
| **Testing** | ❌ Hard to test dicts | ✅ Easy to test objects |
| **Documentation** | ❌ External docs | ✅ Self-documenting |
| **Extensibility** | ❌ Modify dict | ✅ Inherit/compose |
| **Maintainability** | ❌ Scattered logic | ✅ Centralized |

---

## Migration Checklist

- [ ] Install field-framework package
- [ ] Create FieldRegistry in application
- [ ] Register standard fields (or import from field-framework)
- [ ] Update import statements
- [ ] Replace dict access with Field objects
- [ ] Update function signatures (fieldunits → registry)
- [ ] Run tests to verify compatibility
- [ ] Update documentation
- [ ] Remove old field dict code
- [ ] Celebrate cleaner codebase! 🎉
