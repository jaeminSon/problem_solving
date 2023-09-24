import sys
sys.path.append("..")
from custom_type import NAT


a_list_2to32 = [2, 7, 61]
a_list_2to64 = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]


def miller_rabin(n, a):
    d = n - 1
    while d % 2 == 0:
        if pow(a, d, n) == n-1:
            return True
        d //= 2
    last = pow(a, d, n)
    return last == n-1 or last == 1


def is_prime(n: NAT) -> bool:
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


if __name__ == "__main__":
    assert is_prime(2)
    assert not is_prime(4)
    assert not is_prime(6)
