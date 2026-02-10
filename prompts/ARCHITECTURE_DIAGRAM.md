# Architecture Diagram: Field Framework Design

## Current Architecture (Before Refactoring)

```
┌─────────────────────────────────────────────────────────────┐
│                    python_hifimagnetparaview                 │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ method3D.py                                         │    │
│  │                                                     │    │
│  │  dictTypeUnits() {                                 │    │
│  │    TypeUnits = {                                   │    │
│  │      "MagneticField": {                            │    │
│  │        "Symbol": "B",                              │    │
│  │        "Units": [ureg.tesla, ureg.tesla],         │    │
│  │        "Exclude": []                               │    │
│  │      },                                            │    │
│  │      ... 50+ more fields ...                       │    │
│  │    }                                               │    │
│  │  }                                                 │    │
│  └─────────────┬──────────────────────────────────────┘    │
│                │                                            │
│                │ fieldunits dict                            │
│                │                                            │
│  ┌─────────────▼──────────────────────────────────────┐    │
│  │ plot.py                                             │    │
│  │                                                     │    │
│  │  plotOrField(fieldunits: dict, ...):               │    │
│  │    symbol = fieldunits[key]["Symbol"]              │    │
│  │    units = fieldunits[key]["Units"]                │    │
│  │    convert_data(units, values, key)                │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                         magnetrun                            │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ magnetrun/core/fields/                             │    │
│  │                                                     │    │
│  │  field.py      ← Field class definitions           │    │
│  │  utils.py      ← Utility functions                 │    │
│  └─────────────┬──────────────────────────────────────┘    │
│                │                                            │
│                │ (not shared between projects)              │
│                │                                            │
│  ┌─────────────▼──────────────────────────────────────┐    │
│  │ magnetrun/formats/format_definition.py             │    │
│  │                                                     │    │
│  │  FormatDefinition:                                 │    │
│  │    - Maps file columns to field names              │    │
│  │    - Uses fieldunits dict                          │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘

Problems:
  ❌ Code duplication (dictTypeUnits in every project)
  ❌ No shared field definitions
  ❌ Dict-based (error-prone, no type safety)
  ❌ Hard to maintain consistency
  ❌ Manual validation
```

## Proposed Architecture (After Refactoring)

