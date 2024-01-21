from sys import stdin
input = stdin.readline


def convex_hull_trick(A, B):

    def intersection_x(lseg1, lseg2):
        # y=ax+b, (x>=s)
        a1, b1, _ = lseg1
        a2, b2, _ = lseg2
        return 1.*(b2-b1)/(a1-a2)

    n = len(A)
    dp = [0] * n
    stack = []  # (a,b,s) where y=ax+b, x>=s
    pos = 0
    for j in range(1, n):
        intercept = dp[j-1]
        line_seg = [B[j-1], intercept, 0]
        while stack:
            line_seg[2] = intersection_x(stack[-1], line_seg)
            if stack[-1][2] < line_seg[2]:
                break
            else:
                stack.pop()
        stack.append(line_seg)

        # A is monotonically increasing
        while pos+1 < len(stack) and stack[pos+1][2] < A[j]:
            pos += 1
        dp[j] = stack[pos][0] * A[j] + stack[pos][1]

    return dp[n-1]


N = int(input())

rects = []
for _ in range(N):
    w, h = (map(int, input().split()))
    rects.append((w, h))

rects_w_inc = sorted(rects, reverse=True)

new_rects = [rects_w_inc[0]]
for i in range(1, len(rects_w_inc)):
    if new_rects[-1][1] < rects_w_inc[i][1]:
        new_rects.append(rects_w_inc[i])

new_rects = new_rects[::-1]

A = [0] + [el[0] for el in new_rects]
B = [el[1] for el in new_rects] + [0]

ans = convex_hull_trick(A, B)

print(ans)
