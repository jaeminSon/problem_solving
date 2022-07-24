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

for v in range(V):
    if v not in g:
        g[v] = {}

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

l = []
while len(g) > 0:
    nodes = dfs_preorder(g,next(iter(g.keys())))
    l.append(sum([degree[v]%2==1 for v in nodes]))
    for v in nodes:
        del g[v]

remain = sum(l) - 2*(sum([el>0 for el in l])-1)
assert remain % 2 ==0

if remain<=2:
    print(len(l)-1)
else:
    print(len(l)-1+(remain-2)//2)
