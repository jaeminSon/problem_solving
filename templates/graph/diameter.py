import sys
sys.path.append("..")

from collections import defaultdict

from custom_type import GRAPH, NODE


def diameter(graph: GRAPH, root: NODE = 0) -> int:
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


def radius(graph: GRAPH, root: NODE = 0) -> int:
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

    if len(max_dist) > 0:
        argmin = min(range(len(max_dist)), key=lambda i: max_dist[i])
        return argmin, max_dist[argmin]
    else:
        return -1, 0


###################
# graph structure #
######   0   ######
####  1     2 #####
###  3 4   5 6 ####
###################
graph = defaultdict(dict)
graph[0][1] = 1
graph[1][0] = 1
graph[0][2] = 3
graph[2][0] = 3
graph[1][3] = 3
graph[3][1] = 3
graph[1][4] = 5
graph[4][1] = 5
graph[2][5] = 7
graph[5][2] = 7
graph[2][6] = 9
graph[6][2] = 9

assert diameter(graph) == 18
assert radius(graph) == (2, 9)  # node 2 with radius 9
