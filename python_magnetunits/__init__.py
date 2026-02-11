"""
python_magnetunits - Shared field and unit management for scientific computing.

A Python package for managing physical fields and units in scientific computing
applications. Provides type-safe field definitions with integrated unit conversion,
flexible lookup registries, and a library of standard scientific fields.

Features:
    - Type-safe field definitions with pint units
    - Field registry with name/symbol/alias lookup
    - Automatic unit conversion
    - Plot label generation
    - Region/domain exclusions
    - Extensible standard field library
    - Backwards compatibility with dict-based formats

Quick Start:
    >>> from python_magnetunits import Field, FieldRegistry, ureg
    >>> from python_magnetunits.physics import electromagnetic
    >>>
    >>> # Use standard fields
    >>> registry = FieldRegistry()
    >>> electromagnetic.register_electromagnetic_fields(registry)
    >>> B = registry.get("MagneticField")
    >>> print(B.convert(1.0, "gauss"))  # 10000.0
    >>>
    >>> # Or define custom fields
    >>> T = Field(
    ...     name="Temperature",
    ...     symbol="T",
    ...     unit=ureg.kelvin,
    ...     latex_symbol=r"$T$"
    ... )
    >>> registry.register(T)

Documentation:
    https://github.com/yourusername/python_magnetunits

License:
    MIT
"""

from .converters import (
    are_compatible,
    convert_array,
    convert_data,
    convert_value,
    get_unit_string,
)
from .field import Field, ureg
from .registry import FieldRegistry, default_registry
from . import physics

__author__ = "Christophe"

__all__ = [
    # Core classes
    "Field",
    "FieldRegistry",
    "ureg",
    # Registry instances
    "default_registry",
    # Conversion functions
    "convert_data",
    "convert_value",
    "convert_array",
    "get_unit_string",
    "are_compatible",
    # Subpackages
    "physics",
]

# Version is read from package metadata (defined in pyproject.toml)
# This ensures a single source of truth for the version number
try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    # Fallback for Python < 3.8 (though we require 3.11+)
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("python-magnetunits")
except PackageNotFoundError:
    # Package not installed (e.g., running from source without install)
    # This is expected during development before running `pip install -e .`
    __version__ = "0.0.0+unknown"
