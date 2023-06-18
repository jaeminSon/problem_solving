from collections import deque


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

def get_nodes(i,j,m):
    innode = 2*(m*i+j)
    outnode = innode + 1
    return innode, outnode

def is_boundary(i,j,n,m):
    return i==0 or j==0 or i==n-1 or j==m-1

def get_neighbors(i,j,n,m):
    return [(i+dy, j+dx) for dx,dy in zip([0, 0, -1, 1], [-1, 1, 0, 0]) if 0<=i+dy<n and 0<=j+dx<m]

PENALTY = 10**9
INF = 10**15

n, m = map(int, input().split())
adjacency_matrix = [[0 for _ in range(2*n*m+1)] for _ in range(2*n*m+1)]
graph = [list(map(str, input().strip())) for _ in range(n)]
d = list(map(int, input().split()))
for i in range(n):
    for j in range(m):
        if graph[i][j] != '-':
            innode, outnode = get_nodes(i,j,m)
            if graph[i][j] == '*':
                adjacency_matrix[innode][outnode] = INF
                for ne in get_neighbors(i,j,n,m):
                    ne_innode, _ = get_nodes(ne[0],ne[1],m)
                    adjacency_matrix[outnode][ne_innode] = INF
                    source = innode
            else:
                adjacency_matrix[innode][outnode] = d[ord(graph[i][j])-ord('A')] + PENALTY
                for ne in get_neighbors(i,j,n,m):
                    ne_innode, ne_outnode = get_nodes(ne[0],ne[1],m)
                    adjacency_matrix[ne_outnode][innode] = INF
                    adjacency_matrix[outnode][ne_innode] = INF

            if is_boundary(i,j,n,m):
                adjacency_matrix[outnode][2*n*m] = INF

print(dinic(adjacency_matrix2adjacency_list_for_dinic(adjacency_matrix), source, 2*n*m) % PENALTY)
