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

if __name__ == "__main__":
    X = "AGGTAB"
    Y = "GXTXAYB"
    print(longest_common_subsequence(X, Y))
    
    print(traveling_salesman([[0,1,2],[3,0,4],[5,1,0]]))