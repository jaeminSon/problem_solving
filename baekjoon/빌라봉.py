from collections import defaultdict


def radius(graph, root):
    """
    graph: defaultdict(dict) (graph[u][v] == graph[v][u] == weight)
    """
    def dfs_postorder(graph, root):

        stack = [root]
        marked = set([root])
        parent = defaultdict(int)
        parent[root] = -1
        dist_child = defaultdict(int)
        while stack:
            node = stack.pop()
            list_unvisited = [ne for ne in graph[node] if ne not in marked]
            if len(list_unvisited) == 0:  # add leaf node or intermediate node
                dist_child[node] = max([0]+[graph[node][ne]+dist_child[ne] for ne in graph[node] if ne != parent[node]])
            else:
                stack.append(node)  # push node at first visit of the intermediate node
                # push neighbors
                for ne in list_unvisited:
                    if ne not in marked:
                        stack.append(ne)
                        marked.add(ne)
                        parent[ne] = node

        return dist_child, parent

    def dfs_preorder(graph, root, dist_child, parent):
        stack = [(root, 0)]
        marked = set([root])
        max_dist = defaultdict(dict)
        diameter = 0
        while stack:
            node, dist = stack.pop()
            if node == root:
                for ne in graph[node]:
                    max_dist[node][ne] = graph[node][ne] + dist_child[ne]
            else:
                p = parent[node]
                max_dist[node][p] = graph[node][p] + max([max_dist[p][ne] for ne in graph[p] if ne != node], default=0)
                for ch in [ne for ne in graph[node] if ne != p]:
                    max_dist[node][ch] = graph[node][ch] + dist_child[ch]

            for u in graph[node]:
                for v in graph[node]:
                    if u != v:
                        diameter = max(diameter, max_dist[node][v] + max_dist[node][u])

            for ne, w in graph[node].items():
                if ne not in marked:
                    stack.append((ne, dist+w))
                    marked.add(ne)

        return {node: max(max_dist[node].values(), default=0) for node in max_dist}, diameter, marked

    dist_child, parent = dfs_postorder(graph, root)
    max_dist, diameter, visited = dfs_preorder(graph, root, dist_child, parent)

    return min(max_dist.values(), default=0), diameter, visited


graph = defaultdict(dict)

N, M, L = map(int, input().split())

for _ in range(M):
    a, b, t = map(int, input().split())
    graph[a][b] = graph[b][a] = t


list_radius = []
max_diameter = 0
not_marked = set(range(N))
while len(not_marked) > 0:
    root = not_marked.pop()
    r, diameter, marked = radius(graph, root)
    list_radius.append(r)
    if len(marked) > 0:
        max_diameter = max(max_diameter, diameter)
    not_marked -= marked

if len(list_radius) == 0:
    print(L)
elif len(list_radius) == 1:
    print(max_diameter)
elif len(list_radius) == 2:
    print(max(max_diameter, sum(list_radius) + L))
else:
    ans1, ans2, ans3 = 0, 0, 0
    for r in list_radius:
        if ans1 <= r:
            ans3 = ans2
            ans2 = ans1
            ans1 = r
        elif ans2 <= r < ans1:
            ans3 = ans2
            ans2 = r
        elif ans3 <= r:
            ans3 = r

    print(max(max_diameter, ans1+ans2+L, ans2 + ans3+2*L))
