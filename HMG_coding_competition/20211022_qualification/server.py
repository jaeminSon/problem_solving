import sys
import bisect
from collections import Counter

T = int(sys.stdin.readline().rstrip())

def update(counter, sorted_list, val):
    counter.subtract(Counter({val:1}))
    if counter[val] == 0:
        del counter[val]
    
    if val not in counter:
        sorted_list.remove(val)
        
for _ in range(T):
    _ = int(sys.stdin.readline().rstrip())
    
    list_weights = []
    count = 0
    for el in [int(el) for el in sys.stdin.readline().split()]:
        if el > 600:
            count += 1
        else:
            list_weights.append(int(el))
    
    counter = Counter(list_weights)
    unique_weight_sorted = sorted(set(counter.elements()))
    while len(unique_weight_sorted)!=0:
        curr_w = unique_weight_sorted[-1]
        if curr_w == 300:
            count += counter[300] // 3 if counter[300] % 3 == 0 else counter[300] // 3 + 1
            break
        else:
            count+=1
            update(counter, unique_weight_sorted, curr_w)
            
            cand_recip_w = 900 - curr_w
            index_recip = bisect.bisect_right(unique_weight_sorted, cand_recip_w) - 1
            if index_recip >= 0:
                recip_w = unique_weight_sorted[index_recip]
                update(counter, unique_weight_sorted, recip_w)

    print(count)

