import sys
sys.path.append("..")
from custom_type import NAT


def diophantine_all_soln(a: NAT, b: NAT, c: NAT, n: NAT = 2):
    (x0, y0) = diophantine(a, b, c)
    d = gdc(a, b)
    p = a // d
    q = b // d

    for i in range(n):
        x = x0 + i * q
        y = y0 - i * p
        print(x, y)


def diophantine(a: NAT, b: NAT, c: NAT):
    """
    Given a*x + b*y = c, find x and y
    """
    assert c % gdc(a, b) == 0
    (d, x, y) = extended_gcd(a, b)
    r = c / d
    return (r * x, r * y)


def gdc(a: NAT, b: NAT) -> NAT:
    if a < b:
        a, b = b, a

    while a % b != 0:
        a, b = b, a % b

    return b


def extended_gcd(a: NAT, b: NAT):
    """
    d = a*x + b*y = gcd(a,b)
    """
    assert a >= 0 and b >= 0

    if b == 0:
        d, x, y = a, 1, 0
    else:
        (d, p, q) = extended_gcd(b, a % b)
        x = q
        y = p - q * (a // b)

    assert a % d == 0 and b % d == 0
    assert d == a * x + b * y

    return (d, x, y)


if __name__ == "__main__":
    assert diophantine(5, 6, 1) == (-1, 1)
