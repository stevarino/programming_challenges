"""https://projecteuler.net/problem=4
A palindromic number reads the same both ways. The largest palindrome
made from the product of two 2-digit numbers is 9009 = 91 × 99.

Find the largest palindrome made from the product of two 3-digit
numbers.
"""

import math

def get_factors(num):
    """yields a tuple of all factors."""
    factors = []
    for i in range(int(num**0.5)+1, 1, -1):
        if num % i == 0:
            factors.append((i, num/i))
    return factors


def find_palindrome(digits=3):
    """returns the largest palindrome and its factors where
        each factor is a given number of digits."""
    top_str = str((10**digits - 1)**2)

    chars = int(math.ceil(len(top_str)/2.0))
    is_odd_len = len(top_str) % 2

    for i in range(int(top_str[0:chars]), 10**(chars-1), -1):
        suspect = str(i) + str(i)[::-1][is_odd_len:]

        for factors in get_factors(int(suspect)):
            if all(len(str(f)) == digits for f in factors):
                return suspect, factors

if __name__ == '__main__':
    print(find_palindrome(3))
