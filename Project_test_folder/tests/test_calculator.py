import pytest
from calculator import add, subtract, multiply, divide

def test_add():
    # Correct input and expected output
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

    # Edge cases
    assert add(1e10, 1e10) == 2e10
    assert add(-1e10, -1e10) == -2e10

    # Error handling
    with pytest.raises(TypeError):
        add("a", 1)
    with pytest.raises(TypeError):
        add(None, 1)

def test_subtract():
    # Correct input and expected output
    assert subtract(5, 3) == 2
    assert subtract(1, 1) == 0
    assert subtract(0, 0) == 0

    # Edge cases
    assert subtract(1e10, 1e10) == 0
    assert subtract(-1e10, 1e10) == -2e10

    # Error handling
    with pytest.raises(TypeError):
        subtract("a", 1)
    with pytest.raises(TypeError):
        subtract(None, 1)

def test_multiply():
    # Correct input and expected output
    assert multiply(2, 3) == 6
    assert multiply(-1, 1) == -1
    assert multiply(0, 5) == 0

    # Edge cases
    assert multiply(1e10, 1e10) == 1e20
    assert multiply(-1e10, 1e10) == -1e20

    # Error handling
    with pytest.raises(TypeError):
        multiply("a", 1)
    with pytest.raises(TypeError):
        multiply(None, 1)

def test_divide():
    # Correct input and expected output
    assert divide(6, 3) == 2
    assert divide(-4, 2) == -2
    assert divide(0, 1) == 0

    # Edge cases
    assert divide(1e10, 1) == 1e10
    assert divide(-1e10, 1) == -1e10

    # Error handling
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
    with pytest.raises(TypeError):
        divide("a", 1)
    with pytest.raises(TypeError):
        divide(None, 1)