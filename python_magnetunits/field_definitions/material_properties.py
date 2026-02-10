# python_magnetunits/field_definitions/material_properties.py
from field_framework import Field, ureg

def create_material_property_fields():
    """Create standard material property field definitions."""
    return [
        # Mechanical properties
        Field(
            name="Density",
            symbol="ρ",
            unit=ureg.kg / ureg.meter**3,
            description="Mass density",
            latex_symbol=r"$\rho$",
            aliases=["density", "rho", "mass_density"],
            metadata={"category": "material_property", "physics": "mechanical"}
        ),
        Field(
            name="YoungModulus",
            symbol="E",
            unit=ureg.pascal,
            description="Young's modulus (elastic modulus)",
            latex_symbol=r"$E$",
            aliases=["young_modulus", "elastic_modulus", "E_modulus"],
            metadata={"category": "material_property", "physics": "mechanical"}
        ),
        Field(
            name="PoissonRatio",
            symbol="ν",
            unit=ureg.dimensionless,
            description="Poisson's ratio",
            latex_symbol=r"$\nu$",
            aliases=["poisson_ratio", "nu", "poisson"],
            metadata={"category": "material_property", "physics": "mechanical"}
        ),
        
        # Electrical properties
        Field(
            name="ElectricalResistivity",
            symbol="ρ_e",
            unit=ureg.ohm * ureg.meter,
            description="Electrical resistivity",
            latex_symbol=r"$\rho_e$",
            aliases=["resistivity", "rho_e", "electrical_resistivity"],
            metadata={"category": "material_property", "physics": "electrical"}
        ),
        Field(
            name="ElectricalConductivity",
            symbol="σ",
            unit=ureg.siemens / ureg.meter,
            description="Electrical conductivity",
            latex_symbol=r"$\sigma$",
            aliases=["conductivity", "sigma", "electrical_conductivity"],
            metadata={"category": "material_property", "physics": "electrical"}
        ),
        Field(
            name="RelativePermittivity",
            symbol="ε_r",
            unit=ureg.dimensionless,
            description="Relative permittivity (dielectric constant)",
            latex_symbol=r"$\varepsilon_r$",
            aliases=["permittivity", "epsilon_r", "dielectric_constant"],
            metadata={"category": "material_property", "physics": "electrical"}
        ),
        
        # Thermal properties
        Field(
            name="ThermalConductivity",
            symbol="k",
            unit=ureg.watt / (ureg.meter * ureg.kelvin),
            description="Thermal conductivity",
            latex_symbol=r"$k$",
            aliases=["thermal_conductivity", "k_thermal"],
            metadata={"category": "material_property", "physics": "thermal"}
        ),
        Field(
            name="SpecificHeat",
            symbol="c_p",
            unit=ureg.joule / (ureg.kg * ureg.kelvin),
            description="Specific heat capacity at constant pressure",
            latex_symbol=r"$c_p$",
            aliases=["specific_heat", "heat_capacity", "cp"],
            metadata={"category": "material_property", "physics": "thermal"}
        ),
        Field(
            name="ThermalExpansion",
            symbol="α",
            unit=1 / ureg.kelvin,
            description="Coefficient of thermal expansion",
            latex_symbol=r"$\alpha$",
            aliases=["thermal_expansion", "alpha", "expansion_coefficient"],
            metadata={"category": "material_property", "physics": "thermal"}
        ),
        Field(
            name="ThermalDiffusivity",
            symbol="α_th",
            unit=ureg.meter**2 / ureg.second,
            description="Thermal diffusivity",
            latex_symbol=r"$\alpha_{th}$",
            aliases=["thermal_diffusivity", "alpha_th", "diffusivity"],
            metadata={"category": "material_property", "physics": "thermal"}
        ),
        
        # Magnetic properties
        Field(
            name="RelativePermeability",
            symbol="μ_r",
            unit=ureg.dimensionless,
            description="Relative magnetic permeability",
            latex_symbol=r"$\mu_r$",
            aliases=["permeability", "mu_r", "magnetic_permeability"],
            metadata={"category": "material_property", "physics": "magnetic"}
        ),
        Field(
            name="MagneticSusceptibility",
            symbol="χ",
            unit=ureg.dimensionless,
            description="Magnetic susceptibility",
            latex_symbol=r"$\chi$",
            aliases=["susceptibility", "chi", "magnetic_susceptibility"],
            metadata={"category": "material_property", "physics": "magnetic"}
        ),
    ]
