import sys
from collections import defaultdict
from sys import stdin
input = stdin.readline

sys.setrecursionlimit(200_009)

INF_DEG = 1_000_005

class SegmentTreeLazyPropagation:
    # summation query
    def __init__(self, arr):
        N = len(arr)
        self.tree = [[INF_DEG, 0]] * 2 * self.just_bigger_power_2(N)
        self.lazy = [0] * 2 * self.just_bigger_power_2(N)
        self.len = N
        self.initialize(arr, 0, N-1, 0)

    def just_bigger_power_2(self, val):
        i = 0
        while 2**i < val:
            i += 1
        return 2**i

    def merge(self, left, right):
        left_deg, left_count = left
        right_deg, right_count = right

        if left_deg < right_deg:
            return [left_deg, left_count]
        elif left_deg > right_deg:
            return [right_deg, right_count]
        else:
            return [left_deg, left_count + right_count]

    def initialize(self, arr, s, e, index):
        if s <= e:
            if s == e:  # leaf node
                self.tree[index] = [arr[s], 1]
            else:
                mid = (s + e) // 2
                self.initialize(arr, s, mid, index * 2 + 1)
                self.initialize(arr, mid + 1, e, index * 2 + 2)
                self.tree[index] = self.merge(self.tree[index * 2 + 1], self.tree[index * 2 + 2])

    def update(self, s, e, diff):
        self.update_util(0, 0, self.len - 1, s, e, diff)

    def propagate(self, node_index, node_s, node_e):
        if self.lazy[node_index] != 0:  # reflect lazy updates
            self.tree[node_index][0] += self.lazy[node_index]
            assert 0 <= self.tree[node_index][0] < N
            if node_s != node_e:  # intermediate node
                self.lazy[node_index * 2 + 1] += self.lazy[node_index]
                self.lazy[node_index * 2 + 2] += self.lazy[node_index]
            self.lazy[node_index] = 0

    def update_util(self, node_index, node_s, node_e, s, e, diff):
        self.propagate(node_index, node_s, node_e)

        if node_s <= node_e and node_s <= e and node_e >= s:
            if node_s >= s and node_e <= e:  # [node_s, node_e] in [s,e]
                self.lazy[node_index] += diff
                self.propagate(node_index, node_s, node_e)
            else:  # [node_s, node_e] and [s,e] overlapping but not inclusive
                mid = (node_s + node_e) // 2
                self.update_util(node_index * 2 + 1, node_s, mid, s, e, diff)
                self.update_util(node_index * 2 + 2, mid +
                                 1, node_e, s, e, diff)
                self.tree[node_index] = self.merge(self.tree[node_index *
                                                  2 + 1], self.tree[node_index * 2 + 2])

    def query_util(self, node_index, node_s, node_e, s, e):
        self.propagate(node_index, node_s, node_e)

        if node_s <= node_e and node_s <= e and node_e >= s:
            if node_s >= s and node_e <= e:  # [node_s, node_e] in [s,e]
                return self.tree[node_index]
            else:  # [node_s, node_e] and [s,e] overlapping but not inclusive
                mid = (node_s + node_e) // 2
                return self.merge(self.query_util(2 * node_index + 1, node_s, mid, s, e), self.query_util(2 * node_index + 2, mid + 1, node_e, s, e))
        else:
            return [INF_DEG, 0]

    def query(self, s, e):
        # [s,e]
        return self.query_util(0, 0, self.len-1, s, e)



def eulerian_technique(node):
    count = 0
    n_reverse = 0
    stack = [node]
    while stack:
        now = stack[-1]
        if start[now] == 0:
            count += 1
            start[now] = count
        check = False
        for nxt, d in adj[now]:
            if start[nxt] == 0:
                if d == -1:
                    n_reverse += 1
                
                stack.append(nxt)
                check = True
                break
        if check == False:
            end[now] = count
            stack.pop()
    
    return n_reverse


def get_degree(adjacency_list, start, n_reverse):

    def _dfs(node, parent, deg_node):
        degree[start[node]] = n_reverse + deg_node
        for ne, d in adjacency_list[node]:
            if ne != parent:
                _dfs(ne, node, deg_node + d)

    n = len(adjacency_list)
    degree = [None] * n

    _dfs(0, -1, 0)

    return degree


N = int(input())
adj = [[] for _ in range(N)]
direction = defaultdict(dict)
for _ in range(N-1):
    l = input().split()
    u = int(l[0])-1
    v = int(l[2])-1
    if l[1] == "--":
        d = 0
    elif l[1] == "->":
        d = 1
    elif l[1] == "<-":
        d = -1
    adj[u].append((v, d))
    adj[v].append((u, -d))
    direction[u][v] = d
    direction[v][u] = -d

Q = int(input())
queries = []
for _ in range(Q):
    l = input().split()
    u = int(l[0])-1
    v = int(l[2])-1
    if l[1] == "--":
        d = 0
    elif l[1] == "->":
        d = 1
    elif l[1] == "<-":
        d = -1
    queries.append((u, v, d))

start = [0] * N
end = [0] * N
n_reverse = eulerian_technique(0)
start = [s-1 for s in start]
end = [e-1 for e in end]

degree = get_degree(adj, start, n_reverse)

segtree_lazy = SegmentTreeLazyPropagation(degree)

for u, v, d in queries:
    if start[u] > start[v]:
        u, v = v, u
        d *= -1
    
    if direction[u][v] == -1:  # u <- v
        if d == 0:  # u -- v
            segtree_lazy.update(0, start[v]-1, -1)
            segtree_lazy.update(end[v]+1, N-1, -1)
        elif d == 1:  # u -> v
            segtree_lazy.update(0, start[v]-1, -1)
            segtree_lazy.update(end[v]+1, N-1, -1)
            segtree_lazy.update(start[v], end[v], 1)
    elif direction[u][v] == 1:  # u -> v
        if d == -1:  # u <- v
            segtree_lazy.update(0, start[v]-1, 1)
            segtree_lazy.update(end[v]+1, N-1, 1)
            segtree_lazy.update(start[v], end[v], -1)
        elif d == 0:  # u -- v
            segtree_lazy.update(start[v], end[v], -1)
    else:  # u -- v
        if d == -1:  # u <- v
            segtree_lazy.update(0, start[v]-1, 1)
            segtree_lazy.update(end[v]+1, N-1, 1)
        elif d == 1:  # u -> v
            segtree_lazy.update(start[v], end[v], 1)

    deg, count = segtree_lazy.query(0, N-1)
    ans = 0 if deg > 0 else count
    print(ans)

    direction[u][v] = d
