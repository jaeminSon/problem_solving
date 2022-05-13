import sys
from itertools import permutations

N, M, K = [int(el) for el in sys.stdin.readline().split()]
list_weight = [int(el) for el in sys.stdin.readline().split()]

list_workload = []
for order in permutations(range(N)):
    n_move = 0
    workload = 0
    curr_weight = 0
    index = 0
    while n_move < K:
        i = order[index % N]
        weight_if_added = curr_weight + list_weight[i]
        if weight_if_added > M:
            workload += curr_weight
            curr_weight = list_weight[i]
            n_move += 1
        else:
            curr_weight = weight_if_added
        index+=1
                
    list_workload.append(workload)
        
print(min(list_workload))