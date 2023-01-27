def longest_common_subsequence(X, Y):
  
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


def traveling_salesman(distance_matrix):
    
    # initialize table
    n = len(distance_matrix)
    dp = [[None] * (2**n)  for _ in range(n)]
    for i in range(n):
        dp[i][(1 << n) - 1] = distance_matrix[i][0]
    
    # define recursive call
    def _recursive_call(curr, bitmask):
        if dp[curr][bitmask] is None:
            dp[curr][bitmask] = min([distance_matrix[curr][next] + _recursive_call(next, bitmask | (1 << next)) for next in range(n) if bitmask & (1 << next) == 0])
        return dp[curr][bitmask]
    
    return _recursive_call(0, 0)


def bitonic_traveling_salesman(distance_matrix):
    
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
    _recursive_call(0,0)
    
    return dp[0][0]


def convex_hull_trick(A, B, C, D):
    # dp[i] = min(0 ≤ j < i){A[i]B[j] + dp[j]+ C[j]} + D[i] 
    # constraint: B should be monotonically decreasing => O(nlogn)
    #             (additionally) if A is monotonically increasing => O(n)
    # line segment formula: f(x) = B[j] * x + dp[j]+ C[j] (A[i] ~ x)
 
    from bisect import bisect
    
    assert len(A) == len(B)
    if C:
        assert len(A) == len(C)
    if D:
        assert len(A) == len(D)
    
    def intersection_x(lseg1, lseg2):
        # y=ax+b, (x>=s)
        a1,b1,_ = lseg1
        a2,b2,_ = lseg2
        return 1.*(b2-b1)/(a1-a2)
 
    n = len(A)
    dp = [0] * n
    stack = [] # (a,b,s) where y=ax+b, x>=s
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
        #     if stack[mid][2] < A[i]:
        #         lo = mid + 1
        #     else:
        #         hi = mid
        # dp[i] = stack[lo-1][0] * A[i] + stack[lo-1][1]
        
        # A is monotonically increasing
        while pos+1 < len(stack) and stack[pos+1][2] < A[j]:
            pos+=1
        dp[j] = stack[pos][0] * A[j] + stack[pos][1]
 
        if D:
            dp[j] += D[j]
 
    return dp[n-1]

def divide_and_conquer(M, cost):
    # dp[i][j] = min (k < j){dp[i-1][k] + cost[k][j]} 
    # constraint: argmin[i][j] <= argmin[i][j+1] or cost(a, c) + cost(b, d) <= cost(a, d) + cost(b, c) for all a <= b <= c <= d
    # suppose cost is augmented (i.e. cost[0][l]=0, cost[0][t]=0)
    
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

def knuth_speedup(cost):
    # dp[i][j] = min(i < k < j){dp[i][k] + dp[k][j]} + C[i][j]}  
    # constraint: argmin[i][j-1] <= argmin[i][j] <= argmin[i+1][j]
    
    n = len(cost)
    dp = [[0]*n for _ in range(n)]
    opt_k = [[0]*n for _ in range(n)]
    
    # default assignment (no k exists between i and i+d)
    for i in range(n-1):
        opt_k[i][i+1] = i+1 # first k such that i < k
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
    
    assert traveling_salesman([[0,1,2],[3,0,4],[5,1,0]]) == 6
    
    def points2distance_matrix(list_points):
        n_points = len(list_points)
        distance_matrix = [[None]*n_points for _ in range(n_points)]
        from itertools import combinations
        for i,j in combinations(range(n_points), 2):
            p1 = list_points[i]
            p2 = list_points[j]
            distance_matrix[i][j] = ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**(1./2)
            distance_matrix[j][i] = ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**(1./2)
        for i in range(n_points):
            distance_matrix[i][i] = 0
        
        return distance_matrix
 
    assert abs(bitonic_traveling_salesman(points2distance_matrix([(1,1),(2,3),(3,1)])) - 6.47213595499958) < 1e-6

    assert convex_hull_trick(A=[1,2,3,4,5],B=[5,4,3,2,0], C=None, D=None) == 25
    assert convex_hull_trick(A=[1,2,3,10,20,30],B=[6,5,4,3,2,0], C=None, D=None) == 138

    import numpy as np
    weight = np.ones((8,8), dtype=int) - np.eye(8, dtype=int)
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

    assert knuth_speedup([[1,2,3,4],[3,4,5,1],[1,1,1,3], [2,2,2,2]]) == 15
