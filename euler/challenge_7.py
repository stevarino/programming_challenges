"""https://projecteuler.net/problem=7"""

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
