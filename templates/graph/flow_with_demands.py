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


def flow_with_vertex_demand(adjacency_matrix):
    n_nodes = len(adjacency_matrix)
    s = n_nodes-2
    t = n_nodes-1

    total_flow_source = sum([new_adjacency_matrix[s][i] for i in range(n_nodes-2)])
    total_flow_target = sum([new_adjacency_matrix[i][t] for i in range(n_nodes-2)])
    if total_flow_source!=total_flow_target:
        return False
    else:
        max_flow = edmond_karp(adjacency_matrix, s, t)
        return total_flow_source == max_flow


def build_graph_for_vertex_demand(adjacency_matrix, demand):
    
    n_nodes = len(adjacency_matrix)
    new_adjacency_matrix = [[0]*(n_nodes+2) for _ in range(n_nodes+2)]
    for i in range(n_nodes):
        for j in range(n_nodes):
            new_adjacency_matrix[i][j] = adjacency_matrix[i][j]
    
    for i in range(n_nodes):
        if demand[i] < 0: # attach to s
            new_adjacency_matrix[n_nodes][i] = -demand[i]
        else: # attach to t
            new_adjacency_matrix[i][n_nodes+1] = demand[i]

    return new_adjacency_matrix


def flow_with_edge_demand(adjacency_matrix):
    n_nodes = len(adjacency_matrix)
    s = n_nodes-2
    t = n_nodes-1

    total_flow_source = sum([new_adjacency_matrix[s][i] for i in range(n_nodes-2)])

    max_flow = edmond_karp(adjacency_matrix, s, t)

    return total_flow_source == max_flow


def build_graph_for_edge_demand(adjacency_matrix, demand_matrix, s, t, ts_flow):
    n_nodes = len(adjacency_matrix)
    new_adjacency_matrix = [[0]*(n_nodes+2) for _ in range(n_nodes+2)]
    for i in range(n_nodes):
        for j in range(n_nodes):
            new_adjacency_matrix[i][j] = adjacency_matrix[i][j] - demand_matrix[i][j]
    
    for i in range(n_nodes): # s'
        new_adjacency_matrix[n_nodes][i] = sum([demand_matrix[k][i] for k in range(n_nodes)])
    for i in range(n_nodes): # t'
        new_adjacency_matrix[i][n_nodes+1] = sum([demand_matrix[i][k] for k in range(n_nodes)])

    # t-s flow
    new_adjacency_matrix[t][s] = ts_flow

    return new_adjacency_matrix


def build_graph_for_vertex_and_edge_demand(adjacency_matrix, vertex_demand, demand_matrix):
    
    n_nodes = len(adjacency_matrix)
    new_vertex_demand = [0] * n_nodes
    for i in range(n_nodes):
        new_vertex_demand[i] = vertex_demand[i]
    new_adjacency_matrix = [[0]*(n_nodes+2) for _ in range(n_nodes+2)]
    for i in range(n_nodes):
        for j in range(n_nodes):
            new_adjacency_matrix[i][j] = adjacency_matrix[i][j] - demand_matrix[i][j]
            new_vertex_demand[i] += demand_matrix[i][j]
            new_vertex_demand[j] -= demand_matrix[i][j]
    
    for i in range(n_nodes):
        if new_vertex_demand[i] < 0: # attach to s
            new_adjacency_matrix[n_nodes][i] = -new_vertex_demand[i]
        else: # attach to t
            new_adjacency_matrix[i][n_nodes+1] = new_vertex_demand[i]

    return new_adjacency_matrix


def min_flow_edge_demand_binary_search(new_adjacency_matrix, demand_matrix, s, t):

    n_nodes = len(new_adjacency_matrix)
    adjacency_matrix_copy = [[0]*n_nodes for _ in range(n_nodes)]

    low = 0
    high = sum([sum(demand_matrix[i]) for i in range(len(demand_matrix))])
    mid = 0
 
    while low < high:
        
        mid = (high + low) // 2
        new_adjacency_matrix[t][s] = mid
        for i in range(n_nodes):
            for j in range(n_nodes):
                adjacency_matrix_copy[i][j] = new_adjacency_matrix[i][j]

        if flow_with_edge_demand(adjacency_matrix_copy):
            high = mid
        else:
            low = mid + 1
 
    return low

if __name__ == "__main__":
    new_adjacency_matrix = build_graph_for_vertex_demand([[0,0,3,1],[2,0,0,3],[0,0,0,0],[0,0,2,0]], [-3,-3,2,4])
    assert flow_with_vertex_demand(new_adjacency_matrix)
    new_adjacency_matrix = build_graph_for_vertex_demand([[0,0,3,1],[2,0,0,2],[0,0,0,0],[0,0,2,0]], [-3,-3,2,4])
    assert not flow_with_vertex_demand(new_adjacency_matrix)

    adjacency_matrix = [[0,0,4,0,0,0], [5,0,5,4,0,0],[0,0,0,3,0,1],[0,0,0,0,0,5],[3,3,0,0,0,0],[0,0,0,0,0,0]]
    demand_matrix = [[0,0,0,0,0,0],[0,0,1,0,0,0],[0,0,0,0,0,1],[0,0,0,0,0,5],[3,3,0,0,0,0],[0,0,0,0,0,0]]
    new_adjacency_matrix = build_graph_for_edge_demand(adjacency_matrix, demand_matrix, 4, 5, 100)
    assert min_flow_edge_demand_binary_search(new_adjacency_matrix, demand_matrix, 4, 5) == 6 
    
    adjacency_matrix = [[0,0,4,0], [5,0,5,4],[0,0,0,3],[0,0,0,0]]
    vertex_demand = [-3, -4, 2, 5]
    demand_matrix = [[0,0,0,0],[0,0,1,0],[0,0,0,0],[0,0,0,0]]
    new_adjacency_matrix = build_graph_for_vertex_and_edge_demand(adjacency_matrix, vertex_demand, demand_matrix)
    print(new_adjacency_matrix)
    assert flow_with_vertex_demand(new_adjacency_matrix)