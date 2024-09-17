from collections import defaultdict
import sys
sys.setrecursionlimit(100000)

INF = 1 << 20


def bridge_in_graph_loop(adjacency_list, n_nodes, n_edges, root=0):
    bridges = []

    curr = root
    used_edge = [0] * n_edges
    visit_time = [-1] * n_nodes
    lowest_time = [-1] * n_nodes
    parent = [-1] * n_nodes
    index_neighbor = [0] * n_nodes
    visit_time[0] = lowest_time[0] = 0
    timer = 1
    while True:
        if len(adjacency_list[curr]) == index_neighbor[curr]:
            # all neighbors visited, climb to parent

            if curr == root:
                # reach back to the root, thus finished
                break

            # update parent
            p = parent[curr]
            lowest_time[p] = min(lowest_time[p], lowest_time[curr])

            if visit_time[curr] == lowest_time[curr]:
                # curr node is the root of a strongly-connected-component
                bridges.append((curr, p))
            else:
                U[find(curr)] = find(p)

            curr = p
        else:
            neighbor, i = adjacency_list[curr][index_neighbor[curr]]
            index_neighbor[curr] += 1

            if used_edge[i]:
                continue
            used_edge[i] = True

            if visit_time[neighbor] == -1:
                # first time visit to neighbor
                parent[neighbor] = curr
                curr = neighbor
                visit_time[curr] = lowest_time[curr] = timer
                timer += 1
            else:
                # neighbor visited before
                lowest_time[curr] = min(
                    lowest_time[curr], lowest_time[neighbor])

    return bridges


def get_rank(adjacency_list, root):
    # returns valid preorder sequence
    stack = [root]
    marked = set([root])
    rank = {}
    while stack:
        node = stack.pop()
        if len(adjacency_list[node]) == 1:
            rank[node] = len(rank)
        for ne in adjacency_list[node]:
            if ne not in marked:
                stack.append(ne)
                marked.add(ne)
    return rank


def find(k):
    if U[k] != k:
        U[k] = find(U[k])
    return U[k]


N, M = map(int, sys.stdin.readline().split())

G = [[]for _ in range(N)]
for i in range(M):
    s, e = map(int, sys.stdin.readline().split())
    s -= 1
    e -= 1

    G[s].append((e, i))
    G[e].append((s, i))

U = [i for i in range(N)]

bridges = bridge_in_graph_loop(G, N, M)

if len(bridges) == 0:
    print(0)
else:
    shrinked_g = [[] for _ in range(N)]
    for u, v in bridges:
        u = find(u)
        v = find(v)
        shrinked_g[u].append(v)
        shrinked_g[v].append(u)

    rt = 0
    leafs = []
    for i in range(N):
        if len(shrinked_g[i]) == 1:
            leafs.append(i)
        elif len(shrinked_g[i]) > 1:
            rt = i

    rank = get_rank(shrinked_g, rt)
    leafs.sort(key=lambda x: rank[x])

    print((len(leafs)+1) // 2)

    d = len(leafs) // 2
    for i in range(d):
        print(f"{leafs[i]+1} {leafs[i+d]+1}")
    if len(leafs) % 2 == 1:
        print(f"{leafs[0]+1} {leafs[-1]+1}")
