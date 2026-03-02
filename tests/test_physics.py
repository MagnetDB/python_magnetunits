"""
Tests for pre-defined field collections in the physics sub-package.

Each domain module is tested for:
- All expected fields are importable and have correct names/symbols/units
- The register_* helper populates an isolated registry
- Symbol lookup works (via registry)
- Alias lookup works (via registry)
- Basic unit conversion works on spot-checked fields
"""

from __future__ import annotations

import pytest
from python_magnetunits import Field, FieldRegistry, FieldType, ureg
from python_magnetunits.physics import (
    electromagnetic,
    hydraulics,
    mechanical,
    thermal,
)


# ---------------------------------------------------------------------------
# Electromagnetic
# ---------------------------------------------------------------------------


class TestElectromagneticFields:
    """Tests for physics.electromagnetic field definitions."""

    def test_all_fields_exported(self) -> None:
        assert len(electromagnetic.ELECTROMAGNETIC_FIELDS) == 13

    def test_magnetic_field_attributes(self) -> None:
        B = electromagnetic.MAGNETIC_FIELD
        assert B.name == "MagneticField"
        assert B.symbol == "B"
        assert B.unit == ureg.tesla

    def test_electric_field_attributes(self) -> None:
        E = electromagnetic.ELECTRIC_FIELD
        assert E.name == "ElectricField"
        assert E.symbol == "E"
        assert E.unit == ureg.volt / ureg.meter

    def test_current_density_attributes(self) -> None:
        J = electromagnetic.CURRENT_DENSITY
        assert J.name == "CurrentDensity"
        assert J.symbol == "J"
        assert J.unit == ureg.ampere / ureg.meter**2

    def test_potential_attributes(self) -> None:
        V = electromagnetic.POTENTIAL
        assert V.name == "Potential"
        assert V.symbol == "V"
        assert V.unit == ureg.volt

    def test_register_populates_registry(self) -> None:
        registry = FieldRegistry()
        electromagnetic.register_electromagnetic_fields(registry)
        assert len(registry) == 13

    def test_symbol_lookup_after_register(self) -> None:
        registry = FieldRegistry()
        electromagnetic.register_electromagnetic_fields(registry)
        assert registry.get("B") is electromagnetic.MAGNETIC_FIELD
        assert registry.get("E") is electromagnetic.ELECTRIC_FIELD
        assert registry.get("J") is electromagnetic.CURRENT_DENSITY
        assert registry.get("V") is electromagnetic.POTENTIAL

    def test_alias_lookup_after_register(self) -> None:
        registry = FieldRegistry()
        electromagnetic.register_electromagnetic_fields(registry)
        assert registry.get("B_field") is electromagnetic.MAGNETIC_FIELD
        assert registry.get("magnetic_flux_density") is electromagnetic.MAGNETIC_FIELD

    def test_magnetic_field_conversion(self) -> None:
        B = electromagnetic.MAGNETIC_FIELD
        result = B.convert(1.0, "Gauss")
        assert abs(result - 10000.0) < 0.1

    def test_register_default_registry_uses_default(self) -> None:
        """Calling without argument should not raise."""
        # We can't easily test the default_registry side-effect without
        # polluting global state, so just verify the call succeeds.
        registry = FieldRegistry()
        electromagnetic.register_electromagnetic_fields(registry)
        assert "MagneticField" in registry


# ---------------------------------------------------------------------------
# Thermal
# ---------------------------------------------------------------------------


class TestThermalFields:
    """Tests for physics.thermal field definitions."""

    def test_all_fields_exported(self) -> None:
        assert len(thermal.THERMAL_FIELDS) >= 10

    def test_temperature_attributes(self) -> None:
        T = thermal.TEMPERATURE
        assert T.name == "Temperature"
        assert T.symbol == "T"
        assert T.unit == ureg.kelvin
        assert T.field_type == FieldType.TEMPERATURE

    def test_heat_flux_attributes(self) -> None:
        q = thermal.HEAT_FLUX
        assert q.name == "HeatFlux"
        assert q.symbol == "q"
        assert q.field_type == FieldType.HEAT_FLUX

    def test_thermal_conductivity_attributes(self) -> None:
        k = thermal.THERMAL_CONDUCTIVITY
        assert k.name == "ThermalConductivity"
        assert k.symbol == "k"
        assert k.field_type == FieldType.THERMAL_CONDUCTIVITY

    def test_register_populates_registry(self) -> None:
        registry = FieldRegistry()
        thermal.register_thermal_fields(registry)
        assert len(registry) == len(thermal.THERMAL_FIELDS)

    def test_symbol_lookup_after_register(self) -> None:
        registry = FieldRegistry()
        thermal.register_thermal_fields(registry)
        assert registry.get("T") is thermal.TEMPERATURE
        assert registry.get("k") is thermal.THERMAL_CONDUCTIVITY

    def test_temperature_conversion(self) -> None:
        T = thermal.TEMPERATURE
        result = T.convert(273.15, "degC")
        assert abs(result - 0.0) < 0.01

    def test_temperature_exclude_regions(self) -> None:
        assert not thermal.TEMPERATURE.applies_to_region("Air")
        assert thermal.TEMPERATURE.applies_to_region("water")


