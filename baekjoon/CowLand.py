import sys
import math

sys.setrecursionlimit(100000)

N, Q = map(int, input().split())

L = pow(2, math.ceil(math.log2(N)))
segtree = [0] * (2*L)

weight = list(map(int, input().split()))

adj_list = [[] for _ in range(N)]
for _ in range(N-1):
    s, e = map(int, input().split())
    adj_list[s-1].append(e-1)
    adj_list[e-1].append(s-1)

questions = [list(map(int, input().split())) for _ in range(Q)]


def heavy_light_decomposition(adjacency_list):

    def dfs(curr, parent):
        tree["parent"][curr] = parent
        tree["size"][curr] = 1
        for v in adjacency_list[curr]:
            if v != parent:
                tree["size"][curr] += dfs(v, curr)
        return tree["size"][curr]

    def _assign_chain_top(curr, parent, chain_top):
        pos_seg[curr] = count[0]
        count[0] += 1

        tree["chain_top"][curr] = chain_top
        list_child = [v for v in adjacency_list[curr] if v != parent]
        if len(list_child) > 0:  # intermediate node
            node_heavy_edge = max(list_child, key=lambda x: tree["size"][x])
            _assign_chain_top(node_heavy_edge, curr, chain_top)  # remain top for heavy edge
            for v in adjacency_list[curr]:
                if v != parent and v != node_heavy_edge:
                    _assign_chain_top(v, curr, v)  # light edge (new top)

    n_nodes = len(adjacency_list)
    tree = {"size": [None] * n_nodes, "parent": [None] * n_nodes, "chain_top": [None] * n_nodes}
    dfs(0, 0)
    count = [0]
    pos_seg = [0] * n_nodes
    _assign_chain_top(0, 0, 0)
    return tree, pos_seg


def initialize_segtree():
    for i, w in enumerate(weight):
        segtree[L + pos_seg[i]] = w

    for i in range(L-1, 0, -1):
        segtree[i] = segtree[i * 2] ^ segtree[i * 2 + 1]


def update(i, w):
    i += L
    segtree[i] = w
    i = i // 2
    while i > 0:
        segtree[i] = segtree[i * 2] ^ segtree[i * 2 + 1]
        i = i // 2


def range_query(l, r):
    # [l,r]
    l += L
    r += L
    ret = 0
    while l <= r:
        if l % 2 == 1:
            ret = ret ^ segtree[l]
            l += 1
        if r % 2 == 0:
            ret = ret ^ segtree[r]
            r -= 1
        l = l // 2
        r = r // 2
    return ret


def solve(u, v):
    ans = 0

    # different chains
    while tree["chain_top"][u] != tree["chain_top"][v]:
        if tree["size"][tree["chain_top"][u]] < tree["size"][tree["chain_top"][v]]:
            u, v = v, u
        ans ^= range_query(pos_seg[tree["chain_top"][v]], pos_seg[v])
        v = tree["parent"][tree["chain_top"][v]]

    # same chain
    if pos_seg[v] < pos_seg[u]:
        u, v = v, u
    ans ^= range_query(pos_seg[u], pos_seg[v])

    return ans


tree, pos_seg = heavy_light_decomposition(adj_list)
initialize_segtree()

for q in questions:
    if q[0] == 1:
        update(pos_seg[q[1]-1], q[2])
    else:
        print(solve(q[1]-1, q[2]-1))
