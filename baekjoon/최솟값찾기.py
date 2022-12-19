import sys
from collections import deque

N,L  = [int(d) for d in sys.stdin.readline().rstrip().split()]

l = [int(d) for d in sys.stdin.readline().rstrip().split()]

first_element = (l[0],0)

q = deque([first_element])

sol = [first_element]

for i in range(1,len(l)):
    v = l[i]

    while q and q[-1][0] > v:
        q.pop()
    q.append((v,i))

    while q and q[0][1] <= i - L:
        q.popleft()
    sol.append(q[0])

print(" ".join([str(s[0]) for s in sol]))