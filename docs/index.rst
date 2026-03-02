python_magnetunits
==================

**Shared field and unit management for scientific computing with Python**

A robust, type-safe Python package for managing physical fields and units across
scientific computing applications. Provides centralized field definitions, flexible
lookup registries, and seamless unit conversion using the `pint
<https://pint.readthedocs.io>`_ library.

.. code-block:: python

   from python_magnetunits import FieldRegistry
   from python_magnetunits.physics import electromagnetic

   registry = FieldRegistry()
   electromagnetic.register_electromagnetic_fields(registry)

   B = registry.get("MagneticField")
   print(B.convert(1.5, "Gauss"))   # 15000.0
   print(B.format_label("Gauss", use_latex=True))  # "$B$ [G]"

Features
--------

* **Type-safe** field definitions backed by :mod:`pint` units
* **Flexible lookup** by name, symbol, or alias via :class:`~python_magnetunits.FieldRegistry`
* **Unit conversion** for single values and arrays
* **Plot labels** with optional LaTeX rendering
* **Domain exclusions** for multi-domain simulations
* **Pre-defined fields** for four physics domains: electromagnetic, thermal, hydraulics, mechanical
* **Backwards-compatible** helpers for legacy dict-based field systems

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   getting_started
   physics_domains
   formats

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index

.. toctree::
   :maxdepth: 1
   :caption: Development

   changelog

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
