def bridge_in_graph(adjacency_list):
    
    def _bfs(node, curr_time):
 
        visited[node]= True
        time_visit[node] = curr_time
        lowest_time[node] = curr_time
 
        for neighbor in adjacency_list[node]:
            if visited[neighbor] == False : # first visited neighbor
                parent[neighbor] = node
                _bfs(neighbor, curr_time+1)
                lowest_time[node] = min(lowest_time[node], lowest_time[neighbor])
                
                if lowest_time[neighbor] > time_visit[node]:
                    bridges.append((node, neighbor))
            
            elif neighbor != parent[node]: # revisited neighbor (update node's lowest time)
                lowest_time[node] = min(lowest_time[node], time_visit[neighbor])

    n_nodes = len(adjacency_list)

    visited = [False] * n_nodes
    time_visit = [float("Inf")] * n_nodes
    lowest_time = [float("Inf")] * n_nodes
    parent = [-1] * n_nodes

    bridges = []
    for i in range(n_nodes):
        if visited[i] == False:
            _bfs(i, 0)
    
    return bridges

def edge2adjencylist(list_edges):
    max_node_index = max([max(s,e) for s,e in list_edges])
    result = [[] for _ in range(max_node_index+1)]
    for i in range(max_node_index+1):
        for s,e in list_edges:
            if s==i:
                result[i].append(e)
            if e==i:
                result[i].append(s)
    return result
    
    

if __name__ == "__main__":
    print(bridge_in_graph(edge2adjencylist([[1,0],[0,2],[2,1],[0,3],[3,4]]))) # [3,4], [0,3]
    print(bridge_in_graph(edge2adjencylist([[0, 1], [1, 2], [2, 3]]))) # [2,3], [1,2], [0,1]
    print(bridge_in_graph(edge2adjencylist([[0, 1], [1, 2], [2, 0], [1, 3], [1, 4], [1, 6], [3, 5], [4, 5]]))) # [1,6]

