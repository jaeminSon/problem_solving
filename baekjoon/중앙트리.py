import sys

while True:

    N = int(sys.stdin.readline())
    if N==0:
        break
    elif N==1:
        print("0")
    else:
        list_edges = [[] for _ in range(N)]
        for _ in range(N-1):
            s, e, t= [int(el) for el in sys.stdin.readline().split()]
            list_edges[s-1].append((e-1,t))
            list_edges[e-1].append((s-1,t))

        list_edge_tree = [[] for _ in range(N)]
        list_n_ch = [0] * N
        list_total_dist = [0] * N
        total_dist_root = 0
        stack = [(0, 0)]
        set_visited = set([0])
        while stack:
            curr, dist = stack.pop()
            if len(list_edges[curr]) == 1 and curr != 0: # leaf
                total_dist_root += dist
            elif len(list_edge_tree[curr]) > 0: # intermediate nodes revisited
                total_dist_root += dist
                list_n_ch[curr] = len(list_edge_tree[curr]) + sum([list_n_ch[ch] for ch in list_edge_tree[curr]])
            else:
                stack.append((curr, dist))
                for ch in list_edges[curr]:
                    ch_node, edge_dist = ch
                    if ch_node not in set_visited:
                        set_visited.add(ch_node)
                        list_edge_tree[curr].append(ch_node)
                        stack.append((ch_node, dist + edge_dist))

        list_total_dist[0] = total_dist_root
        stack = [0]
        set_visited = set([0])
        while stack:
            curr = stack.pop()
            for ch in list_edges[curr]:
                ch_node, edge_dist = ch
                if ch_node not in set_visited:
                    set_visited.add(ch_node)
                    list_total_dist[ch_node] = list_total_dist[curr] + edge_dist * (N - 2 * list_n_ch[ch_node] - 2)
                    stack.append(ch_node)
        
        print(min(list_total_dist))
            
            