import sys
from collections import defaultdict

sys.setrecursionlimit(500_000)

INF = float("inf")
DP_MAX_LOG_HEIGHT = 19


def eulerian_technique(n, adjacency_list):
    def _dfs(curr, parent):
        count[0] += 1
        start[curr] = count[0]
        dp_parent[0][curr] = parent
        depth[curr] = depth[parent] + 1
        for nxt in adjacency_list[curr]:
            if nxt != parent:
                dist[nxt] = dist[curr] + adjacency_list[curr][nxt]
                _dfs(nxt, curr)

    count = [-1]
    start = [-1] * n
    dp_parent = [[-1] * n for _ in range(DP_MAX_LOG_HEIGHT)]
    depth = [-1] * n
    dist = [0] * n

    _dfs(0, -1)  # start with node of index==0

    return start, dp_parent, depth, dist


def lca(node1, node2):
    if depth[node1] > depth[node2]:
        node1, node2 = node2, node1

    dist = depth[node2]-depth[node1]
    for i in range(DP_MAX_LOG_HEIGHT):
        if (dist >> i) & 1:
            node2 = dp_parent[i][node2]

    if node1 == node2:
        return node1
    else:
        for i in range(DP_MAX_LOG_HEIGHT-1, -1, -1):
            if dp_parent[i][node1] != dp_parent[i][node2]:
                node1 = dp_parent[i][node1]
                node2 = dp_parent[i][node2]
        return dp_parent[0][node1]


def dfs_dist(curr):

    dist_S[curr] = dist_T[curr] = INF
    if is_S[curr]:
        dist_S[curr] = 0
    if is_T[curr]:
        dist_T[curr] = 0

    for nxt in adj_compressed[curr]:
        dfs_dist(nxt)
        cost = adj_compressed[curr][nxt]
        dist_S[curr] = min(dist_S[curr], dist_S[nxt] + cost)
        dist_T[curr] = min(dist_T[curr], dist_T[nxt] + cost)


def dfs_ans(curr):
    ans[0] = min(ans[0], dist_S[curr] + dist_T[curr])
    for nxt in adj_compressed[curr]:
        dfs_ans(nxt)


N, Q = map(int, sys.stdin.readline().split())

adj = defaultdict(dict)
for _ in range(N-1):
    s, e, l = map(int, sys.stdin.readline().split())
    adj[s][e] = l
    adj[e][s] = l


start, dp_parent, depth, dist = eulerian_technique(N, adj)

for i in range(1, DP_MAX_LOG_HEIGHT):
    for j in range(N):
        dp_parent[i][j] = dp_parent[i-1][dp_parent[i-1][j]]

ans = [INF]
is_S = [False] * N
is_T = [False] * N
dist_S = [INF] * N
dist_T = [INF] * N

for _ in range(Q):
    sys.stdin.readline()
    S = list(map(int, sys.stdin.readline().split()))
    T = list(map(int, sys.stdin.readline().split()))
    
    for i in S:
        is_S[i] = True
    for i in T:
        is_T[i] = True

    S_and_T = S + T
    S_and_T = sorted(set(S_and_T), key=lambda x: start[x])
    list_lca = [lca(S_and_T[i], S_and_T[i-1]) for i in range(1, len(S_and_T))]
    all_nodes = sorted(set(S_and_T + list_lca), key=lambda x: start[x])

    adj_compressed = defaultdict(dict)
    for i in range(1, len(all_nodes)):
        curr = all_nodes[i]
        par = lca(all_nodes[i-1], curr)
        adj_compressed[par][curr] = dist[curr] - dist[par]

    dfs_dist(all_nodes[0])
    ans[0] = INF
    dfs_ans(all_nodes[0])
    print(ans[0])

    for i in S:
        is_S[i] = False
    for i in T:
        is_T[i] = False
    for node in all_nodes:
        dist_S[node] = INF
        dist_T[node] = INF
