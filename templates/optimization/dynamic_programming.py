import sys
sys.path.append("..")
from custom_type import LIST1D, LIST2D, REAL, NAT


def longest_common_subsequence(X: LIST1D, Y: LIST1D) -> int:
    """
    Returns the length of the longest common subsequence.
    """
    # initialize dp table
    dp = [[0]*(len(X)+1) for _ in range(len(Y)+1)]

    # fill-in rule
    for i in range(1, len(Y)+1):
        for j in range(1, len(X)+1):
            if X[j-1] == Y[i-1]:
                dp[i][j] = dp[i-1][j-1]+1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # desired value
    ans = dp[-1][-1]

    return ans


def traveling_salesman(distance_matrix: LIST2D) -> REAL:
    """
    Traveling salesman with bitmask.
    """
    # initialize table
    n = len(distance_matrix)
    dp = [[None] * (2**n) for _ in range(n)]
    for i in range(n):
        dp[i][(1 << n) - 1] = distance_matrix[i][0]

    # define recursive call
    def _recursive_call(curr, bitmask):
        if dp[curr][bitmask] is None:
            dp[curr][bitmask] = min([distance_matrix[curr][next] + _recursive_call(next, bitmask | (1 << next))
                                    for next in range(n) if bitmask & (1 << next) == 0])
        return dp[curr][bitmask]

    return _recursive_call(0, 0)


def bitonic_traveling_salesman(distance_matrix: LIST2D) -> REAL:
    """
    Find the minimum distance of a tour that starts from the leftmost vertex, 
    and strictly goes to the right, and then upon reaching the rightmost vertex, 
    the tour goes strictly from right to left-back to the starting vertex. 
    
    dp[i][j] represents minimum cost from ith node to jth node (visiting the rightmost vertex).
    dp[i][j] is updated using dp[i+1][j] and dp[i][j+1].
    """
    def _recursive_call(start_LR, end_RL):
        if dp[start_LR][end_RL] is None:
            curr_node = 1 + max(start_LR, end_RL)
            if curr_node == n_nodes-1:
                dp[start_LR][end_RL] = distance_matrix[start_LR][curr_node] + distance_matrix[curr_node][end_RL]
            else:
                dp[start_LR][end_RL] = min(distance_matrix[start_LR][curr_node] + _recursive_call(curr_node, end_RL),
                                           distance_matrix[curr_node][end_RL] + _recursive_call(start_LR, curr_node))

        return dp[start_LR][end_RL]

    n_nodes = len(distance_matrix)
    dp = [[None]*n_nodes for _ in range(n_nodes)]
    _recursive_call(0, 0)

    return dp[0][0]


def convex_hull_trick(A: LIST1D, B: LIST1D, C: LIST1D, D: LIST1D) -> REAL:
    """
    dp[i] = min(0 ≤ j < i){A[i]B[j] + dp[j]+ C[j]} + D[i]
    assert dp[0] == 0 (null state)
    constraint: B is monotonically decreasing => O(nlogn) with binary search
                B is monotonically decreasing and A is non-decreasing => O(n)
    line segment formula: f(x) = B[j] * x + dp[j]+ C[j] (A[i] ~ x)
    """
    assert len(A) == len(B)
    if C:
        assert len(A) == len(C)
    if D:
        assert len(A) == len(D)

    def intersection_x(lseg1, lseg2):
        # y=ax+b, (x>=s)
        a1, b1, _ = lseg1
        a2, b2, _ = lseg2
        return 1.*(b2-b1)/(a1-a2)

    n = len(A)
    dp = [0] * n
    stack = []  # (a,b,s) where y=ax+b, x>=s
    pos = 0
    for j in range(1, n):
        intercept = dp[j-1] + C[j-1] if C else dp[j-1]
        line_seg = [B[j-1], intercept, 0]
        while stack:
            line_seg[2] = intersection_x(stack[-1], line_seg)
            if stack[-1][2] < line_seg[2]:
                break
            else:
                stack.pop()
        stack.append(line_seg)

        # # A is not monotonically increasing (binary search)
        # lo, hi = 0, len(stack)
        # while lo < hi:
        #     mid = (lo + hi) // 2
        #     if stack[mid][2] < A[j]:
        #         lo = mid + 1
        #     else:
        #         hi = mid
        # dp[j] = stack[lo-1][0] * A[j] + stack[lo-1][1]

        # A is monotonically increasing
        while pos+1 < len(stack) and stack[pos+1][2] < A[j]:
            pos += 1
        dp[j] = stack[pos][0] * A[j] + stack[pos][1]

        if D:
            dp[j] += D[j]

    return dp[n-1]


def convex_hull_trick_lichao_tree(A, B, C, D):
    """
    dp[i] = min(0 ≤ j < i){A[i]B[j] + dp[j]+ C[j]} + D[i]
    assert dp[0] == 0 (null state)
    Time complexity of O(nlogn) with lichao tree.
    """
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


