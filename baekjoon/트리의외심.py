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
max_height = 20

dp_parent = [[0]*n_nodes for _ in range(max_height)]
depth = [0]*n_nodes
visit = [False]*n_nodes

def dfs(curr, parent, d):
    visit[curr] = True
    dp_parent[0][curr]=parent
    depth[curr]=d
    for ch in adjacency_list[curr]:
        if not visit[ch]:
            dfs(ch, curr, d+1)
    
def go_up(node, dist):
    for i in range(max_height, -1,-1):
        if dist & (1<<i):
            node = dp_parent[i][node]
    return node

def lca_query(node1, node2):
    node1=go_up(node1, max(0, depth[node1]-depth[node2]))
    node2=go_up(node2, max(0, depth[node2]-depth[node1]))
    if node1==node2:
        return node1
    else:
        for i in range(max_height-1, -1, -1):
            if dp_parent[i][node1] != dp_parent[i][node2]:
                node1 = dp_parent[i][node1]
                node2 = dp_parent[i][node2]
        return dp_parent[0][node1]

dfs(0, -1, 0)

# preprocess
for i in range(1, max_height):
    for j in range(n_nodes):
        dp_parent[i][j]=dp_parent[i-1][dp_parent[i-1][j]]

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