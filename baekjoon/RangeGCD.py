N = int(input())
sequence = list(map(int, input().split()))
Q = int(input())

operations = []
for _ in range(Q):
    T, A, B = map(int, input().split())
    operations.append((T, A, B))


def gcd(a, b):
    large, small = (a, b) if a >= b else (b, a)
    return large if small == 0 else gcd(small, large % small)


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


class SegmentTree:
    def __init__(self, arr):
        N = len(arr)  # N should be power of 2
        self.tree = [0] * 2 * N
        self.len = N
        # arr = [1, 2, 3, 4]
        # tree = [0, 1+2+3+4, 1+2, 3+4, 1, 2, 3, 4]
        for i in range(N):
            self.tree[N+i] = arr[i]
        for i in range(N - 1, 0, -1):
            self.tree[i] = gcd(self.tree[2*i], self.tree[2*i+1])

    def query(self, l, r):
        # [l, r)
        N = self.len
        res = 0

        l += N
        r += N
        while l < r:  # stop if l==r
            # l is right child (include only l, not parent, move to parent of next node)
            if l % 2 == 1:
                res = gcd(res, self.tree[l])
                l += 1
            if r % 2 == 1:  # r is right child (include r-1, move to parent)
                r -= 1
                res = gcd(res, self.tree[r])
            l //= 2
            r //= 2
        return res

    def updateTreeNode(self, p, value):
        N = self.len
        i = p + N

        self.tree[i] = value
        while i > 1:
            if i % 2 == 0:  # left child
                self.tree[i//2] = gcd(self.tree[i], self.tree[i+1])
            else:  # right child
                self.tree[i//2] = gcd(self.tree[i-1], self.tree[i])
            i //= 2


L = len(sequence)
add_tree = SegmentTreeLazyPropagation(sequence)
gcd_tree = SegmentTree([sequence[0]] + [abs(sequence[i]-sequence[i-1]) for i in range(1, L)])

for T, A, B in operations:
    if T == 0:
        print(gcd(add_tree.query(A-1, A-1), gcd_tree.query(A, B)))
    else:
        add_tree.update(A-1, B-1, T)
        
        new = abs(add_tree.query(A-1, A-1) - add_tree.query(A-2, A-2))
        gcd_tree.updateTreeNode(A-1, new)
        if B < L:
            new = abs(add_tree.query(B, B) - add_tree.query(B-1, B-1))
            gcd_tree.updateTreeNode(B, new)
