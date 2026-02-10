# Your existing code stores material property values
material_data = {
    "Cu": {"rho": 8960, "sigma": 5.96e7, "k": 401},
    "Al": {"rho": 2700, "sigma": 3.77e7, "k": 237}
}

# Use registry for metadata/conversion
rho_field = registry.get("Density")
sigma_field = registry.get("ElectricalConductivity")

# When you need to display or convert
for mat_name, props in material_data.items():
    rho_converted = rho_field.convert(props["rho"], "g/cm^3")
    sigma_label = sigma_field.format_label(use_latex=True)
    print(f"{mat_name}: {rho_converted} g/cm³")
