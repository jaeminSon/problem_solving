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