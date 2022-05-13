import sys

K, P, N = [int(el) for el in sys.stdin.readline().split()]

MOD = 1000000007

def power_mod(P, X, mod):
    if P==1:
        return 1
    else:
        result = 1
        for min_power in range(X):
            result*=P
            if result > MOD:
                r = result % MOD
                result = power_mod(r, X // (min_power+1), mod)
                for _ in range(X % (min_power+1)):
                    result *= P
                    result = result % mod
                return result
        return result
        

result = power_mod(P, 10*N, MOD)
result*=K
result%=MOD
print(result)