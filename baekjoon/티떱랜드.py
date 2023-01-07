import sys

def divide_and_conquer(M, cost):
    
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

N,K  = [int(d) for d in sys.stdin.readline().rstrip().split()]

l = [[int(d) for d in sys.stdin.readline().rstrip().split()] for _ in range(N)]

s = [[0]*N for _ in range(N)]
s[0][0] = l[0][0]
for j in range(1, N):
    s[0][j] = s[0][j-1]+l[0][j]
for i in range(1,N):
    s[i][0] = s[i-1][0]+l[i][0]
    for j in range(1,N):
        s[i][j] = s[i][j-1] + s[i-1][j] + l[i][j] - s[i-1][j-1]

cost = [[0]*(N+1) for _ in range(N+1)]

for j in range(1,N+1):
    cost[1][j] = cost[j][1] = s[j-1][j-1]//2
for i in range(2,N+1):
    for j in range(2,N+1):
        cost[i][j] = (s[j-1][j-1]+s[i-2][i-2])//2 - s[j-1][i-2]

ans = divide_and_conquer(K, cost)
print(ans)