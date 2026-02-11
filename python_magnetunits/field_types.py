"""
Canonical field type classifications for magnet-related applications.

This module defines FieldType enum which categorizes physical quantities
used across magnet-related Python packages. Each type has a default SI unit
and symbol, and provides validation for unit compatibility.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict

from .field import ureg


class FieldType(Enum):
    """
    Field type categories for physical quantities.

    Each type defines:
    - A canonical name (enum value)
    - Default SI unit (for validation/conversion)
    - Default symbol

    Example:
        >>> ftype = FieldType.MAGNETIC_FIELD
        >>> ftype.default_unit
        <Unit('tesla')>
        >>> ftype.default_symbol
        'B'
        >>> ftype.is_compatible(ureg.gauss)
        True
        >>> ftype.is_compatible(ureg.meter)
        False
    """

    # === Time ===
    TIME = "time"

    # === Electromagnetic Fields ===
    MAGNETIC_FIELD = "magnetic_field"
    ELECTRIC_FIELD = "electric_field"
    CURRENT = "current"
    CURRENT_DENSITY = "current_density"
    VOLTAGE = "voltage"

    # === Electromagnetic Material Properties ===
    RESISTANCE = "resistance"
    INDUCTANCE = "inductance"
    ELECTRICAL_RESISTIVITY = "electrical_resistivity"
    ELECTRICAL_CONDUCTIVITY = "electrical_conductivity"
    RELATIVE_PERMITTIVITY = "relative_permittivity"
    RELATIVE_PERMEABILITY = "relative_permeability"
    MAGNETIC_SUSCEPTIBILITY = "magnetic_susceptibility"

    # === Electrical Power ===
    POWER = "power"
    REACTIVE_POWER = "reactive_power"

    # === Thermal Fields ===
    TEMPERATURE = "temperature"
    HEAT_FLUX = "heat_flux"

    # === Thermal Material Properties ===
    THERMAL_CONDUCTIVITY = "thermal_conductivity"
    HEAT_TRANSFER_COEFFICIENT = "heat_transfer_coefficient"
    SPECIFIC_HEAT = "specific_heat"
    THERMAL_EXPANSION = "thermal_expansion"
    THERMAL_DIFFUSIVITY = "thermal_diffusivity"

    # === Hydraulics / Thermohydraulics ===
    PRESSURE = "pressure"
    FLOW_RATE = "flow_rate"
    VELOCITY = "velocity"
    DYNAMIC_VISCOSITY = "dynamic_viscosity"
    KINEMATIC_VISCOSITY = "kinematic_viscosity"

    # === Mechanical Fields ===
    FORCE = "force"
    STRESS = "stress"
    STRAIN = "strain"

    # === Mechanical Material Properties ===
    DENSITY = "density"
    YOUNG_MODULUS = "young_modulus"
    POISSON_RATIO = "poisson_ratio"

    # === Other ===
    ROTATION_SPEED = "rotation_speed"
    PERCENTAGE = "percentage"

    # === Geometry ===
    COORDINATE = "coordinate"
    LENGTH = "length"
    AREA = "area"
    VOLUME = "volume"
    INDEX = "index"

    @property
    def default_unit(self) -> Any:
        """Return default SI unit for this field type."""
        return _FIELD_TYPE_UNITS[self]

    @property
    def default_symbol(self) -> str:
        """Return default symbol for this field type."""
        return _FIELD_TYPE_SYMBOLS[self]

    @property
    def latex_symbol(self) -> str:
        """Return default LaTeX symbol for this field type."""
        return _FIELD_TYPE_LATEX[self]

    def is_compatible(self, unit: Any) -> bool:
        """
        Check if a unit is dimensionally compatible with this field type.

        Args:
            unit: A pint unit or unit string to check

        Returns:
            True if the unit has the same dimensionality as this field type

        Example:
            >>> FieldType.MAGNETIC_FIELD.is_compatible("gauss")
            True
            >>> FieldType.MAGNETIC_FIELD.is_compatible("meter")
            False
        """
        try:
            if isinstance(unit, str):
                unit = ureg(unit)
            ureg.Quantity(1, unit).to(self.default_unit)
            return True
        except Exception:
            return False


# === Default Units (SI base) ===
_FIELD_TYPE_UNITS: Dict[FieldType, Any] = {
    # Time
    FieldType.TIME: ureg.second,
    # Electromagnetic Fields
    FieldType.MAGNETIC_FIELD: ureg.tesla,
    FieldType.ELECTRIC_FIELD: ureg.volt / ureg.meter,
    FieldType.CURRENT: ureg.ampere,
    FieldType.CURRENT_DENSITY: ureg.ampere / ureg.meter**2,
    FieldType.VOLTAGE: ureg.volt,
    # Electromagnetic Material Properties
    FieldType.RESISTANCE: ureg.ohm,
    FieldType.INDUCTANCE: ureg.henry,
    FieldType.ELECTRICAL_RESISTIVITY: ureg.ohm * ureg.meter,
    FieldType.ELECTRICAL_CONDUCTIVITY: ureg.siemens / ureg.meter,
    FieldType.RELATIVE_PERMITTIVITY: ureg.dimensionless,
    FieldType.RELATIVE_PERMEABILITY: ureg.dimensionless,
    FieldType.MAGNETIC_SUSCEPTIBILITY: ureg.dimensionless,
    # Electrical Power
    FieldType.POWER: ureg.watt,
    FieldType.REACTIVE_POWER: ureg.var,
    # Thermal Fields
    FieldType.TEMPERATURE: ureg.kelvin,
    FieldType.HEAT_FLUX: ureg.watt / ureg.meter**2,
    # Thermal Material Properties
    FieldType.THERMAL_CONDUCTIVITY: ureg.watt / (ureg.meter * ureg.kelvin),
    FieldType.HEAT_TRANSFER_COEFFICIENT: ureg.watt / (ureg.meter**2 * ureg.kelvin),
    FieldType.SPECIFIC_HEAT: ureg.joule / (ureg.kilogram * ureg.kelvin),
    FieldType.THERMAL_EXPANSION: 1 / ureg.kelvin,
    FieldType.THERMAL_DIFFUSIVITY: ureg.meter**2 / ureg.second,
    # Hydraulics / Thermohydraulics
    FieldType.PRESSURE: ureg.pascal,
    FieldType.FLOW_RATE: ureg.meter**3 / ureg.second,
    FieldType.VELOCITY: ureg.meter / ureg.second,
    FieldType.DYNAMIC_VISCOSITY: ureg.pascal * ureg.second,
    FieldType.KINEMATIC_VISCOSITY: ureg.meter**2 / ureg.second,
    # Mechanical Fields
    FieldType.FORCE: ureg.newton,
    FieldType.STRESS: ureg.pascal,
    FieldType.STRAIN: ureg.dimensionless,
    # Mechanical Material Properties
    FieldType.DENSITY: ureg.kilogram / ureg.meter**3,
    FieldType.YOUNG_MODULUS: ureg.pascal,
    FieldType.POISSON_RATIO: ureg.dimensionless,
    # Other
    FieldType.ROTATION_SPEED: ureg.radian / ureg.second,
    FieldType.PERCENTAGE: ureg.percent,
    # Geometry
    FieldType.COORDINATE: ureg.meter,
    FieldType.LENGTH: ureg.meter,
    FieldType.AREA: ureg.meter**2,
    FieldType.VOLUME: ureg.meter**3,
    FieldType.INDEX: ureg.dimensionless,
}

# === Default Symbols ===
_FIELD_TYPE_SYMBOLS: Dict[FieldType, str] = {
    # Time
    FieldType.TIME: "t",
    # Electromagnetic Fields
    FieldType.MAGNETIC_FIELD: "B",
    FieldType.ELECTRIC_FIELD: "E",
    FieldType.CURRENT: "I",
    FieldType.CURRENT_DENSITY: "J",
    FieldType.VOLTAGE: "U",
    # Electromagnetic Material Properties
    FieldType.RESISTANCE: "R",
    FieldType.INDUCTANCE: "L",
    FieldType.ELECTRICAL_RESISTIVITY: "ρ_e",
    FieldType.ELECTRICAL_CONDUCTIVITY: "σ",
    FieldType.RELATIVE_PERMITTIVITY: "ε_r",
    FieldType.RELATIVE_PERMEABILITY: "μ_r",
    FieldType.MAGNETIC_SUSCEPTIBILITY: "χ",
    # Electrical Power
    FieldType.POWER: "P",
    FieldType.REACTIVE_POWER: "Q",
    # Thermal Fields
    FieldType.TEMPERATURE: "T",
    FieldType.HEAT_FLUX: "q",
    # Thermal Material Properties
    FieldType.THERMAL_CONDUCTIVITY: "k",
    FieldType.HEAT_TRANSFER_COEFFICIENT: "h",
    FieldType.SPECIFIC_HEAT: "c_p",
    FieldType.THERMAL_EXPANSION: "α",
    FieldType.THERMAL_DIFFUSIVITY: "α_th",
    # Hydraulics / Thermohydraulics
    FieldType.PRESSURE: "P",
    FieldType.FLOW_RATE: "Q",
    FieldType.VELOCITY: "v",
    FieldType.DYNAMIC_VISCOSITY: "μ",
    FieldType.KINEMATIC_VISCOSITY: "ν",
    # Mechanical Fields
    FieldType.FORCE: "F",
    FieldType.STRESS: "σ",
    FieldType.STRAIN: "ε",
    # Mechanical Material Properties
    FieldType.DENSITY: "ρ",
    FieldType.YOUNG_MODULUS: "E",
    FieldType.POISSON_RATIO: "ν",
    # Other
    FieldType.ROTATION_SPEED: "ω",
    FieldType.PERCENTAGE: "%",
    # Geometry
    FieldType.COORDINATE: "x",
    FieldType.LENGTH: "L",
    FieldType.AREA: "A",
    FieldType.VOLUME: "V",
    FieldType.INDEX: "i",
}

# === Default LaTeX Symbols ===
_FIELD_TYPE_LATEX: Dict[FieldType, str] = {
    # Time
    FieldType.TIME: r"$t$",
    # Electromagnetic Fields
    FieldType.MAGNETIC_FIELD: r"$B$",
    FieldType.ELECTRIC_FIELD: r"$E$",
    FieldType.CURRENT: r"$I$",
    FieldType.CURRENT_DENSITY: r"$J$",
    FieldType.VOLTAGE: r"$U$",
    # Electromagnetic Material Properties
    FieldType.RESISTANCE: r"$R$",
    FieldType.INDUCTANCE: r"$L$",
    FieldType.ELECTRICAL_RESISTIVITY: r"$\rho_e$",
    FieldType.ELECTRICAL_CONDUCTIVITY: r"$\sigma$",
    FieldType.RELATIVE_PERMITTIVITY: r"$\varepsilon_r$",
    FieldType.RELATIVE_PERMEABILITY: r"$\mu_r$",
    FieldType.MAGNETIC_SUSCEPTIBILITY: r"$\chi$",
    # Electrical Power
    FieldType.POWER: r"$P$",
    FieldType.REACTIVE_POWER: r"$Q$",
    # Thermal Fields
    FieldType.TEMPERATURE: r"$T$",
    FieldType.HEAT_FLUX: r"$q$",
    # Thermal Material Properties
    FieldType.THERMAL_CONDUCTIVITY: r"$k$",
    FieldType.HEAT_TRANSFER_COEFFICIENT: r"$h$",
    FieldType.SPECIFIC_HEAT: r"$c_p$",
    FieldType.THERMAL_EXPANSION: r"$\alpha$",
    FieldType.THERMAL_DIFFUSIVITY: r"$\alpha_{th}$",
    # Hydraulics / Thermohydraulics
    FieldType.PRESSURE: r"$P$",
    FieldType.FLOW_RATE: r"$Q$",
    FieldType.VELOCITY: r"$v$",
    FieldType.DYNAMIC_VISCOSITY: r"$\mu$",
    FieldType.KINEMATIC_VISCOSITY: r"$\nu$",
    # Mechanical Fields
    FieldType.FORCE: r"$F$",
    FieldType.STRESS: r"$\sigma$",
    FieldType.STRAIN: r"$\varepsilon$",
    # Mechanical Material Properties
    FieldType.DENSITY: r"$\rho$",
    FieldType.YOUNG_MODULUS: r"$E$",
    FieldType.POISSON_RATIO: r"$\nu$",
    # Other
    FieldType.ROTATION_SPEED: r"$\omega$",
    FieldType.PERCENTAGE: r"$\%$",
    # Geometry
    FieldType.COORDINATE: r"$x$",
    FieldType.LENGTH: r"$L$",
    FieldType.AREA: r"$A$",
    FieldType.VOLUME: r"$V$",
    FieldType.INDEX: r"$i$",
}
