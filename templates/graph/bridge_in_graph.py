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


def edge2adjencylist(list_edges):
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
    assert bridge_in_graph(edge2adjencylist([[1, 0], [0, 2], [2, 1], [0, 3], [3, 4]])) == [(3, 4), (0, 3)]
    assert bridge_in_graph(edge2adjencylist([[0, 1], [1, 2], [2, 3]])) == [(2, 3), (1, 2), (0, 1)]
    assert bridge_in_graph(edge2adjencylist([[0, 1], [1, 2], [2, 0], [1, 3], [1, 4], [1, 6], [3, 5], [4, 5]])) == [(1, 6)]
