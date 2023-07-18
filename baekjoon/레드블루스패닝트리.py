
def kruskal_mst(n_nodes, edges):

    def find(parent: list, i: int):
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
        else:  # tie-break (promote xroot)
            parent[yroot] = xroot
            rank[xroot] += 1

    # union-find data structure
    parent = [node for node in range(n_nodes)]
    rank = [0] * n_nodes

    # greedily add edges
    n_edges = 0
    for s, t in edges:
        if find(parent, s) != find(parent, t):
            n_edges += 1
            union(parent, rank, s, t)

    return n_edges


while True:
    n, m, k = map(int, input().split())
    if n == 0 and m == 0 and k == 0:
        break
    blue_edges, red_edges = [], []
    for _ in range(m):
        color, u, v = input().split()
        if color == "B":
            blue_edges.append((int(u)-1, int(v)-1))
        else:
            red_edges.append((int(u)-1, int(v)-1))

    if kruskal_mst(n, blue_edges+red_edges) != n-1:
        print(0)

    if n-1-kruskal_mst(n, red_edges) <= k and k <= kruskal_mst(n, blue_edges):
        print(1)
    else:
        print(0)
