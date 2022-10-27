import sys

def convex_hull_trick(s,a,b,c):
    
    def B(i):
        return -2*a*s[i]

    def C(i):
        return -b*s[i]+a*s[i]**2

    def D(i):
        return a*s[i]**2+b*s[i]+c

    def intersection_x(lseg1, lseg2):
        # y=ax+b, (x>=s)
        a1,b1,_ = lseg1
        a2,b2,_ = lseg2
        return 1.*(b2-b1)/(a1-a2)
 
    n = len(s)
    dp = [0] * n
    stack = [] # (a,b,s) where y=ax+b, x>=s
    pos = 0
    for j in range(1, n):
        intercept = dp[j-1] + C(j-1)
        line_seg = [B(j-1), intercept, 0]
        while stack:
            line_seg[2] = intersection_x(stack[-1], line_seg)
            if stack[-1][2] < line_seg[2]:
                break
            else:
                stack.pop()
        stack.append(line_seg)
 
        while pos+1 < len(stack) and stack[pos+1][2] < s[j]:
            pos+=1
        dp[j] = stack[pos][0] * s[j] + stack[pos][1]
        dp[j] += D(j)
 
    return dp[n-1]

N = int(sys.stdin.readline().rstrip())
a,b,c = [-int(d) for d in sys.stdin.readline().rstrip().split()]
l = [int(d) for d in sys.stdin.readline().rstrip().split()]

s = [0]
for el in l:
    s.append(s[-1]+el)

min_val = convex_hull_trick(s, a,b,c)
print(-min_val)