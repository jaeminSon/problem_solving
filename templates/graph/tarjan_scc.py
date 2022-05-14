def tarjan_scc(adjacency_list):
    
    def _dfs(node):
        
        # visit node in preorder
        visited[node]= True
        stack.append(node)
        visit_time[node] = timer[0]
        lowest_time[node] = timer[0]
        timer[0]+=1
 
        for neighbor in adjacency_list[node]:
            if visited[neighbor] == False : # first visited neighbor
                _dfs(neighbor)
                lowest_time[node] = min(lowest_time[node], lowest_time[neighbor])
            elif not included_in_scc[neighbor]: # revisited neighbor without previous ssc (update node's lowest time)
                lowest_time[node] = min(lowest_time[node], visit_time[neighbor])

        # check scc in postorder
        if lowest_time[node] == visit_time[node]: # root of scc (including leaf)
            scc = []
            w = -1
            while w != node: # values at the back of stack == nodes of the scc (nodes with no-back-edges already popped)
                w = stack.pop()
                scc.append(w)
            list_ssc.append(scc)
            for i in scc:
                included_in_scc[i] = True
            
    n_nodes = len(adjacency_list)

    visited = [False] * n_nodes
    included_in_scc = [False] * n_nodes
    visit_time = [float("Inf")] * n_nodes
    lowest_time = [float("Inf")] * n_nodes
    timer = [0]

    stack = []
    list_ssc = []

    for i in range(n_nodes):
        if not visited[i]:
            _dfs(i)
            
    
    return list_ssc

def edge2adjencylist(list_edges):
    max_node_index = max([max(s,e) for s,e in list_edges])
    result = [[] for _ in range(max_node_index+1)]
    for i in range(max_node_index+1):
        for s,e in list_edges:
            if s==i:
                result[i].append(e)
    return result
    
    

if __name__ == "__main__":
    print(tarjan_scc(edge2adjencylist([[1,0],[0,2],[2,1],[0,3],[3,4]]))) # [[4], [3], [1, 2, 0]]
    print(tarjan_scc(edge2adjencylist([[0, 1], [1, 2], [2, 3]]))) # [[3], [2], [1], [0]]
    print(tarjan_scc(edge2adjencylist([[0, 1], [1, 2], [2, 0], [1, 3], [1, 4], [1, 6], [3, 5], [4, 5]]))) # [[5], [3], [4], [6], [2, 1, 0]]
    print(tarjan_scc(edge2adjencylist([[1, 0], [0, 2], [2, 1], [0, 3], [3, 4]]))) # [[4], [3], [1, 2, 0]]
    print(tarjan_scc(edge2adjencylist([[0, 1], [1, 2], [2, 3]]))) # [[3],[2],[1],[0]]
    print(tarjan_scc(edge2adjencylist([[0, 1], [1, 2], [2, 0], [1, 3], [1,4],[1,6],[3,5],[4,5]]))) # [[5],[3],[4],[6],[2,1,0]]
    print(tarjan_scc(edge2adjencylist([[0, 1], [0,3], [1,2],[1,4],[2,0],[2,6],[3,2],[4,5],[4,6],[5,6],[5,7],[5,8],[5,9],[6,4],[7,9],[8,9],[9,8]]))) # [[8,9],[7],[5,4,6],[3,2,1,0]]
    print(tarjan_scc(edge2adjencylist([[0, 1], [1, 2], [2, 3], [2,4],[3,0],[4,2]]))) # [[4,3,2,1,0]]