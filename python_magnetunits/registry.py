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


