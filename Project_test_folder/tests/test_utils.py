# test_utils.py

import pytest
from Project_test_folder.utils import add_numbers, multiply_numbers, is_even

# Test cases for add_numbers
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (-1, -1, -2),
    (0, 0, 0),
    (1.5, 2.5, 4.0),
    (1e10, 1e10, 2e10)
])
def test_add_numbers(a, b, expected):
    assert add_numbers(a, b) == expected

def test_add_numbers_type_error():
    with pytest.raises(TypeError):
        add_numbers("1", 2)

# Test cases for multiply_numbers
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 6),
    (-1, 3, -3),
    (0, 5, 0),
    (1.5, 2, 3.0),
    (1e5, 1e5, 1e10)
])
def test_multiply_numbers(a, b, expected):
    assert multiply_numbers(a, b) == expected

def test_multiply_numbers_type_error():
    with pytest.raises(TypeError):
        multiply_numbers("2", 3)

# Test cases for is_even
@pytest.mark.parametrize("n, expected", [
    (2, True),
    (3, False),
    (0, True),
    (-2, True),
    (-3, False)
])
def test_is_even(n, expected):
    assert is_even(n) == expected

def test_is_even_type_error():
    with pytest.raises(TypeError):
        is_even("4")