import sys

sys.setrecursionlimit(200000)

N = int(sys.stdin.readline().rstrip())
    
l = [[] for _ in range(N)]
for _ in range(N-1):
    s,e = [int(d) for d in sys.stdin.readline().rstrip().split()]
    l[s-1].append(e-1)
    l[e-1].append(s-1)

def heavy_light_decomposition(adjacency_list):
    
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
        
    n_nodes = len(adjacency_list)
    tree = {"size":[None] * n_nodes, "parent":[None] * n_nodes, "depth":[None] * n_nodes, "chain_top":[None] * n_nodes}
    dfs(0,-1,0)
    _assign_chain_top(0,-1,0)
    return tree

def least_common_ancestor(tree, u, v):
    # iterate until the same chain
    while tree["chain_top"][u] != tree["chain_top"][v]:
        if tree["depth"][tree["chain_top"][u]] < tree["depth"][tree["chain_top"][v]]:
            v = tree["parent"][tree["chain_top"][v]]
        else:
            u = tree["parent"][tree["chain_top"][u]]

    return u if tree["depth"][u] < tree["depth"][v] else v # return node with lower-level


tree = heavy_light_decomposition(l)

M = int(sys.stdin.readline().rstrip())
Q = [[int(d) for d in sys.stdin.readline().rstrip().split()] for _ in range(M)]

for s,e in Q:
    print(least_common_ancestor(tree, s-1, e-1)+1)