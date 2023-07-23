from collections import defaultdict


def retrieve_connected_trees(graph, n_nodes):

    def dfs(graph, root):
        stack = [root]
        marked = set([root])
        preorder = []
        while stack:
            node = stack.pop()
            preorder.append(node)
            for ne in graph[node]:
                if ne not in marked:
                    stack.append(ne)
                    marked.add(ne)
        return preorder

    list_roots = []
    not_marked = set(range(n_nodes))
    while len(not_marked) > 0:
        root = not_marked.pop()
        nodes = dfs(graph, root)
        list_roots.append(nodes[0]) # root node
        not_marked -= set(nodes)
    return list_roots


def diameter(graph, root):
    """
    graph: defaultdict(dict) (graph[u][v] == graph[v][u] == weight)
    """
    def dfs(graph, root):
        stack = [(root, 0)]
        marked = set([root])
        max_dist = 0
        max_dist_node = root
        while stack:
            node, dist = stack.pop()

            if dist > max_dist:
                max_dist_node = node
                max_dist = dist

            for ne, w in graph[node].items():
                if ne not in marked:
                    stack.append((ne, dist+w))
                    marked.add(ne)

        return max_dist, max_dist_node

    _, max_dist_node = dfs(graph, root)
    max_dist, _ = dfs(graph, max_dist_node)
    return max_dist


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

            for ne, w in graph[node].items():
                if ne not in marked:
                    stack.append((ne, dist+w))
                    marked.add(ne)

        return {node: max(max_dist[node].values(), default=0) for node in max_dist}

    dist_child, parent = dfs_postorder(graph, root)
    max_dist = dfs_preorder(graph, root, dist_child, parent)

    return min(max_dist.values(), default=0)


graph = defaultdict(dict)

N, M, L = map(int, input().split())

for _ in range(M):
    a, b, t = map(int, input().split())
    graph[a][b] = graph[b][a] = t

list_roots = retrieve_connected_trees(graph, N)

max_diameter = max([diameter(graph, root) for root in list_roots], default=0)
list_radius = [radius(graph, tree) for tree in list_roots]

if len(list_roots) == 0:
    print(L)
elif len(list_roots) == 1:
    print(max_diameter)
elif len(list_roots) == 2:
    print(max(max_diameter, sum(list_radius) + L))
else:
    list_radius = sorted(list_radius)
    print(max(max_diameter, sum(list_radius[-2:])+L, sum(list_radius[-3:-1])+2*L))
