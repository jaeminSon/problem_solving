import sys

MAX_VAL = 100_000

N, M = [int(d) for d in sys.stdin.readline().rstrip().split()]

l = [int(d) for d in sys.stdin.readline().rstrip().split()]

l_q = [[int(d)-1 for d in sys.stdin.readline().rstrip().split()] for _ in range(M)]

l_without_dup = sorted(set(l))
val2rank = {l_without_dup[i] : i for i in range(len(l_without_dup))}
new_l = [val2rank[el]+1 for el in l]

sqrtN = int(N**(1./2))
l_sorted_queries = sorted(l_q, key=lambda x:(x[0]//sqrtN, x[1]))

curr_val = [0]
    
tree = [0]*(2*MAX_VAL+1) # tree[0] is dummy

def add(s, e, left=False):
    itr = range(e, s-1,-1) if left else range(s, e+1)
    for i in itr:
        
        # fenwick tree query
        if left:
            res = 0
            t = new_l[i]-1 if left else new_l[i]
            while t > 0:
                res += tree[t]
                t -= t & (-t)
            curr_val[0] += res
        else:
            res = [0, 0]
            for p, t in enumerate([MAX_VAL+1,new_l[i]]):
                while t > 0:
                    res[p] += tree[t]
                    t -= t & (-t)
            curr_val[0] += (res[0]-res[1])

        # fenwick tree update
        t = new_l[i]
        while t <= 2*MAX_VAL:
            tree[t] += 1 
            t += t & (-t)
        
def remove(s,e,left=False):
    itr = range(s, e+1) if left else range(e, s-1,-1)
    for i in itr:
        
        # fenwick tree update
        t = new_l[i]
        while t <= 2*MAX_VAL:
            tree[t] -= 1 
            t += t & (-t)
        
        # fenwick tree query
        if left:
            res = 0
            t = new_l[i]-1
            while t > 0:
                res += tree[t]
                t -= t & (-t)
            curr_val[0] -= res
        else:
            res = [0, 0]
            for p, t in enumerate([MAX_VAL+1,new_l[i]]):
                while t > 0:
                    res[p] += tree[t]
                    t -= t & (-t)
            curr_val[0] -= (res[0]-res[1])

add(l_sorted_queries[0][0], l_sorted_queries[0][1])
s, e = l_sorted_queries[0]
dict_ans = {(s,e): curr_val[0]}
for i in range(1, M):
    new_s, new_e = l_sorted_queries[i]
    
    if s>new_s: # add (new_s, new_s+1, ..., s-1)
        add(new_s, s-1, left=True)
    if e<new_e: # add (e+1, e+2, ..., new_e)
        add(e+1, new_e)
    if s<new_s: # remove (s, s+1, ..., new_s-1)
        remove(s, new_s-1, left=True)
    if e>new_e: # remove (new_e+1, ..., e-1, e)
        remove(new_e+1, e)
    
    dict_ans[(new_s,new_e)] = curr_val[0]
    s,e = new_s, new_e

for q in l_q:
    print(dict_ans[tuple(q)])