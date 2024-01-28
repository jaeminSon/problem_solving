from sys import stdin
input = stdin.readline


def convex_hull_trick(A, B, C, D):

    assert len(A) == len(B)
    if C:
        assert len(A) == len(C)
    if D:
        assert len(A) == len(D)

    class Line(object):
        def __init__(self, slope, intercept):
            self.slope = slope
            self.intercept = intercept

        def eval(self, x):
            return self.slope * x + self.intercept

    class Node(object):
        def __init__(self, line, s, e, L=None, R=None):
            self.line = line
            self.s = int(s)
            self.e = int(e)
            self.L = L
            self.R = R

    class LiChaoTree(object):

        def __init__(self, s, e):
            self.tree = [Node(Line(0, -float("inf")), s, e, None, None)]

        def insert(self, new_line: Line, index_node=0):

            s = self.tree[index_node].s
            e = self.tree[index_node].e

            if self.tree[index_node].line.eval(s) > new_line.eval(s):
                high = self.tree[index_node].line
                low = new_line
            else:
                low = self.tree[index_node].line
                high = new_line

            if low.eval(e) <= high.eval(e):
                self.tree[index_node].line = high
            else:
                m = s + e >> 1
                if low.eval(m) < high.eval(m):
                    self.tree[index_node].line = high
                    if self.tree[index_node].R is None:
                        self.tree[index_node].R = len(self.tree)
                        self.tree.append(
                            Node(Line(0, -float("inf")), m, e, None, None))
                    self.insert(low, self.tree[index_node].R)
                else:
                    self.tree[index_node].line = low
                    if self.tree[index_node].L is None:
                        self.tree[index_node].L = len(self.tree)
                        self.tree.append(
                            Node(Line(0, -float("inf")), s, m, None, None))
                    self.insert(high, self.tree[index_node].L)

        def query(self, x, index_node=0):
            if index_node is None:
                return -float("inf")
            else:
                s = self.tree[index_node].s
                e = self.tree[index_node].e
                m = s + e >> 1
                if x <= m:
                    return max(self.tree[index_node].line.eval(x), self.query(x, self.tree[index_node].L))
                else:
                    return max(self.tree[index_node].line.eval(x), self.query(x, self.tree[index_node].R))

    lichao = LiChaoTree(0, 1e9)

    n = len(A)
    dp = [0] * n
    for j in range(1, n):
        intercept = dp[j-1] + C[j-1]
        lichao.insert(Line(-B[j-1], -intercept))
        dp[j] = -lichao.query(A[j])

    return dp[n-1]


n = int(input())
d = [0] + list(map(int, input().split()))
list_p, list_s = [], []
for _ in range(n-1):
    p, s = map(int, input().split())
    list_p.append(p)
    list_s.append(s)
for i in range(1, len(d)):
    d[i] += d[i-1]

A = d
B = list_s + [0]
C = [-d[i]*list_s[i]+list_p[i] for i in range(len(list_s))] + [0]

ans = convex_hull_trick(A, B, C, D=None)
print(ans)
