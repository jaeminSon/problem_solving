import sys
from collections import defaultdict

MOD = 1_000_000_007

N, M  = [int(d) for d in sys.stdin.readline().rstrip().split()]

edges = [(int(d) for d in sys.stdin.readline().rstrip().split()) for i in range(M)]
mod = [1]
for i in range(1, len(edges)):
    mod.append((mod[-1]*3)%MOD)

def dfs(adjacency_list, source, target):
    stack = [source]
    marked = set([source])
    while stack:
        node = stack.pop()
        if node == target:
            return True
        for ne in adjacency_list[node]:
            if ne not in marked:
                stack.append(ne)
                marked.add(ne)
    return False

ans = 0
adj = defaultdict(dict)
for i in range(len(edges)-1, -1, -1):
    s,e = edges[i]
    adj[s][e] = 1
    adj[e][s] = 1
    if dfs(adj, 0, N-1):
        ans += mod[i]
        ans %= MOD
        del adj[s][e]
        del adj[e][s]

print(ans)