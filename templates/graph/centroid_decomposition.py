def get_centroid(adjacency_list:list):

    def get_size(node, parent):
        list_size[node] = 1
        for ne in adjacency_list[node]:
            if ne != parent:
                list_size[node] += get_size(ne, node)
        return list_size[node]

    def _recursive(node, parent):
        for ne in adjacency_list[node]:
            if ne != parent and list_size[ne]*2 > n_nodes:
                return _recursive(ne, node)
        return node

    n_nodes = len(adjacency_list)
    list_size = [0]*n_nodes
    get_size(0,-1)
    return _recursive(0,-1)


if __name__ == "__main__":
    ###################
    # tree structure #
    ######   0   ######
    ####  1     2 #####
    ###  3 4   5 6 ####
    ###################
    adjacency_list = [[1, 2], [0, 3, 4], [0, 5, 6], [1], [1], [2], [2]]
    assert get_centroid(adjacency_list) == 0