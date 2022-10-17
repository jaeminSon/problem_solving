import sys

N = int(sys.stdin.readline().rstrip())

ans = [-1]*N

q = [[] for _ in range(4)]

dict_start = {"A":0, "B":1, "C":2, "D":3}

for i in range(N):
    t,s  = [d for d in sys.stdin.readline().rstrip().split()]
    q[dict_start[s]].append([int(t),i])
    
for i in range(4):
    q[i].sort(reverse=True, key=lambda x:x[0])

def get_non_empty():
    return [i for i in range(4) if len(q[i])!=0]

def get_path(i_non_empty, t):
    return [i for i in i_non_empty if t == q[i][-1][0] and (len(q[i-1])==0 or t!=q[i-1][-1][0])]

while not all([len(q[i])==0 for i in range(4)]):
    if all([len(q[i])!=0 for i in range(4)]) and all([q[i][-1][0]==q[i-1][-1][0] for i in range(4)]):
        break
    else:
        i_non_empty = get_non_empty()
        t = min([q[i][-1][0] for i in i_non_empty])
        i_pass = get_path(i_non_empty, t)
        for i in i_pass:
            ans[q[i][-1][1]] = q[i][-1][0]
            q[i].pop()
        
        for i in get_non_empty():
            if q[i][-1][0]<=t:
                q[i][-1][0]=t+1

for i in range(N):
    print(ans[i])