import math
import sys

sys.setrecursionlimit(20000)

def heavy_light_decomposition(adjacency_list, root):
        
    def dfs(curr, parent):
        tree["parent"][curr] = parent
        tree["size"][curr] = 1
        for v in adjacency_list[curr]:
            if v!=parent:
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
        
    n_nodes = len(adjacency_list)
    tree = {"size":[None] * n_nodes, "parent":[None] * n_nodes, "chain_top":[None] * n_nodes}
    dfs(root,root)
    count = [0]
    pos_seg = [0] * n_nodes
    _assign_chain_top(root,root,root)
    return tree, pos_seg

def initialize_segtree():
    for node, weight in enumerate(weights):
        segtree[L + pos_seg[node]] = weight

    for i in range(L-1, 0, -1):
        segtree[i] = segtree[i * 2] + segtree[i * 2 + 1]

def update(i, w):
    i+=L
    segtree[i] = w
    i = i // 2
    while i > 0:
        segtree[i] = segtree[i * 2] + segtree[i * 2 + 1]
        i = i // 2

def range_query(l, r):
    # [l,r]
    l += L
    r += L
    ret = 0
    while l<=r:
        if l%2==1:
            ret += segtree[l]
            l+=1
        if r%2==0:
            ret += segtree[r]
            r-=1
        l = l // 2
        r = r // 2
    return ret

def solve(u, v):
    ans = 0
    
    # different chains
    while tree["chain_top"][u] != tree["chain_top"][v]:
        if tree["size"][tree["chain_top"][u]] < tree["size"][tree["chain_top"][v]]:
            u, v = v, u
        ans += range_query(pos_seg[tree["chain_top"][v]], pos_seg[v])
        v = tree["parent"][tree["chain_top"][v]]
    
    # same chain
    if pos_seg[v] < pos_seg[u]:
        u, v = v, u
    ans += range_query(pos_seg[u], pos_seg[v])

    return ans

def init_uf(n):
    for i in range(n):
        parent_node[i] = i
        rank[i] = 0

def find(k):
    if parent_node[k] != k:
        parent_node[k] = find(parent_node[k])
    return parent_node[k]

def not_connected(a, b, connect=False):
    x = find(a)
    y = find(b)
    if x!=y:
        if connect:
            if rank[x] > rank[y]:
                parent_node[y] = x
            elif rank[x] < rank[y]:
                parent_node[x] = y
            else:
                parent_node[y] = x
                rank[x] += 1
        return True
    else:
        return False


N = int(sys.stdin.readline().rstrip())

weights = [int(d) for d in sys.stdin.readline().rstrip().split()]

Q = int(sys.stdin.readline().rstrip())
queries = [sys.stdin.readline().rstrip().split() for _ in range(Q)]

parent_node = {}
rank = {}
init_uf(N)
l = [[] for _ in range(N)]
for q in queries:
    if q[0]=="bridge":
        s, e = int(q[1])-1, int(q[2])-1
        if not_connected(s,e, connect=True):
            l[s].append(e)
            l[e].append(s)
for i in range(N):
    if len(l[i])!=0:
        root = i
        root_parent = find(i)
        break
for i in range(N):
    if not_connected(root_parent, i, connect=True):
        l[i].append(root)
        l[root].append(i)

L = pow(2, math.ceil(math.log2(N)))
segtree = [0] * (2*L)
tree, pos_seg = heavy_light_decomposition(l, root)
initialize_segtree()

init_uf(N)
for q in queries:
    if q[0]=="excursion":
        s,e = int(q[1])-1, int(q[2])-1
        if not not_connected(s,e):
            print(solve(s,e))
        else:
            print("impossible")
    elif q[0]=="bridge":
        s, e = int(q[1])-1, int(q[2])-1
        if not_connected(s,e, connect=True):
            print("yes")
        else:
            print("no")
    else:
        update(pos_seg[int(q[1])-1], int(q[2]))
        