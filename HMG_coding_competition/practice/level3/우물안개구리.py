import sys

N, M = [int(el) for el in sys.stdin.readline().split()]

list_weight = [int(el) for el in sys.stdin.readline().split()]
list_rel = [[] for _ in range(N)]

for _ in range(M):
    A, B = [int(el) for el in sys.stdin.readline().split()]    
    list_rel[A-1].append(B-1)
    list_rel[B-1].append(A-1)

n_frog = 0
for i, rel in enumerate(list_rel):
    add_frog = True
    myweight = list_weight[i]
    for friend in rel:
        if myweight <= list_weight[friend]:
            add_frog = False
            break
    if add_frog:
        n_frog+=1

print(n_frog)