```
┌───────────────────────────────────────────────────────────────┐
│                      field-framework                           │
│                    (Shared Python Package)                     │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Core                                                  │    │
│  │                                                       │    │
│  │  Field                    FieldRegistry              │    │
│  │  ┌─────────────┐         ┌──────────────────┐       │    │
│  │  │ name        │         │ register()       │       │    │
│  │  │ symbol      │         │ get()            │       │    │
│  │  │ unit        │◄────────│ list_fields()    │       │    │
│  │  │ latex_symbol│         │ bulk_register()  │       │    │
│  │  │ aliases     │         └──────────────────┘       │    │
│  │  │ excludes    │                                     │    │
│  │  │             │                                     │    │
│  │  │ convert()   │                                     │    │
│  │  │ validate()  │                                     │    │
│  │  │ format_label()│                                   │    │
│  │  └─────────────┘                                     │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Standard Fields Library                               │    │
│  │                                                       │    │
│  │  electromagnetic.py    thermal.py    mechanical.py   │    │
│  │  ┌───────────────┐    ┌─────────┐   ┌──────────┐    │    │
│  │  │ MagneticField │    │ Temp    │   │ Stress   │    │    │
│  │  │ ElectricField │    │ HeatFlux│   │ Strain   │    │    │
│  │  │ Current       │    │ ThermalK│   │ Displace │    │    │
│  │  └───────────────┘    └─────────┘   └──────────┘    │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Compatibility Layer                                   │    │
│  │                                                       │    │
│  │  compat/magnetrun.py                                 │    │
│  │  ┌────────────────────────────────────────┐          │    │
│  │  │ field_to_dict()                        │          │    │
│  │  │ create_fieldunits_dict()               │          │    │
│  │  │ dict_to_field()                        │          │    │
│  │  └────────────────────────────────────────┘          │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Utilities                                             │    │
│  │                                                       │    │
│  │  converters.py    validators.py                      │    │
│  └──────────────────────────────────────────────────────┘    │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             │ pip install field-framework
                             │ (Shared dependency)
                             │
              ┌──────────────┼──────────────┐
              │              │              │
┌─────────────▼─────────┐   │   ┌──────────▼────────────────────┐
│   magnetrun            │   │   │   python_hifimagnetparaview    │
│                        │   │   │                                │
│  from field_framework  │   │   │  from field_framework          │
│  import Field,         │   │   │  import FieldRegistry          │
│         FieldRegistry  │   │   │  from field_framework.standard │
│                        │   │   │  import electromagnetic        │
│  ┌──────────────────┐ │   │   │                                │
│  │ formats/         │ │   │   │  ┌──────────────────────┐      │
│  │                  │ │   │   │  │ method3D.py          │      │
│  │ FormatDefinition │ │   │   │  │                      │      │
│  │                  │ │   │   │  │ def setup_fields():  │      │
│  │ Uses Field       │ │   │   │  │   registry =         │      │
│  │ objects and      │ │   │   │  │     FieldRegistry()  │      │
│  │ FieldRegistry    │ │   │   │  │   em.register_all()  │      │
│  │                  │ │   │   │  │   return registry    │      │
│  └──────────────────┘ │   │   │  └──────────────────────┘      │
│                        │   │   │                                │
│  ┌──────────────────┐ │   │   │  ┌──────────────────────┐      │
│  │ Reads magnetrun  │ │   │   │  │ plot.py              │      │
│  │ format files and │ │   │   │  │                      │      │
│  │ attaches to      │ │   │   │  │ def plotOrField(..., │      │
│  │ Field objects    │ │   │   │  │     registry):       │      │
│  └──────────────────┘ │   │   │  │   field = registry   │      │
└────────────────────────┘   │   │  │     .get(key)        │      │
                             │   │  │   converted =        │      │
                             │   │  │     field.convert()  │      │
                             │   │  │   label = field      │      │
┌────────────────────────┐   │   │  │     .format_label()  │      │
│  Other Future Projects │   │   │  └──────────────────────┘      │
│                        │   │   └────────────────────────────────┘
│  ┌──────────────────┐ │   │
│  │ Can also use     │ │   │
│  │ field-framework  │◄┘   │
│  │ for consistent   │     │
│  │ field management │     │
│  └──────────────────┘     │
└────────────────────────────┘
```

## Data Flow Comparison

### Before (Dict-based)

```
User Request
     │
     ▼
┌──────────────────┐
│ dictTypeUnits()  │  Creates dict with 50+ entries
│ in method3D.py   │  (must be called in each project)
└────────┬─────────┘
         │
         │ fieldunits: dict
         │
         ▼
┌──────────────────┐
│ plot.py          │  Manual dict access
│ fieldunits[key]  │  Error-prone lookups
│ ["Symbol"]       │  String-based keys
└────────┬─────────┘
         │
         │ Manual conversion
         │
         ▼
┌──────────────────┐
│ convert_data()   │  Separate function
│ External utility │  Complex interface
└──────────────────┘
```

### After (Field-based)

```
User Request
     │
     ▼
┌──────────────────────┐
│ setup_fields()       │  Import standard fields
│ registry.register()  │  (or use pre-defined)
└────────┬─────────────┘
         │
         │ registry: FieldRegistry
         │
         ▼
┌──────────────────────┐
│ plot.py              │  Type-safe access
│ field = registry     │  IDE autocomplete
│   .get(key)          │  Clear error messages
└────────┬─────────────┘
         │
         │ field: Field
         │
         ▼
┌──────────────────────┐
│ field.convert()      │  Built-in method
│ field.format_label() │  Self-contained
└──────────────────────┘
```

