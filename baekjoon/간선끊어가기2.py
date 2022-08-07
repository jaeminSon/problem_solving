import sys
from collections import deque

def edmond_karp(adjacency_matrix, source, sink):
    # O(EV^3)
    n_nodes = len(adjacency_matrix)
    parent = [None] * n_nodes
    
    def bfs(adjacency_matrix:list, source:int, sink:int, parent:list):
        #  O(V^2)
        q = deque([source])
        marked = set([source])
        while q:
            node = q.popleft() # visit node 
            for neighbor, capacity in enumerate(adjacency_matrix[node]):
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

adj_mat = [[0]*(N+1) for _ in range(N+1)]
for _ in range(M):
    i, j, w = [int(d) for d in sys.stdin.readline().rstrip().split()]
    adj_mat[i][j] = w
    adj_mat[j][i] = w
        
s, t  = [int(d) for d in sys.stdin.readline().rstrip().split()]

print(edmond_karp(adj_mat, s, t))