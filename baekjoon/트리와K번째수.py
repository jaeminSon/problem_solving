import sys
import math
from collections import defaultdict

sys.setrecursionlimit(100000)

def just_bigger_power_2(val):
    i = 0
    while 2**i < val:
        i += 1
    return 2**i


def generate_tree(tree_size):
    return [[0, 0, 0]] + [[i << 1, i << 1 | 1, 0] for i in range(1, tree_size // 2)] + [[0, 0, 0] for i in range(tree_size // 2)]


def update(node, s, e, increment, index):
    tree[node][2] += increment
    if s != e:
        mid = (s + e) // 2
        left_ch, right_ch, val = tree[node]
        if index <= mid:  # update left child
            tree[node][0] = len(tree)
            tree.append([tree[left_ch][0], tree[left_ch][1], tree[left_ch][2]])
            update(tree[node][0], s, mid, increment, index)
        else:  # update right child
            tree[node][1] = len(tree)
            tree.append(
                [tree[right_ch][0], tree[right_ch][1], tree[right_ch][2]])
            update(tree[node][1], mid + 1, e, increment, index)


def update_tree(cur, par):
    parent[cur] = par
    root[cur] = len(tree)
    tree.append([tree[root[par]][0], tree[root[par]][1], tree[root[par]][2]])
    update(root[cur], 0, L-1, 1, shrinked_coord[cur-1])
    for ne in adj[cur]:
        if ne != parent[cur]:
            update_tree(ne, cur)


def dfs(node, l):
    global step
    appear[node] = step
    depth[node] = l
    visit[step] = node
    level[step] = l
    step += 1
    for ch in adj[node]:
        if appear[ch] is None:
            dfs(ch, l+1)
            visit[step] = node
            level[step] = l
            step += 1


def build_sparse_table(n):
    sparse_table = [[0]*int(math.log2(n)+1) for _ in range(n)]
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
    return sparse_table


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


def get_kth(node_s, node_e, node_lca, node_lca_par, s, e, k):
    if s == e:
        return s
    else:
        left_size = tree[tree[node_s][0]][2] + tree[tree[node_e][0]][2] - tree[tree[node_lca][0]][2] - tree[tree[node_lca_par][0]][2]
        mid = (s + e) // 2
        if k <= left_size:
            return get_kth(tree[node_s][0], tree[node_e][0], tree[node_lca][0], tree[node_lca_par][0], s, mid, k)
        else:
            return get_kth(tree[node_s][1], tree[node_e][1], tree[node_lca][1], tree[node_lca_par][1], mid+1, e, k-left_size)


N, M = [int(d) for d in sys.stdin.readline().rstrip().split()]

l_val = [int(d) for d in sys.stdin.readline().rstrip().split()]

adj = defaultdict(list)
for _ in range(N-1):
    s, e = [int(d) for d in sys.stdin.readline().rstrip().split()]
    adj[s].append(e)
    adj[e].append(s)

queries = [[int(d) for d in sys.stdin.readline().rstrip().split()]
           for _ in range(M)]

n_nodes = len(l_val)
level = [None] * (2*n_nodes+1)
visit = [None] * (2*n_nodes+1)
appear = [None] * (n_nodes+1)
depth = [None] * (n_nodes+1)
step = 0
dfs(1, 0)

sparse_table = build_sparse_table(2*n_nodes-1)

l_unique_sorted = sorted(list(set(l_val)))
mapping = {v: i for i, v in enumerate(l_unique_sorted)}
inverse_mapping = {i: v for i, v in enumerate(l_unique_sorted)}
shrinked_coord = [mapping[el] for el in l_val]

L = len(shrinked_coord)
treesize = 2*just_bigger_power_2(L)
tree = generate_tree(treesize)
parent = [0] * (L+1)
root = [1] * (L+1)

update_tree(1, 0)

for query in queries:
    s, e, k = query
    lca = lca_query(s, e)
    index = get_kth(root[s], root[e], root[lca], root[parent[lca]],0,L-1,k)
    print(inverse_mapping[index])