## Benefits Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                    Benefits of Refactoring                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Reusability                                                     │
│  ═══════════                                                     │
│  Before: ▓▓░░░░░░░░ (20%) - Copy-paste between projects         │
│  After:  ▓▓▓▓▓▓▓▓▓▓ (100%) - Import and use                     │
│                                                                  │
│  Maintainability                                                 │
│  ════════════════                                                │
│  Before: ▓▓▓░░░░░░░ (30%) - Update in multiple places           │
│  After:  ▓▓▓▓▓▓▓▓▓▓ (100%) - Update once, affects all           │
│                                                                  │
│  Type Safety                                                     │
│  ════════════                                                    │
│  Before: ░░░░░░░░░░ (0%) - Dict-based, no checking              │
│  After:  ▓▓▓▓▓▓▓▓▓▓ (100%) - Dataclass with type hints          │
│                                                                  │
│  Developer Experience                                            │
│  ═════════════════════                                           │
│  Before: ▓▓░░░░░░░░ (20%) - Manual lookups, no IDE help         │
│  After:  ▓▓▓▓▓▓▓▓▓░ (90%) - Autocomplete, validation            │
│                                                                  │
│  Testing                                                         │
│  ════════                                                        │
│  Before: ▓▓▓░░░░░░░ (30%) - Hard to test dicts                  │
│  After:  ▓▓▓▓▓▓▓▓▓▓ (100%) - Easy to test objects               │
│                                                                  │
│  Code Clarity                                                    │
│  ═════════════                                                   │
│  Before: ▓▓▓▓░░░░░░ (40%) - Nested dict access                  │
│  After:  ▓▓▓▓▓▓▓▓▓▓ (100%) - Clean object methods               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Package Dependencies

```
┌──────────────────────────────────────────────────────────┐
│                    field-framework                        │
│                                                           │
│  Dependencies:                                            │
│    • pint >= 0.20  (unit management)                      │
│    • Python >= 3.8                                        │
│                                                           │
│  Optional Dependencies:                                   │
│    • numpy (for array operations)                         │
│    • pandas (for DataFrame integration)                   │
└───────────────────────────┬──────────────────────────────┘
                            │
                            │ pip install field-framework
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼─────────┐  ┌──────▼────────┐  ┌──────▼──────────────┐
│   magnetrun      │  │  hifimagnet   │  │  future-project-1   │
│                  │  │  paraview     │  │                     │
│  pyproject.toml: │  │               │  │  Uses same field    │
│  [dependencies]  │  │  requirements:│  │  definitions for    │
│  field-framework │  │  field-       │  │  consistency        │
│    >= 0.1.0      │  │  framework    │  │                     │
└──────────────────┘  └───────────────┘  └─────────────────────┘
```

## Migration Path

```
Phase 1: Extract
┌─────────────┐
│ magnetrun   │
│ fields/     ├──extract──┐
└─────────────┘           │
                          ▼
              ┌─────────────────────┐
              │ field-framework     │
              │ (new package)       │
              └─────────────────────┘

Phase 2: Enhance
┌─────────────────────┐
│ field-framework     │
│ + Add Field class   │
│ + Add Registry      │
│ + Add standard      │
│   fields            │
│ + Add compat layer  │
└─────────────────────┘

Phase 3: Integrate
┌─────────────────────┐       ┌──────────────────────┐
│ field-framework     ├──use──► magnetrun            │
│ (published)         │       │ (updated imports)    │
└─────────────────────┘       └──────────────────────┘
                              
                              ┌──────────────────────┐
                         use──► python_hifimagnet    │
                              │ paraview             │
                              │ (updated imports)    │
                              └──────────────────────┘

Phase 4: Expand
┌─────────────────────┐       ┌──────────────────────┐
│ field-framework     ├──use──► project-n            │
│ (mature library)    │       │ (any new project)    │
└─────────────────────┘       └──────────────────────┘
```

## File Structure

```
field-framework/
│
├── field_framework/
│   ├── __init__.py           ← Public API
│   │     from .field import Field
│   │     from .registry import FieldRegistry
│   │     from .converters import convert_data
│   │
│   ├── field.py              ← Core Field class
│   ├── registry.py           ← FieldRegistry class
│   ├── utils.py              ← Utilities
│   ├── validators.py         ← Validation functions
│   ├── converters.py         ← Unit conversion helpers
│   │
│   ├── standard_fields/      ← Pre-defined fields
│   │   ├── __init__.py
│   │   ├── electromagnetic.py
│   │   ├── thermal.py
│   │   ├── mechanical.py
│   │   └── flow.py
│   │
│   └── compat/               ← Backwards compatibility
│       └── magnetrun.py
│
├── tests/
│   ├── test_field.py
│   ├── test_registry.py
│   ├── test_converters.py
│   └── integration/
│       ├── test_magnetrun.py
│       └── test_hifimagnet.py
│
├── examples/
│   ├── basic_usage.py
│   └── custom_fields.py
│
├── docs/
│   ├── index.md
│   ├── quickstart.md
│   └── api_reference.md
│
├── pyproject.toml
├── README.md
└── LICENSE
```
