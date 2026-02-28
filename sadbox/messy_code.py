"""This module contains a global constant and a function with simplified logic."""

X = 10

def f(z):
    """Checks if a number is strictly between 0 and 100.

    Args:
        z (int): The number to check.

    Returns:
        bool: True if z is greater than 0 and less than 100, False otherwise.
    """
    return 0 < z < 100
