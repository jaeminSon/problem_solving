import sys
from collections import deque

MAX_VAL = 200_001

N = int(sys.stdin.readline().rstrip())

l_val = [int(d) for d in sys.stdin.readline().rstrip().split()]

l = [0]
for i in range(len(l_val)):
    l.append(l[-1]+l_val[i])
for i in range(len(l)):
    l[i] += 100_000

M = int(sys.stdin.readline().rstrip())
queries = []
for _ in range(M):
    s,e = [int(d) for d in sys.stdin.readline().rstrip().split()]
    queries.append((s-1,e))

sqrtN = int(len(l)**(1./2))
l_sorted_queries = sorted(queries, key=lambda x:(x[0]//sqrtN, x[1]))

val2deqeue = [deque() for _ in range(MAX_VAL)]
arr = [0] * len(l)
block_size = int(len(l)**(1./2))
block = [0] * (len(l)//block_size+1)

def update(idx, val):
    block[idx // block_size] += val
    arr[idx] += val

def query():
    for i in range(len(block)-1, -1, -1):
        if block[i] > 0:
            for j in range(block_size-1, -1, -1):
                if i*block_size + j < len(arr) and arr[i*block_size + j] > 0:
                    return i*block_size + j

def add(s, e, left):
    for i in range(e, s-1, -1) if left else range(s, e+1):
        if val2deqeue[l[i]]:
            update(val2deqeue[l[i]][-1] - val2deqeue[l[i]][0], -1)
        if left:
            val2deqeue[l[i]].appendleft(i)
        else:
            val2deqeue[l[i]].append(i)
        update(val2deqeue[l[i]][-1] - val2deqeue[l[i]][0], 1)

def remove(s, e, left):
    for i in range(s, e+1) if left else range(e, s-1, -1):
        update(val2deqeue[l[i]][-1] - val2deqeue[l[i]][0], -1)
        if left:
            val2deqeue[l[i]].popleft()
        else:
            val2deqeue[l[i]].pop()
        if val2deqeue[l[i]]:
            update(val2deqeue[l[i]][-1] - val2deqeue[l[i]][0], +1)

dict_ans = {}
s, e = l_sorted_queries[0]
add(s,e,left=True)
dict_ans[(s,e)] = query()

for i in range(1, M):
    new_s, new_e = l_sorted_queries[i]
    
    if s>new_s: # add (new_s, new_s+1, ..., s-1)
        add(new_s, s-1, left=True)
    if e<new_e: # add (e+1, e+2, ..., new_e)
        add(e+1, new_e, left=False)
    if s<new_s: # remove (s, s+1, ..., new_s-1)
        remove(s, new_s-1, left=True)
    if e>new_e: # remove (new_e+1, ..., e-1, e)
        remove(new_e+1, e, left=False)
    
    dict_ans[(new_s,new_e)] = query()
    
    s,e = new_s, new_e

for q in queries:
    print(dict_ans[tuple(q)])