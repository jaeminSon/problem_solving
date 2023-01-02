import sys

N = int(sys.stdin.readline().rstrip())

MAX_VAL = 600_000

tree = [MAX_VAL]*(N+1)
    
def update(i ,val):
    i+=1
    while i <= N:
        tree[i] = min(val, tree[i])
        i += i & (-i) # right node (same depth) for update 

def query(i):
    res = MAX_VAL
    i = i+1
    while i > 0:
        res = min(res, tree[i])
        i -= i & (-i)
    return res

l = [None] * 3

for i in range(3):
    seq = [int(d) for d in sys.stdin.readline().rstrip().split()]
    if i==0:
        l[i] = seq
    else:
        d = {v:k for k,v in enumerate(seq)}
        l[i] = [d[v] for v in l[0]]
    
n_best = 0
for i in range(N):
    min_val = query(l[1][i])
    if min_val > l[2][i]:
        n_best+=1
    update(l[1][i],l[2][i])

print(n_best)
