# field_framework/standard_fields/electromagnetic.py
from ..field import Field, ureg
from ..registry import default_registry

# Define standard electromagnetic fields
ELECTROMAGNETIC_FIELDS = [
    Field(
        name="MagneticField",
        symbol="B",
        unit=ureg.tesla,
        description="Magnetic flux density",
        latex_symbol=r"$B$",
        aliases=["magnetic_field", "B"],
        metadata={"category": "electromagnetic"}
    ),
    Field(
        name="MagneticField_x",
        symbol="Bx",
        unit=ureg.tesla,
        description="Magnetic field x-component",
        latex_symbol=r"$B_x$",
        aliases=["Bx"],
        metadata={"category": "electromagnetic", "component": "x"}
    ),
    # ... more fields
]

def register_electromagnetic_fields():
    """Register all electromagnetic fields with default registry"""
    default_registry.bulk_register(ELECTROMAGNETIC_FIELDS)
