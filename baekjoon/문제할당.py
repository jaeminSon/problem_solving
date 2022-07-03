import sys

def min_cost_max_flow(capacity_matrix, cost_matrix, source, sink):
    n_nodes = len(capacity_matrix)
    parent = [None] * n_nodes
    
    def bellman_ford(capacity_matrix, cost_matrix, source, sink, parent):
        n_nodes = len(capacity_matrix)
        dist = [float("Inf")] * n_nodes
        dist[source] = 0

        for _ in range(n_nodes - 1):
            for u in range(n_nodes):
                for v in range(n_nodes):
                    if capacity_matrix[u][v] > 0 and dist[u] != float("Inf") and dist[u] + cost_matrix[u][v] < dist[v]:
                        dist[v] = dist[u] + cost_matrix[u][v]
                        parent[v] = u

        if dist[sink] < float("Inf"):
            return True
        else:
            return False  

    min_cost = 0
    max_flow = 0
    while bellman_ford(capacity_matrix, cost_matrix, source, sink, parent):

        path_flow = float("Inf")
        s = sink
        cost = 0
        while s != source:
            path_flow = min(path_flow, capacity_matrix[parent[s]][s])
            cost += cost_matrix[parent[s]][s]
            s = parent[s]

        min_cost += path_flow * cost
        max_flow += path_flow
        
        v = sink
        while(v != source):
            capacity_matrix[parent[v]][v] -= path_flow
            capacity_matrix[v][parent[v]] += path_flow
            v = parent[v]

    return max_flow, min_cost

N = int(sys.stdin.readline().rstrip())
capacity_matrix = [[0]*(2*N+2) for _ in range(2*N+2)]
for i in range(1, N+1):
    capacity_matrix[0][i] = 1
for i in range(1, N+1):
    for j in range(N+1, 2*N+1):
        capacity_matrix[i][j] = 1
for i in range(N+1, 2*N+1):
    capacity_matrix[i][2*N+1] = 1

cost_matrix = [[0]*(2*N+2) for _ in range(2*N+2)]
for i in range(N):
    for j, v in enumerate([int(el) for el in sys.stdin.readline().rstrip().split()]):
        cost_matrix[i+1][N+1+j] = v
        cost_matrix[N+1+j][i+1] = -v

mf, nc = min_cost_max_flow(capacity_matrix, cost_matrix, 0, 2*N+1)
assert mf == N
print(nc)