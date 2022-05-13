def solution(times, times_limit):
    
    n_nodes = len(times)

    dist = [[0]*n_nodes for _ in range(n_nodes)]
    for i in range(n_nodes):
        dist[i][i] = 0
    for i in range(n_nodes):
        for j in range(n_nodes):
            dist[i][j] = times[i][j]

    # floyd-warshall
    for i_m in range(n_nodes):
        for i_s in range(n_nodes):
            for i_e in range(n_nodes):
                if dist[i_s][i_e] > dist[i_s][i_m] + dist[i_m][i_e]:
                    dist[i_s][i_e] = dist[i_s][i_m] + dist[i_m][i_e]
    
    for i_m in range(n_nodes):
        for i_s in range(n_nodes):
            for i_e in range(n_nodes):
                if dist[i_s][i_e] > dist[i_s][i_m] + dist[i_m][i_e]:
                    # negative cycle found
                    return list(range(n_nodes-2))
    
    curr_best = []
    stack = [([0], 0)]
    while stack:
        path, time = stack.pop()
        if path[-1] == n_nodes - 1:
            if time <= times_limit and len(curr_best) < len(path):
                curr_best = path
        else:
            for i in range(n_nodes-1, -1, -1):
                if i not in path:
                    stack.append((path + [i], time + dist[path[-1]][i]))

    return [el-1 for el in sorted(curr_best[1:-1])]

if __name__=="__main__":
    print(solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1))
    print(solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3))