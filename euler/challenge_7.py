"""https://projecteuler.net/problem=7

By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

What is the 10 001st prime number?

"""

def find_nth_prime(nth=6):
    """find the nth prime"""
    primes = [2, 3]
    i = 3
    while len(primes) < nth:
        i += 2
        if all(i % p > 0 for p in primes):
            primes.append(i)
    return i


if __name__ == '__main__':
    print(find_nth_prime(10001))
