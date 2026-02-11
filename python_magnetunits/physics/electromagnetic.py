"""
Standard electromagnetic field definitions.

This module defines commonly used electromagnetic fields that can be registered
with a FieldRegistry for use across scientific computing applications.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..field import Field, ureg

if TYPE_CHECKING:
    from ..registry import FieldRegistry

# Magnetic field components
MAGNETIC_FIELD = Field(
    name="MagneticField",
    symbol="B",
    unit=ureg.tesla,
    description="Magnetic flux density",
    latex_symbol=r"$B$",
    aliases=["B", "B_field", "magnetic_field", "magnetic_flux_density"],
    metadata={"category": "electromagnetic", "type": "scalar"},
)

MAGNETIC_FIELD_X = Field(
    name="MagneticField_x",
    symbol="B_x",
    unit=ureg.tesla,
    description="Magnetic field x-component",
    latex_symbol=r"$B_x$",
    aliases=["Bx", "B_x", "magnetic_field_x"],
    metadata={"category": "electromagnetic", "type": "component", "component": "x"},
)

MAGNETIC_FIELD_Y = Field(
    name="MagneticField_y",
    symbol="B_y",
    unit=ureg.tesla,
    description="Magnetic field y-component",
    latex_symbol=r"$B_y$",
    aliases=["By", "B_y", "magnetic_field_y"],
    metadata={"category": "electromagnetic", "type": "component", "component": "y"},
)

MAGNETIC_FIELD_Z = Field(
    name="MagneticField_z",
    symbol="B_z",
    unit=ureg.tesla,
    description="Magnetic field z-component",
    latex_symbol=r"$B_z$",
    aliases=["Bz", "B_z", "magnetic_field_z"],
    metadata={"category": "electromagnetic", "type": "component", "component": "z"},
)

# Electric field
ELECTRIC_FIELD = Field(
    name="ElectricField",
    symbol="E",
    unit=ureg.volt / ureg.meter,
    description="Electric field strength",
    latex_symbol=r"$E$",
    aliases=["E", "E_field", "electric_field"],
    metadata={"category": "electromagnetic"},
)

ELECTRIC_FIELD_X = Field(
    name="ElectricField_x",
    symbol="E_x",
    unit=ureg.volt / ureg.meter,
    description="Electric field x-component",
    latex_symbol=r"$E_x$",
    aliases=["Ex", "E_x", "electric_field_x"],
    metadata={"category": "electromagnetic", "type": "component", "component": "x"},
)

ELECTRIC_FIELD_Y = Field(
    name="ElectricField_y",
    symbol="E_y",
    unit=ureg.volt / ureg.meter,
    description="Electric field y-component",
    latex_symbol=r"$E_y$",
    aliases=["Ey", "E_y", "electric_field_y"],
    metadata={"category": "electromagnetic", "type": "component", "component": "y"},
)

ELECTRIC_FIELD_Z = Field(
    name="ElectricField_z",
    symbol="E_z",
    unit=ureg.volt / ureg.meter,
    description="Electric field z-component",
    latex_symbol=r"$E_z$",
    aliases=["Ez", "E_z", "electric_field_z"],
    metadata={"category": "electromagnetic", "type": "component", "component": "z"},
)

# Current density
CURRENT_DENSITY = Field(
    name="CurrentDensity",
    symbol="J",
    unit=ureg.ampere / ureg.meter**2,
    description="Current density",
    latex_symbol=r"$J$",
    aliases=["J", "J_field", "current_density"],
    metadata={"category": "electromagnetic"},
)

CURRENT_DENSITY_X = Field(
    name="CurrentDensity_x",
    symbol="J_x",
    unit=ureg.ampere / ureg.meter**2,
    description="Current density x-component",
    latex_symbol=r"$J_x$",
    aliases=["Jx", "J_x"],
    metadata={"category": "electromagnetic", "type": "component", "component": "x"},
)

CURRENT_DENSITY_Y = Field(
    name="CurrentDensity_y",
    symbol="J_y",
    unit=ureg.ampere / ureg.meter**2,
    description="Current density y-component",
    latex_symbol=r"$J_y$",
    aliases=["Jy", "J_y"],
    metadata={"category": "electromagnetic", "type": "component", "component": "y"},
)

CURRENT_DENSITY_Z = Field(
    name="CurrentDensity_z",
    symbol="J_z",
    unit=ureg.ampere / ureg.meter**2,
    description="Current density z-component",
    latex_symbol=r"$J_z$",
    aliases=["Jz", "J_z"],
    metadata={"category": "electromagnetic", "type": "component", "component": "z"},
)

# Potential
POTENTIAL = Field(
    name="Potential",
    symbol="V",
    unit=ureg.volt,
    description="Electric potential",
    latex_symbol=r"$V$",
    aliases=["V", "potential", "electric_potential"],
    metadata={"category": "electromagnetic"},
)


# List of all electromagnetic fields for bulk registration
ELECTROMAGNETIC_FIELDS = [
    MAGNETIC_FIELD,
    MAGNETIC_FIELD_X,
    MAGNETIC_FIELD_Y,
    MAGNETIC_FIELD_Z,
    ELECTRIC_FIELD,
    ELECTRIC_FIELD_X,
    ELECTRIC_FIELD_Y,
    ELECTRIC_FIELD_Z,
    CURRENT_DENSITY,
    CURRENT_DENSITY_X,
    CURRENT_DENSITY_Y,
    CURRENT_DENSITY_Z,
    POTENTIAL,
]


def register_electromagnetic_fields(registry: FieldRegistry | None = None) -> None:
    """
    Register all standard electromagnetic fields with a registry.

    If no registry is provided, registers with the default global registry.

    Args:
        registry: FieldRegistry to register with (uses default if None)

    Example:
        >>> from python_magnetunits import FieldRegistry
        >>> from python_magnetunits.physics import electromagnetic
        >>> registry = FieldRegistry()
        >>> electromagnetic.register_electromagnetic_fields(registry)
        >>> field = registry.get("MagneticField")
    """
    if registry is None:
        from ..registry import default_registry

        registry = default_registry

    registry.bulk_register(ELECTROMAGNETIC_FIELDS)
