# field_framework/converters.py
from typing import Dict, List, Union, Any
from .field import Field, ureg

def convert_data(field_units: Dict[str, List], values: Union[List, Any], 
                 fieldname: str) -> Union[List, Any]:
    """
    Convert values from input unit to output unit.
    
    Compatible with existing magnetrun usage pattern:
    field_units = {"fieldname": [input_unit, output_unit]}
    
    Args:
        field_units: Dict mapping field names to [input_unit, output_unit]
        values: Single value or list of values to convert
        fieldname: Name of the field
    
    Returns:
        Converted value(s) in output unit
    """
    if fieldname not in field_units:
        return values
    
    input_unit, output_unit = field_units[fieldname]
    
    is_list = isinstance(values, list)
    vals = values if is_list else [values]
    
    converted = []
    for val in vals:
        quantity = ureg.Quantity(val, input_unit)
        converted.append(quantity.to(output_unit).magnitude)
    
    return converted if is_list else converted[0]


