import sys
from collections import deque

INF = 501*500*1000

N = int(sys.stdin.readline().rstrip())

adjacency_matrix = [[0]*(N+2) for _ in range(N+2)]
for i, d in enumerate(sys.stdin.readline().rstrip().split()):
    if d=="1":
        adjacency_matrix[0][i+1] = INF
        adjacency_matrix[i+1][0] = INF
    elif d=="2":
        adjacency_matrix[N+1][i+1] = INF
        adjacency_matrix[i+1][N+1] = INF

for i in range(N):
    row = [int(d) for d in sys.stdin.readline().rstrip().split()]
    for j, w in enumerate(row):
        if j>i:
            adjacency_matrix[i+1][j+1] = w
            adjacency_matrix[j+1][i+1] = w

def dinic(adjacency_list, source, sink):
    n_nodes = len(adjacency_list)
    level = [None] * n_nodes
    
    def build_level_graph_via_bfs(source, sink):
        
        for v in range(n_nodes):
            level[v] = -1
        
        level[source] = 0
        q = deque([source])
        while q:
            u = q.popleft()
            for edge in adjacency_list[u]: # edge: (node, flow, capacity, index of reverse node)
                if level[edge[0]] < 0 and edge[1] < edge[2]:
                    level[edge[0]] = level[u]+1
                    q.append(edge[0])
                     
        return False if level[sink] < 0 else True
    
    
    def send_flow(u, flow, sink, n_edges_explored):
        if u == sink:
            return flow
 
        while n_edges_explored[u] < len(adjacency_list[u]):
            # edge: [node, flow, capacity, index of reverse node]
            edge = adjacency_list[u][n_edges_explored[u]]
            if level[edge[0]] == level[u]+1 and edge[1] < edge[2]:
                avail_flow = min(flow, edge[2]-edge[1])
                flow_sent = send_flow(edge[0],avail_flow,sink,n_edges_explored)
                if flow_sent and flow_sent > 0:
                    edge[1] += flow_sent
                    adjacency_list[edge[0]][edge[3]][1] -= flow_sent
                    return flow_sent
            n_edges_explored[u] += 1
        
    if source == sink:
        return -1
        
    max_flow = 0
    while build_level_graph_via_bfs(source,sink):
        n_edges_explored = [0 for _ in range(n_nodes)]
        while True:
            flow = send_flow(source, float('inf'), sink, n_edges_explored)
            if flow is None:
                break
            else:
                max_flow += flow
    
    return max_flow


def adjacency_matrix2adjacency_list_for_dinic(adjacency_matrix):
    # edge: (node, flow, capacity, index of reverse node)
    adjacency_list = [[] for i in range(len(adjacency_matrix))]
    for i in range(len(adjacency_matrix)):
        for j in range(len(adjacency_matrix[0])):
            if adjacency_matrix[i][j] > 0:
                forward_edge = [j, 0, adjacency_matrix[i][j], len(adjacency_list[j])]
                backward_edge = [i, 0, 0, len(adjacency_list[i])]
                adjacency_list[i].append(forward_edge)
                adjacency_list[j].append(backward_edge)
    
    return adjacency_list
    

adjacency_list = adjacency_matrix2adjacency_list_for_dinic(adjacency_matrix)
flow = dinic(adjacency_list, 0, N+1)

# dfs
list_side_A = []
q = deque([0])
marked = set([0])
while q:
    u = q.popleft()
    if u!=0:
        list_side_A.append(u)
    for edge in adjacency_list[u]: # edge: (node, flow, capacity, index of reverse node)
        if edge[1] < edge[2] and edge[0] not in marked:
            q.append(edge[0])
            marked.add(edge[0])
                
list_side_B = set(range(1,N+1)) - set(list_side_A)

print(flow)
print(" ".join([str(d) for d in list_side_A]))
print(" ".join([str(d) for d in list_side_B]))

