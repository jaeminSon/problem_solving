import sys
from collections import deque, defaultdict

def min_cost_max_flow(capacity_matrix, cost_matrix, source, sink):
    
    def SPFA(capacity_matrix, cost_matrix, source, sink, parent):
        n_nodes = len(capacity_matrix)
        dist = [float("Inf")] * n_nodes
        dist[source] = 0

        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in cost_matrix[u]:
                if capacity_matrix[u][v] > 0 and dist[u] != float("Inf") and dist[u] + cost_matrix[u][v] < dist[v]:
                    dist[v] = dist[u] + cost_matrix[u][v]
                    parent[v] = u
                    queue.append(v)
        
        if dist[sink] < float("Inf"):
            return True
        else:
            return False  

    def dictfy(mat, ignore_value=float("Inf")):
        l = []
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if mat[i][j]!=ignore_value:
                    l.append((i,j,mat[i][j]))
        
        d = defaultdict(dict)
        for u, v, w in l:
            d[u][v] = w
        
        return d

    n_nodes = len(capacity_matrix)
    parent = [None] * n_nodes
    
    min_cost = 0
    max_flow = 0
    
    cost_matrix = dictfy(cost_matrix)
    
    while SPFA(capacity_matrix, cost_matrix, source, sink, parent):

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

N, M = [int(el) for el in sys.stdin.readline().rstrip().split()]

capacity_matrix = [[0]*(N+M+2) for _ in range(N+M+2)]
cost_matrix = [[float("Inf")]*(N+M+2) for _ in range(N+M+2)]
for i in range(1, N+1):
    capacity_matrix[0][i] = 1
    cost_matrix[0][i] = 0
for i in range(N+1, N+M+1):
    capacity_matrix[i][N+M+1] = 1
    cost_matrix[i][N+M+1] = 0

for i in range(N):
    row = [int(el) for el in sys.stdin.readline().rstrip().split()]
    if row[0] > 0:
        row = row[1:]
        for j in range(len(row)//2):
            task = row[2*j]
            cost = row[2*j+1]
            capacity_matrix[i+1][N+task] = 1
            cost_matrix[i+1][N+task] = cost
            cost_matrix[N+task][i+1] = -cost

mf, nc = min_cost_max_flow(capacity_matrix, cost_matrix, 0, M+N+1)
print(mf)
print(nc)