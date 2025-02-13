import pytest
from string_utils import reverse_string, to_uppercase, count_vowels

def test_reverse_string():
    # Correct input and expected output
    assert reverse_string("hello") == "olleh"
    assert reverse_string("world") == "dlrow"
    
    # Edge cases
    assert reverse_string("") == ""
    assert reverse_string("a") == "a"
    assert reverse_string("ab") == "ba"
    
    # Error handling
    with pytest.raises(TypeError):
        reverse_string(None)
    with pytest.raises(TypeError):
        reverse_string(123)

def test_to_uppercase():
    # Correct input and expected output
    assert to_uppercase("hello") == "HELLO"
    assert to_uppercase("world") == "WORLD"
    
    # Edge cases
    assert to_uppercase("") == ""
    assert to_uppercase("a") == "A"
    assert to_uppercase("AbC") == "ABC"
    
    # Error handling
    with pytest.raises(TypeError):
        to_uppercase(None)
    with pytest.raises(TypeError):
        to_uppercase(123)

def test_count_vowels():
    # Correct input and expected output
    assert count_vowels("hello") == 2
    assert count_vowels("world") == 1
    
    # Edge cases
    assert count_vowels("") == 0
    assert count_vowels("a") == 1
    assert count_vowels("bcdfg") == 0
    
    # Error handling
    with pytest.raises(TypeError):
        count_vowels(None)
    with pytest.raises(TypeError):
        count_vowels(123)