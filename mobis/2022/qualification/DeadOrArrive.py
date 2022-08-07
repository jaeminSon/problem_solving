import sys

N = int(sys.stdin.readline().rstrip())

d = {}
for i in range(N):
    v, w = [int(d) for d in sys.stdin.readline().rstrip().split()]
    if v not in d:
        d[v] = (w, i+1)
    else:
        if d[v][0] <= w:
            d[v] = (w, i+1)

print(sum(v[1] for v in d.values()))