import sys

N = int(sys.stdin.readline().rstrip())

def sum_harmonic_seq(n):
    # compute n//1 + n//2 + ... + n//n
    s = 0
    i=1
    while i<=n:
        j = n//(n//i)
        s+=(n//i)*(j-i+1)
        i = j+1
    return s

print(sum_harmonic_seq(N-1)+N)