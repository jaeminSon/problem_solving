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

        max_flow +=  path_flow

        v = sink
        while(v != source):
            adjacency_matrix[parent[v]][v] -= path_flow
            adjacency_matrix[v][parent[v]] += path_flow
            v = parent[v]

    return max_flow
 
             
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
    
if __name__=="__main__":
    adjacency_matrix = [[0, 16, 13, 0, 0, 0], [0, 0, 10, 12, 0, 0], [0, 4, 0, 0, 14, 0], [0, 0, 9, 0, 0, 20], [0, 0, 0, 7, 0, 4], [0, 0, 0, 0, 0, 0]]
    print(edmond_karp(adjacency_matrix, 0, 5))
    adjacency_matrix = [[0, 16, 13, 0, 0, 0], [0, 0, 10, 12, 0, 0], [0, 4, 0, 0, 14, 0], [0, 0, 9, 0, 0, 20], [0, 0, 0, 7, 0, 4], [0, 0, 0, 0, 0, 0]]
    print(dinic(adjacency_matrix2adjacency_list_for_dinic(adjacency_matrix), 0, 5))