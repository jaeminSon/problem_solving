import sys
from functools import cmp_to_key
n = int(sys.stdin.readline().rstrip())

l_p = []
for _ in range(n):
    x0, x1, y = [int(d) for d in sys.stdin.readline().rstrip().split()]
    if x0 > x1:
        x0, x1 = x1, x0
    w = x1-x0
    l_p.append((x0, x1, y, w))

def ccw(p1, p2):
    x2,y2,x3,y3=p1[1],p1[0],p2[1],p2[0]
    val = x2*y3-y2*x3
    if val != 0:
        return val
    else:
        return p2[2] - p1[2]

def get_best_at(i):
    x0, x1, y, w = l_p[i]
    best = w
    for x in [x0, x1]:
        k = 0
        for j in range(len(l_p)):
            if j!=i:
                xx0, xx1, yy, ww = l_p[j]
                if y!=yy:
                    if y < yy:
                        stack[k] = [x-xx0, yy-y, ww]
                        stack[k+1] = [x-xx1, yy-y, -ww]
                    elif y > yy:
                        stack[k] = [xx0-x, y-yy, -ww]
                        stack[k+1] = [xx1-x, y-yy, ww]
                    k+=2
        
        stack_used = stack[:k]
        stack_used.sort(key=cmp_to_key(ccw))
        curr_w = w
        for _, _, ws in stack_used:
            best = max(best, curr_w)
            curr_w += ws
    
    return best

stack = [[0,0,0]] * 2 * len(l_p)
ans = 0
for i in range(len(l_p)):
    ans = max(ans, get_best_at(i))
print(ans)
