"""
Unit conversion utilities for field values and arrays.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from .field import ureg


def convert_data(
    field_units: Dict[str, List[Any]],
    values: Union[List[float], float],
    fieldname: str,
) -> Union[List[float], float]:
    """
    Convert field values from input unit to output unit.

    Maintains backwards compatibility with magnetrun's field_units dict format:
        field_units = {"fieldname": [input_unit, output_unit]}

    Args:
        field_units: Dict mapping field names to [input_unit, output_unit] pairs
        values: Single value or list of values to convert (in input unit)
        fieldname: Name of the field to convert

    Returns:
        Converted value(s) in output unit. Returns input value(s) unchanged
        if fieldname is not in field_units dict.

    Raises:
        KeyError: If fieldname not found in field_units
        pint.DimensionalityError: If units are incompatible

    Example:
        >>> field_units = {
        ...     "MagneticField": [ureg.tesla, ureg.gauss],
        ...     "Temperature": [ureg.kelvin, ureg.celsius],
        ... }
        >>> convert_data(field_units, 1.5, "MagneticField")
        15000.0
        >>> convert_data(field_units, [1.0, 2.0], "MagneticField")
        [10000.0, 20000.0]
    """
    if fieldname not in field_units:
        return values

    input_unit, output_unit = field_units[fieldname]

    # Handle both single values and lists
    is_list = isinstance(values, list)
    vals = values if is_list else [values]

    converted = []
    for val in vals:
        quantity = ureg.Quantity(val, input_unit)
        converted.append(quantity.to(output_unit).magnitude)

    return converted if is_list else converted[0]


def convert_value(
    value: float,
    from_unit: Union[str, Any],
    to_unit: Union[str, Any],
) -> float:
    """
    Convert a single value between units.

    This is a simple utility function for direct unit conversions without
    the context of a specific field.

    Args:
        value: Value to convert
        from_unit: Source unit (string or pint Unit)
        to_unit: Target unit (string or pint Unit)

    Returns:
        Converted value

    Raises:
        pint.DimensionalityError: If units are incompatible
        pint.UndefinedUnitError: If unit string is not recognized

    Example:
        >>> convert_value(1.0, "tesla", "gauss")
        10000.0
        >>> convert_value(100, "millimeter", "centimeter")
        10.0
    """
    quantity = ureg.Quantity(value, from_unit)
    return quantity.to(to_unit).magnitude


def convert_array(
    values: List[float],
    from_unit: Union[str, Any],
    to_unit: Union[str, Any],
) -> List[float]:
    """
    Convert an array of values between units.

    Args:
        values: List of values to convert
        from_unit: Source unit (string or pint Unit)
        to_unit: Target unit (string or pint Unit)

    Returns:
        List of converted values

    Example:
        >>> convert_array([1.0, 2.0], "meter", "centimeter")
        [100.0, 200.0]
    """
    return [convert_value(v, from_unit, to_unit) for v in values]


def get_unit_string(unit: Union[str, Any], pretty: bool = True) -> str:
    """
    Get a string representation of a unit.

    Args:
        unit: Unit to format (string or pint Unit)
        pretty: If True, use pretty formatting; otherwise use compact format

    Returns:
        Formatted unit string

    Example:
        >>> get_unit_string("tesla")
        'tesla'
        >>> get_unit_string(ureg.tesla, pretty=True)
        'tesla'
        >>> get_unit_string(ureg.volt / ureg.meter, pretty=True)
        'volt / meter'
    """
    if isinstance(unit, str):
        return unit

    if pretty:
        return f"{unit:~P}"  # Pretty format with ~P
    else:
        return f"{unit:P}"  # Compact format


def are_compatible(
    unit1: Union[str, Any],
    unit2: Union[str, Any],
) -> bool:
    """
    Check if two units are dimensionally compatible.

    Args:
        unit1: First unit (string or pint Unit)
        unit2: Second unit (string or pint Unit)

    Returns:
        True if units are compatible, False otherwise

    Example:
        >>> are_compatible("meter", "centimeter")
        True
        >>> are_compatible("tesla", "gauss")
        True
        >>> are_compatible("tesla", "meter")
        False
    """
    try:
        u1 = ureg(unit1) if isinstance(unit1, str) else unit1
        u2 = ureg(unit2) if isinstance(unit2, str) else unit2
        # Try to convert from u1 to u2
        ureg.Quantity(1, u1).to(u2)
        return True
    except (TypeError, ValueError):
        return False
