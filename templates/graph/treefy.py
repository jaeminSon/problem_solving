import sys
sys.path.append("..")
from custom_type import GRAPH, TREE

from collections import defaultdict



def treefy(edges: GRAPH) -> TREE:
    """
    Split individual node into multiple nodes to make a given graph into a tree.
    >>> treefy([(1, 2), (1, 4), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5)])
    ({1: {2: 1, 4: 1}, 
      2: {1: 1, 3: 1, 6: 1, 5: 1}, 
      4: {1: 1}, 
      3: {2: 1, 7: 1, 8: 1}, 
      6: {2: 1}, 
      5: {2: 1}, 
      7: {3: 1}, 
      8: {3: 1}}, 
      [0, 1, 2, 3, 4, 5, 4, 4, 5, 9, 10, 11, 12, 13])
    """

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
    treenode2graphnode = [i for i in range(max_n_nodes)]
    rank = [0] * max_n_nodes

    n_nodes = len(set([i for e in edges for i in e]))
    tree = defaultdict(dict)
    for u, v in edges:
        root_u = find(u)
        root_v = find(v)
        if root_u == root_v:
            n_nodes += 1
            treenode2graphnode[n_nodes] = v
            v = n_nodes
        else:
            union(u, v)

        tree[u].update({v: 1})
        tree[v].update({u: 1})

    return tree, treenode2graphnode


if __name__ == "__main__":
    print(treefy([(1, 2), (1, 4), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5)]))
