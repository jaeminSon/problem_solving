import sys
sys.path.append("..")
from custom_type import TREE, LIST1D


def bridge_in_graph(adjacency_list: TREE) -> LIST1D:

    def _preorder_dfs(node):

        visited[node] = True
        visit_time[node] = timer[0]
        lowest_time[node] = timer[0]
        timer[0] += 1

        for neighbor in adjacency_list[node]:
            if visited[neighbor] == False:  # first visited neighbor
                parent[neighbor] = node
                _preorder_dfs(neighbor)
                lowest_time[node] = min(lowest_time[node], lowest_time[neighbor])

                if lowest_time[neighbor] > visit_time[node]:
                    bridges.append((node, neighbor))

            elif neighbor != parent[node]:  # revisited neighbors ignoring parent (update node's lowest time)
                lowest_time[node] = min(lowest_time[node], visit_time[neighbor])

    n_nodes = len(adjacency_list)

    visited = [False] * n_nodes
    visit_time = [float("Inf")] * n_nodes
    lowest_time = [float("Inf")] * n_nodes
    parent = [-1] * n_nodes
    timer = [0]

    bridges = []
    for i in range(n_nodes):
        if visited[i] == False:
            _preorder_dfs(i)

    return bridges


def bridge_in_graph_loop(edges, n_nodes, root=0):
    # edges[0] = (s, e)

    adjacency_list = [[]for _ in range(n_nodes)]
    n_edges = len(edges)
    for i, (s, e) in enumerate(edges):
        adjacency_list[s].append((e, i))
        adjacency_list[e].append((s, i))

    bridges = []
    
    curr = root
    used_edge = [0] * n_edges
    visit_time = [-1] * n_nodes
    lowest_time = [-1] * n_nodes
    parent = [-1] * n_nodes
    index_neighbor = [0] * n_nodes
    visit_time[0] = lowest_time[0] = 0
    timer = 1
    while True:
        if len(adjacency_list[curr]) == index_neighbor[curr]:
            # all neighbors visited, climb to parent

            if curr == root:
                # reach back to the root, thus finished
                break
            
            # update parent
            p = parent[curr]
            lowest_time[p] = min(lowest_time[p], lowest_time[curr])
            
            if visit_time[curr] == lowest_time[curr]:
                # curr node is the root of a strongly-connected-component
                bridges.append((curr, p))
            
            curr = p
        else:
            neighbor, i = adjacency_list[curr][index_neighbor[curr]]
            index_neighbor[curr] += 1
            
            if used_edge[i]:
                continue
            used_edge[i] = True
            
            if visit_time[neighbor] == -1:
                # first time visit to neighbor
                parent[neighbor] = curr
                curr = neighbor
                visit_time[curr] = lowest_time[curr] = timer
                timer += 1
            else:
                # neighbor visited before
                lowest_time[curr] = min(lowest_time[curr], lowest_time[neighbor])
                
    return bridges


def edge2adjacencylist(list_edges):
    max_node_index = max([max(s, e) for s, e in list_edges])
    result = [[] for _ in range(max_node_index+1)]
    for i in range(max_node_index+1):
        for s, e in list_edges:
            if s == i:
                result[i].append(e)
            if e == i:
                result[i].append(s)
    return result


if __name__ == "__main__":
    assert bridge_in_graph(edge2adjacencylist([[1, 0], [0, 2], [2, 1], [0, 3], [3, 4]])) == [(3, 4), (0, 3)]
    assert bridge_in_graph(edge2adjacencylist([[0, 1], [1, 2], [2, 3]])) == [(2, 3), (1, 2), (0, 1)]
    assert bridge_in_graph(edge2adjacencylist([[0, 1], [1, 2], [2, 0], [1, 3], [1, 4], [1, 6], [3, 5], [4, 5]])) == [(1, 6)]
    
    assert bridge_in_graph_loop([[0, 1], [1, 2], [2, 0], [1, 3], [1, 4], [1, 6], [3, 5], [4, 5]], 7) == [(6, 1)]