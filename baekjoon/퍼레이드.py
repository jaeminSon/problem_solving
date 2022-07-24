import sys
from collections import defaultdict

N, M = [int(d) for d in sys.stdin.readline().rstrip().split()]

g = defaultdict(dict)
degree = defaultdict(int)
for _ in range(M):
    a, b = [int(d) for d in sys.stdin.readline().rstrip().split()]
    g[a][b] = 1
    g[b][a] = 1
    degree[a] += 1
    degree[b] += 1

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


if len(dfs_preorder(g,next(iter(g.keys()))))==N and (all([d%2==0 for d in degree.values()]) or sum([d%2==0 for d in degree.values()])==N-2):
    print("YES")
else:
    print("NO")
