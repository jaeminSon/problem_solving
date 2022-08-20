from collections import defaultdict
import sys

N = int(sys.stdin.readline().rstrip())

l = [int(d) for d in sys.stdin.readline().rstrip().split()]

Q = int(sys.stdin.readline().rstrip())
l_q = [[int(d)-1 for d in sys.stdin.readline().rstrip().split()] for _ in range(Q)]

sqrtN = int(N**(1./2))
l_sorted_queries = sorted(l_q, key=lambda x:(x[0]//sqrtN, x[1]))

c = defaultdict(int)

def add(s, e):
    for i in range(s, e+1):
        c[l[i]] += 1
    
def remove(s,e):
    for i in range(s, e+1):
        c[l[i]] -= 1
        if c[l[i]]==0:
            del c[l[i]]

add(l_sorted_queries[0][0], l_sorted_queries[0][1])
s, e = l_sorted_queries[0]
dict_ans = {(s,e): len(c)}
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
    
    dict_ans[(new_s,new_e)] = len(c)
    s,e = new_s, new_e

for q in l_q:
    print(dict_ans[tuple(q)])