H, W = map(int, input().split())

avail = [[True] * W for _ in range(H)]

dp = [[[[-1] * W for _ in range(W)] for _ in range(H)] for _ in range(H)]

for i in range(H):
    l = input()
    for j in range(W):
        if l[j] == "X":
            avail[i][j] = False


def grundy(y_s, y_e, x_s, x_e):

    if x_s >= W or y_s >= H:
        # outbound
        return 0

    if x_s > x_e or y_s > y_e:
        # illegal
        return 0

    if dp[y_s][y_e][x_s][x_e] != -1:
        return dp[y_s][y_e][x_s][x_e]

    s = set()
    for i in range(y_s, y_e+1):
        for j in range(x_s, x_e+1):
            if avail[i][j]:
                s.add(grundy(y_s, i-1, x_s, j-1) ^ grundy(y_s, i-1, j+1, x_e) ^ grundy(i+1, y_e, x_s, j-1) ^ grundy(i+1, y_e, j+1, x_e))

    i = 0
    while True:
        if i not in s:
            dp[y_s][y_e][x_s][x_e] = i
            return dp[y_s][y_e][x_s][x_e]
        i += 1


if grundy(0, H-1, 0, W-1):
    print("First")
else:
    print("Second")
