import sys

N = int(sys.stdin.readline())
list_edges = [[] for _ in range(N)]
for _ in range(N-1):
    s, e, t= [int(el) for el in sys.stdin.readline().split()]
    list_edges[s-1].append((e-1,t))
    list_edges[e-1].append((s-1,t))
    
for i in range(N):
    total_dist = 0
    stack = [(i, 0)]
    set_visited = set([i])
    while stack:
        curr, dist = stack.pop()
        total_dist += dist
        for ch in list_edges[curr]:
            edge_ch, edge_dist = ch
            if edge_ch not in set_visited:
                set_visited.add(edge_ch)
                stack.append((edge_ch, dist + edge_dist))

    print(total_dist)
    
    