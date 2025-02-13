class Calculator:
    """Basic calculator class with arithmetic operations."""

    def add(self, a, b):
        """Returns the sum of two numbers."""
        return a + b

    def subtract(self, a, b):
        """Returns the difference of two numbers."""
        return a - b

    def multiply(self, a, b):
        """Returns the product of two numbers."""
        return a * b

    def divide(self, a, b):
        """Returns the division result of two numbers. Handles division by zero."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
