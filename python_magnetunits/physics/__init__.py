"""
Standard field definitions for scientific computing.

This package provides pre-defined field collections organized by physics domain:

- electromagnetic: Magnetic/electric fields, current, voltage, EM material properties
- thermal: Temperature, heat flux, thermal material properties
- hydraulics: Pressure, flow rate, velocity, fluid properties
- mechanical: Stress, strain, displacement, mechanical material properties
"""

from . import electromagnetic
from . import thermal
from . import hydraulics
from . import mechanical

__all__ = [
    "electromagnetic",
    "thermal",
    "hydraulics",
    "mechanical",
]

