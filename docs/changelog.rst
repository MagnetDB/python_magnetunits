Changelog
=========

v0.1.0
------

Initial release.

* :class:`~python_magnetunits.Field` dataclass with integrated pint unit management.
* :class:`~python_magnetunits.FieldType` enum with 41 well-known field categories
  and unit-compatibility validation.
* :class:`~python_magnetunits.FieldRegistry` with name/symbol/alias lookup and
  correct stale-entry cleanup on re-registration.
* :mod:`~python_magnetunits.converters` — backwards-compatible unit conversion
  helpers for dict-based field definitions.
* :mod:`~python_magnetunits.formats` — JSON/YAML field definition import/export
  with full round-trip serialisation.
* :mod:`~python_magnetunits.physics` — pre-defined fields for four domains:

  * :mod:`~python_magnetunits.physics.electromagnetic` (13 fields)
  * :mod:`~python_magnetunits.physics.thermal` (10 fields)
  * :mod:`~python_magnetunits.physics.hydraulics` (11 fields)
  * :mod:`~python_magnetunits.physics.mechanical` (14+ fields)

* Custom SI-compatible ``Gauss`` unit (``1 G = 1e-4 T``).
* Custom ``percent``, ``ppm``, and ``var`` (reactive power) units.
