import sys
sys.path.append("..")
from custom_type import EDGES, TREE

from collections import defaultdict



def graph2tree(edges: EDGES, n_nodes: int) -> TREE:

    def find(k):
        if parent[k] != k:
            parent[k] = find(parent[k])
        return parent[k]

    def union(a, b):
        x = find(a)
        y = find(b)

        if rank[x] > rank[y]:
            parent[y] = x
        elif rank[x] < rank[y]:
            parent[x] = y
        else:
            parent[y] = x
            rank[x] += 1

    max_n_nodes = 2*len(edges)
    parent = [i for i in range(max_n_nodes)]
    original = [i for i in range(max_n_nodes)]
    rank = [0] * max_n_nodes

    tree = defaultdict(dict)
    for u, v in edges:
        root_u = find(u)
        root_v = find(v)
        if root_u == root_v:
            n_nodes += 1
            original[n_nodes] = v
            v = n_nodes
        else:
            union(u, v)

        tree[u].update({v: 1})
        tree[v].update({u: 1})

    return tree, original


if __name__ == "__main__":
    print(graph2tree([(1, 2), (1, 4), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5)], 5))
