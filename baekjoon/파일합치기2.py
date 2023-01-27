import sys

dp = [[0]*5100 for _ in range(5100)]
opt_k = [[0]*5100 for _ in range(5100)]

T = int(sys.stdin.readline().rstrip())

for _ in range(T):
    n = int(sys.stdin.readline())
    l = [int(d) for d in sys.stdin.readline().rstrip().split()]

    s = [0]
    for i in range(n):
        s.append(s[-1]+l[i])
    
    n = len(s)  
    for i in range(n-1):
        opt_k[i][i+1] = i+1
        dp[i][i+1] = 0

    for d in range(2,n):
        for i in range(n-d):
            j = i+d
            dp[i][j] = 1000000007
            for k in range(opt_k[i][j-1], opt_k[i+1][j]+1):
                val = dp[i][k] + dp[k][j] + s[j] - s[i]
                if val < dp[i][j]:
                    dp[i][j] = val
                    opt_k[i][j] = k
    
    print(dp[0][n-1])
