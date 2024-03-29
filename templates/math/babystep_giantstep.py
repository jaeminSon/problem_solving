import sys
sys.path.append("..")
from custom_type import NAT

from math import ceil, sqrt


def babystep_giantstep(a: NAT, b: NAT, p: NAT) -> NAT:
    '''
    Solve x for a^x mod p == b
    '''

    n = ceil(sqrt(p))

    # baby step - a^{1...n} mod p
    set_babystep = {b * pow(a, i, p) % p: i for i in range(n+1)}

    # giant step - meet in the middle
    an = pow(a, n, p)
    for j in range(1, n+1):
        m = pow(an, j, p) % p
        if m in set_babystep:
            return j * n - set_babystep[m]


if __name__ == "__main__":
    assert babystep_giantstep(5, 4, 7) == 2
    assert babystep_giantstep(2, 3, 7) == None
