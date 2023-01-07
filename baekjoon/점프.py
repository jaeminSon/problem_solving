import sys

def power2(val):
    m=0
    v=0
    while v<=val:
        v=(2*v+1)
        m+=1
    return m-1

def solve(l,r):
    if l>r:
        return 0
    elif l==0:
        return solve(l+1, r)
    
    m = power2(l)
    n = power2(r)

    if m==n:
        return m+solve(l-(2**m-1), r-(2**m-1))
    else:
        ret = m+solve(l-(2**m-1),2**m-1)
        for i in range(m, n-1):
            ret = max(ret, (i+1)*(i+2)//2+1)
        ret = max(ret, n+solve(1,r-(2**n-1)))

        return ret
        

T = int(sys.stdin.readline().rstrip())

problems = [(int(v) for v in sys.stdin.readline().rstrip().split()) for _ in range(T)]

for l,r in problems:
    print(solve(l,r))
