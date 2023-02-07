import sys

sys.setrecursionlimit(100000)

MOD = 2**32


def dfs(curr, parent):
    hld["parent"][curr] = parent
    hld["size"][curr] = 1
    for v in adjacency_list[curr]:
        if v != parent:
            dfs(v, curr)
            hld["size"][curr] += hld["size"][v]


def _assign_chain_top(curr, parent, chain_top):
    global count
    pos_seg[curr] = count
    count += 1

    hld["chain_top"][curr] = chain_top
    list_child = [v for v in adjacency_list[curr] if v != parent]
    if len(list_child) > 0:  # intermediate node
        node_heavy_edge = max(list_child, key=lambda x: hld["size"][x])
        # remain top for heavy edge
        _assign_chain_top(node_heavy_edge, curr, chain_top)
        for v in adjacency_list[curr]:
            if v != parent and v != node_heavy_edge:
                _assign_chain_top(v, curr, v)  # light edge (new top)

    pos_seg_end[curr] = count-1


def propagate(node_index, node_s, node_e):
    if lazy_add[node_index] != 0 or lazy_mult[node_index] != 1:  # reflect lazy updates
        tree[node_index] *= lazy_mult[node_index]
        tree[node_index] %= MOD
        tree[node_index] += (node_e - node_s + 1) * lazy_add[node_index]
        tree[node_index] %= MOD
        
        if node_s != node_e:  # intermediate node
            lazy_mult[node_index * 2 + 1] *= lazy_mult[node_index]
            lazy_mult[node_index * 2 + 2] *= lazy_mult[node_index]
            lazy_mult[node_index * 2 + 1] %= MOD
            lazy_mult[node_index * 2 + 2] %= MOD
            
            lazy_add[node_index * 2 + 1] *= lazy_mult[node_index]
            lazy_add[node_index * 2 + 2] *= lazy_mult[node_index]
            lazy_add[node_index * 2 + 1] %= MOD
            lazy_add[node_index * 2 + 2] %= MOD

            lazy_add[node_index * 2 + 1] += lazy_add[node_index]
            lazy_add[node_index * 2 + 2] += lazy_add[node_index]
            lazy_add[node_index * 2 + 1] %= MOD
            lazy_add[node_index * 2 + 2] %= MOD
            
        lazy_add[node_index] = 0
        lazy_mult[node_index] = 1


def update_util(node_index, node_s, node_e, s, e, mult, add):
    propagate(node_index, node_s, node_e)

    if node_s <= node_e and node_s <= e and node_e >= s:
        if node_s >= s and node_e <= e:  # [node_s, node_e] in [s,e]
            tree[node_index] += (node_e - node_s + 1) * add
            tree[node_index] %= MOD
            tree[node_index] *= mult
            tree[node_index] %= MOD
            if node_s != node_e:  # intermediate node
                lazy_mult[node_index * 2 + 1] *= mult
                lazy_mult[node_index * 2 + 2] *= mult
                lazy_mult[node_index * 2 + 1] %= MOD
                lazy_mult[node_index * 2 + 2] %= MOD

                lazy_add[node_index * 2 + 1] *= mult
                lazy_add[node_index * 2 + 2] *= mult
                lazy_add[node_index * 2 + 1] %= MOD
                lazy_add[node_index * 2 + 2] %= MOD
                
                lazy_add[node_index * 2 + 1] += add
                lazy_add[node_index * 2 + 2] += add
                lazy_add[node_index * 2 + 1] %= MOD
                lazy_add[node_index * 2 + 2] %= MOD
                
        else:  # [node_s, node_e] and [s,e] overlapping but not inclusive
            mid = (node_s + node_e) // 2
            update_util(node_index * 2 + 1, node_s, mid, s, e, mult, add)
            update_util(node_index * 2 + 2, mid + 1, node_e, s, e, mult, add)
            tree[node_index] = tree[node_index * 2 + 1] + \
                tree[node_index * 2 + 2]


def query_util(node_index, node_s, node_e, s, e):
    propagate(node_index, node_s, node_e)

    if node_s <= node_e and node_s <= e and node_e >= s:
        if node_s >= s and node_e <= e:  # [node_s, node_e] in [s,e]
            return tree[node_index]
        else:  # [node_s, node_e] and [s,e] overlapping but not inclusive
            mid = (node_s + node_e) // 2
            return query_util(2 * node_index + 1, node_s, mid, s, e) + query_util(2 * node_index + 2, mid + 1, node_e, s, e)
    else:
        return 0  # null value for summation query


def update_sub(r, mult, add):
    global N
    update_util(0, 0, N - 1, pos_seg[r], pos_seg_end[r], mult, add)


def query_sub(r):
    global N
    return query_util(0, 0, N-1, pos_seg[r], pos_seg_end[r]) % MOD


def update_path(u, v, mult, add):
    global N
    while hld["chain_top"][u] != hld["chain_top"][v]:
        if hld["size"][hld["chain_top"][u]] < hld["size"][hld["chain_top"][v]]:
            u, v = v, u
        update_util(0, 0, N-1,
                    pos_seg[hld["chain_top"][v]], pos_seg[v], mult, add)
        v = hld["parent"][hld["chain_top"][v]]

    if pos_seg[v] < pos_seg[u]:
        u, v = v, u
    update_util(0, 0, N-1, pos_seg[u], pos_seg[v], mult, add)


def query_path(u, v):
    global N
    ans = 0
    while hld["chain_top"][u] != hld["chain_top"][v]:
        if hld["size"][hld["chain_top"][u]] < hld["size"][hld["chain_top"][v]]:
            u, v = v, u
        ans += query_util(0, 0, N-1, pos_seg[hld["chain_top"][v]], pos_seg[v])
        ans %= MOD
        v = hld["parent"][hld["chain_top"][v]]

    if pos_seg[v] < pos_seg[u]:
        u, v = v, u
    ans += query_util(0, 0, N-1, pos_seg[u], pos_seg[v])
    ans %= MOD
    
    return ans

N, Q = [int(d) for d in sys.stdin.readline().rstrip().split()]

adjacency_list = [[] for _ in range(N)]
for _ in range(N-1):
    s, e = [int(d)-1 for d in sys.stdin.readline().rstrip().split()]
    adjacency_list[s].append(e)
    adjacency_list[e].append(s)

queries = [sys.stdin.readline().rstrip().split() for _ in range(Q)]

n_nodes = len(adjacency_list)
hld = {"size": [None] * n_nodes, "parent": [None]
        * n_nodes, "chain_top": [None] * n_nodes}

dfs(0, 0)
count = 0
pos_seg = [0] * n_nodes
pos_seg_end = [0] * n_nodes
_assign_chain_top(0, 0, 0)

pow2 = 1
while pow2 < N:
    pow2 *= 2
treesize = 2*pow2
tree = [0] * treesize
lazy_mult = [1] * treesize
lazy_add = [0] * treesize

for q in queries:
    if q[0] == "1":
        update_sub(int(q[1])-1, 1, int(q[2]))
    elif q[0] == "2":
        update_path(int(q[1])-1, int(q[2])-1, 1, int(q[3]))
    elif q[0] == "3":
        update_sub(int(q[1])-1, int(q[2]), 0)
    elif q[0] == "4":
        update_path(int(q[1])-1, int(q[2])-1, int(q[3]), 0)
    elif q[0] == "5":
        print(query_sub(int(q[1])-1))
    elif q[0] == "6":
        print(query_path(int(q[1])-1, int(q[2])-1))
