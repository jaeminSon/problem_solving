import sys
from collections import defaultdict

V, E = [int(d) for d in sys.stdin.readline().rstrip().split()]

g = defaultdict(dict)
degree = defaultdict(int)
for _ in range(E):
    a, b = [int(d) for d in sys.stdin.readline().rstrip().split()]
    g[a-1][b-1] = 1
    g[b-1][a-1] = 1
    degree[a-1] += 1
    degree[b-1] += 1


def dfs_preorder(adjacency_list, root):
    # returns valid preorder sequence
    stack = [root]
    marked = set([root])
    preorder = []
    while stack:
        node = stack.pop()
        preorder.append(node)
        for ne in adjacency_list[node]:
            if ne not in marked:
                stack.append(ne)
                marked.add(ne)
    return preorder

cnt = 0
while len(g) > 0:
    nodes = dfs_preorder(g,next(iter(g.keys())))
    
    n_odd = len([v for v in nodes if degree[v]%2==1])
    if n_odd <= 2:
        cnt += 1
    else:
        cnt += n_odd//2

    for v in nodes:
        del g[v]

print(cnt)