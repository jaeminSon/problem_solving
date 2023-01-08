import sys
import math
from collections import defaultdict

sys.setrecursionlimit(200000)

N,Q  = [int(d) for d in sys.stdin.readline().rstrip().split()]

adj = defaultdict(dict)
for i in range(N-1):
    p = int(sys.stdin.readline().rstrip())
    adj[p-1].update({i+1:1})

L = pow(2, math.ceil(math.log2(N)))
segtree = [1] * (2*L)

problems = [(int(d) for d in sys.stdin.readline().rstrip().split()) for _ in range(Q)]

def heavy_light_decomposition(adjacency_list):
        
    def dfs(curr, parent):
        tree["parent"][curr] = parent
        tree["size"][curr] = 1
        for v in adjacency_list[curr]:
            tree["size"][curr] += dfs(v, curr)
        return tree["size"][curr]
        
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
        
    n_nodes = N
    tree = {"size":[None] * n_nodes, "parent":[None] * n_nodes, "chain_top":[None] * n_nodes}
    dfs(0,0)
    count = [0]
    pos_seg = [0] * n_nodes
    _assign_chain_top(0,0,0)
    return tree, pos_seg

def update(i):
    i+=L
    segtree[i] = 0
    i = i // 2
    while i > 0:
        segtree[i] = segtree[i * 2] & segtree[i * 2 + 1]
        i = i // 2

def range_query(l, r):
    # [l,r]
    l += L
    r += L
    ret = 1
    while l<=r:
        if l%2==1:
            ret = ret & segtree[l]
            l+=1
        if r%2==0:
            ret = ret & segtree[r]
            r-=1
        l = l // 2
        r = r // 2
    return ret

def solve(u, v):
    ans = 1
    
    # different chains
    while tree["chain_top"][u] != tree["chain_top"][v]:
        if tree["size"][tree["chain_top"][u]] < tree["size"][tree["chain_top"][v]]:
            u, v = v, u
        ans = ans & range_query(pos_seg[tree["chain_top"][v]], pos_seg[v])
        v = tree["parent"][tree["chain_top"][v]]
    
    # same chain
    if pos_seg[v] < pos_seg[u]:
        u, v = v, u
    ans = ans & range_query(pos_seg[u]+1, pos_seg[v]) # exclude lca (edge)

    return "YES" if ans==1 else "NO"

tree, pos_seg = heavy_light_decomposition(adj)

for b,c,d in problems:
    ans = solve(b-1, c-1)
    print(ans)
    if d==1:
        if ans=="YES":
            update(pos_seg[b-1])
        else:
            update(pos_seg[c-1])
