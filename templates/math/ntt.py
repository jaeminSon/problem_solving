from math import gcd

def ntt(a, p, root):
    # conditions: 1. root^(p-1) mod p == 1 and root^k mod p !=1 for k < p-1
    #             2. len(a) <= p-1 and p-1 % len(a) = 0
    def just_bigger_power_2(val):
        ans=1
        while ans < val:
            ans*=2
        return ans
    
    if len(a) == 1:
        return a
    elif len(a) % 2 == 1:
        return ntt(a+[0]*(just_bigger_power_2(len(a))-len(a)), p, root)[:len(a)]
    else:
        a_even=ntt(a[0::2], p, root)
        a_odd=ntt(a[1::2], p, root)
        w = pow(root, (p-1)//len(a), p)
        w_N = [1]
        for n in range(1, len(a)//2):
            w_N.append((w_N[n-1]*w) % p)
        return [(a_even[n] +w_N[n]*a_odd[n]) % p for n in range(len(a)//2)] + [(a_even[n]-w_N[n]*a_odd[n]) % p for n in range(len(a)//2)]


def primitive_root(p):
    coprime_set = {num for num in range(1, p) if gcd(num, p) == 1}
    return [g for g in range(1, p) if coprime_set == {pow(g, powers, p)
            for powers in range(1, p)}]


def get_smallest_primitive_root(p):
    coprime_set = {num for num in range(1, p) if gcd(num, p) == 1}
    for g in range(1, p):
        if coprime_set == {pow(g, powers, p) for powers in range(1, p)}:
            return g

def batch_eval_polynomials(c, p, root, queries):
    # given f(x) = c0 + c1*x + c2*x^2+ ... + cn*x^n
    # return [f(1), f(root^k), f(root^2k), f(root^3k), ..., f(root^nk)] where k = (p-1)/len(c)
    # conditions: 1. p should be a prime given by m*2^l + 1
    #             2. len(c) <= p-1 and p-1 % len(c) == 0
    
    rootk = pow(root, (p-1)//len(c), p)
    query2index = {pow(rootk, i, p):i for i in range(len(c))}
    solutions = ntt(c, p, root)
    ans = []
    for query in queries:
        if query == 0:
            ans.append(c[0])
        else:
            ans.append(solutions[query2index[query]])
            
    return ans

if __name__=="__main__":
    assert get_smallest_primitive_root(3 * 2**8 + 1) == 11
    assert ntt([153, 321, 133, 44], 3 * 2**8 + 1, 11) == [651, 276, 690, 533]
    assert batch_eval_polynomials([1, 2, 3]+[0]*(786432-3), 786433, 11, [7,8,9]) == [162, 209, 262]


