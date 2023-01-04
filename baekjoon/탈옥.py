import sys

L, G = [int(d) for d in sys.stdin.readline().rstrip().split()]

c = [int(d) for d in sys.stdin.readline().rstrip().split()]

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

cost = [[0]*(len(c)+1) for _ in range(len(c)+1)]

s=[0]
for v in c:
    s.append(s[-1]+v)

for i in range(1,len(c)+1):
    for j in range(i,len(c)+1):
        cost[i][j] = (s[j]-s[i-1])*(j-i+1)

ans = divide_and_conquer(G, cost)
print(ans)
