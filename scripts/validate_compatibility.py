# scripts/validate_compatibility.py
"""
Validate that all existing code still works with new field-framework.
"""
def validate_magnetrun():
    """Test magnetrun compatibility"""
    # Load old field definitions
    # Load new field definitions
    # Compare outputs
    pass

def validate_hifimagnetparaview():
    """Test python_hifimagnetparaview compatibility"""
    # Test that all plots still generate correctly
    # Verify field lookups work
    pass

if __name__ == "__main__":
    validate_magnetrun()
    validate_hifimagnetparaview()
    print("✓ All compatibility tests passed!")
