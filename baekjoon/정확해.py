import sys

A, B, N = [int(el) for el in sys.stdin.readline().rstrip().split()]

def solve(X, N):
    s = 0
    
    i=2
    while i<=X:
        j = X//(X//i)
        s+=(X//i-1)*(j-i+1)
        i = j+1
    
    i=2
    while i**N <= X:
        s-=(X//(i**N))
        i += 1
    
    return s

print(solve(A+B, N)-solve(A-1, N))