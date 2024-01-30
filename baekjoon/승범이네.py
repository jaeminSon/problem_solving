from sys import stdin
input = stdin.readline

import sys
sys.setrecursionlimit(100_000)

class SegmentTreeLazyPropagation:
    # summation query
    def __init__(self, arr):
        N = len(arr)
        self.tree = [0] * 2 * self.just_bigger_power_2(N)
        self.lazy = [0] * 2 * self.just_bigger_power_2(N)
        self.len = N
        self.initialize(arr, 0, N-1, 0)

    def just_bigger_power_2(self, val):
        i = 0
        while 2**i < val:
            i += 1
        return 2**i

    def initialize(self, arr, s, e, index):
        # arr = [1, 2, 3, 4, 5]
        # tree = [15, 6, 9, 3, 3, 4, 5, 1, 2, 0]
        if s <= e:
            if s == e:  # leaf node
                self.tree[index] = arr[s]
            else:
                mid = (s + e) // 2
                self.initialize(arr, s, mid, index * 2 + 1)
                self.initialize(arr, mid + 1, e, index * 2 + 2)
                self.tree[index] = self.tree[index * 2 + 1] + \
                    self.tree[index * 2 + 2]

    def update(self, s, e, diff):
        self.update_util(0, 0, self.len - 1, s, e, diff)

    def propagate(self, node_index, node_s, node_e):
        if self.lazy[node_index] != 0:  # reflect lazy updates
            self.tree[node_index] += (node_e - node_s + 1) * \
                self.lazy[node_index]
            if node_s != node_e:  # intermediate node
                self.lazy[node_index * 2 + 1] += self.lazy[node_index]
                self.lazy[node_index * 2 + 2] += self.lazy[node_index]
            self.lazy[node_index] = 0

    def update_util(self, node_index, node_s, node_e, s, e, diff):
        self.propagate(node_index, node_s, node_e)

        if node_s <= node_e and node_s <= e and node_e >= s:
            if node_s >= s and node_e <= e:  # [node_s, node_e] in [s,e]
                self.tree[node_index] += (node_e - node_s + 1) * diff
                if node_s != node_e:  # intermediate node
                    self.lazy[node_index * 2 + 1] += diff
                    self.lazy[node_index * 2 + 2] += diff
            else:  # [node_s, node_e] and [s,e] overlapping but not inclusive
                mid = (node_s + node_e) // 2
                self.update_util(node_index * 2 + 1, node_s, mid, s, e, diff)
                self.update_util(node_index * 2 + 2, mid +
                                 1, node_e, s, e, diff)
                self.tree[node_index] = self.tree[node_index *
                                                  2 + 1] + self.tree[node_index * 2 + 2]

    def query_util(self, node_index, node_s, node_e, s, e):
        self.propagate(node_index, node_s, node_e)

        if node_s <= node_e and node_s <= e and node_e >= s:
            if node_s >= s and node_e <= e:  # [node_s, node_e] in [s,e]
                return self.tree[node_index]
            else:  # [node_s, node_e] and [s,e] overlapping but not inclusive
                mid = (node_s + node_e) // 2
                return self.query_util(2 * node_index + 1, node_s, mid, s, e) + self.query_util(2 * node_index + 2, mid + 1, node_e, s, e)
        else:
            return 0  # null value for summation query

    def query(self, s, e):
        # [s,e]
        return self.query_util(0, 0, self.len-1, s, e)


def eulerian_technique(adjacency_list):
    # assume adjacency_list starts with index 0

    def _dfs(node, parent):
        count[0] += 1
        start[node] = count[0]
        for ne in adjacency_list[node]:
            if ne != parent:
                _dfs(ne, node)

        end[node] = count[0]

    n = len(adjacency_list)
    count = [-1]
    start = [-1] * n
    end = [-1] * n

    _dfs(0, -1)

    return start, end


N, M = map(int, input().split())

adj = [[] for _ in range(N)]
for i, el in enumerate(map(int, input().split())):
    if i > 0:
        adj[el-1].append(i)

start, end = eulerian_technique(adj)

segtree_lazy = SegmentTreeLazyPropagation([0]*N)

queries = [list(map(int, input().split())) for _ in range(M)]

for query in queries:
    node_index = query[1] - 1
    if query[0] == 1:
        segtree_lazy.update(start[node_index], end[node_index], query[2])
    elif query[0] == 2:
        print(segtree_lazy.query(start[node_index], start[node_index]))
