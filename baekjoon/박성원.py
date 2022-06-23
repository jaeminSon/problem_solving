import sys
from math import gcd

N = int(sys.stdin.readline().rstrip())
l = [sys.stdin.readline().rstrip() for _ in range(N)]
K = int(sys.stdin.readline().rstrip())

lens = [len(el) for el in l]
l = [int(el) for el in l]
mod_l = [el%K for el in l]
mod_decimal = [1%K]
for _ in range(1,51):
    mod_decimal.append(mod_decimal[-1]*10 % K)

dp = [None] * (2**N)
for i, v in enumerate(l):
    dp[((1 << N) - 1) ^ 1 << i] = [1 if m==v%K else 0 for m in range(K)]

def bitmask_dp(bitmask):
    if dp[bitmask] is None:
        list_mode = [0]*K
        for i in range(N):
            if bitmask & (1 << i) == 0:
                lm = bitmask_dp(bitmask | (1 << i))
                for t in range(K):
                    list_mode[(t*mod_decimal[lens[i]]+mod_l[i])%K] += lm[t]
        dp[bitmask] = list_mode
    return dp[bitmask]

numerator = bitmask_dp(0)[0]
if numerator==0:
    print("0/1")
else:
    denominator = 1
    for n in range(1, N+1):
        denominator*=n
    g = gcd(numerator,denominator)
    print("{}/{}".format(numerator//g, denominator//g))