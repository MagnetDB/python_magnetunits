Format Definitions
==================

The :mod:`python_magnetunits.formats` sub-package provides helpers for loading
and saving field definitions from JSON or YAML configuration files.

This is useful for persisting field configurations, sharing them between
projects, or migrating from legacy dict-based systems.

FieldDefinition
---------------

:class:`~python_magnetunits.formats.format_definition.FieldDefinition` is a
lightweight data container that mirrors the :class:`~python_magnetunits.Field`
attributes but stores everything as plain Python types (strings, lists, dicts).

.. code-block:: python

   from python_magnetunits.formats.format_definition import FieldDefinition

   defn = FieldDefinition(
       name="MagneticField",
       symbol="B",
       unit="tesla",
       latex_symbol=r"$B$",
       aliases=["B_field", "magnetic_flux_density"],
       field_type="MAGNETIC_FIELD",
   )

   # Convert to a Field object
   field = defn.to_field()

FormatDefinition
----------------

:class:`~python_magnetunits.formats.format_definition.FormatDefinition` manages
a collection of :class:`~python_magnetunits.formats.format_definition.FieldDefinition`
objects.  It supports:

* Loading from a ``dict`` (e.g. parsed JSON/YAML)
* Serialising back to a ``dict`` (round-trip safe)
* Registering all contained fields with a :class:`~python_magnetunits.FieldRegistry`

.. code-block:: python

   from python_magnetunits.formats.format_definition import FormatDefinition
   from python_magnetunits import FieldRegistry

   data = {
       "fields": [
           {
               "name": "MagneticField",
               "symbol": "B",
               "unit": "tesla",
               "latex_symbol": "$B$",
               "aliases": ["B_field"],
               "field_type": "MAGNETIC_FIELD",
           }
       ]
   }

   fmt = FormatDefinition.from_dict(data)

   # Register all contained fields
   registry = FieldRegistry()
   fmt.register_fields(registry)

   # Round-trip serialisation
   serialised = fmt.to_dict()

.. seealso::

   :mod:`python_magnetunits.formats.format_definition` — full API reference.
