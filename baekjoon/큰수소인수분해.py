import sys
import random

from math import gcd

a_list_2to32 = [2, 7, 61]
a_list_2to64 = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]


def miller_rabin(n:int, a:int):
    d = n - 1
    while d % 2 == 0:
        if pow(a, d, n) == n-1:
            return True
        d //= 2
    last = pow(a, d, n)
    return last == n-1 or last == 1


def is_prime(n:int):
    if n <= 1:
        return False
    elif n < 2**16:
        for i in range(2, n):
            if i**2 > n:
                break
            if n % i == 0:
                return False
        return True
    else:
        if n <= 2**32:
            a_list = a_list_2to32
        elif n <= 2**64:
            a_list = a_list_2to64
        else:
            raise ValueError("n too big to handle.")
    
        for a in a_list:
            if not miller_rabin(n, a):
                return False
        return True


def g(x, c, n):
    return ((x**2)%n + c) % n

def pollardRho(n):
    if n == 1:
        return 1
    elif is_prime(n):
        return n
    elif n % 2 == 0:
        return 2
    
    x = y = random.randrange(2, n)
    c = random.randrange(1, n)
    d = 1
    while d == 1:
        x = g(x,c,n)
        y = g(g(y,c,n),c,n)
        d = gcd(abs(x - y), n)
        
    if is_prime(d):
        return d
    else:
        return pollardRho(n)
    
    
n = int(sys.stdin.readline().rstrip())

factors = []
while n > 1:
    d = pollardRho(n)
    factors.append(d)
    n //= d

for f in sorted(factors):
    print(f)

