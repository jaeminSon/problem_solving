import math

N = 100
L = pow(2, math.ceil(math.log2(N)))
segtree = [0] * (2*L)

def heavy_light_decomposition(adjacency_list):
        
    def dfs(curr, parent):
        tree["parent"][curr] = parent
        tree["size"][curr] = 1
        for v in adjacency_list[curr]:
            if v!=parent:
                dfs(v, curr)
                tree["size"][curr] += tree["size"][v]
        
    def _assign_chain_top(curr, parent, chain_top):
        pos_seg[curr] = count[0]
        count[0] += 1
        
        tree["chain_top"][curr] = chain_top
        list_child = [v for v in adjacency_list[curr] if v!=parent]
        if len(list_child) > 0: # intermediate node
            node_heavy_edge = max(list_child, key=lambda x:tree["size"][x])
            _assign_chain_top(node_heavy_edge, curr, chain_top) # remain top for heavy edge
            for v in adjacency_list[curr]:
                if v!=parent and v!=node_heavy_edge:
                    _assign_chain_top(v, curr, v) # light edge (new top)
        
    n_nodes = len(adjacency_list)
    tree = {"size":[None] * n_nodes, "parent":[None] * n_nodes, "chain_top":[None] * n_nodes}
    dfs(0,0)
    count = [0]
    pos_seg = [0] * n_nodes
    _assign_chain_top(0,0,0)
    return tree, pos_seg

def initialize_segtree():
    for p, c, w in edge:
        if tree["parent"][p] == c:
            p,c = c,p
        segtree[L + pos_seg[c]] = w

    for i in range(L-1, 0, -1):
        segtree[i] = max(segtree[i * 2], segtree[i * 2 + 1])
        # segtree[i] = segtree[i * 2] + segtree[i * 2 + 1]

def update(i, w):
    i+=L
    segtree[i] = w
    i = i // 2
    while i > 0:
        segtree[i] = max(segtree[i * 2], segtree[i * 2 + 1])
        # segtree[i] = segtree[i * 2] + segtree[i * 2 + 1]
        i = i // 2

def range_query(l, r):
    # [l,r]
    l += L
    r += L
    ret = 0
    while l<=r:
        if l%2==1:
            ret = max(ret, segtree[l])
            # ret += segtree[l]
            l+=1
        if r%2==0:
            ret = max(ret, segtree[r])
            # ret += segtree[r]
            r-=1
        l = l // 2
        r = r // 2
    return ret

def range_query_between_nodes(u, v):
    ans = 0
    
    # different chains
    while tree["chain_top"][u] != tree["chain_top"][v]:
        if tree["size"][tree["chain_top"][u]] < tree["size"][tree["chain_top"][v]]:
            u, v = v, u
        ans = max(ans, range_query(pos_seg[tree["chain_top"][v]], pos_seg[v]))
        # ans += range_query(pos_seg[tree["chain_top"][v]], pos_seg[v])
        v = tree["parent"][tree["chain_top"][v]]
    
    # same chain
    if pos_seg[v] < pos_seg[u]:
        u, v = v, u
    ans = max(ans, range_query(pos_seg[u]+1, pos_seg[v])) # exclude lca when edge weight is assigned to child
    # ans = max(ans, range_query(pos_seg[u], pos_seg[v]))
    # ans += range_query(pos_seg[u], pos_seg[v]) # sum query from u to v

    return ans

if __name__=="__main__":
    edge = [(0, 1, 1), (1, 2, 2)]
    adjacency_list = [[1], [0, 2], [1]]

    tree, pos_seg = heavy_light_decomposition(adjacency_list)
    initialize_segtree()
    
    assert range_query_between_nodes(1,0)==1 # max weight between node 1 and 0
    update(pos_seg[1],3) # update edge (0-1)'s weight to 3 (node 1 is child)
    assert range_query_between_nodes(1,0)==3 # max weight between node 1 and 0
    