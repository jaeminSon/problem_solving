import sys

N = int(sys.stdin.readline().rstrip())
l = [int(d)-1 for d in sys.stdin.readline().rstrip().split()]

dp = [[0]*N for _ in range(N)]

for v in range(N):
    for j in range(N-2, 0, -1):
        offset = 1 if l[j+1] < v else 0
        dp[v][j] = dp[v][j+1] + offset

ans = 0
for i in range(N):
    for j in range(i+1,N-1):
        if l[i] < l[j]:
            ans += dp[l[i]][j]

print(ans)