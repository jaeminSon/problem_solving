import heapq

INF = 10 ** 10 + 1
size = 1 << 11


class SegmentTreeLazyPropagation:
    def __init__(self, arr):
        N = len(arr)
        self.tree = [INF] * 2 * self.just_bigger_power_2(N)
        self.lazy = [INF] * 2 * self.just_bigger_power_2(N)
        self.len = N
        self.initialize(arr, 0, N-1, 0)

    def just_bigger_power_2(self, val):
        i = 0
        while 2**i < val:
            i += 1
        return 2**i

    def initialize(self, arr, s, e, index):
        if s <= e:
            if s == e:  # leaf node
                self.tree[index] = arr[s]
            else:
                mid = (s + e) // 2
                self.initialize(arr, s, mid, index * 2 + 1)
                self.initialize(arr, mid + 1, e, index * 2 + 2)
                self.tree[index] = min(
                    self.tree[index * 2 + 1], self.tree[index * 2 + 2])

    def update(self, s, e, diff):
        self.update_util(0, 0, self.len - 1, s, e, diff)

    def propagate(self, node_index, node_s, node_e):
        if self.lazy[node_index] != 0:  # reflect lazy updates
            self.tree[node_index] = min(
                self.tree[node_index], self.lazy[node_index])
            if node_s != node_e:  # propagate to children which are intermediate nodes
                self.lazy[node_index * 2 +
                          1] = min(self.lazy[node_index * 2 + 1], self.lazy[node_index])
                self.lazy[node_index * 2 +
                          2] = min(self.lazy[node_index * 2 + 2], self.lazy[node_index])
            self.lazy[node_index] = INF

    def update_util(self, node_index, node_s, node_e, s, e, diff):
        self.propagate(node_index, node_s, node_e)

        if node_s <= node_e and node_s <= e and node_e >= s:
            if node_s >= s and node_e <= e:  # [node_s, node_e] in [s,e]
                self.lazy[node_index] = diff
                self.propagate(node_index, node_s, node_e)
            else:  # [node_s, node_e] and [s,e] overlapping but not inclusive
                mid = (node_s + node_e) // 2
                self.update_util(node_index * 2 + 1, node_s, mid, s, e, diff)
                self.update_util(node_index * 2 + 2, mid +
                                 1, node_e, s, e, diff)
                self.tree[node_index] = min(
                    self.tree[node_index * 2 + 1], self.tree[node_index * 2 + 2])

    def query_util(self, node_index, node_s, node_e, s, e):
        self.propagate(node_index, node_s, node_e)

        if node_s <= node_e and node_s <= e and node_e >= s:
            if node_s >= s and node_e <= e:  # [node_s, node_e] in [s,e]
                return self.tree[node_index]
            else:  # [node_s, node_e] and [s,e] overlapping but not inclusive
                mid = (node_s + node_e) // 2
                return min(self.query_util(2 * node_index + 1, node_s, mid, s, e), self.query_util(2 * node_index + 2, mid + 1, node_e, s, e))
        else:
            return INF

    def query(self, s, e):
        return self.query_util(0, 0, self.len-1, s, e)


def set_dist_dijkstra(s, adjacency_list, distance):

    distance[s] = 0
    pq = [(0, s)]

    while pq:
        cost, curr = heapq.heappop(pq)
        if distance[curr] < cost:
            continue
        for next, cost in adjacency_list[curr]:
            if distance[next] > distance[curr] + cost:
                distance[next] = distance[curr] + cost
                heapq.heappush(pq, (distance[next], next))


def set_parent(par, dist, init_element):

    stack = [init_element]

    while stack:
        curr, prev, root = stack.pop()

        if node2rank[curr] != 0:
            root = curr

        par[curr] = root

        for next, cost in adjacency_list[curr]:
            if not (node2rank[curr] == 0 and node2rank[next] != 0) and (par[next] == 0) and (next != prev) and (dist[next] == dist[curr]+cost):
                stack.append((next, curr, root))


n, m, start, end = map(int, input().split())
adjacency_list = [[] for _ in range(n + 1)]

for _ in range(m):
    u, v, w = map(int, input().split())
    adjacency_list[u].append((v, w))
    adjacency_list[v].append((u, w))

k, *path = list(map(int, input().split()))

node2rank = [0] * 2001
for index in range(k):
    node2rank[path[index]] = index + 1

par_start = [0] * 2001
par_end = [0] * 2001

dist_start = [INF] * (n + 1)
dist_end = [INF] * (n + 1)

set_dist_dijkstra(start, adjacency_list, dist_start)
set_dist_dijkstra(end, adjacency_list, dist_end)

set_parent(par_start, dist_start, (path[0], -1, path[0]))
set_parent(par_end, dist_end, (path[-1], -1, path[-1]))

segtree = SegmentTreeLazyPropagation([INF]*len(path))

for i in range(1, n + 1):
    for j, cost in adjacency_list[i]:
        if node2rank[i] and node2rank[j] and abs(node2rank[i] - node2rank[j]) == 1:
            continue
        edge_start = node2rank[par_start[i]]
        edge_end = node2rank[par_end[j]] - 1
        segtree.update(edge_start, edge_end, dist_start[i] + cost + dist_end[j])

ans = []
for i in range(1, k):
    result = segtree.query(i, i)
    ans.append(result if result != INF else -1)

print(*ans, sep="\n")
