Getting Started
===============

Installation
------------

Install from PyPI::

   pip install python_magnetunits

Or install in development mode from source::

   git clone https://github.com/MagnetDB/python_magnetunits.git
   cd python_magnetunits
   pip install -e ".[dev]"

Requirements:

* Python 3.9+
* pint >= 0.20

Basic Usage
-----------

Using Pre-defined Fields
~~~~~~~~~~~~~~~~~~~~~~~~

The package ships with a standard library of physical fields organised by domain.
The quickest way to get started is to register one of the pre-defined domain
collections and then look up fields by name, symbol, or alias:

.. code-block:: python

   from python_magnetunits import FieldRegistry
   from python_magnetunits.physics import electromagnetic

   registry = FieldRegistry()
   electromagnetic.register_electromagnetic_fields(registry)

   # Lookup by name, symbol, or alias
   B = registry.get("MagneticField")   # by name
   B = registry.get("B")               # by symbol
   B = registry.get("B_field")         # by alias

   # Convert a value
   value_in_gauss = B.convert(1.5, "Gauss")    # 15000.0

   # Generate a plot axis label
   label = B.format_label("Gauss", use_latex=True)  # "$B$ [G]"

Defining Custom Fields
~~~~~~~~~~~~~~~~~~~~~~

You can define your own fields alongside (or instead of) the pre-defined ones:

.. code-block:: python

   from python_magnetunits import Field, FieldRegistry, ureg

   temperature = Field(
       name="Temperature",
       symbol="T",
       unit=ureg.kelvin,
       description="Absolute temperature",
       latex_symbol=r"$T$",
       aliases=["temp", "T_absolute"],
       exclude_regions=["vacuum"],
       metadata={"category": "thermal"},
   )

   registry = FieldRegistry()
   registry.register(temperature)

   temp_celsius = temperature.convert(273.15, "degC")  # 0.0
   label = temperature.format_label("degC")            # "T [°C]"

Using FieldType for Validated Fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`~python_magnetunits.FieldType` provides a catalogue of well-known field
categories. When you attach a ``FieldType`` to a :class:`~python_magnetunits.Field`,
the unit dimensionality is validated at construction time:

.. code-block:: python

   from python_magnetunits import Field, FieldType, ureg

   # This works — tesla is dimensionally correct for MAGNETIC_FIELD
   B = Field(
       name="MagneticField",
       symbol="B",
       unit=ureg.tesla,
       field_type=FieldType.MAGNETIC_FIELD,
   )

   # This raises ValueError — meter is not compatible with MAGNETIC_FIELD
   # Field(name="Wrong", symbol="X", unit=ureg.meter, field_type=FieldType.MAGNETIC_FIELD)

You can also create fields directly from a ``FieldType`` using the factory
:meth:`~python_magnetunits.Field.from_field_type`, which fills in sensible
defaults (symbol, unit, LaTeX symbol) automatically:

.. code-block:: python

   from python_magnetunits import Field, FieldType

   B = Field.from_field_type(FieldType.MAGNETIC_FIELD)
   print(B.symbol)   # "B"
   print(B.unit)     # tesla

   # Override specific attributes
   B_mT = Field.from_field_type(
       FieldType.MAGNETIC_FIELD,
       name="B_mT",
       unit="millitesla",
   )

Converting Arrays of Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from python_magnetunits import Field

   field = Field(name="B", symbol="B", unit="tesla")
   values_tesla = [1.0, 2.0, 3.0]
   values_gauss = field.convert_array(values_tesla, "Gauss")
   # [10000.0, 20000.0, 30000.0]

Backwards-Compatible Conversion Helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are migrating from an older dict-based system, the :mod:`~python_magnetunits.converters`
module provides drop-in replacements:

.. code-block:: python

   from python_magnetunits import convert_data, convert_value, are_compatible, ureg

   field_units = {
       "MagneticField": [ureg.tesla, ureg.Gauss],
       "Temperature":   [ureg.kelvin, ureg.degC],
   }

   # Single value
   B_gauss = convert_data(field_units, 1.5, "MagneticField")   # 15000.0

   # Arrays
   vals = convert_data(field_units, [1.0, 2.0], "MagneticField")  # [10000.0, 20000.0]

   # Compatibility check
   print(are_compatible("tesla", "Gauss"))  # True
   print(are_compatible("tesla", "meter"))  # False

Registry Operations
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from python_magnetunits import FieldRegistry
   from python_magnetunits.physics import electromagnetic, thermal

   registry = FieldRegistry()
   electromagnetic.register_electromagnetic_fields(registry)
   thermal.register_thermal_fields(registry)

   # Count fields
   print(len(registry))   # 23

   # Check membership
   print("B" in registry)   # True

   # List all fields (or filter by category)
   all_fields = registry.list_fields()
   em_fields  = registry.list_fields(category="electromagnetic")

   # Remove a field
   registry.remove("Temperature")

Custom Units
~~~~~~~~~~~~

The package extends pint's unit registry with a small set of units commonly needed
in electromagnetic and scientific computing contexts:

======= ========================== =========================
Symbol  Definition                 Use case
======= ========================== =========================
``%``   ``0.01``                   Percentages
``ppm`` ``1e-6``                   Parts per million
``var`` ``volt * ampere``          Reactive power (VAr)
``G``   ``1e-4 tesla`` (custom)    Magnetic flux density
======= ========================== =========================

.. note::

   pint ships with a built-in CGS ``gauss`` that has *different dimensionality*
   from the SI ``tesla`` family.  This package defines a custom ``Gauss``
   (capital G, alias ``G``) that converts correctly as ``1 T = 10 000 G``.

.. code-block:: python

   from python_magnetunits import ureg

   q = ureg.Quantity(1.0, "tesla")
   print(q.to("Gauss").magnitude)  # 10000.0
