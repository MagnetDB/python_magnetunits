# tests/test_field.py
def test_field_creation():
    field = Field(
        name="MagneticField",
        symbol="B",
        unit="tesla"
    )
    assert field.name == "MagneticField"
    assert field.symbol == "B"

def test_field_conversion():
    field = Field(name="B", symbol="B", unit="tesla")
    result = field.convert(1.0, "gauss")
    assert abs(result - 10000.0) < 0.01

def test_field_label_formatting():
    field = Field(
        name="B",
        symbol="B",
        unit="tesla",
        latex_symbol=r"$B$"
    )
    assert field.format_label("gauss", use_latex=True) == r"$B$ [G]"

