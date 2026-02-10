"""
Tests for the FieldRegistry class.
"""

import pytest
from python_magnetunits import Field, FieldRegistry, ureg


class TestFieldRegistryCreation:
    """Test FieldRegistry creation and basic operations."""

    def test_create_empty_registry(self) -> None:
        """Test creating an empty registry."""
        registry = FieldRegistry()
        assert len(registry) == 0

    def test_registry_len(self) -> None:
        """Test that len() works on registry."""
        registry = FieldRegistry()
        field = Field(name="B", symbol="B", unit="tesla")
        registry.register(field)
        assert len(registry) == 1


class TestFieldRegistryRegistration:
    """Test field registration."""

    def test_register_single_field(self) -> None:
        """Test registering a single field."""
        registry = FieldRegistry()
        field = Field(name="MagneticField", symbol="B", unit="tesla")
        registry.register(field)
        assert len(registry) == 1

    def test_register_multiple_fields(self) -> None:
        """Test registering multiple fields."""
        registry = FieldRegistry()
        B = Field(name="B", symbol="B", unit="tesla")
        E = Field(name="E", symbol="E", unit="volt/meter")
        registry.register(B)
        registry.register(E)
        assert len(registry) == 2

    def test_register_overwrites_existing(self) -> None:
        """Test that registering a field with same name overwrites."""
        registry = FieldRegistry()
        field1 = Field(name="B", symbol="B", unit="tesla")
        field2 = Field(name="B", symbol="B_new", unit="gauss")
        registry.register(field1)
        registry.register(field2)
        assert len(registry) == 1
        assert registry.get("B").symbol == "B_new"

    def test_bulk_register(self) -> None:
        """Test bulk registration of multiple fields."""
        registry = FieldRegistry()
        fields = [
            Field(name="B", symbol="B", unit="tesla"),
            Field(name="E", symbol="E", unit="volt/meter"),
            Field(name="J", symbol="J", unit="ampere/meter**2"),
        ]
        registry.bulk_register(fields)
        assert len(registry) == 3


class TestFieldRegistryLookup:
    """Test field lookup by various methods."""

    def test_lookup_by_name(self) -> None:
        """Test looking up field by name."""
        registry = FieldRegistry()
        field = Field(name="MagneticField", symbol="B", unit="tesla")
        registry.register(field)
        found = registry.get("MagneticField")
        assert found is field

    def test_lookup_by_symbol(self) -> None:
        """Test looking up field by symbol."""
        registry = FieldRegistry()
        field = Field(name="MagneticField", symbol="B", unit="tesla")
        registry.register(field)
        found = registry.get("B")
        assert found is field

    def test_lookup_by_alias(self) -> None:
        """Test looking up field by alias."""
        registry = FieldRegistry()
        field = Field(
            name="MagneticField",
            symbol="B",
            unit="tesla",
            aliases=["B_field", "magnetic_field"],
        )
        registry.register(field)
        assert registry.get("B_field") is field
        assert registry.get("magnetic_field") is field

    def test_lookup_nonexistent_returns_none(self) -> None:
        """Test that looking up nonexistent field returns None."""
        registry = FieldRegistry()
        assert registry.get("NonExistent") is None

    def test_lookup_priority_name_over_symbol(self) -> None:
        """Test that name lookup has priority over symbol."""
        registry = FieldRegistry()
        B_field = Field(name="B", symbol="B", unit="tesla")
        registry.register(B_field)
        # Should find by exact name match
        assert registry.get("B") is B_field

    def test_lookup_ambiguous_alias_returns_none(self) -> None:
        """Test that ambiguous aliases return None."""
        registry = FieldRegistry()
        field1 = Field(name="Field1", symbol="F1", unit="tesla", aliases=["F"])
        field2 = Field(name="Field2", symbol="F2", unit="gauss", aliases=["F"])
        registry.register(field1)
        registry.register(field2)
        # Alias "F" matches both fields - should return None
        assert registry.get("F") is None


class TestFieldRegistryListing:
    """Test listing fields."""

    def test_list_all_fields(self) -> None:
        """Test listing all registered fields."""
        registry = FieldRegistry()
        fields_to_register = [
            Field(name="B", symbol="B", unit="tesla"),
            Field(name="E", symbol="E", unit="volt/meter"),
        ]
        registry.bulk_register(fields_to_register)
        listed = registry.list_fields()
        assert len(listed) == 2
        assert all(f in listed for f in fields_to_register)

    def test_list_fields_by_category(self) -> None:
        """Test listing fields filtered by category."""
        registry = FieldRegistry()
        B = Field(
            name="B",
            symbol="B",
            unit="tesla",
            metadata={"category": "electromagnetic"},
        )
        T = Field(
            name="T",
            symbol="T",
            unit="kelvin",
            metadata={"category": "thermal"},
        )
        registry.bulk_register([B, T])
        
        em_fields = registry.list_fields(category="electromagnetic")
        assert len(em_fields) == 1
        assert em_fields[0] is B
        
        thermal_fields = registry.list_fields(category="thermal")
        assert len(thermal_fields) == 1
        assert thermal_fields[0] is T


class TestFieldRegistryContainment:
    """Test 'in' operator and has_field method."""

    def test_has_field(self) -> None:
        """Test has_field method."""
        registry = FieldRegistry()
        field = Field(name="B", symbol="B", unit="tesla", aliases=["B_field"])
        registry.register(field)
        assert registry.has_field("B") is True
        assert registry.has_field("B_field") is True
        assert registry.has_field("NonExistent") is False

    def test_contains_operator(self) -> None:
        """Test 'in' operator for containment."""
        registry = FieldRegistry()
        field = Field(name="B", symbol="B", unit="tesla")
        registry.register(field)
        assert "B" in registry
        assert "NonExistent" not in registry


class TestFieldRegistryRemoval:
    """Test field removal from registry."""

    def test_remove_existing_field(self) -> None:
        """Test removing an existing field."""
        registry = FieldRegistry()
        field = Field(name="B", symbol="B", unit="tesla", aliases=["B_field"])
        registry.register(field)
        assert "B" in registry
        
        result = registry.remove("B")
        assert result is True
        assert "B" not in registry

    def test_remove_nonexistent_field(self) -> None:
        """Test removing a nonexistent field."""
        registry = FieldRegistry()
        result = registry.remove("NonExistent")
        assert result is False

    def test_remove_cleans_up_aliases(self) -> None:
        """Test that removal cleans up aliases."""
        registry = FieldRegistry()
        field = Field(name="B", symbol="B", unit="tesla", aliases=["B_field"])
        registry.register(field)
        
        registry.remove("B")
        
        # Alias lookup should now fail
        assert registry.get("B_field") is None

    def test_remove_field_with_multiple_aliases(self) -> None:
        """Test removing field with multiple aliases."""
        registry = FieldRegistry()
        field = Field(
            name="B",
            symbol="B",
            unit="tesla",
            aliases=["B_field", "magnetic_field", "flux_density"],
        )
        registry.register(field)
        registry.remove("B")
        
        assert registry.get("B_field") is None
        assert registry.get("magnetic_field") is None
        assert registry.get("flux_density") is None


class TestFieldRegistryRepr:
    """Test registry string representation."""

    def test_repr(self) -> None:
        """Test repr of registry."""
        registry = FieldRegistry()
        field = Field(name="B", symbol="B", unit="tesla")
        registry.register(field)
        
        repr_str = repr(registry)
        assert "FieldRegistry" in repr_str
        assert "1" in repr_str  # Number of fields
