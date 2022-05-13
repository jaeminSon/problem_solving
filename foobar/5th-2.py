from math import factorial
from collections import Counter


def solution(w, h, s):
    sum_xg = 0

    def sum_chain(n, i=1):
        yield [n]
        for t in range(i, n//2+1):
            for chain in sum_chain(n-t, t):
                yield [t] + chain

    def gcd(a, b):
        if a>=b:
            large, small = a, b
        else:
            large, small = b, a
        
        if small == 0:
            return large
        else:
            return gcd(small, large % small)

    def get_n_cycles(sum_chain, n):
        val = factorial(n)
        for digit, count in Counter(sum_chain).items():
            val //= (digit**count)*factorial(count)
        return val


    sum_xg = 0
    for w_chain in sum_chain(w):
        for h_chain in sum_chain(h):
            n_total_cycles = get_n_cycles(w_chain, w)*get_n_cycles(h_chain, h)
            sum_xg += n_total_cycles*(s**sum([sum([gcd(i,j) for i in w_chain]) for j in h_chain]))

    return str(sum_xg // (factorial(w)*factorial(h)))


if __name__=="__main__":
    print(solution(2, 3, 4))
    print(solution(2, 2, 2))