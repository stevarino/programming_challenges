"""https://projecteuler.net/problem=9

A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,

a2 + b2 = c2
For example, 32 + 42 = 9 + 16 = 25 = 52.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.

"""
import operator
from functools import reduce


def find_pythagorean_wholes(total=1000):
    """returns the pythagorean set where the sum is the
        given total."""
    leg_max = total/2
    for i in range(1, leg_max):
        for j in range(1, leg_max):
            hyp = (i**2+j**2)**0.5
            if hyp.is_integer() and (hyp+i+j) == total:
                return i, j, hyp

if __name__ == '__main__':
    print(reduce(operator.mul, find_pythagorean_wholes(1000)))
