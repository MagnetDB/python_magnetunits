"""
Format loading utilities for JSON/YAML field definitions.

This module provides classes for loading field definitions from external files,
enabling data-driven configuration of field mappings for different file formats.
"""

from .format_definition import (
    FieldDefinition,
    FormatDefinition,
    FormatMetadata,
    get_field_type,
    normalize_unit,
    UNIT_ALIASES,
)

__all__ = [
    "FieldDefinition",
    "FormatDefinition",
    "FormatMetadata",
    "get_field_type",
    "normalize_unit",
    "UNIT_ALIASES",
]
