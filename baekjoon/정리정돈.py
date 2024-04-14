from collections import deque, defaultdict

def min_cost_max_flow_fast(capacity_matrix, cost_matrix, source, sink):

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
                if mat[i][j] != ignore_value:
                    l.append((i, j, mat[i][j]))

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
        while (v != source):
            capacity_matrix[parent[v]][v] -= path_flow
            capacity_matrix[v][parent[v]] += path_flow
            v = parent[v]

    return max_flow, min_cost

def dist(p1, p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**(1./2)

N = int(input())

points = []
points_reflected = []
for i in range(N):
    x,y  = map(int, input().split())
    points.append((x,y))
    points_reflected.append((-x,y))

capacity_matrix = [[0]*(2*N+2) for _ in range(2*N+2)]
cost_matrix = [[float("Inf")]*(2*N+2) for _ in range(2*N+2)]
for i in range(1, N+1):
    capacity_matrix[0][i] = 1
    cost_matrix[0][i] = 0
for i in range(N+1, 2*N+1):
    capacity_matrix[i][2*N+1] = 1
    cost_matrix[i][2*N+1] = 0

for i in range(N):
    for j in range(N):
        capacity_matrix[i+1][N+1+j] = 1
        d = dist(points[i], points_reflected[j]) / 2
        cost_matrix[i+1][N+1+j] = d
        cost_matrix[N+1+j][i+1] = -d

max_flow, min_cost = min_cost_max_flow_fast(capacity_matrix, cost_matrix, 0, 2*N+1)

assert max_flow == N

print(f'{min_cost:.3f}')