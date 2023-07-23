from collections import defaultdict


def diameter(graph):
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

    _, max_dist_node = dfs(graph, 0)
    max_dist, _ = dfs(graph, max_dist_node)
    return max_dist

graph = defaultdict(dict)

V = int(input())

for _ in range(V):
    l  = list(map(int, input().split()))
    for i in range(1, len(l)-1, 2):
        graph[l[0]-1][l[i]-1] = l[i+1]

print(diameter(graph))