import sys
from collections import deque

N,F,D  = [int(d) for d in sys.stdin.readline().rstrip().split()]

n_nodes = F+2*N+D+2

adj_mat = [[0]*n_nodes for _ in range(n_nodes)]
for i in range(1,F+1):
    adj_mat[0][i] = 1
for i in range(F+2*N+1,F+2*N+D+1):
    adj_mat[i][n_nodes-1] = 1

for i in range(F+1,F+N+1):
    l = [int(d) for d in sys.stdin.readline().rstrip().split()]
    n_f, n_d = l[0], l[1]
    
    l_f = [l[2+k] for k in range(n_f)]
    for node_f in l_f:
        adj_mat[node_f][i] = 1
        adj_mat[i][i+N] = 1
    
    l_d = [l[2+n_f+k] + F + 2*N for k in range(n_d)]
    for node_d in l_d:
        adj_mat[i+N][node_d] = 1


def dinic(adjacency_list, source, sink):
    # O(V^2E)
    # adjacency_list[v][k]: kth edge of node v
    # edge: [node, flow, capacity, index of reverse node]
    
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


print(dinic(adjacency_matrix2adjacency_list_for_dinic(adj_mat), 0, n_nodes-1))
