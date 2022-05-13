import sys

K, P, N = [int(el) for el in sys.stdin.readline().split()]

result = K
for _ in range(N):
    result*=P
    result %= 1000000007

print(result)
