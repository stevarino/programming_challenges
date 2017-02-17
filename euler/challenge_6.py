"""https://projecteuler.net/problem=6"""

def squaresum_sumsquare_diff(num=10):
    """sum(1..n)**2 - sum(1..n**2)"""
    squaresum = ((num+1)*(num/2))**2
    sumsquare = sum(i**2 for i in range(num+1))
    return squaresum-sumsquare


if __name__ == '__main__':
    print(squaresum_sumsquare_diff(100))
