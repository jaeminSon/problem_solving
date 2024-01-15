import sys
sys.setrecursionlimit(10 ** 5)
input = sys.stdin.readline


def ccw(p1, p2, p3) -> bool:
    x1, y1, x2, y2, x3, y3 = p1[1], p1[0], p2[1], p2[0], p3[1], p3[0]
    return x1*y2+x2*y3+x3*y1-y1*x2-y2*x3-y3*x1 < 0


def interserct(p1, p2, p3, p4):
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)


def two_SAT(adjacency_list):

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


N = int(input())
sticks = [None] + [list(map(int, input().split())) for _ in range(3 * N)]
adjacency_list = [[] for _ in range(6 * N + 1)]

for i in range(N):
    for m, n in [(3*i+1, 3*i+2), (3*i+1, 3*i+3), (3*i+2, 3*i+3)]:
        # -m v -n
        adjacency_list[m].append(-n)
        adjacency_list[n].append(-m)

for i in range(1, len(sticks)):
    for j in range(i+1, len(sticks)):
        l1 = sticks[i]
        l2 = sticks[j]
        if interserct(l1[:2], l1[2:4], l2[:2], l2[2:4]):
            # i v j
            adjacency_list[-i].append(j)
            adjacency_list[-j].append(i)

ans = two_SAT(adjacency_list)

if ans is None:
    print(-1)
else:
    remove = [str(i+1) for i in range(len(ans)) if ans[i]]
    print(len(remove))
    print(" ".join(remove))
