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

level = [None] * (2*n_nodes-1)
visit = [None] * (2*n_nodes-1)
appear = [None] * n_nodes
depth = [None] * n_nodes

step = 0

n = 2*n_nodes-1
sparse_table = [[0]*int(math.log2(n)+1) for _ in range(n)]
    
def dfs(node, l):
    global step
    appear[node] = step
    depth[node] = l
    visit[step] = node
    level[step] = l
    step+=1
    for ch in adjacency_list[node]:
        if appear[ch] is None:
            dfs(ch, l+1)
            visit[step] = node
            level[step] = l
            step+=1
    
def lca_query(node1, node2):
    if node1 == node2:
        return node1
    elif appear[node1] <= appear[node2]:
        L, R = appear[node1], appear[node2]
    else:
        L, R = appear[node2], appear[node1]
    
    j = int(math.log2(R - L + 1))

    if sparse_table[L][j][0] > sparse_table[R - (1 << j) + 1][j][0]:
        return visit[sparse_table[R - (1 << j) + 1][j][1]]
    else:
        return visit[sparse_table[L][j][1]]

def go_up(s, d):
    for _ in range(d):
        for e in backward_adj[s]:
            s = e
    return s

dfs(0,0)

# build_sparse_table
for i in range(n):
    sparse_table[i][0] = (level[i], i)
j = 1
while (1 << j) <= n:
    i = 0
    while i + (1 << j) - 1 < n:
        # min in [i, i+2^j-1] = min(min in [i,i+2^(j-1)-1], min in [i+2^(j-1), i+2^j-1])
        if sparse_table[i][j - 1][0] > sparse_table[i + (1 << (j - 1))][j - 1][0]:
            sparse_table[i][j] = sparse_table[i + (1 << (j - 1))][j - 1]
        else:
            sparse_table[i][j] = sparse_table[i][j - 1]
        i += 1
    j += 1    

# remain backward edges
backward_adj = defaultdict(dict)
for s in adjacency_list:
    for e in adjacency_list[s]:
        if depth[s] > depth[e]:
            backward_adj[s].update({e:1})

# solve
for p in problems:
    a,b,c = p
    lca_ab = lca_query(a,b)
    lca_bc = lca_query(b,c)
    lca_ca = lca_query(c,a)
    
    if lca_ab == lca_bc == lca_ca:
        depths = sorted([depth[a],depth[b],depth[c]])
        if depths[0] == depths[1] and (depths[2]-depths[0]) % 2 == 0:
            d = depths[2] - depth[lca_ab] - (depths[2] - depths[0])//2
            deepest_node = max([a,b,c], key=lambda x: depth[x])
            print(go_up(deepest_node, d)+1)
        else:
            print(-1)
    else:
        lca_top = lca_query(lca_ab, c)
        if depth[lca_ab] == depth[lca_ca] < depth[lca_bc]:
            l_dist = [depth[b]-depth[lca_bc], depth[c]-depth[lca_bc], depth[lca_bc]-depth[lca_top]+depth[a]-depth[lca_top]]
        elif depth[lca_ab] == depth[lca_bc] < depth[lca_ca]:
            l_dist = [depth[c]-depth[lca_ca], depth[a]-depth[lca_ca], depth[lca_ca]-depth[lca_top]+depth[b]-depth[lca_top]]
        elif depth[lca_ca] == depth[lca_bc] < depth[lca_ab]:
            l_dist = [depth[a]-depth[lca_ab], depth[b]-depth[lca_ab], depth[lca_ab]-depth[lca_top]+depth[c]-depth[lca_top]]
        else:
            raise ValueError("lca infeasible.")

        l_dist = sorted(l_dist)
        if l_dist[0] == l_dist[1] and (l_dist[2]-l_dist[0]) % 2==0:
            d = l_dist[0] + (l_dist[2]-l_dist[0])//2
            deepest_node = max([a,b,c], key=lambda x: depth[x])
            print(go_up(deepest_node, d)+1)
        else:
            print(-1)