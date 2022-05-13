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

if __name__ == "__main__":
    X = "AGGTAB"
    Y = "GXTXAYB"
    print(longest_common_subsequence(X, Y))