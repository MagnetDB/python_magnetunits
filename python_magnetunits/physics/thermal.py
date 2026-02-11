"""
Standard thermal field definitions.

This module defines commonly used thermal fields that can be registered
with a FieldRegistry for use across scientific computing applications.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from ..field import Field, ureg
from ..field_types import FieldType

if TYPE_CHECKING:
    from ..registry import FieldRegistry


# =============================================================================
# Temperature
# =============================================================================

TEMPERATURE = Field(
    name="Temperature",
    symbol="T",
    unit=ureg.kelvin,
    field_type=FieldType.TEMPERATURE,
    description="Absolute temperature",
    latex_symbol=r"$T$",
    aliases=["T", "temp", "temperature"],
    exclude_regions=["Air"],
    metadata={"category": "thermal", "type": "scalar"},
)


# =============================================================================
# Heat Flux
# =============================================================================

HEAT_FLUX = Field(
    name="HeatFlux",
    symbol="q",
    unit=ureg.watt / ureg.meter**2,
    field_type=FieldType.HEAT_FLUX,
    description="Heat flux (power per unit area)",
    latex_symbol=r"$q$",
    aliases=["q", "heat_flux", "thermal_flux"],
    metadata={"category": "thermal", "type": "scalar"},
)

HEAT_FLUX_X = Field(
    name="HeatFlux_x",
    symbol="q_x",
    unit=ureg.watt / ureg.meter**2,
    field_type=FieldType.HEAT_FLUX,
    description="Heat flux x-component",
    latex_symbol=r"$q_x$",
    aliases=["qx", "q_x", "heat_flux_x"],
    metadata={"category": "thermal", "type": "component", "component": "x"},
)

HEAT_FLUX_Y = Field(
    name="HeatFlux_y",
    symbol="q_y",
    unit=ureg.watt / ureg.meter**2,
    field_type=FieldType.HEAT_FLUX,
    description="Heat flux y-component",
    latex_symbol=r"$q_y$",
    aliases=["qy", "q_y", "heat_flux_y"],
    metadata={"category": "thermal", "type": "component", "component": "y"},
)

HEAT_FLUX_Z = Field(
    name="HeatFlux_z",
    symbol="q_z",
    unit=ureg.watt / ureg.meter**2,
    field_type=FieldType.HEAT_FLUX,
    description="Heat flux z-component",
    latex_symbol=r"$q_z$",
    aliases=["qz", "q_z", "heat_flux_z"],
    metadata={"category": "thermal", "type": "component", "component": "z"},
)


# =============================================================================
# Thermal Material Properties
# =============================================================================

THERMAL_CONDUCTIVITY = Field(
    name="ThermalConductivity",
    symbol="k",
    unit=ureg.watt / (ureg.meter * ureg.kelvin),
    field_type=FieldType.THERMAL_CONDUCTIVITY,
    description="Thermal conductivity",
    latex_symbol=r"$k$",
    aliases=["k", "k_thermal", "thermal_conductivity"],
    exclude_regions=["Air"],
    metadata={"category": "thermal", "type": "material_property"},
)

HEAT_TRANSFER_COEFFICIENT = Field(
    name="HeatTransferCoefficient",
    symbol="h",
    unit=ureg.watt / (ureg.meter**2 * ureg.kelvin),
    field_type=FieldType.HEAT_TRANSFER_COEFFICIENT,
    description="Convective heat transfer coefficient",
    latex_symbol=r"$h$",
    aliases=["h", "htc", "heat_transfer_coefficient", "convection_coefficient"],
    metadata={"category": "thermal", "type": "material_property"},
)

SPECIFIC_HEAT = Field(
    name="SpecificHeat",
    symbol="c_p",
    unit=ureg.joule / (ureg.kilogram * ureg.kelvin),
    field_type=FieldType.SPECIFIC_HEAT,
    description="Specific heat capacity at constant pressure",
    latex_symbol=r"$c_p$",
    aliases=["cp", "c_p", "specific_heat", "heat_capacity"],
    metadata={"category": "thermal", "type": "material_property"},
)

THERMAL_EXPANSION = Field(
    name="ThermalExpansion",
    symbol="α",
    unit=1 / ureg.kelvin,
    field_type=FieldType.THERMAL_EXPANSION,
    description="Coefficient of thermal expansion",
    latex_symbol=r"$\alpha$",
    aliases=["alpha", "thermal_expansion", "expansion_coefficient", "cte"],
    metadata={"category": "thermal", "type": "material_property"},
)

THERMAL_DIFFUSIVITY = Field(
    name="ThermalDiffusivity",
    symbol="α_th",
    unit=ureg.meter**2 / ureg.second,
    field_type=FieldType.THERMAL_DIFFUSIVITY,
    description="Thermal diffusivity",
    latex_symbol=r"$\alpha_{th}$",
    aliases=["alpha_th", "thermal_diffusivity", "diffusivity"],
    metadata={"category": "thermal", "type": "material_property"},
)


# =============================================================================
# Field Collections
# =============================================================================

# Heat flux and components
HEAT_FLUX_FIELDS: List[Field] = [
    HEAT_FLUX,
    HEAT_FLUX_X,
    HEAT_FLUX_Y,
    HEAT_FLUX_Z,
]

# Material properties
THERMAL_MATERIAL_PROPERTIES: List[Field] = [
    THERMAL_CONDUCTIVITY,
    HEAT_TRANSFER_COEFFICIENT,
    SPECIFIC_HEAT,
    THERMAL_EXPANSION,
    THERMAL_DIFFUSIVITY,
]

# All thermal fields
THERMAL_FIELDS: List[Field] = [
    TEMPERATURE,
] + HEAT_FLUX_FIELDS + THERMAL_MATERIAL_PROPERTIES


def register_thermal_fields(registry: "FieldRegistry") -> None:
    """
    Register all standard thermal fields with a registry.

    Args:
        registry: FieldRegistry to register fields with

    Example:
        >>> from python_magnetunits import FieldRegistry
        >>> from python_magnetunits.physics import thermal
        >>> registry = FieldRegistry()
        >>> thermal.register_thermal_fields(registry)
        >>> field = registry.get("Temperature")
    """
    registry.bulk_register(THERMAL_FIELDS)


def register_thermal_material_properties(registry: "FieldRegistry") -> None:
    """Register only thermal material property fields."""
    registry.bulk_register(THERMAL_MATERIAL_PROPERTIES)
