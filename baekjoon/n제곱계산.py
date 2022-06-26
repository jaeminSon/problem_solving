from re import L
import sys

N = int(sys.stdin.readline().rstrip())

def matmul(a,b):
    return [[(a[0][0]*b[0][0]+a[0][1]*b[1][0]) % 1000, (a[0][0]*b[0][1]+a[0][1]*b[1][1]) % 1000],
            [(a[1][0]*b[0][0]+a[1][1]*b[1][0]) % 1000, (a[1][0]*b[0][1]+a[1][1]*b[1][1]) % 1000]]

def exponent_matmul(n):
    if n==1:
        return [[6, -4],[1, 0]]
    else:
        if n%2==0:
            half = exponent_matmul(n//2)
            return matmul(half, half)
        else:
            half = exponent_matmul(n//2)
            return matmul(matmul(half, half), [[6, -4],[1, 0]])
    

for i in range(N):
    n = int(sys.stdin.readline().rstrip())
    m = exponent_matmul(n-1)
    ans = (m[0][0]*6+m[0][1]*2 - 1) % 1000
    print("Case #{}: {}".format(i+1, str(ans).zfill(3)))
    