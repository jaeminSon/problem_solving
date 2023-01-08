import sys
import math
from collections import defaultdict

sys.setrecursionlimit(100000)

N = int(sys.stdin.readline().rstrip())

# no weight (uniform weight)
adjacency_list = defaultdict(dict)
for _ in range(N-1):
    s,e  = [int(d)-1 for d in sys.stdin.readline().rstrip().split()]
    adjacency_list[s].update({e:1})
    adjacency_list[e].update({s:1})

Q = int(sys.stdin.readline().rstrip())

problems = [(int(d)-1 for d in sys.stdin.readline().rstrip().split()) for _ in range(Q)]

n_nodes = len(adjacency_list)
tree = {"size":[None] * n_nodes, "parent":[None] * n_nodes, "depth":[None] * n_nodes, "chain_top":[None] * n_nodes}


def dfs(curr, parent, depth):
    tree["parent"][curr] = parent
    tree["depth"][curr] = depth
    tree["size"][curr] = 1
    for v in adjacency_list[curr]:
        if v!=parent:
            tree["size"][curr] += dfs(v, curr, depth+1)
    return tree["size"][curr]
    
def _assign_chain_top(curr, parent, chain_top):
    tree["chain_top"][curr] = chain_top
    list_child = [v for v in adjacency_list[curr] if v!=parent]
    if len(list_child) > 0: # intermediate node
        node_heavy_edge = max(list_child, key=lambda x:tree["size"][x])
        _assign_chain_top(node_heavy_edge, curr, chain_top) # remain top for heavy edge
        for v in adjacency_list[curr]:
            if v!=parent and v!=node_heavy_edge:
                _assign_chain_top(v, curr, v) # light edge (new top)
    
dfs(0,-1,0)
_assign_chain_top(0,-1,0)

def lca_query(u, v):
    # iterate until the same chain
    while tree["chain_top"][u] != tree["chain_top"][v]:
        if tree["depth"][tree["chain_top"][u]] < tree["depth"][tree["chain_top"][v]]:
            v = tree["parent"][tree["chain_top"][v]]
        else:
            u = tree["parent"][tree["chain_top"][u]]

    return u if tree["depth"][u] < tree["depth"][v] else v # return node with lower-level


def go_up(s, d):
    for _ in range(d):
        for e in backward_adj[s]:
            s = e
    return s

# remain backward edges
backward_adj = defaultdict(dict)
for s in adjacency_list:
    for e in adjacency_list[s]:
        if tree["depth"][s] > tree["depth"][e]:
            backward_adj[s].update({e:1})

# solve
for p in problems:
    a,b,c = p
    lca_ab = lca_query(a,b)
    lca_bc = lca_query(b,c)
    lca_ca = lca_query(c,a)
    
    if lca_ab == lca_bc == lca_ca:
        depths = sorted([tree["depth"][a],tree["depth"][b],tree["depth"][c]])
        if depths[0] == depths[1] and (depths[2]-depths[0]) % 2 == 0:
            d = depths[2] - tree["depth"][lca_ab] - (depths[2] - depths[0])//2
            deepest_node = max([a,b,c], key=lambda x: tree["depth"][x])
            print(go_up(deepest_node, d)+1)
        else:
            print(-1)
    else:
        lca_top = lca_query(lca_ab, c)
        if tree["depth"][lca_ab] == tree["depth"][lca_ca] < tree["depth"][lca_bc]:
            l_dist = [tree["depth"][b]-tree["depth"][lca_bc], tree["depth"][c]-tree["depth"][lca_bc], tree["depth"][lca_bc]-tree["depth"][lca_top]+tree["depth"][a]-tree["depth"][lca_top]]
        elif tree["depth"][lca_ab] == tree["depth"][lca_bc] < tree["depth"][lca_ca]:
            l_dist = [tree["depth"][c]-tree["depth"][lca_ca], tree["depth"][a]-tree["depth"][lca_ca], tree["depth"][lca_ca]-tree["depth"][lca_top]+tree["depth"][b]-tree["depth"][lca_top]]
        elif tree["depth"][lca_ca] == tree["depth"][lca_bc] < tree["depth"][lca_ab]:
            l_dist = [tree["depth"][a]-tree["depth"][lca_ab], tree["depth"][b]-tree["depth"][lca_ab], tree["depth"][lca_ab]-tree["depth"][lca_top]+tree["depth"][c]-tree["depth"][lca_top]]
        else:
            raise ValueError("lca infeasible.")

        l_dist = sorted(l_dist)
        if l_dist[0] == l_dist[1] and (l_dist[2]-l_dist[0]) % 2==0:
            d = l_dist[0] + (l_dist[2]-l_dist[0])//2
            deepest_node = max([a,b,c], key=lambda x: tree["depth"][x])
            print(go_up(deepest_node, d)+1)
        else:
            print(-1)