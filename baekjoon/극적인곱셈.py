import sys
from math import gcd

N, K = [int(d) for d in sys.stdin.readline().rstrip().split()]

if K < N:
    print(0)
else:
    g = gcd(10*N-1, K)
    div = (10*N-1) // g
    for n_digit in range(1, 1000):
        if (10**(n_digit-1)-N) % div ==0:
            print(K*(10**(n_digit-1)-N)//(10*N-1)*10+K)
            exit(0)
    print(0)