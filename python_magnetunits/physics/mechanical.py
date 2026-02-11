"""
Standard mechanical field definitions.

This module defines commonly used mechanical fields for structural simulations,
including stress, strain, displacement, force, and mechanical material properties.

Note: Density field has been removed from this module to avoid duplication.
      Use hydraulics.DENSITY instead for mass density.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from ..field import Field, ureg
from ..field_types import FieldType

if TYPE_CHECKING:
    from ..registry import FieldRegistry


# =============================================================================
# Force
# =============================================================================

FORCE = Field(
    name="Force",
    symbol="F",
    unit=ureg.newton,
    field_type=FieldType.FORCE,
    description="Force magnitude",
    latex_symbol=r"$F$",
    aliases=["F", "force"],
    metadata={"category": "mechanical", "type": "vector_magnitude"},
)

FORCE_X = Field(
    name="Force_x",
    symbol="F_x",
    unit=ureg.newton,
    field_type=FieldType.FORCE,
    description="Force x-component",
    latex_symbol=r"$F_x$",
    aliases=["Fx", "F_x", "force_x"],
    metadata={"category": "mechanical", "type": "component", "component": "x"},
)

FORCE_Y = Field(
    name="Force_y",
    symbol="F_y",
    unit=ureg.newton,
    field_type=FieldType.FORCE,
    description="Force y-component",
    latex_symbol=r"$F_y$",
    aliases=["Fy", "F_y", "force_y"],
    metadata={"category": "mechanical", "type": "component", "component": "y"},
)

FORCE_Z = Field(
    name="Force_z",
    symbol="F_z",
    unit=ureg.newton,
    field_type=FieldType.FORCE,
    description="Force z-component",
    latex_symbol=r"$F_z$",
    aliases=["Fz", "F_z", "force_z"],
    metadata={"category": "mechanical", "type": "component", "component": "z"},
)


# =============================================================================
# Stress
# =============================================================================

STRESS = Field(
    name="Stress",
    symbol="σ",
    unit=ureg.pascal,
    field_type=FieldType.STRESS,
    description="Stress (general / von Mises)",
    latex_symbol=r"$\sigma$",
    aliases=["sigma", "stress", "von_mises_stress"],
    metadata={"category": "mechanical", "type": "tensor_scalar"},
)

STRESS_XX = Field(
    name="Stress_xx",
    symbol="σ_xx",
    unit=ureg.pascal,
    field_type=FieldType.STRESS,
    description="Normal stress xx-component",
    latex_symbol=r"$\sigma_{xx}$",
    aliases=["sigma_xx", "stress_xx"],
    metadata={"category": "mechanical", "type": "tensor_component", "component": "xx"},
)

STRESS_YY = Field(
    name="Stress_yy",
    symbol="σ_yy",
    unit=ureg.pascal,
    field_type=FieldType.STRESS,
    description="Normal stress yy-component",
    latex_symbol=r"$\sigma_{yy}$",
    aliases=["sigma_yy", "stress_yy"],
    metadata={"category": "mechanical", "type": "tensor_component", "component": "yy"},
)

STRESS_ZZ = Field(
    name="Stress_zz",
    symbol="σ_zz",
    unit=ureg.pascal,
    field_type=FieldType.STRESS,
    description="Normal stress zz-component",
    latex_symbol=r"$\sigma_{zz}$",
    aliases=["sigma_zz", "stress_zz"],
    metadata={"category": "mechanical", "type": "tensor_component", "component": "zz"},
)

STRESS_XY = Field(
    name="Stress_xy",
    symbol="σ_xy",
    unit=ureg.pascal,
    field_type=FieldType.STRESS,
    description="Shear stress xy-component",
    latex_symbol=r"$\sigma_{xy}$",
    aliases=["sigma_xy", "stress_xy", "tau_xy"],
    metadata={"category": "mechanical", "type": "tensor_component", "component": "xy"},
)

STRESS_XZ = Field(
    name="Stress_xz",
    symbol="σ_xz",
    unit=ureg.pascal,
    field_type=FieldType.STRESS,
    description="Shear stress xz-component",
    latex_symbol=r"$\sigma_{xz}$",
    aliases=["sigma_xz", "stress_xz", "tau_xz"],
    metadata={"category": "mechanical", "type": "tensor_component", "component": "xz"},
)

STRESS_YZ = Field(
    name="Stress_yz",
    symbol="σ_yz",
    unit=ureg.pascal,
    field_type=FieldType.STRESS,
    description="Shear stress yz-component",
    latex_symbol=r"$\sigma_{yz}$",
    aliases=["sigma_yz", "stress_yz", "tau_yz"],
    metadata={"category": "mechanical", "type": "tensor_component", "component": "yz"},
)


# =============================================================================
# Strain
# =============================================================================

STRAIN = Field(
    name="Strain",
    symbol="ε",
    unit=ureg.dimensionless,
    field_type=FieldType.STRAIN,
    description="Strain (general / equivalent)",
    latex_symbol=r"$\varepsilon$",
    aliases=["epsilon", "strain", "equivalent_strain"],
    metadata={"category": "mechanical", "type": "tensor_scalar"},
)

STRAIN_XX = Field(
    name="Strain_xx",
    symbol="ε_xx",
    unit=ureg.dimensionless,
    field_type=FieldType.STRAIN,
    description="Normal strain xx-component",
    latex_symbol=r"$\varepsilon_{xx}$",
    aliases=["epsilon_xx", "strain_xx"],
    metadata={"category": "mechanical", "type": "tensor_component", "component": "xx"},
)

STRAIN_YY = Field(
    name="Strain_yy",
    symbol="ε_yy",
    unit=ureg.dimensionless,
    field_type=FieldType.STRAIN,
    description="Normal strain yy-component",
    latex_symbol=r"$\varepsilon_{yy}$",
    aliases=["epsilon_yy", "strain_yy"],
    metadata={"category": "mechanical", "type": "tensor_component", "component": "yy"},
)

STRAIN_ZZ = Field(
    name="Strain_zz",
    symbol="ε_zz",
    unit=ureg.dimensionless,
    field_type=FieldType.STRAIN,
    description="Normal strain zz-component",
    latex_symbol=r"$\varepsilon_{zz}$",
    aliases=["epsilon_zz", "strain_zz"],
    metadata={"category": "mechanical", "type": "tensor_component", "component": "zz"},
)


# =============================================================================
# Displacement
# =============================================================================

DISPLACEMENT = Field(
    name="Displacement",
    symbol="u",
    unit=ureg.meter,
    field_type=FieldType.LENGTH,
    description="Displacement magnitude",
    latex_symbol=r"$u$",
    aliases=["u", "displacement", "disp"],
    metadata={"category": "mechanical", "type": "vector_magnitude"},
)

DISPLACEMENT_X = Field(
    name="Displacement_x",
    symbol="u_x",
    unit=ureg.meter,
    field_type=FieldType.LENGTH,
    description="Displacement x-component",
    latex_symbol=r"$u_x$",
    aliases=["ux", "u_x", "displacement_x"],
    metadata={"category": "mechanical", "type": "component", "component": "x"},
)

DISPLACEMENT_Y = Field(
    name="Displacement_y",
    symbol="u_y",
    unit=ureg.meter,
    field_type=FieldType.LENGTH,
    description="Displacement y-component",
    latex_symbol=r"$u_y$",
    aliases=["uy", "u_y", "displacement_y"],
    metadata={"category": "mechanical", "type": "component", "component": "y"},
)

DISPLACEMENT_Z = Field(
    name="Displacement_z",
    symbol="u_z",
    unit=ureg.meter,
    field_type=FieldType.LENGTH,
    description="Displacement z-component",
    latex_symbol=r"$u_z$",
    aliases=["uz", "u_z", "displacement_z"],
    metadata={"category": "mechanical", "type": "component", "component": "z"},
)


# =============================================================================
# Mechanical Material Properties
# =============================================================================

YOUNG_MODULUS = Field(
    name="YoungModulus",
    symbol="E",
    unit=ureg.pascal,
    field_type=FieldType.YOUNG_MODULUS,
    description="Young's modulus (elastic modulus)",
    latex_symbol=r"$E$",
    aliases=["E_modulus", "young_modulus", "elastic_modulus"],
    metadata={"category": "mechanical", "type": "material_property"},
)

POISSON_RATIO = Field(
    name="PoissonRatio",
    symbol="ν",
    unit=ureg.dimensionless,
    field_type=FieldType.POISSON_RATIO,
    description="Poisson's ratio",
    latex_symbol=r"$\nu$",
    # FIXED: Changed "nu" to "nu_poisson" to avoid conflict with KinematicViscosity
    aliases=["nu_poisson", "poisson_ratio", "poisson"],
    metadata={"category": "mechanical", "type": "material_property"},
)

# NOTE: DENSITY has been removed from this module.
# Use hydraulics.DENSITY for mass density to avoid duplication.
# If you need a mechanical-specific density, import from hydraulics:
#   from python_magnetunits.physics.hydraulics import DENSITY


# =============================================================================
# Field Collections
# =============================================================================

# Force and components
FORCE_FIELDS: List[Field] = [
    FORCE,
    FORCE_X,
    FORCE_Y,
    FORCE_Z,
]

# Stress (scalar and tensor components)
STRESS_FIELDS: List[Field] = [
    STRESS,
    STRESS_XX,
    STRESS_YY,
    STRESS_ZZ,
    STRESS_XY,
    STRESS_XZ,
    STRESS_YZ,
]

# Strain (scalar and tensor components)
STRAIN_FIELDS: List[Field] = [
    STRAIN,
    STRAIN_XX,
    STRAIN_YY,
    STRAIN_ZZ,
]

# Displacement and components
DISPLACEMENT_FIELDS: List[Field] = [
    DISPLACEMENT,
    DISPLACEMENT_X,
    DISPLACEMENT_Y,
    DISPLACEMENT_Z,
]

# Material properties (DENSITY removed - use hydraulics.DENSITY)
MECHANICAL_MATERIAL_PROPERTIES: List[Field] = [
    YOUNG_MODULUS,
    POISSON_RATIO,
]

# All mechanical fields
MECHANICAL_FIELDS: List[Field] = (
    FORCE_FIELDS
    + STRESS_FIELDS
    + STRAIN_FIELDS
    + DISPLACEMENT_FIELDS
    + MECHANICAL_MATERIAL_PROPERTIES
)


def register_mechanical_fields(registry: "FieldRegistry") -> None:
    """
    Register all standard mechanical fields with a registry.

    Note: This does not include DENSITY. Use hydraulics.register_hydraulic_fields()
    or hydraulics.register_fluid_properties() if you need density.

    Args:
        registry: FieldRegistry to register fields with

    Example:
        >>> from python_magnetunits import FieldRegistry
        >>> from python_magnetunits.physics import mechanical
        >>> registry = FieldRegistry()
        >>> mechanical.register_mechanical_fields(registry)
        >>> field = registry.get("Stress")
    """
    registry.bulk_register(MECHANICAL_FIELDS)


def register_stress_fields(registry: "FieldRegistry") -> None:
    """Register only stress fields (scalar and tensor components)."""
    registry.bulk_register(STRESS_FIELDS)


def register_strain_fields(registry: "FieldRegistry") -> None:
    """Register only strain fields."""
    registry.bulk_register(STRAIN_FIELDS)


def register_displacement_fields(registry: "FieldRegistry") -> None:
    """Register only displacement fields."""
    registry.bulk_register(DISPLACEMENT_FIELDS)


def register_mechanical_material_properties(registry: "FieldRegistry") -> None:
    """Register only mechanical material property fields (YoungModulus, PoissonRatio)."""
    registry.bulk_register(MECHANICAL_MATERIAL_PROPERTIES)
