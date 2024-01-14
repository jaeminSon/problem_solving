import sys
sys.setrecursionlimit(10 ** 5)
input = sys.stdin.readline

n, m = map(int, input().split())

adjacency_list = [[] for _ in range(2 * n + 1)]
for _ in range(m):
    i, j = map(int, input().split())
    adjacency_list[-i].append(j)
    adjacency_list[-j].append(i)


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
            _postorder_dfs(i)  # later node can visit former node

    # check if former node can visit later node by reversing the graph
    adjacency_list_transpose = _transpose_graph(adjacency_list)
    scc = [-1] * n_nodes
    count_scc = 0
    while stack:
        i = stack.pop()
        if scc[i] == -1:
            _dfs_transposed_graph(i, count_scc)
            count_scc += 1

    return scc


def solve_2SAT(scc):
    ans = []
    for i in range(1, n+1):
        if scc[i] > scc[-i]:
            ans.append(True)
        elif scc[i] < scc[-i]:
            ans.append(False)
        else:
            return None

    return ans


scc = kosaraju_scc(adjacency_list)

ans = solve_2SAT(scc)

if ans is None:
    print(0)
else:
    print(1)
    print(" ".join([str(int(el)) for el in ans]))
