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
    # constraint: 1. B is monotonically decreasing => O(nlogn)
    #             2. A is monotonically increasing => O(n)
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
    for i in range(1, n):
        line_seg = [B[i-1], dp[i-1] + C[i-1] if C else dp[i-1], 0]
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
        while pos+1 < len(stack) and stack[pos+1][2] < A[i]:
            pos+=1
        dp[i] = stack[pos][0] * A[i] + stack[pos][1]
 
    return dp[n-1]


if __name__ == "__main__":
    X = "AGGTAB"
    Y = "GXTXAYB"
    print(longest_common_subsequence(X, Y))
    
    print(traveling_salesman([[0,1,2],[3,0,4],[5,1,0]]))
    
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
 
    print(bitonic_traveling_salesman(points2distance_matrix([(1,1),(2,3),(3,1)])))

    print(convex_hull_trick(A=[1,2,3,4,5],B=[5,4,3,2,0], C=None, D=None))
    print(convex_hull_trick(A=[1,2,3,10,20,30],B=[6,5,4,3,2,0], C=None, D=None))