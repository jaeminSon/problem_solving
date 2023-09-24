import sys
sys.path.append("..")
from custom_type import TREE, TREE_HLD, NODE


def heavy_light_decomposition(adjacency_list: TREE) -> TREE_HLD:

    def dfs(curr, parent, depth):
        tree["parent"][curr] = parent
        tree["depth"][curr] = depth
        tree["size"][curr] = 1
        for v in adjacency_list[curr]:
            if v != parent:
                tree["size"][curr] += dfs(v, curr, depth+1)
        return tree["size"][curr]

    def _assign_chain_top(curr, parent, chain_top):
        tree["chain_top"][curr] = chain_top
        list_child = [v for v in adjacency_list[curr] if v != parent]
        if len(list_child) > 0:  # intermediate node
            node_heavy_edge = max(list_child, key=lambda x: tree["size"][x])
            _assign_chain_top(node_heavy_edge, curr, chain_top)  # remain top for heavy edge
            for v in adjacency_list[curr]:
                if v != parent and v != node_heavy_edge:
                    _assign_chain_top(v, curr, v)  # light edge (new top)

    n_nodes = len(adjacency_list)
    tree = {"size": [None] * n_nodes, "parent": [None] * n_nodes, "depth": [None] * n_nodes, "chain_top": [None] * n_nodes}
    dfs(0, -1, 0)
    _assign_chain_top(0, -1, 0)
    return tree


def least_common_ancestor(tree: TREE_HLD, u: NODE, v: NODE) -> NODE:
    # iterate until the same chain
    while tree["chain_top"][u] != tree["chain_top"][v]:
        if tree["depth"][tree["chain_top"][u]] < tree["depth"][tree["chain_top"][v]]:
            v = tree["parent"][tree["chain_top"][v]]
        else:
            u = tree["parent"][tree["chain_top"][u]]

    return u if tree["depth"][u] < tree["depth"][v] else v  # return node with lower-level


def max_node(tree: TREE_HLD, u: NODE, v: NODE) -> NODE:

    # get max-node for each chain
    dict_max_node = {n: 0 for n in set(tree["chain_top"])}
    for node in range(len(tree["chain_top"])):
        dict_max_node[tree["chain_top"][node]] = max(tree["chain_top"][node], node)

    # sweep until lca
    lca = least_common_ancestor(tree, u, v)
    ans = 0
    for node in [u, v]:
        while tree["chain_top"][node] != tree["chain_top"][lca]:
            ans = max(ans, dict_max_node[tree["chain_top"][node]])
            node = tree["parent"][tree["chain_top"][node]]

    return ans


if __name__ == "__main__":
    ########################
    #### tree structure ####
    ######      0   ########
    ####  1     2     3 ####
    ###       4 5 6      ###
    ########################
    adjacency_list = [[1, 2, 3], [0], [0, 4, 5, 6], [0], [2], [2], [2]]
    tree = heavy_light_decomposition(adjacency_list)
    assert least_common_ancestor(tree, 4, 6) == 2
    assert least_common_ancestor(tree, 1, 6) == 0
    assert least_common_ancestor(tree, 1, 3) == 0
    assert max_node(tree, 4, 6) == 6
    assert max_node(tree, 1, 6) == 6
    assert max_node(tree, 1, 3) == 3
