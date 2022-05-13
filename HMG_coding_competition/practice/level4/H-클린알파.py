import sys

P, N = [int(el) for el in sys.stdin.readline().split()]

list_n = [int(el) for el in sys.stdin.readline().split()]

MOD = 1000000007
sum = 0
for n in list_n:
    sum = sum * P + n
    sum = sum % MOD

print(sum)
