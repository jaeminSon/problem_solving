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

list_odd_node = []
list_even_node = []
list_dispense_node = []
while len(g) > 0:
    nodes = dfs_preorder(g,next(iter(g.keys())))
    list_odd_node.append([v for v in nodes if degree[v]%2==1])
    list_even_node.append([v for v in nodes if degree[v]%2==0])
    if len(list_odd_node[-1]) == 0:
        list_dispense_node.append([list_even_node[-1][0]]*2)
    else:
        list_dispense_node.append(list_odd_node[-1])
    
    for v in nodes:
        del g[v]

list_new_edge = []
if len(list_dispense_node) == 1:
    while len(list_odd_node[0]) > 0:
        v = list_odd_node[0].pop()
        w = list_odd_node[0].pop()
        list_new_edge.append((v, w))
else:
    for i in range(len(list_dispense_node)-1, -1, -1):
        v = list_dispense_node[i].pop()
        w = list_dispense_node[i-1].pop()
        list_new_edge.append((v, w))
    for i in range(len(list_dispense_node)):
        while len(list_dispense_node[i]) > 0:
            v = list_dispense_node[i].pop()
            w = list_dispense_node[i].pop()
            list_new_edge.append((v, w))

print(len(list_new_edge))
for u,v in list_new_edge:
    print("{} {}".format(u+1, v+1))
