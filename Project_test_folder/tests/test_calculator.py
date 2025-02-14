import pytest
from calculator import Calculator

@pytest.fixture
def calculator():
    return Calculator()

def test_add(calculator):
    assert calculator.add(2, 3) == 5
    assert calculator.add(-1, 1) == 0
    assert calculator.add(0, 0) == 0
    assert calculator.add(1.5, 2.5) == 4.0

def test_subtract(calculator):
    assert calculator.subtract(5, 3) == 2
    assert calculator.subtract(-1, -1) == 0
    assert calculator.subtract(0, 0) == 0
    assert calculator.subtract(2.5, 1.5) == 1.0

def test_multiply(calculator):
    assert calculator.multiply(2, 3) == 6
    assert calculator.multiply(-1, 1) == -1
    assert calculator.multiply(0, 5) == 0
    assert calculator.multiply(1.5, 2) == 3.0

def test_divide(calculator):
    assert calculator.divide(6, 3) == 2
    assert calculator.divide(-4, 2) == -2
    assert calculator.divide(0, 1) == 0
    assert calculator.divide(2.5, 0.5) == 5.0

    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculator.divide(1, 0)