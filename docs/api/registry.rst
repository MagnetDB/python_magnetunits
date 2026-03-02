FieldRegistry
=============

.. automodule:: python_magnetunits.registry
   :members:
   :undoc-members:
   :show-inheritance:

Module-level instances
----------------------

.. autodata:: python_magnetunits.registry.default_registry
   :annotation: = FieldRegistry()

   The default global :class:`FieldRegistry` instance.  All
   ``register_*_fields()`` functions in the physics sub-package use this
   instance when called without an explicit ``registry`` argument.
