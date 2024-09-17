import sys
sys.setrecursionlimit(20_0000)


def dfs(curr, prev=-1):
    if len(G[curr]) == 1:
        leafs.append(curr)
    for nxt in G[curr]:
        if nxt != prev:
            dfs(nxt, curr)

N, _ = map(int, sys.stdin.readline().split())

G = [[]for _ in range(N)]
for i in range(N-1):
    s, e = map(int, sys.stdin.readline().split())
    G[s].append(e)
    G[e].append(s)

leafs = []
dfs(0)

print((len(leafs)+1) // 2)

d = len(leafs) // 2
for i in range(d):
    print(f"{leafs[i]} {leafs[i+d]}")
if len(leafs) % 2 == 1:
    print(f"{leafs[0]} {leafs[-1]}")
