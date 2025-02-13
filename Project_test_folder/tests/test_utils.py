import pytest
from utils import add_numbers, multiply_numbers, is_even

# Test cases for add_numbers
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),  # Correct input
    (0, 0, 0),  # Edge case: both numbers zero
    (-1, 1, 0),  # Edge case: negative and positive
    (1.5, 2.5, 4.0),  # Floating point numbers
])
def test_add_numbers(a, b, expected):
    assert add_numbers(a, b) == expected

def test_add_numbers_type_error():
    with pytest.raises(TypeError):
        add_numbers("a", 1)

# Test cases for multiply_numbers
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 6),  # Correct input
    (0, 5, 0),  # Edge case: one number zero
    (-2, 3, -6),  # Edge case: negative and positive
    (1.5, 2, 3.0),  # Floating point numbers
])
def test_multiply_numbers(a, b, expected):
    assert multiply_numbers(a, b) == expected

def test_multiply_numbers_type_error():
    with pytest.raises(TypeError):
        multiply_numbers("a", 1)

# Test cases for is_even
@pytest.mark.parametrize("n, expected", [
    (2, True),  # Correct input
    (3, False),  # Correct input
    (0, True),  # Edge case: zero
    (-2, True),  # Edge case: negative even
    (-3, False),  # Edge case: negative odd
])
def test_is_even(n, expected):
    assert is_even(n) == expected

def test_is_even_type_error():
    with pytest.raises(TypeError):
        is_even("a")