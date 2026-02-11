"""
Standard hydraulic and thermohydraulic field definitions.

This module defines commonly used hydraulic fields for fluid flow simulations,
including pressure, flow rate, velocity, and fluid properties.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from ..field import Field, ureg
from ..field_types import FieldType

if TYPE_CHECKING:
    from ..registry import FieldRegistry


# =============================================================================
# Pressure
# =============================================================================

PRESSURE = Field(
    name="Pressure",
    symbol="P",
    unit=ureg.pascal,
    field_type=FieldType.PRESSURE,
    description="Static pressure",
    latex_symbol=r"$P$",
    aliases=["P", "pressure", "static_pressure"],
    metadata={"category": "hydraulics", "type": "scalar"},
)

PRESSURE_DROP = Field(
    name="PressureDrop",
    symbol="ΔP",
    unit=ureg.pascal,
    field_type=FieldType.PRESSURE,
    description="Pressure drop",
    latex_symbol=r"$\Delta P$",
    aliases=["dP", "delta_P", "pressure_drop"],
    metadata={"category": "hydraulics", "type": "scalar"},
)


# =============================================================================
# Flow Rate
# =============================================================================

FLOW_RATE = Field(
    name="FlowRate",
    symbol="Q",
    unit=ureg.meter**3 / ureg.second,
    field_type=FieldType.FLOW_RATE,
    description="Volumetric flow rate",
    latex_symbol=r"$Q$",
    aliases=["Q", "flow_rate", "volumetric_flow_rate", "flow"],
    metadata={"category": "hydraulics", "type": "scalar"},
)

MASS_FLOW_RATE = Field(
    name="MassFlowRate",
    symbol="ṁ",
    unit=ureg.kilogram / ureg.second,
    field_type=None,  # No FieldType defined for mass flow rate (kg/s)
    description="Mass flow rate",
    latex_symbol=r"$\dot{m}$",
    aliases=["mdot", "m_dot", "mass_flow_rate", "mass_flow"],
    metadata={"category": "hydraulics", "type": "scalar"},
)


# =============================================================================
# Velocity
# =============================================================================

VELOCITY = Field(
    name="Velocity",
    symbol="v",
    unit=ureg.meter / ureg.second,
    field_type=FieldType.VELOCITY,
    description="Flow velocity magnitude",
    latex_symbol=r"$v$",
    aliases=["v", "velocity", "flow_velocity"],
    metadata={"category": "hydraulics", "type": "vector_magnitude"},
)

VELOCITY_X = Field(
    name="Velocity_x",
    symbol="v_x",
    unit=ureg.meter / ureg.second,
    field_type=FieldType.VELOCITY,
    description="Velocity x-component",
    latex_symbol=r"$v_x$",
    aliases=["vx", "v_x", "velocity_x"],
    metadata={"category": "hydraulics", "type": "component", "component": "x"},
)

VELOCITY_Y = Field(
    name="Velocity_y",
    symbol="v_y",
    unit=ureg.meter / ureg.second,
    field_type=FieldType.VELOCITY,
    description="Velocity y-component",
    latex_symbol=r"$v_y$",
    aliases=["vy", "v_y", "velocity_y"],
    metadata={"category": "hydraulics", "type": "component", "component": "y"},
)

VELOCITY_Z = Field(
    name="Velocity_z",
    symbol="v_z",
    unit=ureg.meter / ureg.second,
    field_type=FieldType.VELOCITY,
    description="Velocity z-component",
    latex_symbol=r"$v_z$",
    aliases=["vz", "v_z", "velocity_z"],
    metadata={"category": "hydraulics", "type": "component", "component": "z"},
)


# =============================================================================
# Fluid Properties
# =============================================================================

DYNAMIC_VISCOSITY = Field(
    name="DynamicViscosity",
    symbol="μ",
    unit=ureg.pascal * ureg.second,
    field_type=FieldType.DYNAMIC_VISCOSITY,
    description="Dynamic viscosity",
    latex_symbol=r"$\mu$",
    aliases=["mu", "dynamic_viscosity", "viscosity"],
    metadata={"category": "hydraulics", "type": "material_property"},
)

KINEMATIC_VISCOSITY = Field(
    name="KinematicViscosity",
    symbol="ν",
    unit=ureg.meter**2 / ureg.second,
    field_type=FieldType.KINEMATIC_VISCOSITY,
    description="Kinematic viscosity",
    latex_symbol=r"$\nu$",
    # FIXED: Changed "nu" to "nu_kinematic" to avoid conflict with PoissonRatio
    aliases=["nu_kinematic", "kinematic_viscosity"],
    metadata={"category": "hydraulics", "type": "material_property"},
)

DENSITY = Field(
    name="Density",
    symbol="ρ",
    unit=ureg.kilogram / ureg.meter**3,
    field_type=FieldType.DENSITY,
    description="Mass density",
    latex_symbol=r"$\rho$",
    aliases=["rho", "density", "mass_density"],
    metadata={"category": "hydraulics", "type": "material_property"},
)


# =============================================================================
# Field Collections
# =============================================================================

# Pressure fields
PRESSURE_FIELDS: List[Field] = [
    PRESSURE,
    PRESSURE_DROP,
]

# Flow rate fields
FLOW_RATE_FIELDS: List[Field] = [
    FLOW_RATE,
    MASS_FLOW_RATE,
]

# Velocity and components
VELOCITY_FIELDS: List[Field] = [
    VELOCITY,
    VELOCITY_X,
    VELOCITY_Y,
    VELOCITY_Z,
]

# Fluid properties
FLUID_PROPERTIES: List[Field] = [
    DYNAMIC_VISCOSITY,
    KINEMATIC_VISCOSITY,
    DENSITY,
]

# All hydraulic fields
HYDRAULIC_FIELDS: List[Field] = (
    PRESSURE_FIELDS
    + FLOW_RATE_FIELDS
    + VELOCITY_FIELDS
    + FLUID_PROPERTIES
)


def register_hydraulic_fields(registry: "FieldRegistry") -> None:
    """
    Register all standard hydraulic fields with a registry.

    Args:
        registry: FieldRegistry to register fields with

    Example:
        >>> from python_magnetunits import FieldRegistry
        >>> from python_magnetunits.physics import hydraulics
        >>> registry = FieldRegistry()
        >>> hydraulics.register_hydraulic_fields(registry)
        >>> field = registry.get("Pressure")
    """
    registry.bulk_register(HYDRAULIC_FIELDS)


def register_velocity_fields(registry: "FieldRegistry") -> None:
    """Register only velocity field and components."""
    registry.bulk_register(VELOCITY_FIELDS)


def register_fluid_properties(registry: "FieldRegistry") -> None:
    """Register only fluid property fields."""
    registry.bulk_register(FLUID_PROPERTIES)
