from field_framework import FieldRegistry
from python_magnetunits.field_definitions import (
    create_electromagnetic_fields,
    create_thermal_fields,
    create_material_property_fields
)

# Create registry with all fields
registry = FieldRegistry()
registry.bulk_register(create_electromagnetic_fields())
registry.bulk_register(create_thermal_fields())
registry.bulk_register(create_material_property_fields())

# Look up material property fields
rho_field = registry.get("ρ")  # or "Density" or "rho"
print(f"{rho_field.name}: {rho_field.symbol} [{rho_field.unit}]")
# Output: Density: ρ [kilogram / meter ** 3]

# Get formatted label for plotting
label = rho_field.format_label(target_unit="g/cm^3", use_latex=True)
# Output: "$\rho$ [g/cm³]"

# Convert values (when you have them from elsewhere)
rho_copper = 8.96  # g/cm³
rho_si = rho_field.convert(rho_copper, "kg/m^3")
# Output: 8960.0

# List all material property fields
mat_fields = registry.list_fields(category="material_property")
for field in mat_fields:
    print(f"  - {field.name} ({field.symbol}): {field.unit}")
