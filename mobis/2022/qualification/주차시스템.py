import sys

N, M  = [int(d) for d in sys.stdin.readline().rstrip().split()]

MULTIPLE = 2000

vacant = set()
score_lookup = [0]*(MULTIPLE**2)
for i in range(N):
    row = [int(d) for d in sys.stdin.readline().rstrip().split()]
    for j in range(M):
        if row[j]!=1:
            key = i*MULTIPLE+j
            if row[j]==0:
                score_lookup[key] = 1
            elif row[j]==2:
                score_lookup[key] = -2
            vacant.add(key)

best = 0
while vacant:
    root = vacant.pop()
    q = [root]
    val = score_lookup[root]
    while q:
        c = q.pop()
        for nec in [c-1, c+1, c+MULTIPLE, c-MULTIPLE]:
            if nec in vacant:
                val += score_lookup[nec]
                q.append(nec)
                vacant.remove(nec)
    best = max(best, val)

print(best)