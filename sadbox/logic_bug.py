"""Module for demonstrating a countdown function with a logical bug fix."""

def count_down(n):
    """Counts down from a given number to 1.

    Args:
        n (int): The starting number for the countdown.
    """
    while n > 0:
        print(n)
        n -= 1
