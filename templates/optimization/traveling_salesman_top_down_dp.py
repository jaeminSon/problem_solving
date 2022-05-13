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
    
if __name__=="__main__":
    print(traveling_salesman([[0,1,2],[3,0,4],[5,1,0]]))