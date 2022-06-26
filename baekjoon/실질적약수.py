import sys

N = int(sys.stdin.readline().rstrip())

ans = 0

i=2
while i<=N:
    j = N//(N//i)
    ans+= (N//i)*((i+j)*(j-i+1)//2) % 1_000_000
    i = j+1

ans -= (N*(N+1)//2-1) % 1_000_000

print(ans % 1_000_000)