from collections import defaultdict

def get_centroid_recursive(adjacency_list:list):

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


def get_centroid_loop(adjacency_list:list):

    def get_size(root):
        stack = [root]
        visited = set()
        marked = set([root])
        while stack:
            node = stack.pop()
            list_neighbors = [ne for ne in adjacency_list[node] if ne not in marked]
            if len(list_neighbors)==0:
                if node in visited: # intermediate node
                    list_size[node] = 1 + sum([list_size[ne] for ne in adjacency_list[node]])
                else: # leaf node
                    list_size[node] = 1
            else:
                stack.append(node) # push node at first visit of the intermediate node
                # push neighbors
                for ne in list_neighbors:
                    if ne not in marked:
                        stack.append(ne)
                        marked.add(ne)
                visited.add(node)
                    
    def find_centroid(root):
        stack = [root]
        marked = set([root])
        while stack:
            node = stack.pop()
            for ne in adjacency_list[node]:
                if ne not in marked and list_size[ne]*2 > n_nodes:
                    marked.add(ne)
                    stack.append(ne)
        return node

    n_nodes = len(adjacency_list)
    list_size = [0]*n_nodes
    get_size(0)
    return find_centroid(0)

def centroid_decomposition(adjacency_list:dict):
    
    list_size = [0]*(max(adjacency_list.keys())+1)
    
    def get_size(node, parent):
        list_size[node] = 1
        for ne in adjacency_list[node]:
            if ne != parent:
                list_size[node] += get_size(ne, node)
        return list_size[node]

    def get_centroid(node, parent, n_nodes):
        for ne in adjacency_list[node]:
            if ne != parent and list_size[ne]*2 > n_nodes:
                return get_centroid(ne, node, n_nodes)
        return node

    def _recursive(node):
        if len(adjacency_list[node]) == 0:
            children[node] = set()
            return node
        else:
            n_nodes = get_size(node,-1)
            c = get_centroid(node, -1, n_nodes)
            
            neighbors = adjacency_list[c]
            
            for ne in adjacency_list[c]:
                adjacency_list[ne].remove(c)
            del adjacency_list[c]
            
            for ne in neighbors:
                next_c = _recursive(ne)
                children[c].add(next_c)
                parent[next_c] = c
                
            return c
    
    children = defaultdict(set)
    parent = defaultdict(int)
    
    root = _recursive(min(adjacency_list.keys()))
    parent[root] = -1
    
    return parent, children


if __name__ == "__main__":
    ###################
    # tree structure #
    ######   0   ######
    ####  1     2 #####
    ###  3 4   5 6 ####
    ###################
    adjacency_list = [[1, 2], [0, 3, 4], [0, 5, 6], [1], [1], [2], [2]]
    assert get_centroid_recursive(adjacency_list) == 0
    assert get_centroid_loop(adjacency_list) == 0
    
    print(centroid_decomposition({1:{4}, 2:{4}, 3:{4}, 4:{1,2,3,5}, 5:{4, 6}, 6:{5, 7, 10}, 7:{6,8,9}, 8:{7}, 9:{7}, 10:{11, 6}, 11:{10,12,13}, 12:{11, 14}, 13:{11,15,16}, 14:{12}, 15:{13}, 16:{13}}))