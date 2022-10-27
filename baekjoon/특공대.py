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

    def pop():
        s_a.pop()
        s_b.pop()
        s_s.pop()
 
    n = len(s)
    dp = [0] * n
    
    # (a,b,s) where y=ax+b, x>=s
    s_a = []
    s_b = []
    s_s = []
    
    pos = 0
    for j in range(1, n):
        intercept = dp[j-1] + C(j-1)
        line_seg = [B(j-1), intercept, 0]
        while s_a:
            line_seg[2] = intersection_x((s_a[-1],s_b[-1],s_s[-1]), line_seg)
            if s_s[-1] < line_seg[2]:
                break
            else:
                pop()
        s_a.append(line_seg[0])
        s_b.append(line_seg[1])
        s_s.append(line_seg[2])
 
        while pos+1 < len(s_a) and s_s[pos+1] < s[j]:
            pos+=1
        dp[j] = s_a[pos] * s[j] + s_b[pos]
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