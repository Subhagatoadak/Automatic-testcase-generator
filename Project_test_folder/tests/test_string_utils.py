import pytest
from Project_test_folder.string_utils import reverse_string, to_uppercase, count_vowels

# Test cases for reverse_string
@pytest.mark.parametrize("input_str, expected_output", [
    ("hello", "olleh"),
    ("", ""),
    ("a", "a"),
    ("racecar", "racecar"),
    ("12345", "54321"),
])
def test_reverse_string(input_str, expected_output):
    assert reverse_string(input_str) == expected_output

def test_reverse_string_edge_cases():
    assert reverse_string(" ") == " "
    assert reverse_string("!@#$") == "$#@!"
    assert reverse_string("ab cd") == "dc ba"

def test_reverse_string_error_handling():
    with pytest.raises(TypeError):
        reverse_string(None)
    with pytest.raises(TypeError):
        reverse_string(123)

# Test cases for to_uppercase
@pytest.mark.parametrize("input_str, expected_output", [
    ("hello", "HELLO"),
    ("", ""),
    ("a", "A"),
    ("HELLO", "HELLO"),
    ("12345", "12345"),
])
def test_to_uppercase(input_str, expected_output):
    assert to_uppercase(input_str) == expected_output

def test_to_uppercase_edge_cases():
    assert to_uppercase(" ") == " "
    assert to_uppercase("!@#$") == "!@#$"
    assert to_uppercase("ab cd") == "AB CD"

def test_to_uppercase_error_handling():
    with pytest.raises(TypeError):
        to_uppercase(None)
    with pytest.raises(TypeError):
        to_uppercase(123)

# Test cases for count_vowels
@pytest.mark.parametrize("input_str, expected_output", [
    ("hello", 2),
    ("", 0),
    ("a", 1),
    ("HELLO", 2),
    ("bcdfg", 0),
])
def test_count_vowels(input_str, expected_output):
    assert count_vowels(input_str) == expected_output

def test_count_vowels_edge_cases():
    assert count_vowels(" ") == 0
    assert count_vowels("!@#$") == 0
    assert count_vowels("aeiouAEIOU") == 10

def test_count_vowels_error_handling():
    with pytest.raises(TypeError):
        count_vowels(None)
    with pytest.raises(TypeError):
        count_vowels(123)