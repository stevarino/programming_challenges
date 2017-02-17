"""https://projecteuler.net/problem=6

The sum of the squares of the first ten natural numbers is,

12 + 22 + ... + 102 = 385
The square of the sum of the first ten natural numbers is,

(1 + 2 + ... + 10)2 = 552 = 3025
Hence the difference between the sum of the squares of the first ten
natural numbers and the square of the sum is 3025 − 385 = 2640.

Find the difference between the sum of the squares of the first one
hundred natural numbers and the square of the sum.
"""

def squaresum_sumsquare_diff(num=10):
    """sum(1..n)**2 - sum(1..n**2)"""
    squaresum = ((num+1)*(num/2))**2
    sumsquare = sum(i**2 for i in range(num+1))
    return squaresum-sumsquare


if __name__ == '__main__':
    print(squaresum_sumsquare_diff(100))
