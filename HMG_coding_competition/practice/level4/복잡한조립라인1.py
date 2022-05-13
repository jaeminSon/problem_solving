import sys

K, N = [int(el) for el in sys.stdin.readline().split()]

list_duration = [[0]*K for _ in range(N)]
list_travel_time = [[[0]*K for _ in range(K)] for _ in range(N)]

for i in range(N):
    list_info = [int(el) for el in sys.stdin.readline().split()]
    for j in range(K):
        list_duration[i][j] = list_info[j]
    if i!=N-1:
        index = K
        for j in range(K):
            for l in range(K):
                if j!=l:
                    list_travel_time[i][j][l] = list_info[index]
                    index+=1
         
dp = [[0 for _ in range(K)] for _ in range(N)]
for j in range(K):
    dp[0][j] = list_duration[0][j]

for i in range(1, N):
    for j in range(K):
        min_duration = min([dp[i-1][l] + list_travel_time[i-1][l][j] for l in range(K)] + [dp[i-1][j]])
        dp[i][j] = min_duration + list_duration[i][j] 

min_total_duration = min(dp[N-1])
    
print(min_total_duration)