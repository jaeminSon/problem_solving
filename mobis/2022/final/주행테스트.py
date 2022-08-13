import sys
from collections import defaultdict

V, E = [int(d) for d in sys.stdin.readline().rstrip().split()]

if E==0: # no edges, connect 1 to 1
    print(1)
else:
    g = defaultdict(dict)
    degree = defaultdict(int)
    for _ in range(E):
        a, b = [int(d) for d in sys.stdin.readline().rstrip().split()]
        if a==b:
            if a==1 and E == 1:
                print(0)
                exit(0)
            else:
                g[a-1] = {}
        else:
            g[a-1][b-1] = 1
            g[b-1][a-1] = 1
            degree[a-1] += 1
            degree[b-1] += 1
    
    if 0 not in g:
        g[0] = {}

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

    n_odd_deg_nodes = []
    while len(g) > 0:
        nodes = dfs_preorder(g,next(iter(g.keys())))
        n_odd_deg_nodes.append(sum([degree[v]%2==1 for v in nodes]))
        for v in nodes:
            del g[v]

    n_component_containing_odd_deg_nodes = sum([el>0 for el in n_odd_deg_nodes])
    n_remaining_odd_degree_nodes = sum(n_odd_deg_nodes) - 2*n_component_containing_odd_deg_nodes
    print(len(n_odd_deg_nodes)+n_remaining_odd_degree_nodes//2)

    