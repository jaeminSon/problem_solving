def kruskal_mst(adjacency_list):

    def find(parent:list, i:int):
        if parent[i] != i:
            parent[i] = find(parent, parent[i])
        return parent[i]
 
    def union(parent, rank, x, y):
        xroot = find(parent, x)
        yroot = find(parent, y)
        
        # subsume to higher rank
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else: # tie-break (promote xroot)
            parent[yroot] = xroot
            rank[xroot] += 1

    # sort edges
    edges = [(s,t,w) for s, e in enumerate(adjacency_list) for t, w in e]
    edges.sort(key=lambda x:x[2])

    # union-find data structure
    n_nodes = len(adjacency_list)
    parent = [node for node in range(n_nodes)]
    rank = [0] * n_nodes

    # greedily add edges
    mst = []
    for s, t, w in edges:
        if find(parent, s) != find(parent, t):
            mst.append((s, t, w))
            union(parent, rank, s, t)

    return mst
 
import heapq
def prim_mst(adjacency_list):
    
    start_node = min([(s,t,w) for s, e in enumerate(adjacency_list) for t, w in e], key=lambda x:x[2])[0]
    visited = set([start_node])
    edges = [(cost, start_node, to) for to, cost in adjacency_list[start_node]]
    heapq.heapify(edges)
    
    mst = []
    while edges:
        cost, s, t = heapq.heappop(edges)
        if t not in visited:
            visited.add(t)
            mst.append((s,t, cost))
            for next, cost in adjacency_list[t]:
                if next not in visited:
                    heapq.heappush(edges, (cost, t, next))

    return mst
 
if __name__ == "__main__":
    assert kruskal_mst([[(1,10),(2,6),(3,5)],[(0,10),(3,15)],[(0,6),(3,4)],[(0,5),(2,4)]]) ==  [(2, 3, 4), (0, 3, 5), (0, 1, 10)]
    assert kruskal_mst([[(1,10),(2,6),(3,5)],[(3,15)],[(3,4)],[]]) ==  [(2, 3, 4), (0, 3, 5), (0, 1, 10)]
    assert prim_mst([[(1,10),(2,6),(3,5)],[(0,10),(3,15)],[(0,6),(3,4)],[(0,5),(2,4)]]) == [(2, 3, 4), (3, 0, 5), (0, 1, 10)]
    assert kruskal_mst([[(1,2),(3,6)],[(0,2),(2,3),(3,8),(4,5)],[(1,3),(3,7)],[(0,6),(1,8),(4,9)],[(1,5),(2,7),(3,9)]]) ==  [(0, 1, 2), (1, 2, 3), (1, 4, 5), (0, 3, 6)]
    assert prim_mst([[(1,2),(3,6)],[(0,2),(2,3),(3,8),(4,5)],[(1,3),(3,7)],[(0,6),(1,8),(4,9)],[(1,5),(2,7),(3,9)]]) ==  [(0, 1, 2), (1, 2, 3), (1, 4, 5), (0, 3, 6)]