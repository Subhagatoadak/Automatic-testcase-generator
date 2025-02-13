def reverse_string(s):
    """Reverses the input string."""
    return s[::-1]

def to_uppercase(s):
    """Converts a string to uppercase."""
    return s.upper()

def count_vowels(s):
    """Counts the number of vowels in a string."""
    return sum(1 for char in s.lower() if char in "aeiou")
