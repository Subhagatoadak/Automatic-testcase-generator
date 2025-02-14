import pytest
from utils import add_numbers, multiply_numbers, is_even

def test_add_numbers():
    assert add_numbers(1, 2) == 3
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0
    assert add_numbers(1.5, 2.5) == 4.0
    with pytest.raises(TypeError):
        add_numbers("a", 1)

def test_multiply_numbers():
    assert multiply_numbers(2, 3) == 6
    assert multiply_numbers(-1, 1) == -1
    assert multiply_numbers(0, 5) == 0
    assert multiply_numbers(1.5, 2) == 3.0
    with pytest.raises(TypeError):
        multiply_numbers("a", 1)

def test_is_even():
    assert is_even(2) is True
    assert is_even(3) is False
    assert is_even(0) is True
    assert is_even(-2) is True
    with pytest.raises(TypeError):
        is_even("a")