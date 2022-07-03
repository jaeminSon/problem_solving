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
 
def min_cost_max_flow(capacity_matrix, cost_matrix, source, sink):
    # O(EV*O(bellman_ford))
    # cost_matrix: cost *per flow* 
    #              no default value (check capacity matrix when indexing cost matrix)
    #              cost_matrix[j][i]=-v if cost_matrix[i][j]=v)
    n_nodes = len(capacity_matrix)
    parent = [None] * n_nodes
    
    def bellman_ford(capacity_matrix, cost_matrix, source, sink, parent):
        # O(V^3)
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

from collections import deque, defaultdict
def min_cost_max_flow_fast(capacity_matrix, cost_matrix, source, sink):
    # O(EV|f|)
    # cost_matrix: cost *per flow*
    #              default value: Inf
    #              cost_matrix[j][i]=-v if cost_matrix[i][j]=v
    
    def SPFA(capacity_matrix, cost_matrix:dict, source, sink, parent):
        # update only updated vertices in bellman-ford
        # average: O(E), worst: O(EV)
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
    
    while SPFA(capacity_matrix, dictfy(cost_matrix), source, sink, parent):

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
    assert edmond_karp(adjacency_matrix, 0, 5) == 23
    adjacency_matrix = [[0, 16, 13, 0, 0, 0], [0, 0, 10, 12, 0, 0], [0, 4, 0, 0, 14, 0], [0, 0, 9, 0, 0, 20], [0, 0, 0, 7, 0, 4], [0, 0, 0, 0, 0, 0]]
    assert dinic(adjacency_matrix2adjacency_list_for_dinic(adjacency_matrix), 0, 5) == 23
    assert min_cost_max_flow([[0,3,1,0,3],[0,0,2,0,0],[0,0,0,1,6],[0,0,0,0,2],[0,0,0,0,0]],[[0,1,0,0,2],[0,0,0,3,0],[0,0,0,0,0],[0,0,0,0,1],[0,0,0,0,0]],0,4) == (6,8)
    assert min_cost_max_flow_fast([[0,3,1,0,3],[0,0,2,0,0],[0,0,0,1,6],[0,0,0,0,2],[0,0,0,0,0]],[[0,1,0,0,2],[0,0,0,3,0],[0,0,0,0,0],[0,0,0,0,1],[0,0,0,0,0]],0,4) == (6,8)