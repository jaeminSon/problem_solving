import sys
sys.path.append("..")
from custom_type import TREE, LIST1D


def prufer2tree(prufer:LIST1D) -> TREE:

    n_nodes = len(prufer) + 2
    vertex_set = [0] * n_nodes

    for parent in prufer:
        vertex_set[parent] += 1

    adjacent_list = [[] for _ in range(n_nodes)]
    for parent in prufer:
        for child in range(n_nodes):  # find child node from smallest node
            if vertex_set[child] == 0:
                adjacent_list[parent].append(child)
                adjacent_list[child].append(parent)
                vertex_set[child] = -1
                vertex_set[parent] -= 1
                break

    # last edge
    child, parent = [i for i in range(n_nodes) if vertex_set[i] == 0]
    adjacent_list[parent].append(child)
    adjacent_list[child].append(parent)

    return adjacent_list


def tree2prufer(adjacent_list:TREE) -> LIST1D:
    n_nodes = len(adjacent_list)
    adjacent_list_as_set = [set(vertices) for vertices in adjacent_list]

    prufer = []
    while len(prufer) < n_nodes-2:
        # find leaf with smallest index
        for i, set_vertices in enumerate(adjacent_list_as_set):
            if len(set_vertices) == 1:
                curr_leaf = i
                prufer.append(set_vertices.pop())
                break

        # remove the chosen leaf
        for set_vertices in adjacent_list_as_set:
            set_vertices -= set([curr_leaf])

    return prufer


if __name__ == "__main__":
    assert prufer2tree([3, 0, 2, 3]) ==  [[4, 2], [3], [0, 3], [1, 2, 5], [0], [3]]
    assert tree2prufer([[4, 2], [3], [0, 3], [1, 2, 5], [0], [3]]) == [3, 0, 2, 3]
