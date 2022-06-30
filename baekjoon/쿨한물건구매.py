import sys

D, P, Q = [int(el) for el in sys.stdin.readline().split()]
if P < Q:
    P, Q = Q, P

cand = []
for x in range(min(Q, int((D+P-1)//P))+1):
    y = int((D - P*x + Q - 1)//Q)
    y = 0 if y<0 else y
    cand.append(P*x+Q*y)
    
print(min(cand))
