import sys
sys.path.append("..")
from custom_type import GRAPH, LIST1D


def two_SAT(adjacency_list: GRAPH) -> LIST1D:
    """
    Assumptions
    - adjacency_list has 2*n+1 elements where n is the number of variable types.
    - variable type numbering starts from 1 to n indexing adjacency_list.
    - adjacency_list[0] = [] # dummy node
    """

    def kosaraju_scc(adjacency_list):

        def _postorder_dfs(node):
            visited[node] = True
            for next_node in adjacency_list[node]:
                if not visited[next_node]:
                    _postorder_dfs(next_node)
            stack.append(node)

        def _dfs_transposed_graph(node, count_scc):
            scc[node] = count_scc
            for next_node in adjacency_list_transpose[node]:
                if scc[next_node] == -1:
                    _dfs_transposed_graph(next_node, count_scc)

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
                _postorder_dfs(i)

        adjacency_list_transpose = _transpose_graph(adjacency_list)
        scc = [-1] * n_nodes
        count_scc = 0
        while stack:
            i = stack.pop()
            if scc[i] == -1:
                _dfs_transposed_graph(i, count_scc)
                count_scc += 1

        return scc

    def solve_2SAT(scc, n_variable_types):
        ans = []
        for i in range(1, n_variable_types+1):
            if scc[i] > scc[-i]:
                ans.append(True)
            elif scc[i] < scc[-i]:
                ans.append(False)
            else:
                return None

        return ans

    n_variable_types = len(adjacency_list) // 2

    scc = kosaraju_scc(adjacency_list)

    ans = solve_2SAT(scc, n_variable_types)

    return ans


def cnf2graph(formula):

    variables = set([abs(el) for el in sum([list(el) for el in formula], [])])
    assert max(variables) == len(variables)

    adjacency_list = [[] for _ in range(2 * len(variables) + 1)]
    for i, j in formula:
        # xi v xj == (-xi -> xj) /\ (-xj -> xi)
        adjacency_list[-i].append(j)  # -xi -> xj
        adjacency_list[-j].append(i)  # -xj -> xi

    return adjacency_list


if __name__ == "__main__":

    # (-x1 v x2) /\ (-x2 v x3) /\ (x1 v x3) /\ (x3 v x2)
    formula_2sat = [(-1, 2), (-2, 3), (1, 3), (3, 2)]
    adjacency_list = cnf2graph(formula_2sat)

    assert two_SAT(adjacency_list) in [[True, True, True],
                                       [False, False, True],
                                       [False, True, True]]
