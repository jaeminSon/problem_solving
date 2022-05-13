import sys

K, N = [int(el) for el in sys.stdin.readline().split()]

list_duration = [[0 for _ in range(K)] for _ in range(N)]
list_travel_time = [0 for _ in range(N-1)]

for i in range(N):
    list_info = [int(el) for el in sys.stdin.readline().split()]
    for j in range(K):
        list_duration[i][j] = list_info[j]
    if i!=N-1:
        list_travel_time[i] = list_info[-1]
    
dp = [[0 for _ in range(K)] for _ in range(N)]
for j in range(K):
    dp[0][j] = list_duration[0][j]

for i in range(1, N):
    min_duration = 10**7
    for j in range(K):
        min_duration = min(dp[i-1][j] + list_travel_time[i-1], min_duration)
    for j in range(K):
        dp[i][j] = min(dp[i-1][j], min_duration) + list_duration[i][j] 


min_total_duration = dp[N-1][0]
for j in range(K):
    min_total_duration = min(dp[N-1][j], min_total_duration)
    
print(min_total_duration)