def divide_and_conquer(M: NAT, cost: LIST2D) -> REAL:
    """
    dp[i][j] = min (k < j){dp[i-1][k] + cost[k][j]}
    Constraint: argmin[i][j] <= argmin[i][j+1],
                or equivalently, cost(a, c) + cost(b, d) <= cost(a, d) + cost(b, c) for all a <= b <= c <= d
    Suppose cost is augmented (i.e. cost[0][l]=0, cost[0][t]=0)
    Time complexity: 0<=i<=m, 0<=j<=n => O(mn*logn)
    """
    def _recursive(i, m, n, l, r):
        # compute dp[i][m], ...,dp[i][n] with opt_k in [l,r]
        if m > n:
            return
        else:
            # set value for mid position
            mid = (m+n)//2
            opt_k = l
            # recurrence: dp[i][j] = min (k < j){dp[i-1][k] + cost[k+1][j]}
            for k in range(l, min(r+1, N-1)):
                if dp[i-1][k] + cost[k+1][mid] < dp[i][mid]:
                    dp[i][mid] = dp[i-1][k] + cost[k+1][mid]
                    opt_k = k

            _recursive(i, m, mid-1, l, opt_k)
            _recursive(i, mid+1, n, opt_k, r)

    N = len(cost)
    dp = [[float("inf")]*N for _ in range(M+1)]
    for i in range(1, N):
        dp[1][i] = cost[1][i]

    for i in range(2, M+1):
        _recursive(i, 1, N-1, 1, N-1)

    return dp[M][N-1]


def knuth_speedup(cost: LIST2D) -> REAL:
    """
    Knuth-Yao dynamic programming speedup,
    also known as the Knuth-Yao optimization, is a technique that accelerates
    the computation of certain dynamic programming algorithms.
    It was introduced by Donald Knuth and Andrew Yao in their paper
    "Efficient Binary-Search Trees" in 1976.

    This implements the following recurrence relation,

    dp[i][j] = min(i < k < j){dp[i][k] + dp[k][j] + cost[i][j]},

    where opt[i][j-1] <= opt[i][j] <= opt[i+1][j] with opt[i][j] representing
    the value of 'k' that minimizes the given expression.

    Equivalently, the cost function satisfies either of the following conditions.

    1) cost[b][c] <= cost[a][d]
    2) cost[a][c]+cost[b][d] <= cost[a][d]+cost[b][c]

    Reference: https://cp-algorithms.com/dynamic_programming/knuth-optimization.html

    - time complexity: O(n^2)
    - space complexity: O(n^2)
    """

    n = len(cost)
    dp = [[0]*n for _ in range(n)]
    opt_k = [[0]*n for _ in range(n)]

    # default assignment (no k exists between i and i+d)
    for i in range(n-1):
        opt_k[i][i+1] = i+1  # first k such that i < k
        dp[i][i+1] = cost[i][i+1]

    # fill in dp matrix diagonally
    for d in range(2, n):
        for i in range(n-d):
            j = i+d
            dp[i][j] = float("inf")
            for k in range(opt_k[i][j-1], opt_k[i+1][j]+1):
                val = dp[i][k] + dp[k][j] + cost[i][j]
                if val < dp[i][j]:
                    dp[i][j] = val
                    opt_k[i][j] = k

    return dp[0][n-1]


if __name__ == "__main__":
    X = "AGGTAB"
    Y = "GXTXAYB"
    assert longest_common_subsequence(X, Y) == 4

    assert traveling_salesman([[0, 1, 2], [3, 0, 4], [5, 1, 0]]) == 6

    def points2distance_matrix(list_points):
        n_points = len(list_points)
        distance_matrix = [[None]*n_points for _ in range(n_points)]
        from itertools import combinations
        for i, j in combinations(range(n_points), 2):
            p1 = list_points[i]
            p2 = list_points[j]
            distance_matrix[i][j] = ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**(1./2)
            distance_matrix[j][i] = ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**(1./2)
        for i in range(n_points):
            distance_matrix[i][i] = 0

        return distance_matrix

    assert abs(bitonic_traveling_salesman(points2distance_matrix([(1, 1), (2, 3), (3, 1)])) - 6.47213595499958) < 1e-6

    assert convex_hull_trick(A=[1, 2, 3, 4, 5], B=[5, 4, 3, 2, 0], C=None, D=None) == 25
    assert convex_hull_trick(A=[1, 2, 3, 10, 20, 30], B=[6, 5, 4, 3, 2, 0], C=None, D=None) == 138

    import numpy as np
    weight = np.ones((8, 8), dtype=int) - np.eye(8, dtype=int)
    n = len(weight)
    S = [[0]*(n+1) for _ in range(n+1)]
    subS = [[0]*(n+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, n+1):
            S[i][j] = weight[i-1][j-1] + S[i - 1][j] + S[i][j - 1] - S[i - 1][j - 1]
    for i in range(1, n+1):
        for j in range(i, n+1):
            subS[i][j] = S[i-1][i-1] - S[i-1][j] - S[j][i-1] + S[j][j]
    assert divide_and_conquer(3, subS) == 14

    assert knuth_speedup([[1, 2, 3, 4], [3, 4, 5, 1], [1, 1, 1, 3], [2, 2, 2, 2]]) == 15
