import sys
from collections import defaultdict

N, Q = [int(d) for d in sys.stdin.readline().rstrip().split()]

l = [int(d) for d in sys.stdin.readline().rstrip().split()]
l_q = [[int(d)-1 for d in sys.stdin.readline().rstrip().split()] for _ in range(Q)]

sqrtN = int(len(l)**(1./2))
l_sorted_queries = sorted(l_q, key=lambda x:(x[0]//sqrtN, x[1]))

v2c = defaultdict(int)
c2n = defaultdict(int)

best = 0

def add(s, e):
    global best
    for i in range(s, e+1):
        v2c[l[i]] += 1
        c2n[v2c[l[i]]-1]-=1
        c2n[v2c[l[i]]]+=1
        if v2c[l[i]] > best:
            best = v2c[l[i]]
    
def remove(s,e):
    global best
    for i in range(s, e+1):
        v2c[l[i]] -= 1
        c2n[v2c[l[i]]+1]-=1
        c2n[v2c[l[i]]]+=1
        if v2c[l[i]]+1==best and c2n[v2c[l[i]]+1]==0:
            best-=1
            
add(l_sorted_queries[0][0], l_sorted_queries[0][1])
s, e = l_sorted_queries[0]
dict_ans = {(s,e):best}
for i in range(1, Q):
    new_s, new_e = l_sorted_queries[i]
    
    if s>new_s: # add (new_s, new_s+1, ..., s-1)
        add(new_s, s-1)
    if e<new_e: # add (e+1, e+2, ..., new_e)
        add(e+1, new_e)
    if s<new_s: # remove (s, s+1, ..., new_s-1)
        remove(s, new_s-1)
    if e>new_e: # remove (new_e+1, ..., e-1, e)
        remove(new_e+1, e)
    
    dict_ans[(new_s,new_e)] = best
    
    s,e = new_s, new_e


for q in l_q:
    print(dict_ans[tuple(q)])