import sys
sys.path.append("..")
from custom_type import NAT, LIST1D

from math import gcd


def ntt(a: NAT, p: NAT, root: NAT) -> LIST1D:
    # conditions: 1. root^(p-1) mod p == 1 and root^k mod p !=1 for k < p-1
    #             2. len(a) <= p-1 and p-1 % len(a) = 0
    #             3. len(a) given by 2^k
    def just_bigger_power_2(val):
        ans = 1
        while ans < val:
            ans *= 2
        return ans

    if len(a) == 1:
        return a
    else:
        a_even = ntt(a[0::2], p, root)
        a_odd = ntt(a[1::2], p, root)
        w = pow(root, (p-1)//len(a), p)
        w_N = [1]
        for n in range(1, len(a)//2):
            w_N.append((w_N[n-1]*w) % p)
        return [(a_even[n] + w_N[n]*a_odd[n]) % p for n in range(len(a)//2)] + [(a_even[n]-w_N[n]*a_odd[n]) % p for n in range(len(a)//2)]


def ntt_without_padding(a: NAT, p: NAT, root: NAT) -> LIST1D:
    # inverse ntt of the returned value != original sequence (condition len(a) == 2^k violated)
    # conditions: 1. root^(p-1) mod p == 1 and root^k mod p !=1 for k < p-1
    #             2. len(a) <= p-1 and p-1 % len(a) = 0

    def just_bigger_power_2(val):
        ans = 1
        while ans < val:
            ans *= 2
        return ans

    if len(a) == 1:
        return a
    elif len(a) % 2 == 1:
        return ntt_without_padding(a+[0]*(just_bigger_power_2(len(a))-len(a)), p, root)[:len(a)]
    else:
        a_even = ntt_without_padding(a[0::2], p, root)
        a_odd = ntt_without_padding(a[1::2], p, root)
        w = pow(root, (p-1)//len(a), p)
        w_N = [1]
        for n in range(1, len(a)//2):
            w_N.append((w_N[n-1]*w) % p)
        return [(a_even[n] + w_N[n]*a_odd[n]) % p for n in range(len(a)//2)] + [(a_even[n]-w_N[n]*a_odd[n]) % p for n in range(len(a)//2)]


def primitive_root(p: NAT) -> LIST1D:
    """
    2 is a primitive root mod 5, because powers of 2 consistute relatively primal to 5
    {1, 2, 3, 4} == set of coprime of 5
    2^0 mod 5 == 1
    2^1 mod 5 == 2
    2^2 mod 5 == 4
    2^3 mod 5 == 3
    """
    coprime_set = {num for num in range(1, p) if gcd(num, p) == 1}
    return [g for g in range(1, p) if coprime_set == {pow(g, powers, p)
            for powers in range(1, p)}]


def get_smallest_primitive_root(p: NAT) -> NAT:
    coprime_set = {num for num in range(1, p) if gcd(num, p) == 1}
    for g in range(1, p):
        if coprime_set == {pow(g, powers, p) for powers in range(1, p)}:
            return g


def batch_eval_polynomials(c: LIST1D, p: NAT, root: NAT, queries: LIST1D):
    # given f(x) = c0 + c1*x + c2*x^2+ ... + cn*x^n
    # return [f(1), f(root), f(root^2), f(root^3), ..., f(root^n)]
    # conditions: 1. p should be a prime given by m*2^l + 1
    #             2. len(c) == p-1

    assert len(c) == p-1
    query2index = {pow(root, i, p): i for i in range(len(c))}
    solutions = ntt_without_padding(c, p, root)
    ans = []
    for query in queries:
        if query == 0:
            ans.append(c[0])
        else:
            ans.append(solutions[query2index[query]])

    return ans


if __name__ == "__main__":
    assert get_smallest_primitive_root(3 * 2**8 + 1) == 11
    assert ntt([153, 321, 133, 44], 3 * 2**8 + 1, 11) == [651, 276, 690, 533]
    assert batch_eval_polynomials([1, 2, 3]+[0]*(786432-3), 786433, 11, [7, 8, 9, 1, 0]) == [162, 209, 262, 6, 1]
