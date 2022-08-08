import sys
from collections import deque, defaultdict

def edmond_karp(n_nodes, adjacency_matrix, source, sink):
    # O(EV^3)
    parent = [None] * n_nodes
    
    def bfs(adjacency_matrix:list, source:int, sink:int, parent:list):
        #  O(V^2)
        q = deque([source])
        marked = set([source])
        while q:
            node = q.popleft() # visit node 
            for neighbor, capacity in adjacency_matrix[node].items():
                if neighbor not in marked and capacity > 0:
                    parent[neighbor] = node
                    if neighbor == sink: # sink reached
                        return True
                    else:
                        marked.add(neighbor)
                        q.append(neighbor)
        return False

    max_flow = 0
    while bfs(adjacency_matrix, source, sink, parent):

        path_flow = float("Inf")
        s = sink
        while s != source:
            path_flow = min(path_flow, adjacency_matrix[parent[s]][s])
            s = parent[s]

        max_flow += path_flow

        v = sink
        while(v != source):
            adjacency_matrix[parent[v]][v] -= path_flow
            adjacency_matrix[v][parent[v]] += path_flow
            v = parent[v]

    return max_flow

N, M  = [int(d) for d in sys.stdin.readline().rstrip().split()]

intermediate_nodes = []
adj_mat = defaultdict(dict)
for _ in range(M):
    i, j, a, b, c = [int(d) for d in sys.stdin.readline().rstrip().split()]
    if i > j:
        i,j = j,i
    
    if i==1 and j==N:
        adj_mat[1][N] = adj_mat[1].get(N, 0) + b
        adj_mat[N][1] = 0
    elif i==1 and j!=N:
        adj_mat[1][j] = adj_mat[1].get(j, 0) + b
        adj_mat[j][N] = adj_mat[j].get(N, 0) + a
        adj_mat[j][1] = 0
        adj_mat[N][j] = 0
    elif i!=1 and j==N:
        adj_mat[1][i] = adj_mat[1].get(i, 0) + c
        adj_mat[i][N] = adj_mat[i].get(N, 0) + b
        adj_mat[i][1] = 0
        adj_mat[N][i] = 0
    else:
        intermediate_nodes.append((i,j,a,b,c))

n_nodes = N+1
for node in intermediate_nodes:
    i,j,a,b,c = node

    adj_mat[i][j] = adj_mat[i].get(j, 0) + b
    adj_mat[j][i] = adj_mat[j].get(i, 0) + b

    # add hallucination node (top)
    adj_mat[1][n_nodes] = c
    adj_mat[n_nodes][i] = c
    adj_mat[n_nodes][j] = c
    if i in adj_mat[1]:
        adj_mat[1][n_nodes] += adj_mat[1][i]
        adj_mat[n_nodes][i] += adj_mat[1][i]
        del adj_mat[1][i]
        del adj_mat[i][1]
    if j in adj_mat[j]:
        adj_mat[1][n_nodes] += adj_mat[1][j]
        adj_mat[n_nodes][j] += adj_mat[1][j]
        del adj_mat[1][j]
        del adj_mat[j][1]
    adj_mat[n_nodes][1] = 0
    adj_mat[i][n_nodes] = 0
    adj_mat[j][n_nodes] = 0
    n_nodes+=1
    # add hallucination node (bottom)
    adj_mat[i][n_nodes] = a
    adj_mat[j][n_nodes] = a
    adj_mat[n_nodes][N] = a
    if N in adj_mat[i]:
        adj_mat[i][n_nodes] += adj_mat[i][N]
        adj_mat[n_nodes][N] += adj_mat[i][N]
        del adj_mat[i][N]
        del adj_mat[N][i]
    if N in adj_mat[j]:
        adj_mat[j][n_nodes] += adj_mat[j][N]
        adj_mat[n_nodes][N] += adj_mat[j][N]
        del adj_mat[j][N]
        del adj_mat[N][j]
    adj_mat[n_nodes][i] = 0
    adj_mat[n_nodes][j] = 0
    adj_mat[N][n_nodes] = 0
    n_nodes+=1
        
print(edmond_karp(n_nodes, adj_mat, 1, N))