import sys
from collections import deque

MAX_COST = 1_000_000_001

n, m = [int(d) for d in sys.stdin.readline().rstrip().split()]
n_nodes = 2*n+2
adj_mat = [[0]*n_nodes for _ in range(n_nodes)]

s, t = [int(d) for d in sys.stdin.readline().rstrip().split()]
adj_mat[0][2*s-1] = MAX_COST
adj_mat[2*t][n_nodes-1] = MAX_COST

c = [int(sys.stdin.readline().rstrip()) for _ in range(n)]
for i, v in enumerate(c):
    adj_mat[2*i+1][2*i+2] = v

for i in range(m):
    s,t = [int(d) for d in sys.stdin.readline().rstrip().split()]
    adj_mat[2*s][2*t-1] = MAX_COST
    adj_mat[2*t][2*s-1] = MAX_COST
    
def dinic(adjacency_list, source, sink, any_flow=False):
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
        
    if any_flow:
        assert source != sink
        return build_level_graph_via_bfs(source,sink)
    else:
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

adjacency_list = adjacency_matrix2adjacency_list_for_dinic(adj_mat)
dinic(adjacency_list, 0, n_nodes-1)

l_answer = set([])
for i in range(1, len(adjacency_list), 2):
    for e in adjacency_list[i]:
        if e[1] == e[2] > 0:
            if e[0] == i+1 and dinic(adjacency_list, 0, i, True) and not dinic(adjacency_list, 0, e[0], True):
                l_answer.add((e[0]+1)//2)
print(" ".join([str(v) for v in sorted(l_answer)]))

