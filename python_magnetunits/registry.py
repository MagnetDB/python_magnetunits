"""
Field registry for centralized field management and lookup.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .field import Field


class FieldRegistry:
    """
    Central registry for field definitions with lookup by name, symbol, or alias.

    The FieldRegistry provides a single source of truth for field definitions across
    your scientific computing applications. It supports flexible lookup by:
    - Field name (exact match)
    - Field symbol (e.g., "B" for magnetic field)
    - Field aliases (alternative identifiers)

    This enables consistent field definitions across multiple projects while supporting
    both strict field lookup and forgiving alias-based matching.

    Example:
        >>> registry = FieldRegistry()
        >>> B = Field(name="MagneticField", symbol="B", unit="tesla", aliases=["B_field"])
        >>> registry.register(B)
        >>> registry.get("MagneticField")  # lookup by name
        Field(name='MagneticField', ...)
        >>> registry.get("B")  # lookup by symbol
        Field(name='MagneticField', ...)
        >>> registry.get("B_field")  # lookup by alias
        Field(name='MagneticField', ...)
    """

    def __init__(self) -> None:
        """Initialize an empty field registry."""
        self._fields: Dict[str, Field] = {}
        self._by_symbol: Dict[str, Field] = {}
        self._by_alias: Dict[str, List[Field]] = {}

    def register(self, field: Field) -> None:
        """
        Register a field in the registry.

        Fields are indexed by name, symbol, and all aliases for flexible lookup.
        If a field with the same name already exists, it is replaced.

        Args:
            field: The Field object to register

        Example:
            >>> registry = FieldRegistry()
            >>> field = Field(name="Temperature", symbol="T", unit="kelvin")
            >>> registry.register(field)
        """
        self._fields[field.name] = field
        self._by_symbol[field.symbol] = field
        for alias in field.aliases:
            if alias not in self._by_alias:
                self._by_alias[alias] = []
            self._by_alias[alias].append(field)

    def get(self, identifier: str) -> Optional[Field]:
        """
        Get a field by name, symbol, or alias.

        The lookup is performed in order of priority:
        1. Direct field name match
        2. Symbol match
        3. Alias match (returns field if unambiguous)

        Args:
            identifier: Name, symbol, or alias to look up

        Returns:
            Field object if found, None otherwise. Returns None if alias matches
            multiple fields (ambiguous).

        Example:
            >>> registry = FieldRegistry()
            >>> B = Field(name="MagneticField", symbol="B", unit="tesla")
            >>> registry.register(B)
            >>> registry.get("MagneticField")  # Returns the Field
            >>> registry.get("B")  # Also returns the Field
            >>> registry.get("NonExistent")  # Returns None
        """
        # Try direct name lookup (highest priority)
        if identifier in self._fields:
            return self._fields[identifier]

        # Try symbol lookup
        if identifier in self._by_symbol:
            return self._by_symbol[identifier]

        # Try alias lookup (may be ambiguous)
        if identifier in self._by_alias:
            matches = self._by_alias[identifier]
            if len(matches) == 1:
                return matches[0]
            # Multiple matches - ambiguous, return None
            # Caller can handle or raise error if needed

        return None

    def list_fields(self, category: Optional[str] = None) -> List[Field]:
        """
        List all registered fields, optionally filtered by category.

        Args:
            category: Optional metadata category to filter by

        Returns:
            List of Field objects, optionally filtered by category

        Example:
            >>> registry = FieldRegistry()
            >>> # ... register fields ...
            >>> em_fields = registry.list_fields(category="electromagnetic")
        """
        fields = list(self._fields.values())
        if category:
            fields = [f for f in fields if f.metadata.get("category") == category]
        return fields

    def bulk_register(self, fields: List[Field]) -> None:
        """
        Register multiple fields at once.

        Args:
            fields: List of Field objects to register

        Example:
            >>> registry = FieldRegistry()
            >>> fields = [
            ...     Field(name="B", symbol="B", unit="tesla"),
            ...     Field(name="E", symbol="E", unit="volt/meter"),
            ... ]
            >>> registry.bulk_register(fields)
        """
        for field in fields:
            self.register(field)

    def has_field(self, identifier: str) -> bool:
        """
        Check if a field exists in the registry.

        Args:
            identifier: Name, symbol, or alias to check

        Returns:
            True if field exists, False otherwise
        """
        return self.get(identifier) is not None

    def remove(self, field_name: str) -> bool:
        """
        Remove a field from the registry by name.

        Also removes any aliases and symbol mappings.

        Args:
            field_name: Name of the field to remove

        Returns:
            True if field was removed, False if not found
        """
        if field_name not in self._fields:
            return False

        field = self._fields[field_name]
        del self._fields[field_name]

        # Remove symbol mapping
        if field.symbol in self._by_symbol:
            del self._by_symbol[field.symbol]

        # Remove alias mappings
        for alias in field.aliases:
            if alias in self._by_alias:
                self._by_alias[alias] = [
                    f for f in self._by_alias[alias] if f.name != field_name
                ]
                if not self._by_alias[alias]:
                    del self._by_alias[alias]

        return True

    def __len__(self) -> int:
        """Return the number of registered fields."""
        return len(self._fields)

    def __contains__(self, identifier: str) -> bool:
        """Support 'in' operator for checking field existence."""
        return self.has_field(identifier)

    def __repr__(self) -> str:
        """String representation of the registry."""
        return f"FieldRegistry(fields={len(self._fields)})"


# Global default registry instance
default_registry: FieldRegistry = FieldRegistry()
