import sys
sys.path.append("..")
from custom_type import NAT


def sum_harmonic_seq(n: NAT) -> NAT:
    # compute n//1 + n//2 + ... + n//n
    s = 0
    i = 1
    while i <= n:
        j = n//(n//i)
        s += (n//i)*(j-i+1)
        i = j+1
    return s


assert sum_harmonic_seq(16) == 50
