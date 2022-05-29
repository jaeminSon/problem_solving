def heavy_light_decomposition(adjacency_list):
    
    def dfs(curr, parent, depth):
        tree["parent"][curr] = parent
        tree["depth"][curr] = depth
        tree["size"][curr] = 1
        for v in adjacency_list[curr]:
            if v!=parent:
                tree["size"][curr] += dfs(v, curr, depth+1)
        return tree["size"][curr]
        
    def _assign_chain_top(curr, parent, chain_top):
        tree["chain_top"][curr] = chain_top
        list_child = [v for v in adjacency_list[curr] if v!=parent]
        if len(list_child) > 0: # intermediate node
            node_heavey_edge = max(list_child, key=lambda x:tree["size"][x])
            _assign_chain_top(node_heavey_edge, curr, chain_top) # remain top for heavy edge
            for v in adjacency_list[curr]:
                if v!=parent and v!=node_heavey_edge:
                    _assign_chain_top(v, curr, v) # light edge (new top)
        
    n_nodes = len(adjacency_list)
    tree = {"size":[None] * n_nodes, "parent":[None] * n_nodes, "depth":[None] * n_nodes, "chain_top":[None] * n_nodes}
    dfs(0,0,0)
    _assign_chain_top(0,0,0)
    return tree

def least_common_ancestor(data, u, v):
    # iterate until the same chain
    while data["chain_top"][u] != data["chain_top"][v]:
        if data["depth"][data["chain_top"][u]] < data["depth"][data["chain_top"][v]]:
            v = data["parent"][data["chain_top"][v]]
        else:
            u = data["parent"][data["chain_top"][u]]

    return v if data["depth"][u] < data["depth"][v] else v # return node with lower-level

def max_node(data, u, v):
    
    # get max-node for each chain
    dict_max_node = {n:0 for n in set(data["chain_top"])}
    for node in range(len(tree["chain_top"])):
        dict_max_node[data["chain_top"][node]] = max(data["chain_top"][node], node)
    
    # sweep until lca
    lca = least_common_ancestor(data, u, v)
    ans = 0
    for node in [u, v]:
        while data["chain_top"][node] != data["chain_top"][lca]:
            ans = max(ans, dict_max_node[data["chain_top"][node]])
            node = data["parent"][data["chain_top"][node]]

    return ans

if __name__ == "__main__":
    ########################
    #### tree structure ####
    ######      0   ########
    ####  1     2     3 ####
    ###       4 5 6      ###
    ########################
    adjacency_list = [[1,2,3],[0],[0,4,5,6],[0],[2],[2],[2]]
    tree = heavy_light_decomposition(adjacency_list)
    print(least_common_ancestor(tree, 4, 6)) # 2
    print(least_common_ancestor(tree, 1, 6)) # 0
    print(least_common_ancestor(tree, 1, 3)) # 0
    print(max_node(tree, 4, 6)) # 0
    print(max_node(tree, 1, 6)) # 0
    print(max_node(tree, 1, 3)) # 0
    