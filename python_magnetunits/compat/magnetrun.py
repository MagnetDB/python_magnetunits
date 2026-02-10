# field_framework/compat/magnetrun.py
"""
Backwards compatibility layer for magnetrun's fieldunits dict format.
"""
from typing import Dict, List
from ..field import Field, ureg

def field_to_dict(field: Field, input_unit=None, output_unit=None) -> Dict:
    """
    Convert Field object to magnetrun's dict format.
    
    Returns:
        {
            "Symbol": str,
            "mSymbol": str,  # optional
            "Units": [input_unit, output_unit],
            "Exclude": List[str],
            "Val": Any  # optional
        }
    """
    result = {
        "Symbol": field.symbol,
        "Units": [
            input_unit or field.unit,
            output_unit or field.unit
        ],
        "Exclude": field.exclude_regions
    }
    
    if field.latex_symbol and field.latex_symbol != field.symbol:
        result["mSymbol"] = field.latex_symbol
    
    if field.default_value is not None:
        result["Val"] = field.default_value
    
    return result


def create_fieldunits_dict(fields: List[Field], 
                           distance_unit: str = "meter") -> Dict:
    """
    Create magnetrun-compatible fieldunits dictionary from Field list.
    
    This function mimics the behavior of dictTypeUnits() from method3D.py
    """
    ureg_local = ureg
    du = ureg_local.Unit(distance_unit)
    
    fieldunits = {}
    for field in fields:
        # Determine appropriate units based on field type
        # This logic would need to be customized per field
        fieldunits[field.name] = field_to_dict(field)
    
    return fieldunits
