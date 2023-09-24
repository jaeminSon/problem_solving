import sys
sys.path.append("..")
from custom_type import GRAPH, LIST2D


def tarjan_scc(adjacency_list: GRAPH) -> LIST2D:

    def _dfs(node):

        # visit node in preorder
        visited[node] = True
        stack.append(node)
        visit_time[node] = timer[0]
        lowest_time[node] = timer[0]
        timer[0] += 1

        for neighbor in adjacency_list[node]:
            if visited[neighbor] == False:  # first visited neighbor
                _dfs(neighbor)
                lowest_time[node] = min(lowest_time[node], lowest_time[neighbor])
            elif not included_in_scc[neighbor]:  # revisited neighbor without previous ssc (update node's lowest time)
                lowest_time[node] = min(lowest_time[node], visit_time[neighbor])

        # check scc in postorder
        if lowest_time[node] == visit_time[node]:  # root of scc (including leaf)
            scc = []
            w = -1
            while w != node:  # values at the back of stack == nodes of the scc (nodes with no-back-edges already popped)
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


def kosaraju_scc(adjacency_list: GRAPH) -> LIST2D:

    def _postorder_dfs(node):
        visited[node] = True
        for next_node in adjacency_list[node]:
            if not visited[next_node]:
                _postorder_dfs(next_node)
        stack.append(node)

    def _dfs_transposed_graph(node):
        visited[node] = True
        scc = [node]
        for next_node in adjacency_list_transpose[node]:
            if visited[next_node] == False:
                scc += _dfs_transposed_graph(next_node)
        return scc

    def _transpose_graph(adjacency_list):
        n_nodes = len(adjacency_list)
        adjacency_list_transpose = [[] for _ in range(n_nodes)]
        for s in range(n_nodes):
            for t in adjacency_list[s]:
                adjacency_list_transpose[t].append(s)
        return adjacency_list_transpose

    n_nodes = len(adjacency_list)
    stack = []
    visited = [False]*(n_nodes)
    for i in range(n_nodes):
        if not visited[i]:
            _postorder_dfs(i)  # later node can visit former node

    # check if former node can visit later node by reversing the graph
    adjacency_list_transpose = _transpose_graph(adjacency_list)
    visited = [False]*(n_nodes)
    list_scc = []
    while stack:
        i = stack.pop()
        if visited[i] == False:
            list_scc.append(_dfs_transposed_graph(i))

    return list_scc


def edge2adjencylist(list_edges):
    max_node_index = max([max(s, e) for s, e in list_edges])
    result = [[] for _ in range(max_node_index+1)]
    for i in range(max_node_index+1):
        for s, e in list_edges:
            if s == i:
                result[i].append(e)
    return result


if __name__ == "__main__":
    print(tarjan_scc(edge2adjencylist([[1, 0], [0, 2], [2, 1], [0, 3], [3, 4]])))  # [[4], [3], [1, 2, 0]]
    print(tarjan_scc(edge2adjencylist([[0, 1], [1, 2], [2, 3]])))  # [[3], [2], [1], [0]]
    print(tarjan_scc(edge2adjencylist([[0, 1], [1, 2], [2, 0], [1, 3], [1, 4], [1, 6], [3, 5], [4, 5]])))  # [[5], [3], [4], [6], [2, 1, 0]]
    print(tarjan_scc(edge2adjencylist([[1, 0], [0, 2], [2, 1], [0, 3], [3, 4]])))  # [[4], [3], [1, 2, 0]]
    print(tarjan_scc(edge2adjencylist([[0, 1], [1, 2], [2, 3]])))  # [[3],[2],[1],[0]]
    print(tarjan_scc(edge2adjencylist([[0, 1], [1, 2], [2, 0], [1, 3], [1, 4], [1, 6], [3, 5], [4, 5]])))  # [[5],[3],[4],[6],[2,1,0]]
    print(tarjan_scc(edge2adjencylist([[0, 1], [0, 3], [1, 2], [1, 4], [2, 0], [2, 6], [3, 2], [4, 5], [4, 6],
          [5, 6], [5, 7], [5, 8], [5, 9], [6, 4], [7, 9], [8, 9], [9, 8]])))  # [[8,9],[7],[5,4,6],[3,2,1,0]]
    print(tarjan_scc(edge2adjencylist([[0, 1], [1, 2], [2, 3], [2, 4], [3, 0], [4, 2]])))  # [[4,3,2,1,0]]

    print(kosaraju_scc(edge2adjencylist([[0, 1], [0, 3], [1, 2], [1, 4], [2, 0], [2, 6], [3, 2], [4, 5], [4, 6],
          [5, 6], [5, 7], [5, 8], [5, 9], [6, 4], [7, 9], [8, 9], [9, 8]])))  # [[8,9],[7],[5,4,6],[3,2,1,0]]
    print(kosaraju_scc(edge2adjencylist([[0, 1], [1, 2], [2, 3], [2, 4], [3, 0], [4, 2]])))  # [[4,3,2,1,0]]
    print(kosaraju_scc(edge2adjencylist([[0, 1], [1, 2], [2, 3]])))  # [[3], [2], [1], [0]]
