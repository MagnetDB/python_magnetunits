Physics Domains
===============

The :mod:`python_magnetunits.physics` sub-package provides pre-defined
:class:`~python_magnetunits.Field` collections for four physics domains.
Each module exports:

* Module-level ``Field`` constants (e.g. ``MAGNETIC_FIELD``, ``PRESSURE``).
* A ``DOMAIN_FIELDS`` list containing all fields in that domain.
* A ``register_domain_fields(registry=None)`` helper that registers the full
  collection with a :class:`~python_magnetunits.FieldRegistry`.

All domain registration functions default to the global
:data:`~python_magnetunits.default_registry` when no registry is passed.

----

Electromagnetic
---------------

Module: :mod:`python_magnetunits.physics.electromagnetic`

.. code-block:: python

   from python_magnetunits import FieldRegistry
   from python_magnetunits.physics import electromagnetic

   registry = FieldRegistry()
   electromagnetic.register_electromagnetic_fields(registry)

Fields
~~~~~~

=========================== ======= =============================
Name                        Symbol  Unit
=========================== ======= =============================
``MagneticField``           B       tesla
``MagneticField_x``         B_x     tesla
``MagneticField_y``         B_y     tesla
``MagneticField_z``         B_z     tesla
``ElectricField``           E       volt / meter
``CurrentDensity``          J       ampere / meter²
``Potential``               V       volt
``Conductivity``            σ       siemens / meter
``Permeability``            μ       henry / meter
``RelativePermeability``    μ_r     dimensionless
``RelativePermittivity``    ε_r     dimensionless
=========================== ======= =============================

----

Thermal
-------

Module: :mod:`python_magnetunits.physics.thermal`

.. code-block:: python

   from python_magnetunits import FieldRegistry
   from python_magnetunits.physics import thermal

   registry = FieldRegistry()
   thermal.register_thermal_fields(registry)

Fields
~~~~~~

================================= ======= =============================
Name                              Symbol  Unit
================================= ======= =============================
``Temperature``                   T       kelvin
``HeatFlux``                      q       watt / meter²
``HeatFlux_x``                    q_x     watt / meter²
``HeatFlux_y``                    q_y     watt / meter²
``HeatFlux_z``                    q_z     watt / meter²
``ThermalConductivity``           k       watt / (meter · kelvin)
``HeatTransferCoefficient``       h       watt / (meter² · kelvin)
``SpecificHeat``                  c_p     joule / (kilogram · kelvin)
``ThermalExpansion``              α       1 / kelvin
``ThermalDiffusivity``            α_th    meter² / second
================================= ======= =============================

.. note::
   ``Temperature`` and ``ThermalConductivity`` have ``exclude_regions=["Air"]``
   set by default, as these fields are typically not solved in air gaps.

----

Hydraulics
----------

Module: :mod:`python_magnetunits.physics.hydraulics`

.. code-block:: python

   from python_magnetunits import FieldRegistry
   from python_magnetunits.physics import hydraulics

   registry = FieldRegistry()
   hydraulics.register_hydraulic_fields(registry)

Fields
~~~~~~

========================= ======= ==============================
Name                      Symbol  Unit
========================= ======= ==============================
``Pressure``              P       pascal
``PressureDrop``          ΔP      pascal
``FlowRate``              Q       meter³ / second
``MassFlowRate``          ṁ       kilogram / second
``Velocity``              v       meter / second
``Velocity_x``            v_x     meter / second
``Velocity_y``            v_y     meter / second
``Velocity_z``            v_z     meter / second
``DynamicViscosity``      μ       pascal · second
``KinematicViscosity``    ν       meter² / second
``Density``               ρ       kilogram / meter³
========================= ======= ==============================

----

Mechanical
----------

Module: :mod:`python_magnetunits.physics.mechanical`

.. code-block:: python

   from python_magnetunits import FieldRegistry
   from python_magnetunits.physics import mechanical

   registry = FieldRegistry()
   mechanical.register_mechanical_fields(registry)

Fields
~~~~~~

================================ ======= =============================
Name                             Symbol  Unit
================================ ======= =============================
``Force``                        F       newton
``Force_x``                      F_x     newton
``Force_y``                      F_y     newton
``Force_z``                      F_z     newton
``Stress``                       σ       pascal
``Strain``                       ε       dimensionless
``Displacement``                 u       meter
``Displacement_x``               u_x     meter
``Displacement_y``               u_y     meter
``Displacement_z``               u_z     meter
``YoungModulus``                 E       pascal
``PoissonRatio``                 ν       dimensionless
``Density``                      ρ       kilogram / meter³
``ThermalExpansionCoefficient``  α       1 / kelvin
================================ ======= =============================

Combining Domains
-----------------

Multiple domains can be registered in the same registry.  The only constraint
is that aliases must remain unambiguous — if two fields share an alias and both
are registered, :meth:`~python_magnetunits.FieldRegistry.get` returns ``None``
for that alias (ambiguous lookup) while name and symbol lookups still work:

.. code-block:: python

   from python_magnetunits import FieldRegistry
   from python_magnetunits.physics import electromagnetic, thermal, hydraulics, mechanical

   registry = FieldRegistry()
   electromagnetic.register_electromagnetic_fields(registry)
   thermal.register_thermal_fields(registry)
   hydraulics.register_hydraulic_fields(registry)
   mechanical.register_mechanical_fields(registry)

   print(len(registry))   # combined field count

   B = registry.get("MagneticField")
   T = registry.get("Temperature")
   P = registry.get("Pressure")
   F = registry.get("Force")
