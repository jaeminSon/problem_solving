import sys
sys.setrecursionlimit(10**9)
from collections import Counter

N = int(sys.stdin.readline().rstrip())

e = [[] for _ in range(N)]
for i in range(N-1):
    n1, n2 = [int(el) for el in sys.stdin.readline().rstrip().split()]
    e[n1-1].append(n2-1)
    e[n2-1].append(n1-1)

d = [len(ne) for ne in e]
r = [0 if d[i]==1 else -1 for i in range(N)]
v = [[0] if d[i]==1 else -1 for i in range(N)]
called = [False] * N

def get_visible(node):
    if v[node] != -1:
        return v[node]
    else:
        called[node] = True
        list_v = []
        for ne in e[node]:
            if not called[ne]:
                v[ne] = get_visible(ne)
                list_v += v[ne]
        
        counter = Counter(list_v)
        visible_ranks = set([val for val in counter if counter[val]>=2])
        rank = max(visible_ranks) + 1 if visible_ranks else 0
        set_forbidden = set(counter.keys())
        while rank in set_forbidden:
            rank+=1
        r[node] = rank
        return [rank] + list(set([v for v in list_v if v > rank]))

root = 0
while d[root] == 1:
    root+=1
get_visible(root)

print(max(r))
