import sys

N = int(sys.stdin.readline().rstrip())

list_duration = [[0]*2 for _ in range(N)]
list_switch = [[0]*2 for _ in range(N)]

for i in range(N):
    info = [int(el) for el in sys.stdin.readline().split()]
    for k in range(2):
        list_duration[i][k] = info[k]
    if i!=N-1:
        for k in range(2):
            list_switch[i][k] = info[k+2]

dp = [[0]*2 for _ in range(N)]
for k in range(2):
    dp[0][k] = list_duration[0][k]
for i in range(1, N):
    for k in range(2):
        dp[i][k] = min(dp[i-1][k], dp[i-1][1-k]+list_switch[i-1][1-k]) + list_duration[i][k]
        
print(min(dp[N-1]))

