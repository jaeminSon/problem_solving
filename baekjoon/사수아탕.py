import sys

n, m = [int(e) for e in sys.stdin.readline().rstrip().split()]

intercept_zero = 0
l = []
for _ in range(n):
    x = int(sys.stdin.readline().rstrip())
    if x==0:
        intercept_zero = m
    else:
        l.append(x)
l.append(0)
l = sorted(l)
s = l.index(0)

MAX_PENALTY = n*m

def left(i,j,k):
    if k==0:
        return 0
    
    if L[i][j]!=-1:
        return L[i][j]
    
    if i>0 and j<LEN-1:
        L[i][j] = min(left(i-1,j,k-1)+k*(l[i]-l[i-1]), right(i,j+1,k-1)+k*(l[j+1]-l[i]))
    elif i==0 and j<LEN-1:
        L[i][j] = right(i,j+1,k-1)+k*(l[j+1]-l[i])
    elif i>0 and j==LEN-1:
        L[i][j] = left(i-1,j,k-1)+k*(l[i]-l[i-1])
    else:
        L[i][j] = MAX_PENALTY
    
    return L[i][j]


def right(i,j,k):
    if k==0:
        return 0
    
    if R[i][j]!=-1:
        return R[i][j]
    
    if i>0 and j<LEN-1:
        R[i][j] = min(left(i-1,j,k-1)+k*(l[j]-l[i-1]), right(i,j+1,k-1)+k*(l[j+1]-l[j]))
    elif i==0 and j<LEN-1:
        R[i][j] = right(i,j+1,k-1)+k*(l[j+1]-l[j])
    elif i>0 and j==LEN-1:
        R[i][j] = left(i-1,j,k-1)+k*(l[j]-l[i-1])
    else:
        R[i][j] = MAX_PENALTY

    return R[i][j]

LEN = len(l)
ans = 0
for k in range(0,n+1):
    L = [[-1]*(LEN) for _ in range(LEN)]
    R = [[-1]*(LEN) for _ in range(LEN)]
    ans = max(ans, k*m-left(s,s,k))

print(ans+intercept_zero)
