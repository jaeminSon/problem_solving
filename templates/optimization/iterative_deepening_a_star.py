def iterative_deepening_a_star(adjacency_matrix, heuristic_matrix, start, goal):

    def _recursive_call(s, goal, distance):
        if s == goal:
            return True, distance
        elif distance + heuristic_matrix[s][goal] > threshold[0]:
            return False, distance + heuristic_matrix[s][goal]
        else:
            min_estimate = float("inf")
            for i, w in enumerate(adjacency_matrix[s]):
                if w!=0:
                    path_found, res = _recursive_call(i, goal, distance + adjacency_matrix[s][i])
                    if path_found:
                        return True, res
                    else:
                        min_estimate = min(min_estimate, res)
            return False, min_estimate

    threshold = [heuristic_matrix[start][goal]]
    path_found = False
    while not path_found:
        path_found, res = _recursive_call(start, goal, 0)
        if path_found:
            return res
        elif res == float("inf"):
            return None
        else:
            threshold = [res]

if __name__ == "__main__":
    root2 = 1.41
    adjacency_matrix = [[0,3,3,0,0,0,0],[0,0,0,3,3,0,0],[0,0,0,0,0,3,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,3],[0,0,0,0,0,0,0]]
    heuristic_matrix = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
    print(iterative_deepening_a_star(adjacency_matrix, heuristic_matrix, 0, 6))