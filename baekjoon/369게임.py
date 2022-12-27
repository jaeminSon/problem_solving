import sys
sys.setrecursionlimit(100000)

MOD = 20150523

A,B  = [d for d in sys.stdin.readline().rstrip().split()]
A_minus_1 = str(int(A)-1)

arr = [[[[-1 for _ in range(2)] for _ in range(2)] for _ in range(3)] for _ in range(100001)]

def dp(v, i, r, d, b):
    # (value, decimal index, remainder of digit sum, has digit of 3 or 6 or 9, is boundary)
    
    if len(v) <= i: # increment clap by 1 if (1) has digit 3 or 6 or 9, or (2) remainder of mod 3 is 0
        return d or r==0
    
    if arr[i][r][d][b]!=-1:
        return arr[i][r][d][b]
    
    arr[i][r][d][b] = 0
    
    if b == 1:
        for j in range(10):
            if j <= int(v[i]):
                arr[i][r][d][b] = (arr[i][r][d][b] + dp(v, i+1, (r+j)%3, d or (j%3==0 and j!=0), j==int(v[i]))) % MOD
    else:
        for j in range(10):
            arr[i][r][d][b] = (arr[i][r][d][b] + dp(v, i+1, (r+j)%3, d or (j%3==0 and j!=0), False)) % MOD
    
    return arr[i][r][d][b]

count_B = dp(B,0,0,0,1)
for i in range(100001):
    for r in range(3):
        for b in range(2):
            for d in range(2):
                arr[i][r][b][d] = -1
count_A_minus_1 = dp(A_minus_1,0,0,0,1)

print(count_B - count_A_minus_1)