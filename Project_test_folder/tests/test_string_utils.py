import pytest
from string_utils import reverse_string, to_uppercase, count_vowels

@pytest.mark.parametrize("input_str, expected", [
    ("hello", "olleh"),
    ("", ""),
    ("a", "a"),
    ("racecar", "racecar"),
    ("12345", "54321"),
])
def test_reverse_string(input_str, expected):
    assert reverse_string(input_str) == expected

@pytest.mark.parametrize("input_str, expected", [
    ("hello", "HELLO"),
    ("", ""),
    ("a", "A"),
    ("RaceCar", "RACECAR"),
    ("12345", "12345"),
])
def test_to_uppercase(input_str, expected):
    assert to_uppercase(input_str) == expected

@pytest.mark.parametrize("input_str, expected", [
    ("hello", 2),
    ("", 0),
    ("a", 1),
    ("racecar", 3),
    ("bcdfg", 0),
    ("AEIOU", 5),
])
def test_count_vowels(input_str, expected):
    assert count_vowels(input_str) == expected

@pytest.mark.parametrize("input_str", [
    None,
    123,
    45.67,
    ["a", "b", "c"],
    {"key": "value"},
])
def test_reverse_string_invalid_input(input_str):
    with pytest.raises(TypeError):
        reverse_string(input_str)

@pytest.mark.parametrize("input_str", [
    None,
    123,
    45.67,
    ["a", "b", "c"],
    {"key": "value"},
])
def test_to_uppercase_invalid_input(input_str):
    with pytest.raises(TypeError):
        to_uppercase(input_str)

@pytest.mark.parametrize("input_str", [
    None,
    123,
    45.67,
    ["a", "b", "c"],
    {"key": "value"},
])
def test_count_vowels_invalid_input(input_str):
    with pytest.raises(TypeError):
        count_vowels(input_str)