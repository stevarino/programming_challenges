"""https://projecteuler.net/problem=5

2520 is the smallest number that can be divided by each of the
numbers from 1 to 10 without any remainder.

What is the smallest positive number that is evenly divisible by all
of the numbers from 1 to 20?
"""

from collections import defaultdict
import operator
from functools import reduce

def find_primes_counts(number):
    """Returns a dictionary consisting of prime:count"""
    counts = defaultdict(int)
    i = 2
    while number > 1:
        while number % i == 0:
            number = number / i
            counts[i] += 1
        i += 1
    return counts

def reduce_counts(left, right):
    """Modifies count a by adding elements from b if greater"""
    for k in right:
        if right[k] > left[k]:
            left[k] = right[k]
    return left

def multiply_count(cnt):
    """converts a prime count to the smallest multiple"""
    return reduce(operator.mul, [operator.pow(*i) for i in cnt.items()])

def find_min_multiple(num=20):
    """Returns the smallest number that is a multiple of all integers up
        to the given number."""
    prime_counts = [find_primes_counts(i) for i in range(num+1)]
    return multiply_count(reduce(reduce_counts, prime_counts))


if __name__ == '__main__':
    print(find_min_multiple(20))
