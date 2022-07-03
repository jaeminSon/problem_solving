import sys
from math import ceil, sqrt


def babystep_giantstep(a, b, p):
    '''
    Solve x for a^x mod p == b
    '''
    
    n = ceil(sqrt(p))

    # baby step - b*a^{1...n} mod p
    set_babystep = {b * pow(a, i, p) % p: i for i in range(n+1)}

    # giant step - meet in the middle
    an = pow(a, n, p)
    for j in range(1, n+1):
        m = pow(an, j, p) % p
        if m in set_babystep:
            return j * n - set_babystep[m]

while True:
    try:
        p,b,n  = [int(d) for d in sys.stdin.readline().rstrip().split()]
    except:
        break
    ans = babystep_giantstep(b,n,p)
    print("no solution" if ans is None else ans)