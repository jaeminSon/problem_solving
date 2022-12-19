import sys
from collections import deque

n = int(sys.stdin.readline().rstrip())

l = [int(d) for d in sys.stdin.readline().rstrip().split()]

n_q = int(sys.stdin.readline().rstrip())

problems = [int(sys.stdin.readline().rstrip()) for _ in range(n_q)]

def cost(f, t):
    return 1 if l[f] <= l[t] else 0

############################
# reduce tuple for memory
MULT = 1_000_001
def get_index(val):
    return val % MULT
def get_dp(val):
    return val // MULT
############################

for p in problems:
    sol = n
    
    q = deque([(0,l[0])])

    for i in range(1,len(l)):

        while q and get_index(q[0][0]) < i - p:
            q.popleft()
        sol = get_dp(q[0][0]) + cost(get_index(q[0][0]),i)

        while q and (get_dp(q[-1][0]) > sol or (get_dp(q[-1][0]) == sol and q[-1][1] <= l[i])):
            q.pop()
        q.append((sol*MULT+i,l[i]))

    print(sol)
