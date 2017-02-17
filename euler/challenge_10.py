"""https://projecteuler.net/problem=10"""

def gen_primes(limit=2e6):
    """Generates primes, based on Sieve of Eratosthenes
        http://code.activestate.com/recipes/117119/
    """
    factorable = {}
    for i in range(2, int(limit)):
        if i not in factorable:
            yield i
            factorable[i*i] = [i]
        else:
            for j in factorable[i]:
                factorable.setdefault(i+j, []).append(j)
            del factorable[i]


if __name__ == '__main__':
    print(sum(gen_primes(2e6)))
