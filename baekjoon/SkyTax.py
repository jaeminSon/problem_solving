from sys import stdin, setrecursionlimit

input = stdin.readline
setrecursionlimit(100_000)

log_max_depth = 20


def dfs(i):
    size[i] = 1
    for ch in graph[i]:
        if size[ch] == 0:
            par[0][ch] = i
            depth[ch] = depth[i] + 1
            size[i] += dfs(ch)
    return size[i]


def up(node, dist):
    for i in range(log_max_depth):
        if (dist >> i) & 1:
            node = par[i][node]
    return node

def lca(a, b):
    if depth[a] > depth[b]:
        a, b = b, a

    b = up(b, depth[b]-depth[a])

    if a == b:
        return a
    else:
        for i in range(log_max_depth-1, -1, -1):
            if par[i][a] != par[i][b]:
                a = par[i][a]
                b = par[i][b]
        return par[0][a]


tc = int(input())
for t in range(tc):

    n_nodes, Qs, cap = map(int, input().split())
    graph = [[] for _ in range(n_nodes+1)]
    for _ in range(n_nodes - 1):
        a, b = map(int, input().split())
        graph[a].append(b)
        graph[b].append(a)

    par = [[0]*(n_nodes+1) for _ in range(log_max_depth)]
    depth = [0] * (n_nodes+1)
    size = [0] * (n_nodes+1)

    dfs(cap)

    print(f'Case #{t+1}:')
    for p in range(1, log_max_depth):
        for i in range(1, n_nodes+1):
            par[p][i] = par[p-1][par[p-1][i]]

    for q in range(Qs):
        a, b = map(int, input().split())
        if a == 0:
            cap = b
        else:
            if cap == b:
                print(n_nodes)
            elif lca(cap, b) == b:
                ch = up(cap, depth[cap] - depth[b] - 1)
                print(n_nodes - size[ch])
            else:
                print(size[b])
