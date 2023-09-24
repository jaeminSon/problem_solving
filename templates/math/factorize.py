import sys
sys.path.append("..")
from custom_type import NAT, LIST1D


def factorize(v: NAT) -> LIST1D:
    if v == 1:
        return []
    elif v % 2 == 0:
        return [2]+factorize(v//2)
    else:
        for i in range(3, v+1, 2):
            if v % i == 0:
                return [i] + factorize(v//i)


assert factorize(100) == [2, 2, 5, 5]
assert factorize(2**3) == [2, 2, 2]
assert factorize(2*3*7*11*13) == [2, 3, 7, 11, 13]
