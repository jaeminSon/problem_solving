import sys

N = int(sys.stdin.readline().rstrip())

l = [int(sys.stdin.readline().rstrip()) for _ in range(N)]
val2lindex = {v:i for i,v in enumerate(l)}
sorted_l = sorted(l)
global_min = sorted_l[0]

visited = [False] * N

def find_cycle(i):
    s = sorted_l[i]
    c = [s]
    visited[val2lindex[s]] = True
    
    next = sorted_l[val2lindex[s]]
    while s!=next:
        c.append(next)
        visited[val2lindex[next]] = True
        next = sorted_l[val2lindex[next]]
        
    return c

ans = 0
for i in range(N):
    if not visited[i]:
        c = find_cycle(i)
        # (3,2,1) -> (1,2,3)
        # (1) + (40,20,30) -> (20,40,1,30) -> (1,20,30,40)
        min_c = min(c)
        ans += (sum(c) + min(min_c*(len(c)-2), min_c + global_min + len(c)*global_min))

print(ans)