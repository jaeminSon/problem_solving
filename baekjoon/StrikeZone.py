from sys import stdin
input = stdin.readline
from collections import defaultdict


class Node:
    def __init__(self, s, l, r, b):  # sum, left-sum, right-sum, best
        self.s = s
        self.l = l
        self.r = r
        self.b = b


class BestPrefixSumSegmentTree:

    def __init__(self, bias):
        # bias should be power of 2 and greater than max number of elements
        self.bias = bias
        self.n_trees = 2*bias
        self.tree = [Node(0, 0, 0, 0)
                     for _ in range(self.n_trees)]  # 0th tree empty

    def clear(self):
        for i in range(self.n_trees):
            self.replace(i, 0)

    def merge(self, a, b):
        # t <- a + b
        s = a.s + b.s
        return Node(s, max(a.l, a.s + b.l), max(b.r, a.r + b.s), max(a.r + b.l, a.b, b.b, s))

    def increment(self, i, v):
        self.tree[i].s += v
        self.tree[i].l += v
        self.tree[i].r += v
        self.tree[i].b += v

    def replace(self, i, v):
        self.tree[i].s = v
        self.tree[i].l = v
        self.tree[i].r = v
        self.tree[i].b = v

    def update(self, i, v):
        i += self.bias
        self.increment(i, v)
        # self.replace(x, v)
        while i > 1:
            if i % 2 == 0:  # left child
                self.tree[i//2] = self.merge(self.tree[i], self.tree[i+1])
            else:  # right child
                self.tree[i//2] = self.merge(self.tree[i-1], self.tree[i])
            i //= 2

    def query(self, l, r):
        # [l, r]
        l += self.bias
        r += self.bias
        ret = Node(0, 0, 0, 0)
        while l <= r:
            if l % 2 == 1:
                ret = self.merge(self.tree[l], ret)
                l += 1
            if r % 2 == 1:
                ret = self.merge(ret, self.tree[r])
                r -= 1
            l //= 2
            r //= 2
        return ret

n1 = int(input())
P1 = [list(map(int, input().split())) for _ in range(n1)]

n2 = int(input())
P2 = [list(map(int, input().split())) for _ in range(n2)]

c1, c2 = list(map(int, input().split()))

P = P1 + P2

mapping = [[] for _ in range(2)]
for dim in range(2):
    unique_sorted = sorted(list(set([el[dim] for el in P])))
    mapping[dim] = {v: i+1 for i, v in enumerate(unique_sorted)}

unique_y_sorted = sorted(set([mapping[0][el[0]] for el in P]))
line = defaultdict(list)
for el in P1:
    line[mapping[0][el[0]]].append((mapping[1][el[1]], c1))
for el in P2:
    line[mapping[0][el[0]]].append((mapping[1][el[1]], -c2))

segtree = BestPrefixSumSegmentTree(2048)
ans = 0
for i in range(len(unique_y_sorted)):
    segtree.clear()
    for j in range(i, len(unique_y_sorted)):
        for x, w in line[unique_y_sorted[j]]:
            segtree.update(x, w)
        ans = max(ans, segtree.tree[1].b)

print(ans)
