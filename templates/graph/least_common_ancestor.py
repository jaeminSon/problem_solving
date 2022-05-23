def least_common_ancestor(adjacency_list, node1, node2):
    n_nodes = len(adjacency_list)
    level = [None] * (2*n_nodes)
    visit = [None] * (2*n_nodes)
    appear = [None] * n_nodes

    def _dfs(node, l):
        appear[node] = index[0]
        visit[index[0]] = node
        level[index[0]] = l
        index[0]+=1
        for ch in adjacency_list[node]:
            _dfs(ch, l+1)
            visit[index[0]] = node
            level[index[0]] = l
            index[0]+=1

    index = [0]
    _dfs(0,0)

    index_from = min(appear[node1], appear[node2])
    index_to = max(appear[node1], appear[node2])
    index_visit = min(range(index_from, index_to+1), key=lambda i:level[i]) # can be O(nlogn) preprocess and O(1) query with sparse table
    return visit[index_visit]
    


if __name__=="__main__":
    assert least_common_ancestor([[1,7],[2,3,6],[],[4,5],[],[],[],[8,9],[],[]], 4, 6) == 1