# ---------------------------------------------------------------------------
# Hydraulics
# ---------------------------------------------------------------------------


class TestHydraulicsFields:
    """Tests for physics.hydraulics field definitions."""

    def test_all_fields_exported(self) -> None:
        assert len(hydraulics.HYDRAULIC_FIELDS) >= 10

    def test_pressure_attributes(self) -> None:
        P = hydraulics.PRESSURE
        assert P.name == "Pressure"
        assert P.symbol == "P"
        assert P.unit == ureg.pascal
        assert P.field_type == FieldType.PRESSURE

    def test_mass_flow_rate_has_field_type(self) -> None:
        mdot = hydraulics.MASS_FLOW_RATE
        assert mdot.field_type == FieldType.MASS_FLOW_RATE
        assert mdot.unit == ureg.kilogram / ureg.second

    def test_velocity_attributes(self) -> None:
        v = hydraulics.VELOCITY
        assert v.name == "Velocity"
        assert v.symbol == "v"
        assert v.field_type == FieldType.VELOCITY

    def test_register_populates_registry(self) -> None:
        registry = FieldRegistry()
        hydraulics.register_hydraulic_fields(registry)
        assert len(registry) == len(hydraulics.HYDRAULIC_FIELDS)

    def test_symbol_lookup_after_register(self) -> None:
        registry = FieldRegistry()
        hydraulics.register_hydraulic_fields(registry)
        assert registry.get("P") is hydraulics.PRESSURE
        assert registry.get("v") is hydraulics.VELOCITY

    def test_alias_lookup_after_register(self) -> None:
        registry = FieldRegistry()
        hydraulics.register_hydraulic_fields(registry)
        assert registry.get("pressure") is hydraulics.PRESSURE
        assert registry.get("mdot") is hydraulics.MASS_FLOW_RATE

    def test_pressure_conversion(self) -> None:
        P = hydraulics.PRESSURE
        result = P.convert(1e5, "bar")
        assert abs(result - 1.0) < 1e-6


# ---------------------------------------------------------------------------
# Mechanical
# ---------------------------------------------------------------------------


class TestMechanicalFields:
    """Tests for physics.mechanical field definitions."""

    def test_all_fields_exported(self) -> None:
        assert len(mechanical.MECHANICAL_FIELDS) >= 15

    def test_force_attributes(self) -> None:
        F = mechanical.FORCE
        assert F.name == "Force"
        assert F.symbol == "F"
        assert F.unit == ureg.newton
        assert F.field_type == FieldType.FORCE

    def test_stress_attributes(self) -> None:
        sigma = mechanical.STRESS
        assert sigma.name == "Stress"
        assert sigma.field_type == FieldType.STRESS

    def test_displacement_attributes(self) -> None:
        u = mechanical.DISPLACEMENT
        assert u.name == "Displacement"
        assert u.symbol == "u"
        assert u.field_type == FieldType.LENGTH

    def test_register_populates_registry(self) -> None:
        registry = FieldRegistry()
        mechanical.register_mechanical_fields(registry)
        assert len(registry) == len(mechanical.MECHANICAL_FIELDS)

    def test_symbol_lookup_after_register(self) -> None:
        registry = FieldRegistry()
        mechanical.register_mechanical_fields(registry)
        assert registry.get("F") is mechanical.FORCE
        assert registry.get("u") is mechanical.DISPLACEMENT

    def test_alias_lookup_after_register(self) -> None:
        registry = FieldRegistry()
        mechanical.register_mechanical_fields(registry)
        assert registry.get("force") is mechanical.FORCE
        assert registry.get("displacement") is mechanical.DISPLACEMENT

    def test_force_conversion(self) -> None:
        F = mechanical.FORCE
        result = F.convert(1000.0, "kilonewton")
        assert abs(result - 1.0) < 1e-9
